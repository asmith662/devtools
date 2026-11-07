import importlib.abc
import importlib.util
import json
import pathlib
import runpy
import site
import sys

root=pathlib.Path(sys.argv[1]).resolve()
selected_site=pathlib.Path(sys.argv[2]).resolve()
target=pathlib.Path(sys.argv[3]).resolve()
rest=sys.argv[4:]
denied_roots=tuple(root/p for p in ('src','tests','scripts','apps','experiments'))+(root.parent/'learned-intelligence',root.parent/'devtools',root/'.local/learning-migration/v2',root/'docs/development/learning-qualification')
violations=[]
def guard(event,args):
    if event=='open' and isinstance(args[0],(str,bytes)):
        p=pathlib.Path(args[0].decode() if isinstance(args[0],bytes) else args[0]).resolve()
        if '.tmp' in tuple(v.lower() for v in p.parts) or any(p.is_relative_to(r) for r in denied_roots):
            violations.append(str(p));raise PermissionError('donor/development/canonical/archive read denied')
class NoDonor(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0]=='learned_intelligence':raise ImportError('donor package denied')
sys.addaudithook(guard)
sys.meta_path.insert(0,NoDonor())
for r in denied_roots:
    try:(r/'denied-probe.py').read_bytes()
    except PermissionError:pass
    else:raise AssertionError(('inactive guard',r))
try:__import__('learned_intelligence')
except ImportError:pass
else:raise AssertionError('inactive import guard')
probes=len(violations)
site.addsitedir(str(selected_site))
sys.argv=[str(target),*rest]
runpy.run_path(str(target),run_name='__main__')
origins={}
for name,module in tuple(sys.modules.items()):
    if name=='devtools' or name.startswith('devtools.'):
        path=getattr(module,'__file__',None)
        if path:
            assert pathlib.Path(path).resolve().is_relative_to(selected_site),(name,path)
            origins[name]=path
assert len(violations)==probes,violations
print(json.dumps({'package_guard':'PASS','denied_roots':list(map(str,denied_roots)),'active_probe_count':probes,'actual_denied_accesses':0,'devtools_modules':len(origins),'devtools_origin':origins['devtools']}))
