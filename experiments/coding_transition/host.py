"""One read-only four-call diagnostic; all decisions run through the shared agent."""
from __future__ import annotations
import argparse, asyncio, hashlib, json, sys
from dataclasses import replace
from pathlib import Path
import support as s
from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.navigation import NavigationPolicy
from devtools.agents.coding.projection import ProjectionPolicy, request_bytes, source_feedback
from devtools.agents.coding.repository import CodingObjective, EditLimits, RepositoryCodingHost
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Timestamp, Stopwatch
from devtools.models.interaction import InteractionSource, ModelResponse, ModelSettings, PromptMessage
from devtools.resources.commands import Command
from devtools.tools import ToolRunner
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.source import ScopedSourceTool, SourceScope
from scripts.backlog.checkout import Checkout
from scripts.backlog.work import WorkCycle

ROOT=s.CANONICAL; CASE=s.CASE; STATE=s.STATE
TOOLS=frozenset({'read_source','find_source','read_source_unit'})
READ=tuple(RepositoryResourceAddress(p) for p in (
    'src/devtools/agents/coding/repository.py','src/devtools/agents/coding/navigation.py',
    'src/devtools/agents/coding/projection.py','src/devtools/agents/coding/edits.py',
    'src/devtools/agents/coding/process.py','src/devtools/agents/coding/models.py',
    'src/devtools/tools/source.py','src/devtools/tools/checks.py',
    'src/devtools/context/repository/snapshot.py','src/devtools/context/repository/resource.py',
    'src/devtools/models/interaction/prompt.py','tests/agents/coding/test_repository.py',
    'src/devtools/agents/coding/docs/overview.md',
    'experiments/local_maintenance_task_navigation/focused.py',
))
NAMES=frozenset({'RepositoryCodingHost.__init__','RepositoryCodingHost.build_request',
    'RepositoryCodingHost.prepare','RepositoryCodingHost.apply','SourceScope',
    'assert_metadata','test_inventory_charged_to_prompt_budget'})
LIMITS=CodingLimits(4,1,6,Duration.seconds(90),Duration.seconds(360))

class Host(RepositoryCodingHost):
    def build_request(self,messages):
        request=super().build_request(messages)
        return replace(request,tools=tuple(t for t in request.tools if t.name in TOOLS),
            provider_settings=s.LlamaCppRequestSettings(**s.QWEN38_INSTRUCT_SAMPLING))

    def classify(self,response):
        if any(c.name not in TOOLS for c in response.tool_calls):
            raise ValueError('Read-only diagnostic refuses non-navigation operation')
        return super().classify(response)

def observe(repository):
    scope=SourceScope.observe(root=resolve_path(ROOT),repository=repository,addresses=READ,maximum_resource_bytes=32768)
    corpus=define_repository_text_corpus(discovery=discover_repository_resource_addresses(
        repository=repository,root=scope.root,requested_addresses=READ,
        maximum_resource_count=32,maximum_traversal_entry_count=256),selected_addresses=READ)
    return scope,corpus

def host_for(scope,corpus):
    # Required objective contract, never advertised or executed by this read-only host.
    checks=FixedCheckPlan(scope.root,(FixedCheck('unavailable-in-read-only-diagnostic',
        Command(sys.executable).args('-I','-c','raise SystemExit(77)').cwd(scope.root).with_timeout(Duration.seconds(1))),),scope)
    async def authorize(call,arguments):
        if call.name not in TOOLS:raise PermissionError('Outside frozen read-only authority')
    async def effect(changes):raise PermissionError('No edit authority')
    def archive(values):
        assert all(text==next(r.content for r in scope.snapshot.resources if r.address==address) for address,text in values.items())
    def restore(address,text):
        # CodingObjective requires a nonempty custody surface. No write is allowed.
        assert (ROOT/address.value).read_bytes().decode('utf-8')==text
    return Host(CodingObjective((CASE/'objective.md').read_text(encoding='utf-8'),scope,(READ[0],),checks,
        EditLimits(4096,32768,8192,2),8192,32768),corpus=corpus,authorize=authorize,
        apply_changes=effect,archive=archive,restore=restore,
        settings=ModelSettings(maximum_output_tokens=4096,thinking_enabled=False),navigation=True,
        navigation_policy=NavigationPolicy(6,6144,2),
        projection=ProjectionPolicy(24576,20000,frozenset({'find_source'}),report_source_state=True))

