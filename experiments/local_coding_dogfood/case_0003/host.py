"""One authorized real maintenance attempt in the guarded canonical checkout."""
from __future__ import annotations
import argparse, asyncio, hashlib, json, sys
from dataclasses import replace
from pathlib import Path
import support as s
import composition as c
from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding.repository import CodingObjective, EditLimits, write_source_changes
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Stopwatch, Timestamp
from devtools.models.interaction import ModelSettings
from devtools.observability.commands.models import CommandOrigin
from devtools.observability.commands.patterns import summarize_patterns
from devtools.resources.commands import Command, CommandOutputPolicy
from devtools.resources.filesystem import BinaryFile, TextFile, write
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.repository.validation import ChangeValidationPlan, CheckSelection, InspectAndValidateTool
from devtools.tools.source import SourceScope
from scripts.backlog.checkout import Checkout
from scripts.backlog.work import WorkCycle

CASE,STATE,ROOT=s.CASE,s.STATE,s.CANONICAL
BASE='721978cb9f88833a3dc3ecadc80e84aa2c6d4735'
EDITABLE=tuple(RepositoryResourceAddress(p.relative_to(ROOT).as_posix()) for p in sorted((ROOT/'src/devtools/agents/coding').glob('*.py')))
READ=EDITABLE+tuple(RepositoryResourceAddress(p) for p in [
 'src/devtools/agents/model_tools.py','src/devtools/tools/source.py','src/devtools/tools/checks.py',
 'src/devtools/context/repository/snapshot.py','src/devtools/context/repository/resource.py',
 'src/devtools/models/interaction/prompt.py','tests/agents/coding/test_inventory.py',
 'tests/agents/coding/test_repository.py','src/devtools/agents/coding/docs/overview.md',
 'docs/development/bounded-coding-agent.md','docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md',
])
c.CASE,c.CANONICAL,c.STATE=CASE,ROOT,STATE
c.EDITABLE=EDITABLE

def checks(root,scope):
 return FixedCheckPlan(resolve_path(root),(
  FixedCheck('focused-acceptance',Command(sys.executable).args('-B','-m','pytest','--no-cov','-q','tests/agents/coding/test_inventory.py','tests/agents/coding/test_repository.py').cwd(scope.root).with_timeout(Duration.seconds(60))),
  FixedCheck('coding-lint',Command('uv').args('run','ruff','check','src/devtools/agents/coding').cwd(scope.root).with_timeout(Duration.seconds(30))),
  FixedCheck('coding-format',Command('uv').args('run','ruff','format','--check','src/devtools/agents/coding').cwd(scope.root).with_timeout(Duration.seconds(30))),
 ),source_scope=scope,output_policy=CommandOutputPolicy(max_stdout_bytes=8192,max_stderr_bytes=8192))

def procedure_tool(root,scope,revision,label):
 frozen=json.loads((CASE/'freeze.json').read_text())
 allowed=frozenset(EDITABLE)|frozenset(RepositoryResourceAddress(n) for n in frozen['starting_untracked'])
 return InspectAndValidateTool(ChangeValidationPlan(checks(root,scope),revision,allowed,tuple(CheckSelection(n) for n in ['focused-acceptance','coding-lint','coding-format'])),origin=CommandOrigin('local-maintenance-host','B-0035','primary-0003',label))
c.procedure_tool=procedure_tool

def observe(repository):
 scope=SourceScope.observe(root=resolve_path(ROOT),repository=repository,addresses=READ,maximum_resource_bytes=32768)
 corpus=define_repository_text_corpus(discovery=discover_repository_resource_addresses(repository=repository,root=scope.root,requested_addresses=READ,maximum_resource_count=32,maximum_traversal_entry_count=256),selected_addresses=READ)
 return scope,corpus

def objective(scope):
 text=(CASE/'objective.md').read_text()+ '\nNative tools: list_repository/search_source return scoped metadata, read_source discloses exact character spans. Read before grounded replace_source. Budget: eight requests/three proposals, twenty acquisition actions; no arbitrary commands. Use small exact anchors within acquired ranges. Tests and fixed checks are immutable.\n'
 return CodingObjective(text,scope,EDITABLE,checks(ROOT,scope),EditLimits(4096,32768,8192,2),8192,32768)

