"""One post-extraction canonical-checkout attempt; the framework owns the loop."""
from __future__ import annotations
import argparse,asyncio,hashlib,json,sys
from pathlib import Path
import composition as c
import support as s
from devtools.agents.coding import CodingLimits,run_coding_agent
from devtools.agents.coding.repository import CodingObjective,EditLimits,write_source_changes
from devtools.agents.coding.projection import ProjectionPolicy
from devtools.agents.coding.navigation import NavigationPolicy
from devtools.context import Repository,RepositoryResourceAddress
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.core.paths import resolve_path
from devtools.core.time import Duration,Stopwatch,Timestamp
from devtools.models.interaction import ModelSettings
from devtools.observability.commands.models import CommandOrigin
from devtools.observability.commands.patterns import summarize_patterns
from devtools.resources.commands import Command,CommandOutputPolicy
from devtools.resources.filesystem import BinaryFile,write
from devtools.tools.checks import FixedCheck,FixedCheckPlan
from devtools.tools.repository.validation import ChangeValidationPlan,CheckSelection,InspectAndValidateTool
from devtools.tools.source import SourceScope
from scripts.backlog.checkout import Checkout
from scripts.backlog.work import WorkCycle

HERE=s.CASE;ROOT=s.CANONICAL;STATE=s.STATE
EDITABLE=tuple(RepositoryResourceAddress(p.relative_to(ROOT).as_posix()) for p in sorted((ROOT/'src/devtools/agents/coding').glob('*.py')))
READ=EDITABLE+tuple(RepositoryResourceAddress(p) for p in ('src/devtools/agents/model_tools.py','src/devtools/tools/source.py','src/devtools/tools/checks.py','src/devtools/context/repository/snapshot.py','src/devtools/context/repository/resource.py','src/devtools/models/interaction/prompt.py','tests/agents/coding/test_repository.py','src/devtools/agents/coding/docs/overview.md','experiments/local_maintenance_task_navigation/focused.py'))

def checks(scope):
    specs=(('focused-acceptance',sys.executable,('-B','-X','utf8','-m','pytest','--no-cov','-q','--tb=short','experiments/local_maintenance_task_navigation/focused.py','tests/agents/coding/test_repository.py'),90),('coding-lint','uv',('run','ruff','check','src/devtools/agents/coding'),30),('coding-format','uv',('run','ruff','format','--check','src/devtools/agents/coding'),30),('strict-typing','uv',('run','mypy'),60))
    return FixedCheckPlan(scope.root,tuple(FixedCheck(n,Command(exe).args(*args).cwd(scope.root).with_timeout(Duration.seconds(t))) for n,exe,args,t in specs),scope,CommandOutputPolicy(max_stdout_bytes=16384,max_stderr_bytes=8192))

def procedure_tool(root,scope,revision,label):
    frozen=json.loads((HERE/'freeze.json').read_text())
    allowed=frozenset(EDITABLE)|frozenset(RepositoryResourceAddress(p) for p in frozen['starting_untracked'])
    return InspectAndValidateTool(ChangeValidationPlan(checks(scope),revision,allowed,tuple(CheckSelection(ch.name) for ch in checks(scope).checks)),origin=CommandOrigin('local-maintenance-host','B-0035','maintenance-task-navigation-0001',label))
c.procedure_tool=procedure_tool

def observe(repository):
    scope=SourceScope.observe(root=resolve_path(ROOT),repository=repository,addresses=READ,maximum_resource_bytes=32768)
    corpus=define_repository_text_corpus(discovery=discover_repository_resource_addresses(repository=repository,root=scope.root,requested_addresses=READ,maximum_resource_count=32,maximum_traversal_entry_count=256),selected_addresses=READ)
    return scope,corpus

def objective(scope):
    text=(HERE/'objective.md').read_text(encoding='utf-8')+'\nThe initial task_candidates view is an incomplete lexical suggestion, not the required inventory. Select exact source with read_source_unit, refine find_source query/path/mode when needed, or explicitly browse with browse=true within the two-action outline allowance. An omitted query searches the objective prefix. You choose the investigation and edits. read_source remains available for adjacent Unicode ranges or generic resources. Metadata is not source; acquire exact current source before edits. Limits: ten requests, four proposals, at most three applied candidates (two validation-feedback repairs), twenty acquisition actions. The resulting-source ceiling remains 32768 bytes per file. No source/edit limits may be increased.\n'
    return CodingObjective(text,scope,EDITABLE,checks(scope),EditLimits(4096,32768,8192,2),8192,32768)