async def preload(host):
    # Explicit host selection, not fabricated native calls or autonomous discovery.
    records=[]
    units=[u for u in host.index.views[1].units if u.qualified_name in NAMES]
    assert len(units)==7
    for unit in units:
        option=SourceRangeDisclosureOption('Authorized diagnostic working set',unit,unit.start,unit.end,8192)
        materialized=await ToolRunner().execute(ScopedSourceTool(host.scope,maximum_bytes=8192),option)
        assert not option.truncated
        host.disclosures.append(option);host.source_results.append(materialized)
        host._source_messages[len(host.messages)]=(option,)
        host.messages.append(PromptMessage('user',json.dumps({**source_feedback(option,materialized.items[0].text),
            'host_selected_unit':unit.qualified_name},ensure_ascii=False)))
        records.append(dict(trigger='host',tool='ScopedSourceTool',name=unit.qualified_name,
            path=unit.resource.address.value,span=list(option.span),snapshot=str(option.snapshot_id),
            content_identity=str(unit.resource.content_identity),bytes=len(option.text.encode()),partial=False))
    return records

def files():
    return {p.name:s.digest(p) for p in CASE.iterdir() if p.suffix in {'.py','.md'} and p.name not in {'REPORT.md','README.md'}}

async def preview():
    scope,corpus=observe(Repository.new());host=host_for(scope,corpus)
    disclosed=await preload(host)
    request=await host.prepare(CodingProgress(LIMITS))
    assert request_bytes(request)<=32768 and len(host.active_disclosures)==7
    assert not any(m.tool_calls or m.tool_call_id for m in request.prompt.messages)
    assert {t.name for t in request.tools}==TOOLS
    class ScriptedPreflight:
        source=InteractionSource('explicit-deterministic-preflight-not-live')
        async def send(self,request):return ModelResponse('Preflight stop only; no behavioral claim.',self.source)
    result=await run_coding_agent(ScriptedPreflight(),limits=LIMITS,host=host)
    assert result.disposition=='stopped' and result.custody.restored and result.progress.actions==0
    s.save(STATE.parent/'preflight.json',dict(at=str(Timestamp.now()),status='passed',
        qualification='Read-only source/interaction feasibility, not an oracle certifying B-0035 implementation.',
        complete_bytes=request_bytes(request),host_disclosures=disclosed,active_sources=len(host.active_disclosures),
        hidden_oracle_disclosed=False,live_model_calls=0,scripted_preflight_calls=1,edits=0,checks=0))
    print(json.dumps(dict(bytes=request_bytes(request),sources=len(host.active_disclosures))))

