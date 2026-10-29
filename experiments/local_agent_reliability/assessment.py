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
STATE = ROOT / '.local/reliability/evaluation'
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
        self.delegate = LlamaCppInteraction(endpoint='http://127.0.0.1:8080', model='qwen38-local', source=InteractionSource('reliability-0001-'+role))
        self.out, self.role, self.records = out, role, []

    @property
    def source(self):
        return self.delegate.source

    async def send(self, request):
        if len(self.records) >= (6 if self.role == 'acting' else 1):
            raise RuntimeError('Frozen model-call limit')
        effective = replace(request, provider_settings=request.provider_settings or LlamaCppRequestSettings(**QWEN38_INSTRUCT_SAMPLING))
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

async def make_host(root, out):
    root.mkdir(parents=True, exist_ok=False)
    for p in (HERE/'fixture').glob('*.py'):
        write(TextFile(resolve_path(root/p.name), p.read_text(encoding='utf-8')), overwrite=False)
    for args in [('init',), ('add', '.'), ('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','Authored reliability input')]:
        result = await command(root, 'git', *args)
        assert result['exit_code'] == 0, result
    addresses = tuple(RepositoryResourceAddress(p) for p in ('occupancy.py','contracts.py','focused.py'))
    repository = Repository(RepositoryId('reliability-0001-room'))
    scope = SourceScope.observe(root=resolve_path(root), repository=repository, addresses=addresses)
    corpus = define_repository_text_corpus(discovery=discover_repository_resource_addresses(repository=repository, root=scope.root, requested_addresses=addresses, maximum_resource_count=4, maximum_traversal_entry_count=128), selected_addresses=addresses)
    checks = FixedCheckPlan(scope.root, (FixedCheck('focused', Command(sys.executable).args('-B','focused.py').cwd(scope.root).with_timeout(Duration.seconds(20))),), scope)
    objective = CodingObjective((HERE/'objective.md').read_text(encoding='utf-8'), scope, (addresses[0],), checks, EditLimits(8192,12288,24576,2),8192,32768)
    async def admit(call, arguments):
        assert scope.root == objective.scope.root
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
        indices = frozenset({1,2}) if str(host.scope.snapshot.id) == initial_snapshot else frozenset()
        return SummarySelection(indices, indices)
    summary = SummaryCompaction(auxiliary, selection, 1, 24576,4096,ModelSettings(maximum_output_tokens=2048, thinking_enabled=False),Duration.seconds(180),retain_payloads=True,provider_settings=LlamaCppRequestSettings(**QWEN38_INSTRUCT_SAMPLING,response_format='json_object'))
    host = RepositoryCodingHost(objective, corpus=corpus,authorize=admit,apply_changes=apply,archive=archive,restore=restore,settings=SETTINGS,projection=ProjectionPolicy(12000,6000,frozenset({'inspect_probe'})),summary=summary)
    call = ModelToolCall('inspect_probe','{}','prior-probe')
    payload = dict(fixture_authored=True,probe=json.loads((HERE/'probe.json').read_text()),metadata=[{'topic':'room occupancy','source_acquired':False}]*240)
    host.messages.extend((PromptMessage('assistant','Retained host-authored investigation, not earlier live model activity.',(call,)),PromptMessage('tool',json.dumps(payload),tool_call_id=call.provider_call_id),PromptMessage('assistant','Next inspect current authorized source before proposing a change.')))
    return host, auxiliary


async def freeze():
    assert not (HERE/'freeze.json').exists()
    # Real independently evaluated hypothesis; no reference patch is input.
    probe = await command(HERE/'fixture',sys.executable,'-B','-c',"from occupancy import occupied_minutes; intervals=[(2,10),(4,6)]; actual=occupied_minutes(sorted(intervals,key=lambda x:x[1]),(0,12)); print({'hypothesis':'sorting by end before additive accounting','nested_intervals':intervals,'observed':actual,'expected':8}); assert actual == 8")
    assert probe['exit_code'] == 1 and "'observed': 10" in probe['stdout']
    save(HERE/'probe.json',probe,fresh=True)
    host,_ = await make_host(STATE/'freeze-task',STATE/'freeze-output')
    original = host.build_request(tuple(host.messages))
    save(HERE/'history.json',dict(request=plain(original),snapshot=plain(host.scope.snapshot),original_bytes=request_bytes(original)))
    focused = await command(STATE/'freeze-task',sys.executable,'-B','focused.py')
    grade = await command(ROOT,sys.executable,'-B',str(HERE/'oracle.py'),str(STATE/'freeze-task'))
    assert focused['exit_code'] == grade['exit_code'] == 1
    head = await command(ROOT,'git','rev-parse','HEAD')
    revision = await command(STATE/'freeze-task','git','rev-parse','HEAD')
    files={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    save(HERE/'freeze.json',dict(at=str(Timestamp.now()),baseline=head['stdout'].strip(),task_revision=revision['stdout'].strip(),files=files,source_hashes={p.name:sha(p) for p in (HERE/'fixture').glob('*.py')},original_bytes=request_bytes(original),profile=plain(QWEN38_27B_UD_IQ4_XS),sampling=QWEN38_INSTRUCT_SAMPLING,baseline_focused=focused,baseline_oracle=grade,framework={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'src/devtools').rglob('*.py')}),fresh=True)
    print('FROZEN',request_bytes(original),len(files))


async def run():
    frozen=json.loads((HERE/'freeze.json').read_text())
    for p,h in frozen['files'].items(): assert sha(HERE/p)==h,p
    for p,h in frozen['framework'].items(): assert sha(ROOT/p)==h,p
    out=HERE/'evidence'
    save(out/'ENTERED.json',dict(at=str(Timestamp.now()),freeze=sha(HERE/'freeze.json')),fresh=True)
    root=STATE/'primary'
    host,auxiliary=await make_host(root,out)
    original=host.build_request(tuple(host.messages))
    assert plain(original)==json.loads((HERE/'history.json').read_text())['request']
    host.request_compaction()
    acting=Interaction(out,'acting')
    timer=Stopwatch()
    result=await run_coding_agent(acting,host=host,limits=LIMITS)
    timer.stop()
    save(out/'result.json',dict(result=plain(result),seconds=timer.elapsed.total_seconds,messages=plain(host.messages),requests=plain(host.requests),projections=plain(host.projection_outcomes),attempts=plain(host.compaction.attempts),checks=plain(host.check_results),source_results=plain(host.source_results),history_prefix_unchanged=plain(host.messages[:len(original.prompt.messages)])==plain(original.prompt.messages)),fresh=True)
    assert all(sha(root/p)==h for p,h in frozen['source_hashes'].items())
    candidate=json.loads((out/'candidate.json').read_text()) if (out/'candidate.json').exists() else {}
    if candidate:
        grading=STATE/'grade';grading.mkdir()
        for p in (HERE/'fixture').glob('*.py'): write(TextFile(resolve_path(grading/p.name),candidate.get(p.name,p.read_text(encoding='utf-8'))))
        grade=await command(ROOT,sys.executable,'-B',str(HERE/'oracle.py'),str(grading))
    else: grade=dict(outcome='no candidate')
    save(out/'grade.json',grade,fresh=True)
    print(result.disposition,result.accepted,grade,timer.elapsed.total_seconds)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['freeze','run']);args=parser.parse_args()
    asyncio.run(freeze() if args.mode=='freeze' else run())