def frozen_files():
    return {p.name:s.digest(p) for p in HERE.iterdir() if p.suffix in {'.py','.md'} and p.name not in {'REPORT.md','SUMMARY.md','README.md'}}|{'preflight.json':s.digest(HERE/'preflight.json')}

async def freeze():
    assert not (HERE/'freeze.json').exists() and not (STATE/'ENTERED.json').exists()
    assert not await s.git(ROOT,'diff','--name-only') and not await s.git(ROOT,'diff','--cached','--name-only')
    assert not (ROOT/'.local/backlog/checkout-owner').exists()
    preflight=json.loads((HERE/'preflight.json').read_text());assert preflight['status']=='passed' and preflight['reference']['passed']==10 and preflight['feasibility']['passed']
    gate=json.loads((ROOT/'.local/task-navigation/protected.json').read_text());assert gate['exit_code']==0 and gate['inputs_unchanged']
    for path,digest in gate['inputs'].items():assert s.digest(ROOT/path)==digest,path
    model=await s.service_identity();assert model['context']==32768
    scope,corpus=observe(Repository.new());del corpus
    head=await s.git(ROOT,'rev-parse','HEAD')
    untracked=list(filter(None,(await s.git(ROOT,'ls-files','--others','--exclude-standard','-z')).split('\0')))
    value=dict(schema='maintenance-feedback-freeze-v1',at=str(Timestamp.now()),source_head=head,task='B-0035 first-request authorized inventory',root=str(ROOT),repository_id=str(scope.snapshot.repository_id),snapshot_id=str(scope.snapshot.id),source_snapshot=s.plain(scope.snapshot),source_sha256={a.value:s.digest(ROOT/a.value) for a in READ},source_blobs={a.value:await s.git(ROOT,'hash-object','--path='+a.value,a.value) for a in READ},baseline_raw={a.value:(ROOT/a.value).read_bytes().hex() for a in EDITABLE},files=frozen_files(),editable=[a.value for a in EDITABLE],readable=[a.value for a in READ],starting_untracked={p:s.digest(ROOT/p) for p in untracked},model=model,sampling=s.QWEN38_INSTRUCT_SAMPLING,limits=dict(model_requests=10,proposals=4,applied_candidates=3,repair_opportunities=2,acquisition_actions=20,call_seconds=150,agent_seconds=1080,outer_seconds=1200,input_tokens=28160,output_tokens=4096,prompt_bytes=32768,disclosure_bytes=8192,source_bytes=32768,region_bytes=4096,aggregate_bytes=8192,operations=2),context=dict(strategy='deterministic only',trigger_bytes=24576,target_bytes=20000,metadata_operations=['find_source'],auxiliary_calls=0,reason='Fresh task with no useful prior working-state history; no auxiliary inference justified.'),navigation_policy=dict(maximum_candidates=6,maximum_bytes=6144,outline_actions=2,query='first 256 Unicode characters of actual objective',complete_inventory=False),tools=['find_source','read_source_unit','read_source','replace_source','validate_candidate','inspect_and_validate_change'],checks=s.plain(checks(scope)),objective=objective(scope).text,oracle_preflight=preflight['status'],validated_navigation=gate['head'],feasibility=preflight['feasibility'],prior_attempt='experiments/local_maintenance_navigation/freeze.json',scoring=dict(candidate='All frozen focused and withheld checks plus independent source/authority review; exact model bytes only.',worker='Known candidate validation, terminal completion and restoration reported separately.',integration='Independent review and committed protected validation required. No automatic publication or Codex replacement.'),privacy='Public authorized source only; reference_checks.py, heldout.py, preflight details and source implementations of hidden oracles are outside model scope. Source admission is not an OS sandbox.')
    value['digest']=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    s.save(HERE/'freeze.json',value,fresh=True)
    print(json.dumps(dict(head=head,digest=value['digest'],snapshot=value['snapshot_id'],read=len(READ),editable=len(EDITABLE))))

