"""Explicit finite oracle gate; uses pytest and managed Commands, never inference."""
from __future__ import annotations
import ast,asyncio,json,sys,xml.etree.ElementTree as ET
from dataclasses import asdict
from pathlib import Path
import support as s
from devtools.core.paths import resolve_path
from devtools.core.time import Duration,Timestamp
from devtools.evaluation.preflight import OracleComparison,check_oracle_expectations
from devtools.resources.commands import Command

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];STATE=ROOT/'.local/host-cohesion'

async def suite(label,paths,expected_failures=()):
    xml=STATE/(label+'.xml')
    if xml.exists():raise FileExistsError(xml)
    command=Command(sys.executable).args('-B','-X','utf8','-m','pytest','--no-cov','-q','--tb=short',*paths,'--junitxml='+str(xml)).cwd(resolve_path(ROOT)).with_timeout(Duration.seconds(120))
    result=await s.managed(command,label)
    assert not result.stdout_truncated and not result.stderr_truncated
    root=ET.parse(xml).getroot();cases=root.findall('.//testcase')
    assert cases and not root.findall('.//error') and not root.findall('.//skipped')
    failed={case.attrib['name'] for case in cases if case.find('failure') is not None}
    assert failed==set(expected_failures),(label,failed)
    assert result.exit_code==(1 if failed else 0)
    return dict(command=s.plain(command),exit_code=result.exit_code,passed=len(cases)-len(failed),failed=sorted(failed),errors=0,xml_sha256=s.digest(xml),stdout=result.stdout.decode('utf-8'),stderr=result.stderr.decode('utf-8'))

def historical_review():
    prior=ROOT/'experiments/local_agent_reliability'
    module=ast.parse((prior/'fixture/focused.py').read_text(encoding='utf-8'))
    values=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='cases')
    reservations,window,expected=values[1];cells=[x for x in range(*window) if any(a<=x<b for a,b in reservations)]
    clipped=[(max(a,window[0]),min(b,window[1])) for a,b in reservations]
    assert cells==[2,5] and sum(b-a for a,b in clipped)==2 and expected==3
    candidate=json.loads((prior/'evidence/candidate.json').read_text())['occupancy.py']
    response=json.loads((prior/'evidence/acting-5.json').read_text())['response']
    spans=[]
    for call in response['tool_calls']:
        args=json.loads(call['arguments_json']);old=args['old_text'];assert candidate.count(old)==1
        begin=candidate.index(old);spans.append(dict(call_id=call['provider_call_id'],path=args['path'],start=begin,end=begin+len(old)))
    overlap=[max(x['start'] for x in spans),min(x['end'] for x in spans)];assert overlap[0]<overlap[1]
    result=json.loads((prior/'evidence/result.json').read_text())
    feedback=[m for m in result['messages'] if m['role']=='tool' and m['tool_call_id'] in {x['call_id'] for x in spans}]
    assert len(feedback)==2 and all(json.loads(m['content'])==dict(status='REFUSED',reason='Edit anchors overlap.') for m in feedback)
    return dict(interval=dict(reservations=reservations,window=window,frozen_expected=expected,clipped=clipped,unit_cells=cells,independent_expected=2),overlap=dict(spans=spans,intersection=overlap,shared_text=candidate[slice(*overlap)],feedback=feedback,disposition=result['result']['disposition'],progress=result['result']['progress']),conclusion='Atomic refusal was correct. The second of two authorized proposals exhausted the run. Existing feedback identifies overlap; original exact calls identify the two conflicting anchors. No edit-engine change is justified for this case.')

async def run():
    assert not (HERE/'preflight.json').exists()
    review=historical_review()
    sizes={p.name:p.stat().st_size for p in (ROOT/'src/devtools/agents/coding').glob('*.py')}
    assert all(size<32768 for size in sizes.values()) and 32768-sizes['repository.py']>=2048
    feasibility=dict(passed=True,sizes=sizes,source_limit=32768,repository_margin=32768-sizes['repository.py'],region_limit=4096,aggregate_limit=8192,operations=2,assessment='Existing host offers bounded initial/prepare composition seams; the metadata obligation can be expressed with localized additions and refresh handling, without new files, a framework or limit changes. More than 2 KiB of whole-file margin and independent 4 KiB region / 8 KiB aggregate limits remain. This is a feasibility assessment, not a reference patch or guarantee of model success.')
    comparisons=(OracleComparison('inventory-addresses','inventory','normal',2,len({'package/source.py','README.md'}),'independent permitted-address set'),OracleComparison('utf8-boundary','inventory','boundary',1,len('é'.encode('utf-8'))-len('é'),'UTF-8 encoding specification and raw file byte controls'),OracleComparison('empty-resource','inventory','empty',0,len(b''),'empty byte sequence'),OracleComparison('interval-review','review','boundary',2,len(review['interval']['unit_cells']),'independent occupied-unit-cell enumeration'))
    issues=check_oracle_expectations(obligations=('inventory','review'),comparisons=comparisons);assert not issues
    reference=await suite('positive-reference',['experiments/local_maintenance_cohesion/reference_checks.py'])
    focused=await suite('focused-baseline',['experiments/local_maintenance_cohesion/focused.py'],('test_first_request_scoped_inventory','test_inventory_not_duplicated_on_prepare','test_inventory_charged_to_prompt_budget'))
    heldout=await suite('heldout-baseline',['experiments/local_maintenance_cohesion/heldout.py'],('test_current_snapshot_not_cached','test_native_correlation_and_metadata_coexist','test_empty_resource_unicode_and_readonly','test_projection_preserves_metadata_and_objective','test_utf8_size_differs_from_character_count'))
    value=dict(at=str(Timestamp.now()),status='passed',feasibility=feasibility,comparisons=[asdict(c) for c in comparisons],issues=issues,reference=reference,focused=focused,heldout=heldout,historical_review=review,qualification='Finite empirical cross-checks and private reference observations; not proof of all behavior. Reference/heldout code is excluded from model read scope. Baseline failures are exact assertions, not runtime or collection errors.')
    s.save(HERE/'preflight.json',value,fresh=True)
    print(json.dumps(dict(status='passed',reference_passed=reference['passed'],focused=focused['failed'],heldout=heldout['failed'],overlap=review['overlap']['intersection'])))

if __name__=='__main__':asyncio.run(run())
