"""Frozen experiment composition; the framework is the only coding state machine."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
from dataclasses import asdict, is_dataclass, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding.compaction import AdaptiveCompaction, SummaryCompaction, SummarySelection
from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.projection import ProjectionPolicy, request_bytes
from devtools.agents.coding.repository import CodingObjective, EditLimits, RepositoryCodingHost, write_source_changes
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.identity import RepositoryId
from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Stopwatch, Timestamp
from devtools.models.interaction import InteractionSource, ModelResponse, ModelSettings, ModelToolCall, PromptMessage
from devtools.models.interaction.providers.llama_cpp import LlamaCppInteraction
from devtools.models.interaction.providers.llama_cpp_request_settings import LlamaCppRequestSettings
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import TextFile, write
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.source import SourceScope
from scripts.qwen.llama_cpp_profile import QWEN38_INSTRUCT_SAMPLING, QWEN38_27B_UD_IQ4_XS

HERE = Path(__file__).resolve().parent
STATE = ROOT / '.local/adaptive-compaction/evaluation'
LIMITS = CodingLimits(6, 2, 16, Duration.seconds(240), Duration.seconds(1200))
SETTINGS = ModelSettings(maximum_output_tokens=4096, thinking_enabled=False)


def plain(value):
    if isinstance(value, BaseException):
        return dict(type=type(value).__name__, message=str(value))
    if is_dataclass(value):
        return {k: plain(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [plain(v) for v in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def save(path, value, fresh=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    write(TextFile(resolve_path(path), json.dumps(plain(value), ensure_ascii=False, indent=2)+'\n'), overwrite=not fresh)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


async def command(root, *args):
    result = await CommandExecutor(output_policy=CommandOutputPolicy(max_stdout_bytes=32768, max_stderr_bytes=32768)).execute(
        Command(args[0]).args(*args[1:]).cwd(resolve_path(root)).with_timeout(Duration.seconds(30)))
    return dict(argv=args, exit_code=result.exit_code, stdout=result.stdout.decode(errors='replace'), stderr=result.stderr.decode(errors='replace'))


class Interaction:
    def __init__(self, out, role):
        self.delegate = LlamaCppInteraction(endpoint='http://127.0.0.1:8080', model='qwen38-local', source=InteractionSource('adaptive-0001-'+role))
        self.out, self.role, self.records = out, role, []

    @property
    def source(self):
        return self.delegate.source

    async def send(self, request):
        if len(self.records) >= (6 if self.role == 'acting' else 2):
            raise RuntimeError('Frozen model-call limit')
        effective = replace(request, provider_settings=LlamaCppRequestSettings(**QWEN38_INSTRUCT_SAMPLING))
        record = dict(index=len(self.records)+1, at=str(Timestamp.now()), entered=False, request=plain(effective), host_bytes=request_bytes(request))
        self.records.append(record)
        path = self.out / (self.role+'-'+str(record['index'])+'.json')
        save(path, record, fresh=True)
        async with asyncio.timeout(20):
            tokens = await self.delegate.count_input_tokens(effective)
        record['input_tokens_measured'] = tokens
        if tokens > 28160 or request_bytes(effective) > 32768:
            record['capacity_refused'] = True
            save(path, record)
            raise ValueError('Frozen complete request capacity exceeded')
        timer = Stopwatch()
        record['entered'] = True
        save(path, record)
        try:
            response = await self.delegate.send(effective)
            record['response'] = plain(response)
            return response
        except BaseException as error:
            record['error'] = plain(error)
            raise
        finally:
            timer.stop()
            record['seconds'] = timer.elapsed.total_seconds
            record['finished_at'] = str(Timestamp.now())
            save(path, record)


async def make_host(root, treatment, out):
    root.mkdir(parents=True, exist_ok=True)
    for p in (HERE/'fixture').glob('*.py'):
        write(TextFile(resolve_path(root/p.name), p.read_text(encoding='utf-8')), overwrite=False)
    for args in [('init',), ('add', '.'), ('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','Authored frozen input')]:
        result = await command(root, 'git', *args)
        assert result['exit_code'] == 0, result
    addresses = tuple(RepositoryResourceAddress(p) for p in ('reducer.py','rules.py','focused.py'))
    repository = Repository(RepositoryId('adaptive-0001-events'))
    scope = SourceScope.observe(root=resolve_path(root), repository=repository, addresses=addresses)
    corpus = define_repository_text_corpus(discovery=discover_repository_resource_addresses(repository=repository, root=scope.root, requested_addresses=addresses, maximum_resource_count=4, maximum_traversal_entry_count=128), selected_addresses=addresses)
    checks = FixedCheckPlan(scope.root, (FixedCheck('focused', Command(sys.executable).args('-B','focused.py').cwd(scope.root).with_timeout(Duration.seconds(20))),), scope)
    objective = CodingObjective((HERE/'objective.md').read_text(), scope, (addresses[0],), checks, EditLimits(8192,12288,24576,2),8192,32768)
    async def admit(call, arguments):
        scope_root = scope.root
        assert scope_root == objective.scope.root
    async def apply(changes):
        write_source_changes(scope.root, changes)
    def archive(values):
        save(out/'candidate.json', values, fresh=True)
    def restore(address, text):
        assert text is not None
        write(TextFile(resolve_path(root/address.value), text))
    auxiliary = Interaction(out, 'summary')
    initial_snapshot = str(scope.snapshot.id)
    def selection(messages):
        indices = frozenset({3,4}) if str(host.scope.snapshot.id) == initial_snapshot else frozenset()
        return SummarySelection(indices, indices)
    summary = None if treatment == 'A' else SummaryCompaction(auxiliary, selection, 2, 24576,4096,ModelSettings(maximum_output_tokens=2048, thinking_enabled=False),Duration.seconds(180),retain_payloads=True,
        adaptive=AdaptiveCompaction(24000,6144,lambda _: frozenset({4})) if treatment == 'C' else None)
    host = RepositoryCodingHost(objective, corpus=corpus,authorize=admit,apply_changes=apply,archive=archive,restore=restore,settings=SETTINGS,projection=ProjectionPolicy(24000,12000,frozenset({'list_repository','search_source'})),summary=summary)
    host.progress = CodingProgress(LIMITS)
    # Authored metadata, explicitly not claimed as previous live model actions.
    for name, identity, payload in [
        ('list_repository','seed-inventory',{'fixture_authored':True,'catalog':[{'path':'reducer.py','kind':'python','purpose':'event accounting'}]*260}),
        ('search_source','seed-search',{'fixture_authored':True,'probe':json.loads((HERE/'probe.json').read_text()),'ranked_metadata':[{'path':'reducer.py','term':'identity','source_acquired':False}]*150}),
    ]:
        call = ModelToolCall(name,'{}',identity)
        host.messages.extend((PromptMessage('assistant','Retained authored investigation', (call,)), PromptMessage('tool',json.dumps(payload),tool_call_id=identity)))
    # Actual pre-freeze fixed check and source Tool entry; no invented receipts.
    for call in [ModelToolCall('validate_candidate','{}','seed-check'), *[ModelToolCall('read_source',json.dumps(dict(path=a.value,start=0,end=len(scope.snapshot.resource_at(a).content))),'seed-read-'+a.value) for a in addresses[:2]]]:
        response = ModelResponse('', InteractionSource('authored-seed-host'), tool_calls=(call,))
        host.classify(response)
        await host.acquire(response)
    return host, auxiliary


async def freeze():
    assert not (HERE/'freeze.json').exists()
    # Literal independently executed counterexample, not a solution patch.
    result = await command(ROOT, sys.executable, '-c', "events=[('a','x',3),('b','x',7)]; seen=set(); actual={};\nfor s,i,d in events:\n if i not in seen: actual[s]=actual.get(s,0)+d; seen.add(i)\nprint(actual); assert actual == {'a':3,'b':7}")
    assert result['exit_code'] == 1 and "{'a': 3}" in result['stdout']
    save(HERE/'probe.json',dict(rejected_hypothesis='Global event ID suppression',observed=result,conclusion='Distinct streams may reuse an event ID. Current implementation still fails; no edits made. Rejected events must not reserve an ID.'))
    host, _ = await make_host(STATE/'freeze-task','A',STATE/'freeze-output')
    request = host.build_request(tuple(host.messages))
    save(HERE/'history.json', dict(request=plain(request), snapshot=plain(host.scope.snapshot), source_bindings=plain(host._source_messages), check_results=plain(host.check_results), original_bytes=request_bytes(request)))
    # Baseline and held-out must fail; no reference patch or grading enters input.
    grade = await command(ROOT,sys.executable,str(HERE/'oracle.py'),str(STATE/'freeze-task'))
    assert grade['exit_code'] == 1
    files={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    save(HERE/'freeze.json',dict(at=str(Timestamp.now()),baseline='d5d18b589948f19f457a29161b8811da8f7cf0ee',files=files,source_hashes={p.name:sha(p) for p in (HERE/'fixture').glob('*.py')},original_bytes=request_bytes(request),profile=plain(QWEN38_27B_UD_IQ4_XS),sampling=QWEN38_INSTRUCT_SAMPLING,baseline_oracle=grade,framework={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'src/devtools/agents/coding').rglob('*.py')}),fresh=True)
    print('FROZEN',request_bytes(request),len(files))


async def run(treatment):
    frozen=json.loads((HERE/'freeze.json').read_text())
    for p,h in frozen['files'].items(): assert sha(HERE/p)==h,p
    for p,h in frozen['framework'].items(): assert sha(ROOT/p)==h,p
    out=HERE/'evidence'/treatment
    save(out/'ENTERED.json',dict(at=str(Timestamp.now()),freeze=sha(HERE/'freeze.json')),fresh=True)
    root=STATE/treatment
    host,auxiliary=await make_host(root,treatment,out)
    original=host.build_request(tuple(host.messages))
    assert request_bytes(original)==frozen['original_bytes']
    assert plain(original)==json.loads((HERE/'history.json').read_text())['request']
    if treatment=='B': host.request_compaction()
    acting=Interaction(out,'acting')
    timer=Stopwatch()
    result=await run_coding_agent(acting,host=host,limits=LIMITS)
    timer.stop()
    save(out/'result.json',dict(result=plain(result),seconds=timer.elapsed.total_seconds,messages=plain(host.messages),requests=plain(host.requests),projections=plain(host.projection_outcomes),attempts=plain(host.compaction.attempts) if host.compaction else [],decisions=host.compaction.decisions if host.compaction else [],checks=plain(host.check_results),source_results=plain(host.source_results),history_prefix_unchanged=plain(host.messages[:len(original.prompt.messages)])==plain(original.prompt.messages)),fresh=True)
    assert all(sha(root/p)==h for p,h in frozen['source_hashes'].items())
    candidate=json.loads((out/'candidate.json').read_text()) if (out/'candidate.json').exists() else {}
    if candidate:
        grading=STATE/(treatment+'-grade');grading.mkdir()
        for p in (HERE/'fixture').glob('*.py'): write(TextFile(resolve_path(grading/p.name),candidate.get(p.name,p.read_text())))
        grade=await command(ROOT,sys.executable,str(HERE/'oracle.py'),str(grading))
    else: grade=dict(outcome='no candidate')
    save(out/'grade.json',grade,fresh=True)
    print(treatment,result.disposition,result.accepted,grade,timer.elapsed.total_seconds)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['freeze','A','B','C']);args=parser.parse_args()
    asyncio.run(freeze() if args.mode=='freeze' else run(args.mode))
