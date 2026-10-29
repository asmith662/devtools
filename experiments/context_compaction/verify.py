"""Effect-free frozen evidence verification; never invokes either model."""
import hashlib
import json
from pathlib import Path

from devtools.agents.coding.compaction.format import validate_summary
from devtools.models.interaction import ModelToolCall, Prompt, PromptMessage

HERE=Path(__file__).resolve().parent


def main():
    freeze=json.loads((HERE/'freeze.json').read_text())
    for name,expected in freeze['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==expected,name
    original=json.loads((HERE/'history.json').read_text())['request']
    assert len(json.dumps(original,ensure_ascii=False).encode())==40010
    initial=[]
    for treatment in 'ABC':
        root=HERE/'evidence'/treatment
        result=json.loads((root/'result.json').read_text())
        assert result['history_prefix_unchanged']
        assert result['result']['custody']['restored']
        assert result['result']['progress']['model_calls']<=6
        assert result['result']['progress']['proposals']<=2
        assert result['seconds']<1200
        assert len(result['attempts'])<=2
        for request in result['requests']:
            messages=tuple(PromptMessage(**{**m,'tool_calls':tuple(ModelToolCall(**c) for c in m['tool_calls'])}) for m in request['prompt']['messages'])
            Prompt('', 'messages',messages)
            assert len(json.dumps(request,ensure_ascii=False).encode())<=32768
        initial.append(result['requests'][0])
        first=result['projections'][0]
        assert first['resulting_bytes']==4306
        assert not set(range(1,5)).intersection(first['selected_indices'])
        assert len(first['active_sources'])==2
        if treatment in 'BC':
            attempt=result['attempts'][0]
            assert attempt['entered'] and attempt['response_received']
            assert not attempt['validated'] and not attempt['adopted']
            assert attempt['error']['type']=='JSONDecodeError'
            response=json.loads((root/'summary-1.json').read_text())['response']['content']
            assert response.startswith('```json\n') and response.endswith('\n```')
            # Offline inspection only: never feed a corrected summary to an actor.
            selected=json.loads(attempt['request']['prompt']['messages'][1]['content'])
            refs={int(i):record['digest'] for i,record in selected['records'].items()}
            validate_summary(response[8:-4],refs,frozenset(selected['replacement_indices']),selected['historical_sources'])
        grade=json.loads((root/'grade-utf8.json').read_text())
        assert grade['exit_code']==(0 if treatment=='B' else 1)
    assert initial[0]==initial[1]==initial[2]
    print('Frozen inputs; 3 equivalent initial Prompts; native boundaries; 2 rejected raw summaries; offline inner provenance; exact source/custody; independent grades verified.')


if __name__=='__main__': main()
