"""Read-only verification of the closed failed maintenance attempt; no inference."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,sys
from dataclasses import asdict
from pathlib import Path
from devtools.agents.coding import repository as owner
from devtools.agents.model_tools import normalize_tool_descriptor
from devtools.context.repository.resource import ContentIdentity
from devtools.models.interaction import ModelRequest,ModelSettings,ModelToolCall,Prompt,PromptMessage

C=Path(__file__).resolve().parent;R=C.parents[2]
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify():
 f=load(C/'freeze.json');copy=dict(f);digest=copy.pop('task_digest')
 assert hashlib.sha256(json.dumps(copy,sort_keys=True,separators=(',',':')).encode()).hexdigest()==digest
 relocation=load(C/'closed-input-map.json')['inputs']
 for name,value in f['files'].items():
  path=C/relocation[name]['retained'] if name in relocation else R/name
  assert sha(path)==value,name
 manifest=load(C/'manifest.json')
 for item in manifest['files']:
  assert sha(C/item['path'])==item['sha256'] and (C/item['path']).stat().st_size==item['bytes'],item['path']
 w=load(C/'evidence/worker-result.json');o=load(C/'evidence/outcome.json');d=load(C/'evidence/diagnosis.json')
 assert o['task_digest']==digest and o['accepted'] is False and o['disposition']=='failed'
 assert o['failure_phase']=='preparation' and not o['candidate_validated'] and not o['completed']
 assert w['result']['error']=='Coding Prompt byte budget exceeded.' and not w['result']['completion_error']
 assert w['result']['custody']['restored'] and not w['result']['custody']['reconciliation_required']
 assert not w['applied'] and not w['proposals'] and o['proposals']==0
 requests=w['requests'];assert len(requests)==o['model_calls']==5
 assert all(r['inference_entered'] and r['outcome']=='normalized-response' for r in requests)
 for r in requests:
  n=r['number'];assert load(C/f'evidence/request-{n}-outcome.json')==r
  assert r['measured_input_tokens']==r['response']['usage']['input_tokens']
 ids=[call['provider_call_id'] for r in requests for call in r['response']['tool_calls']]
 assert len(ids)==len(set(ids))==6
 assert all(e['acknowledged'] for e in w['result']['progress']['effects'])
 snapshots={v['address']['value']:v for v in f['source_snapshot']['resources']}
 trace=[]
 for a in w['acquisitions']:
  consumed=[r['number'] for r in requests if any(m['role']=='tool' and m['tool_call_id']==a['call_id'] and json.loads(m['content'])==a['result'] for m in r['request']['prompt']['messages'])]
  if a['kind']=='source':
   v=a['result'];source=snapshots[v['path']];start,end=v['span']
   assert v['snapshot']==f['snapshot_id'] and v['version']==str(ContentIdentity.from_text(source['content']))
   assert v['text']==source['content'][start:end] and len(v['text'].encode())<=8192
  trace.append(dict(kind=a['kind'],call_id=a['call_id'],arguments=a['arguments'],consumed_by=consumed))
 assert trace[-1]['consumed_by']==[] and all(t['consumed_by'] for t in trace[:-1])
 messages=tuple(PromptMessage(**{**m,'tool_calls':tuple(ModelToolCall(**v) for v in m['tool_calls'])}) for m in w['messages'])
 request=ModelRequest(Prompt('','messages',messages),settings=ModelSettings(maximum_output_tokens=4096,thinking_enabled=False),tools=tuple(normalize_tool_descriptor(v) for v in (owner._READ,owner._EDIT,owner._CHECK)))
 size=len(json.dumps(asdict(request),ensure_ascii=False).encode());assert size==d['next_request_bytes']==36640>32768
 for name,value in load(C/'evidence/candidate-hashes.json').items():
  assert value==f['source_sha256'][name]==sha(C/'evidence/unchanged-archive'/name)
 baseline=(C/'evidence/baseline.stdout').read_bytes()
 assert b'6 failed, 23 passed' in baseline
 launch=load(C/'evidence/launch-result.json');assert launch['exit_code']==0 # carrier completion, not worker success
 return dict(task_digest=digest,model_calls=5,edit_proposals=0,worker_accepted=False,worker_disposition='failed',failure_phase='preparation',next_request_bytes=size,prompt_byte_limit=32768,next_inference_entered=False,next_token_count=None,input_tokens=d['total_input'],output_tokens=d['total_output'],total_tokens=d['total_input']+d['total_output'],worker_seconds=o['seconds'],outer_seconds=launch['seconds'],source_reads=d['reads'],acquisition_trace=trace,archived_source_unchanged=True,production_change_delivered=False,review_verdict=d['review'])

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--baseline-tests',action='store_true');args=parser.parse_args()
 if args.baseline_tests:
  # Original frozen oracle imports its original test module name. Resolve that
  # name to the exact relocated input only within this read-only verifier process.
  name='tests.agents.coding.test_inventory'
  spec=importlib.util.spec_from_file_location(name,C/'characterization/test_inventory.py');module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
  import pytest
  code=pytest.main(['--no-cov','-q',str(C/'characterization/test_inventory.py'),str(C/'oracle.py'),'tests/agents/coding/test_repository.py'])
  raise SystemExit(code) # Expected baseline remains six failures / twenty-three passes.
 print(json.dumps(verify(),indent=2))