async def freeze():
    assert not (CASE/'freeze.json').exists() and not (STATE/'ENTERED.json').exists()
    assert not await s.git(ROOT,'diff','--name-only') and not await s.git(ROOT,'diff','--cached','--name-only')
    assert not (ROOT/'.local/backlog/checkout-owner').exists()
    gate=json.loads((STATE.parent/'protected.json').read_text());assert gate['exit_code']==0 and gate['inputs_unchanged']
    for p,h in gate['inputs'].items():assert s.digest(ROOT/p)==h,p
    preflight=json.loads((STATE.parent/'preflight.json').read_text());assert preflight['status']=='passed'
    model=await s.service_identity();assert model['context']==32768
    scope,corpus=observe(Repository.new());host=host_for(scope,corpus)
    records=await preload(host);request=await host.prepare(CodingProgress(LIMITS))
    untracked=list(filter(None,(await s.git(ROOT,'ls-files','--others','--exclude-standard','-z')).split('\0')))
    value=dict(schema='coding-transition-diagnostic-v1',at=str(Timestamp.now()),source_head=await s.git(ROOT,'rev-parse','HEAD'),
        repository_id=str(scope.snapshot.repository_id),snapshot_id=str(scope.snapshot.id),source_snapshot=s.plain(scope.snapshot),
        source_sha256={a.value:s.digest(ROOT/a.value) for a in READ},files=files(),
        starting_untracked={p:s.digest(ROOT/p) for p in untracked},model=model,
        limits=dict(acting_calls=4,auxiliary_calls=0,tool_actions=6,edits=0,checks=0,call_seconds=90,
            agent_seconds=360,outer_seconds=420,input_tokens=28160,output_tokens=4096,prompt_bytes=32768,disclosure_bytes=8192),
        host_disclosures=records,initial_request=s.plain(request),initial_bytes=request_bytes(request),
        tools=sorted(TOOLS),editable=[],compatibility_custody_surface=[READ[0].value],preflight=preflight,protected_implementation=gate['head'],
        scoring=dict(pass_condition='At least one source-supported concrete next engineering action or specific genuinely missing contract/blocker. Independent review must cite response and actual disclosed source; generic readiness or smaller Context alone is insufficient.',
            failure='Only repeated investigation, unsupported action, false completion, or no specific next step before the finite limit.',
            incomplete='Provider/capacity/custody error prevents a qualified behavioral observation.',
            exclusion='No maintenance success, candidate correctness, causal benefit of annotation, or model-general effectiveness can be established by this read-only single sample.'),
        privacy='Public scoped source and public focused diagnostics only; no hidden oracle, reference patch, credentials or environment disclosure.')
    value['digest']=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    s.save(CASE/'freeze.json',value,fresh=True);print(json.dumps(dict(bytes=value['initial_bytes'],digest=value['digest'])))

async def run():
    frozen=json.loads((CASE/'freeze.json').read_text());assert files()==frozen['files']
    assert await s.service_identity()==frozen['model']
    for p,h in frozen['source_sha256'].items():assert s.digest(ROOT/p)==h,p
    head=await s.git(ROOT,'rev-parse','HEAD');await s.git(ROOT,'merge-base','--is-ancestor',frozen['source_head'],head)
    scope,corpus=observe(Repository(RepositoryId.parse(frozen['repository_id'])))
    assert str(scope.snapshot.id)==frozen['snapshot_id']
    checkout=Checkout(WorkCycle(ROOT),'investigation-transition-0001','main',head)
    async with checkout:
        s.save(STATE/'ENTERED.json',dict(at=str(Timestamp.now()),head=head,digest=frozen['digest'],owner=checkout.record),fresh=True)
        host=host_for(scope,corpus);records=await preload(host)
        initial=await host.prepare(CodingProgress(LIMITS));assert s.plain(initial)==frozen['initial_request']
        # Avoid counting a preparation check as an acting request or prior consumption.
        host.requests.clear();host.projection_outcomes.clear();host.active_disclosures=()
        model=s.MeasuredInteraction();timer=Stopwatch()
        result=await run_coding_agent(model,limits=LIMITS,host=host);timer.stop()
        s.save(STATE/'result.json',dict(at=str(Timestamp.now()),result=s.plain(result),seconds=timer.elapsed.total_seconds,
            host_disclosures=records,requests=model.records,messages=s.plain(host.messages),
            projections=s.plain(host.projection_outcomes),source_results=s.plain(host.source_results),
            command_records=s.RECORDS,command_observations=s.plain(s.OBSERVATIONS)),fresh=True)
        assert result.custody.restored and not result.custody.reconciliation_required
    assert not (ROOT/'.local/backlog/checkout-owner').exists()
    for p,h in frozen['source_sha256'].items():assert s.digest(ROOT/p)==h,p
    for p,h in frozen['starting_untracked'].items():assert s.digest(ROOT/p)==h,p
    s.save(STATE/'terminal.json',dict(at=str(Timestamp.now()),disposition=result.disposition,model_calls=result.progress.model_calls,
        actions=result.progress.actions,proposals=result.progress.proposals,seconds=timer.elapsed.total_seconds,
        source_unchanged=True,checkout_released=True,accepted=result.accepted),fresh=True)
    print((STATE/'terminal.json').read_text())

async def main(action):
    async with asyncio.timeout(420):await {'preview':preview,'freeze':freeze,'run':run}[action]()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['preview','freeze','run'])
    asyncio.run(main(parser.parse_args().action))