async def run():
    frozen=json.loads((HERE/'freeze.json').read_text());assert frozen_files()==frozen['files']
    head=await s.git(ROOT,'rev-parse','HEAD')
    await s.git(ROOT,'merge-base','--is-ancestor',frozen['source_head'],head)
    assert not await s.git(ROOT,'diff',frozen['source_head'],head,'--','src','tests','apps','scripts','pyproject.toml','uv.lock')
    for p,h in frozen['source_sha256'].items():assert s.digest(ROOT/p)==h,p
    assert await s.service_identity()==frozen['model']
    scope,corpus=observe(Repository(RepositoryId.parse(frozen['repository_id'])));assert str(scope.snapshot.id)==frozen['snapshot_id']
    checkout=Checkout(WorkCycle(ROOT),'local-maintenance-task-navigation-0001','main',head,files=[dict(path=a.value,text=(ROOT/a.value).read_bytes().decode('utf-8')) for a in EDITABLE])
    admissions=[];applied=[]
    async with checkout:
        s.save(STATE/'ENTERED.json',dict(at=str(Timestamp.now()),digest=frozen['digest'],head=head,owner=checkout.record),fresh=True)
        def archive(current):
            hashes={}
            for address,text in current.items():
                assert address in EDITABLE and text is not None
                raw=(ROOT/address.value).read_bytes();assert raw.decode('utf-8')==text
                target=STATE/'candidate'/address.value;target.parent.mkdir(parents=True,exist_ok=True)
                write(BinaryFile(resolve_path(target),raw),overwrite=False);hashes[address.value]=s.digest(target)
            s.save(STATE/'candidate-hashes.json',hashes,fresh=True)
        def restore(address,text):
            assert address in EDITABLE and text is not None
            raw=bytes.fromhex(frozen['baseline_raw'][address.value]);assert raw.decode('utf-8')==text
            write(BinaryFile(resolve_path(ROOT/address.value),raw))
        async def authorize(call,value):
            assert call.name in frozen['tools'];admissions.append(dict(id=call.provider_call_id,name=call.name,input=type(value).__name__))
        async def effect(changes):
            if len(applied)>=3:raise ValueError('Frozen two-repair envelope exhausted before application')
            for change in changes:assert change.address in EDITABLE;checkout.expect(change.address.value,change.after)
            applied.append(s.plain(changes));write_source_changes(scope.root,changes)
        host=c.Host(objective(scope),corpus=corpus,authorize=authorize,apply_changes=effect,archive=archive,restore=restore,settings=ModelSettings(maximum_output_tokens=4096,thinking_enabled=False),navigation=True,navigation_policy=NavigationPolicy(6,6144,2),projection=ProjectionPolicy(24576,20000,frozenset({'find_source'})))
        host.revision=head;host.acquisitions=[];host.proposal_events=[];host.procedures=[]
        model=s.MeasuredInteraction();timer=Stopwatch()
        result=await run_coding_agent(model,limits=CodingLimits(10,4,20,Duration.seconds(150),Duration.seconds(1080)),host=host)
        timer.stop()
        s.save(STATE/'result.json',dict(at=str(Timestamp.now()),result=s.plain(result),accepted=result.accepted,seconds=timer.elapsed.total_seconds,admissions=admissions,applied=applied,acquisitions=host.acquisitions,proposals=host.proposal_events,procedures=host.procedures,requests=model.records,messages=s.plain(host.messages),projections=s.plain(host.projection_outcomes),source_results=s.plain(host.source_results),command_records=s.RECORDS,command_observations=s.plain(s.OBSERVATIONS),patterns=s.plain(summarize_patterns(tuple(s.OBSERVATIONS)))),fresh=True)
        assert host.last_completion.restored and not host.last_completion.reconciliation_required,'Unknown source requires preserved owner/manual reconciliation'
    assert not await s.git(ROOT,'diff','--name-only')
    for p,h in frozen['starting_untracked'].items():assert s.digest(ROOT/p)==h,p
    s.save(STATE/'terminal.json',dict(at=str(Timestamp.now()),accepted=result.accepted,disposition=result.disposition,model_calls=result.progress.model_calls,proposals=result.progress.proposals,actions=result.progress.actions,seconds=timer.elapsed.total_seconds,restored=True),fresh=True)
    print(json.dumps(json.loads((STATE/'terminal.json').read_text())))

async def main(action):
    async with asyncio.timeout(1200):await (freeze() if action=='freeze' else run())
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['freeze','run']);asyncio.run(main(parser.parse_args().action))
