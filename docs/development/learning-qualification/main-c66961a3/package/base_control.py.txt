import asyncio
import importlib.util
import json
import pathlib
import runpy
import sys
import tempfile

for name in ('numpy','scipy','sklearn','threadpoolctl'):
    assert importlib.util.find_spec(name) is None,name
import devtools.agents.coding
import devtools.agents.learning.process
from devtools.tools.learning import ManagedLearningWorker
from devtools.learning.investigation.errors import LearningUnavailableError
try:ManagedLearningWorker.current()
except LearningUnavailableError as e:assert e.observation.kind.value=='unavailable'
else:raise AssertionError('base environment unexpectedly fitted')
fixture=runpy.run_path(sys.argv[1])
root=pathlib.Path(tempfile.mkdtemp(prefix='devtools-learning-base-wheel-'))
result=asyncio.run(fixture['scenario'](root,'success'))
assert result['accepted'] and result['completed'] and result['restored']
assert result['model_calls']==2 and result['checks'][-1][0]['exit']==0
assert result['archive']['module.py']==fixture['GOOD']
assert result['source']==fixture['SOURCE']
assert not any(n.split('.')[0] in ('numpy','scipy','sklearn','threadpoolctl') for n in sys.modules)
report={'status':'PASS','optional_numerical_distributions':'ABSENT','source_root':str(root),'coding':result}
pathlib.Path(sys.argv[2]).write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'base_wheel':'PASS','coding_accepted':result['accepted'],'root':str(root)}))
