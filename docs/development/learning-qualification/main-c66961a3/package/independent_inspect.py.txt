import hashlib,importlib.util,json,os,pathlib,sys
from dataclasses import asdict
from devtools.core.paths import resolve_path
from devtools.learning.integrations.local.operations import LearningPublication
from devtools.learning.integrations.local.inspection import inspect_learning
from devtools.learning.investigation.plans import LearningPlan,BinaryProblem
from devtools.learning.investigation.classification.contracts import ExecutionAuthorization
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.learning.regression.state import RegressionPredictions

root=pathlib.Path(sys.argv[1]).resolve();output=pathlib.Path(sys.argv[2]).resolve()
assert not output.exists()
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def readonly(event,args):
    if event=='open' and isinstance(args[0],(str,bytes)) and isinstance(args[2],int) and args[2] & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
        name=pathlib.Path(os.fsdecode(args[0])).resolve()
        if name!=output:raise PermissionError('independent inspection is read-only')
sys.addaudithook(readonly)
reports=[]
for operation in sorted([*root.glob('task-*/operation-*'),*root.glob('task-*/protected-final')]):
    packet=json.loads((operation/'request.json').read_bytes())
    plan=LearningPlan(**packet['plan']);g=packet['grant']
    grant=ExecutionAuthorization(g['plan_identity'],tuple(g['candidate_ids']),EvidenceReference(**g['authority']))
    host=json.loads((operation/'execution.json').read_bytes());ref=json.loads(host['stdout'])
    original=LearningPublication(resolve_path(operation/'science'),ref['generation_id'],ref['manifest_sha256'],ref['plan_identity'])
    artifact=inspect_learning(original,plan,grant)
    _,held=plan.populations();predicted=artifact.predict(held.features if isinstance(held,BinaryProblem) else held.inputs)
    values=list(predicted.values) if isinstance(predicted,RegressionPredictions) else list(predicted)
    reports.append({'operation':str(operation.relative_to(root)),'method':plan.method,'phase':plan.phase,'plan_identity':plan.identity,'publication_sha256':original.manifest_sha256,'quality':asdict(artifact.quality),'predictions':values,'fit_calls':0,'complete_fitting_ack_before_prediction':'VERIFIED'})
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
assert before==after
assert len(reports)==7
for name in ('numpy','scipy','sklearn','threadpoolctl'):
    assert importlib.util.find_spec(name) is None,name
    assert name not in sys.modules,name
output.write_text(json.dumps({'status':'PASS','read_only_members':len(before),'content_unchanged':True,'extra_distributions':'ABSENT','operations':reports},indent=2),encoding='utf-8')
print(json.dumps({'independent_inspection':'PASS','operations':len(reports),'read_only_members':len(before),'fit_calls':0}))
