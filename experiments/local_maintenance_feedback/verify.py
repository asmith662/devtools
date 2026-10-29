"""Verify retained identities/native facts only; never run model or old effects."""
import hashlib,json
from pathlib import Path
from devtools.models.interaction import ModelToolCall,Prompt,PromptMessage

HERE=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    frozen=load(HERE/'freeze.json')
    for p,h in frozen['files'].items():assert hashlib.sha256((HERE/p).read_bytes()).hexdigest()==h,p
    assert load(HERE/'preflight.json')['status']=='passed'
    d=load(HERE/'evidence/result.json');assert not d['accepted'] and not d['applied'] and not d['procedures']
    assert d['result']['disposition']=='model_limit' and d['result']['progress']['model_calls']==8
    assert d['result']['custody']['restored'] and not d['result']['custody']['reconciliation_required']
    assert len(d['proposals'])==2 and all(not p['admitted'] for p in d['proposals'])
    for record in d['requests']:
        assert record['inference_entered'] and record['outcome']=='normalized-response'
        assert record['measured_input_tokens']<=28160
        messages=tuple(PromptMessage(**{**m,'tool_calls':tuple(ModelToolCall(**c) for c in m['tool_calls'])}) for m in record['request']['prompt']['messages'])
        Prompt('', 'messages',messages)
        assert not any('UNTRUSTED DERIVED' in m.content for m in messages)
    refusals=[m for m in d['messages'] if m['role']=='tool' and 'REFUSED' in m['content']]
    assert len(refusals)==2 and all(json.loads(m['content'])['reason']=='Structured edit exceeds the bounded source size' for m in refusals)
    assert refusals[0] in d['requests'][-1]['request']['prompt']['messages']
    for p,entry in load(HERE/'evidence/candidate.json').items():
        raw=entry['content_utf8'].encode();assert hashlib.sha256(raw).hexdigest()==entry['sha256']
        assert raw==bytes.fromhex(frozen['baseline_raw'][p])
    review=load(HERE/'independent-review.json');assert review['application_count']==review['worker_checks']==0
    assert len(review['focused']['failed'])==3 and len(review['heldout']['failed'])==5
    assert all(row['proposed_bytes']>32768 for row in review['proposal_sizes'])
    measures=load(HERE/'measurements.json')
    assert measures['auxiliary_calls']==0 and measures['admitted_proposals']==0
    assert measures['input_tokens']==46979 and measures['output_tokens']==1326
    for index,span in [(6,[10841,10970]),(7,[11896,11977])]:
        assert any(s['path']=='src/devtools/agents/coding/repository.py' and s['span'][0]<=span[0] and span[1]<=s['span'][1] for s in measures['projections'][index]['active_sources'])
    print('Frozen inputs, eight actual requests, native correlation, two size refusals, consumed first refusal, unchanged archive, restoration and independent rejection verified; no inference or effect replay.')
if __name__=='__main__':main()