def all_frozen():
 return {p.relative_to(ROOT).as_posix():s.digest(p) for p in sorted(CASE.glob('*.py'))+ [CASE/'objective.md',ROOT/'tests/agents/coding/test_inventory.py']}

async def prepare():
 assert not (CASE/'freeze.json').exists() and not (STATE/'ENTERED.json').exists()
 assert await s.git(ROOT,'rev-parse','HEAD')==BASE and not await s.git(ROOT,'diff','--name-only') and not await s.git(ROOT,'diff','--cached','--name-only') and not (ROOT/'.local/backlog/checkout-owner').exists()
 identity=await s.service_identity();assert identity['context']==32768
 scope,corpus=observe(Repository.new())
 baseline=await s.managed(checks(ROOT,scope).checks[0].command,'baseline-focused')
 hidden=await s.managed(Command(sys.executable).args('-B','-m','pytest','--no-cov','-q',str(CASE/'oracle.py')).cwd(scope.root).with_timeout(Duration.seconds(60)),'baseline-heldout')
 assert baseline.exit_code==hidden.exit_code==1
 input_text=objective(scope).text;s.save(STATE/'initial-prompt.json',dict(content=input_text),fresh=True)
 untracked=set(filter(None,(await s.git(ROOT,'ls-files','--others','--exclude-standard','-z')).split('\0')))
 frozen=dict(schema='local-framework-maintenance-freeze-v1',at=str(Timestamp.now()),canonical_main=BASE,canonical_root=str(ROOT),backlog='docs/backlog/items/B-0035-investigate-tool-facing-capability-exposure.md',selection='Existing Case0002 follow-up under B-0035: complete bounded initial resource metadata avoids a listing-only model request; standard neutral coding host is the consumer. Delivered bugs excluded; frozen experiment repairs excluded; large cohesion and architectural decisions excluded.',repository_id=str(scope.snapshot.repository_id),snapshot_id=str(scope.snapshot.id),source_snapshot=s.plain(scope.snapshot),source_blobs={a.value:await s.git(ROOT,'hash-object','--path='+a.value,a.value) for a in READ},source_sha256={a.value:s.digest(ROOT/a.value) for a in READ},editable=[a.value for a in EDITABLE],readable=[a.value for a in READ],files=all_frozen(),prompt_sha256=s.digest(STATE/'initial-prompt.json'),starting_untracked={n:s.digest(ROOT/n) for n in sorted(untracked)},model=identity,settings=dict(thinking_enabled=False,maximum_output_tokens=4096,sampling=s.QWEN38_INSTRUCT_SAMPLING),limits=dict(model_requests=8,edit_proposals=3,repair_opportunities=2,acquisition_actions=20,call_seconds=150,agent_wall_seconds=1080,outer_wall_seconds=1200,input_tokens=28160,output_tokens=4096,prompt_bytes=32768,disclosure_bytes=8192,source_bytes=32768,region_bytes=4096,aggregate_bytes=8192,operations=2),tools=['list_repository','search_source','read_source','replace_source','validate_candidate','inspect_and_validate_change'],checks=s.plain(checks(ROOT,scope)),baseline=s.RECORDS,scoring=dict(candidate='All frozen focused checks and hidden oracle plus independent minimality/authority review; exact model bytes only.',worker='accepted, completed, restored known source; no unknown or unauthorized effects.',integration='Separate review, committed protected gate, actual ordinary publication; no automatic authority.'),privacy='Selected public project source and bounded fixed-test output only; no private log/environment collection. Source scope is not an OS sandbox; host inspects unexpected changes. No model Git/publication authority.')
 frozen['baseline_raw']={a.value:(ROOT/a.value).read_bytes().hex() for a in EDITABLE}
 frozen['task_digest']=hashlib.sha256(json.dumps(frozen,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 s.save(CASE/'freeze.json',frozen,fresh=True);s.save(STATE/'prepare-records.json',s.RECORDS)
 print(json.dumps(dict(snapshot=frozen['snapshot_id'],digest=frozen['task_digest'],read=len(READ),editable=len(EDITABLE),model_ready=True)))

async def run():
 frozen=json.loads((CASE/'freeze.json').read_text());assert all_frozen()==frozen['files'] and s.digest(STATE/'initial-prompt.json')==frozen['prompt_sha256']
 assert await s.git(ROOT,'rev-parse','HEAD')==BASE
 for n,h in frozen['source_sha256'].items():assert s.digest(ROOT/n)==h,n
 identity=await s.service_identity();assert identity['profile_fingerprint']==frozen['model']['profile_fingerprint']
 scope,corpus=observe(Repository(RepositoryId.parse(frozen['repository_id'])));assert str(scope.snapshot.id)==frozen['snapshot_id']
 cycle=WorkCycle(ROOT)
 checkout=Checkout(cycle,'local-maintenance-case0003','main',BASE,files=[dict(path=a.value,text=(ROOT/a.value).read_text(encoding='utf-8')) for a in EDITABLE])
 admissions=[];applied=[]
 async with checkout:
  s.save(STATE/'ENTERED.json',dict(at=str(Timestamp.now()),task_digest=frozen['task_digest'],checkout_owner=checkout.record),fresh=True)
  def archive(current):
   target=STATE/'candidate';hashes={}
   for address,text in current.items():
    assert address in EDITABLE and text is not None
    destination=target/address.value;destination.parent.mkdir(parents=True,exist_ok=True)
    raw=(ROOT/address.value).read_bytes();assert raw.decode('utf-8')==text
    write(BinaryFile(resolve_path(destination),raw),overwrite=False);hashes[address.value]=s.digest(destination)
   s.save(STATE/'candidate-hashes.json',hashes,fresh=True)
  def restore(address,text):
   assert address in EDITABLE and text is not None
   # Restore exact original Git worktree bytes, including line endings.
   original=frozen['source_snapshot']['resources'];before=next(r['content'] for r in original if r['address']['value']==address.value)
   assert before==text
   raw=bytes.fromhex(frozen['baseline_raw'][address.value])
   write(BinaryFile(resolve_path(ROOT/address.value),raw))
  async def authorize(call,value):
   assert call.name in frozen['tools'];admissions.append(dict(id=call.provider_call_id,name=call.name,typed_input=type(value).__name__))
  async def effect(changes):
   for change in changes:assert change.address in EDITABLE;checkout.expect(change.address.value,change.after)
   applied.append(s.plain(changes));write_source_changes(scope.root,changes)
  host=c.Host(objective(scope),corpus=corpus,authorize=authorize,apply_changes=effect,archive=archive,restore=restore,settings=ModelSettings(maximum_output_tokens=4096,thinking_enabled=False))
  host.revision=BASE;host.acquisitions=[];host.proposal_events=[];host.procedures=[]
  interaction=s.MeasuredInteraction();timer=Stopwatch()
  result=await run_coding_agent(interaction,limits=CodingLimits(8,3,20,Duration.seconds(150),Duration.seconds(1080)),host=host)
  timer.stop();s.save(STATE/'worker-result.json',dict(at=str(Timestamp.now()),result=s.plain(result),accepted=result.accepted,seconds=timer.elapsed.total_seconds,admissions=admissions,applied=applied,acquisitions=host.acquisitions,proposals=host.proposal_events,procedures=host.procedures,requests=interaction.records,messages=s.plain(host.messages)),fresh=True)
  assert host.last_completion.restored and not host.last_completion.reconciliation_required,'Unknown source: retain Checkout owner for explicit reconciliation'
 assert not await s.git(ROOT,'diff','--name-only')
 for n,h in frozen['starting_untracked'].items():assert s.digest(ROOT/n)==h,n
 s.save(STATE/'outcome.json',dict(at=str(Timestamp.now()),task_digest=frozen['task_digest'],accepted=result.accepted,disposition=result.disposition,candidate_validated=result.candidate_validated,completed=result.completed,failure_phase=result.failure_phase,model_calls=result.progress.model_calls,proposals=result.progress.proposals,actions=result.progress.actions,seconds=timer.elapsed.total_seconds,restored=True,command_records=s.RECORDS,command_observations=s.plain(s.OBSERVATIONS),patterns=s.plain(summarize_patterns(tuple(s.OBSERVATIONS)))),fresh=True)
 print(json.dumps(dict(accepted=result.accepted,disposition=result.disposition,calls=result.progress.model_calls,proposals=result.progress.proposals,seconds=timer.elapsed.total_seconds)))

if __name__=='__main__':
 action=argparse.ArgumentParser();action.add_argument('action',choices=['prepare','run']);args=action.parse_args()
 asyncio.run(prepare() if args.action=='prepare' else run())
