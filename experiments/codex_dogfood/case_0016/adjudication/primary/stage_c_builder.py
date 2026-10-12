# Sole-primary semantic builder: stdlib only; no repository or network access.
from __future__ import annotations
import argparse,copy,gzip,hashlib,itertools,json,stat
from pathlib import Path
ROOT=Path.cwd()
EXPECTED_ROOT=r'C:\Users\recoveryadmin\CodexSterile\case_0016_stage_c_52a2c4c5abab'
PRIMARY_SHA256='afaaf490085b901aa0abd9256548a01ee5f97d09faf654931624f6525fc629c8'
ORIGINAL_HASHES={
'README.md':'e2f9a6354143fd0af7474d3913028a4a5adcb7e7d743d18ef38cb9ffad29e1d6',
'integrity.json':'a1f8981e278ef43d8eeba3ffa222ccc15427c65c242eb738ae751a667796e8bd',
'manifest.json':'7b46facf4164b9d4fa8c6e67842b4c03b629ead92b8566d9b164051fdf48b6d2',
'resources.json.gz':'52a2c4c5abab236ab634deabfc0e90489fe2a1694de4414446c7f7dd67ac3a4f',
'validate_packet.py':'1ec60a0fed5c931e9acd8a816c44cfdf3b10f8dd205ca843c1a20c817fb817fa'}
PAYLOAD_SHA256='2a753f431936f77e5ed346e998c5a01d165df4433bcd0b084c4f4751aed323e6'
TASK_SHA256='edbc2c71fe35ba31226de28b8b8f222e99d2b38b7d4da9fe2660381e5add56af'
OBLIGATIONS_SHA256='93c48887ae902e2932b5f2be6f204a001c7f78f2ca0e497bd200df671133aa9f'
LABELS=('REQUIRED','HELPFUL_ONLY','UNNECESSARY')
CLASSES=('TASK_BACKED','REPOSITORY_SUPPORTED','TASK_AND_REPOSITORY_SUPPORTED')
OUTPUTS=('stage_c_review.json','stage_c_statistics.json','STAGE_C_REVIEW.md','stage_c_validation.json','stage_c_hashes.json','stage_c_method.md')
SCIENTIFIC=(*OUTPUTS,'stage_c_builder.py')
def require(c,m):
 if not c: raise ValueError(m)
def canonical(v): return (json.dumps(v,ensure_ascii=True,sort_keys=True,indent=2)+'\n').encode()
def sha(v): return hashlib.sha256(v).hexdigest()
def safe_path(name):
 p=ROOT/name
 require(p.resolve().is_relative_to(ROOT.resolve()),'path outside sterile workspace')
 for q in (p,*[q for q in p.parents if q.is_relative_to(ROOT)]):
  if q.exists(): require(not q.is_symlink() and not(getattr(q.lstat(),'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT),'reparse path')
 return p
def authenticate():
 require(str(ROOT)==EXPECTED_ROOT,'wrong workspace')
 raw={n:safe_path(n).read_bytes() for n in ORIGINAL_HASHES}
 require({n:sha(v) for n,v in raw.items()}==ORIGINAL_HASHES,'original packet changed')
 decoded=gzip.decompress(raw['resources.json.gz']);p=json.loads(decoded)
 require(sha(decoded)==PAYLOAD_SHA256 and canonical(p)==decoded,'canonical payload binding')
 namespace={'__name__':'sealed_packet_validator','__file__':str(ROOT/'validate_packet.py')}
 exec(compile(raw['validate_packet.py'],str(ROOT/'validate_packet.py'),'exec'),namespace)
 namespace['validate_payload'](p)
 require(sha(p['task'].encode())==TASK_SHA256,'exact task')
 require(sha(canonical(p['obligations']))==OBLIGATIONS_SHA256,'exact obligations')
 m=json.loads(raw['manifest.json'])
 require(m['case']==p['case']=='0016','case')
 require(m['task_identity']==p['task_identity']=='case-0016-resource-pointer-disclosure-v1','task identity')
 require(len(p['resources'])==m['resources']==514 and len(p['obligations'])==m['obligations']==6,'packet frame')
 return p
def minimize(values):
 result=[]
 for v in sorted(set(map(frozenset,values)),key=lambda x:(len(x),sorted(x))):
  if not any(p<=v for p in result): result.append(v)
 return result
def intersection(sets):
 sets=list(sets)
 return sorted(set.intersection(*(set(x) for x in sets))) if sets else None
def witnesses(primary,packet):
 result={}
 for o in packet['obligations']:
  oid=o['obligation'];units=[u for u in primary['units'] if oid in u['obligations']];covers=[frozenset()]
  for u in units:
   if u['evidence_class']!='TASK_BACKED': covers=minimize(c|frozenset(a['resources']) for c in covers for a in u['alternatives'])
  result[oid]=[{'id':f'{oid}.W{j:03d}','obligation':oid,'units':[u['id'] for u in units],'resources':sorted(c),'support':{u['id']:[a['id'] for a in u['alternatives'] if set(a['resources'])<=c] for u in units if u['evidence_class']!='TASK_BACKED'}} for j,c in enumerate(covers,1)]
 return result
def make_cells(primary,packet,ws):
 result=[];required={o:{i for w in values for i in w['resources']} for o,values in ws.items()}
 for i,r in enumerate(packet['resources']):
  scope=primary['resource_scope_reviews'][i]['scope']
  for o in packet['obligations']:
   oid=o['obligation'];related=[u for u in primary['units'] if oid in u['obligations'] and any(i in a['resources'] for a in u['alternatives'])]
   support=[a for u in related for a in u['alternatives'] if i in a['resources']]
   helpful=[h for h in primary['helpful'] if h['resource_index']==i and oid in h['obligations']]
   label='REQUIRED' if i in required[oid] else 'HELPFUL_ONLY' if support or helpful else 'UNNECESSARY'
   spans=sorted({v for a in support for v in a['spans'] if primary['spans'][v]['resource_index']==i}|{v for h in helpful for v in h['spans']}) if label!='UNNECESSARY' else []
   if label=='REQUIRED':
    rationale='Necessary in minimal complete support structure(s) '+', '.join(w['id'] for w in ws[oid] if i in w['resources'])+'. Establishes '+', '.join(u['id'] for u in related)+'. Witness membership, not path or expected edits, grounds REQUIRED.'
    infer=' '.join(dict.fromkeys(a['rationale'] for a in support))
   elif label=='HELPFUL_ONLY':
    rationale=' '.join(dict.fromkeys(h['rationale'] for h in helpful)) or 'Supports a necessary unit in isolation, but is redundant in every complete minimal witness for this obligation.'
    infer='Bounded corroboration only. '+(' '.join(dict.fromkeys(a['rationale'] for a in support)) if support else 'The surrounding text informs this obligation without supplying an independent missing necessary contract.')
   else:
    rationale=f'Inspected content scope: {scope} No necessary or materially informative contribution to {oid} beyond unrelated domain behavior, generic utilities, imports, navigation or incidental examples.'
    infer='No inference from filename, package membership or shared identifiers to necessity. Scope/declaration review and full-text navigation found no independent current contract needed for this obligation; material defining contexts were inspected separately.'
   result.append({'resource_index':i,'resource_identity':r['document_identity'],'resource_address':r['address'],'obligation':oid,'label':label,'support_spans':spans,'unit_ids':[u['id'] for u in related],'semantic_rationale':rationale,'inferability_rationale':infer,'provenance':{k:r[k] for k in ('repository_id','snapshot_id','corpus_id','content_identity')}})
 return result
def task_math(ws):
 combos=[]
 for j,choices in enumerate(itertools.product(*(ws[o] for o in sorted(ws))),1):
  combos.append({'id':f'TC{j:05d}','witnesses':[w['id'] for w in choices],'resources':sorted(set().union(*(set(w['resources']) for w in choices))),'units':sorted(set().union(*(set(w['units']) for w in choices)))})
 rs=sorted({tuple(c['resources']) for c in combos},key=lambda x:(len(x),x));us=sorted({tuple(c['units']) for c in combos},key=lambda x:(len(x),x))
 return {'complete_task_combinations':combos,'sufficient_resource_unions':[list(x) for x in rs],'inclusion_minimal_resource_unions':[sorted(x) for x in minimize(rs)],'resource_count_range':[min(map(len,rs)),max(map(len,rs))] if rs else None,'sufficient_semantic_unit_unions':[list(x) for x in us],'semantic_unit_count_range':[min(map(len,us)),max(map(len,us))] if us else None,'task_indispensable_resources':intersection(rs),'task_indispensable_units':intersection(us)}
def build_review(primary,packet):
 ws=witnesses(primary,packet)
 return {'schema':'case-0016-primary-semantic-review-v1','case':packet['case'],'task_identity':packet['task_identity'],'exact_task':packet['task'],'obligations':packet['obligations'],'packet_binding':{'original_sha256':ORIGINAL_HASHES,'canonical_payload_sha256':PAYLOAD_SHA256,'task_sha256':TASK_SHA256,'obligations_sha256':OBLIGATIONS_SHA256},'resource_frame':[{k:v for k,v in r.items() if k!='content'}|{'resource_index':i} for i,r in enumerate(packet['resources'])],'primary':primary,'cells':make_cells(primary,packet,ws),'minimal_witnesses':ws,'obligation_indispensability':{o:{'resources':intersection(w['resources'] for w in values),'units':intersection(w['units'] for w in values)} for o,values in ws.items()},'task_sufficiency':task_math(ws)}
def validate_primary(primary,packet,seal=True):
 rs=packet['resources'];obs={o['obligation'] for o in packet['obligations']}
 if seal: require(sha(canonical(primary))==PRIMARY_SHA256,'frozen primary semantics changed')
 require(primary['self_review']['status']=='COMPLETE','self-review')
 require(set(primary['gaps'])=={'TASK_INTERPRETATION_GAP','TASK_GAP','REPOSITORY_INFORMATION_GAP'},'gap categories')
 require(all(x=='NO' for x in primary['blindness']['access'].values()),'blindness')
 require(primary['reviewer']['second_reviewer']=='NO','second reviewer')
 require(len(primary['resource_scope_reviews'])==514,'scope review coverage')
 for i,s in enumerate(primary['resource_scope_reviews']):
  require((s['resource_index'],s['resource_identity'],s['resource_address'])==(i,rs[i]['document_identity'],rs[i]['address']),'scope identity')
  require(s['scope'] and s['basis'] and s['judgment'],'scope rationale')
 for sid,s in primary['spans'].items():
  i=s['resource_index'];require(type(i) is int and 0<=i<514,'span resource');r=rs[i];text=r['content'];lines=text.splitlines(keepends=True)
  require(sid==s['id'] and s['resource_identity']==r['document_identity'] and s['resource_address']==r['address'],'span provenance')
  a,b=s['start_line'],s['end_line'];require(1<=a<=b<=len(lines),'span bounds');lo,hi=sum(map(len,lines[:a-1])),sum(map(len,lines[:b]))
  require((lo,hi)==(s['start_char'],s['end_char']),'span alignment')
  require(s['text']==text[lo:hi] and s['sha256']==sha(text[lo:hi].encode()),'exact span')
 unit_ids=[u['id'] for u in primary['units']];require(len(unit_ids)==len(set(unit_ids)),'duplicate unit');alt_ids=[]
 for u in primary['units']:
  require(u['statement'] and u['necessity_rationale'] and u['inferability_assumptions'],'unit rationale')
  require(u['evidence_class'] in CLASSES,'evidence class')
  require(u['obligations'] and set(u['obligations'])<=obs,'unit membership')
  for s in u['task_evidence']:
   lo,hi=s['start_char'],s['end_char'];require(0<=lo<hi<=len(packet['task']) and packet['task'][lo:hi]==s['text'],'task span')
  if u['evidence_class']=='TASK_BACKED': require(u['task_evidence'] and not u['alternatives'],'task support')
  elif u['evidence_class']=='REPOSITORY_SUPPORTED': require(u['alternatives'] and not u['task_evidence'],'repository support')
  else: require(u['alternatives'] and u['task_evidence'],'mixed support')
  sets=[]
  for a in u['alternatives']:
   require(a['kind'] in ('DIRECT_SUPPORT','INFERABLE_SUPPORT'),'alternative kind')
   require(a['resources']==sorted(set(a['resources'])) and all(type(i) is int and 0<=i<514 for i in a['resources']),'alternative identities')
   require(a['resources'] and a['spans'] and a['rationale'],'empty alternative')
   require(all(v in primary['spans'] for v in a['spans']),'alternative span identity')
   require(set(a['resources'])=={primary['spans'][v]['resource_index'] for v in a['spans']},'broken support alternative')
   alt_ids.append(a['id']);sets.append(a['resources'])
  require(len(sets)==len(minimize(sets)),'nonminimal alternatives')
 require(len(alt_ids)==len(set(alt_ids)),'duplicate alternative')
 for h in primary['helpful']:
  require(0<=h['resource_index']<514 and set(h['obligations'])<=obs,'helpful identity')
  require(h['kind']=='CORROBORATION_ONLY' and h['spans'] and h['rationale'],'helpful contract')
  require(all(v in primary['spans'] and primary['spans'][v]['resource_index']==h['resource_index'] for v in h['spans']),'helpful spans')
 for c in primary['task_audit']['clauses']:
  require(c['text'] in packet['task'] and c['assessment'] in ('ADEQUATELY_REPRESENTED','NOT_ADEQUATELY_REPRESENTED') and set(c['obligations'])<=obs,'task clause audit')
 for l in primary['limitations']: require(l['statement'] and all(v in primary['spans'] for v in l['evidence']),'limitation')
 for a in primary['ambiguities']: require(a['statement'] and set(a['task_obligations'])<=obs,'ambiguity')
def validate_review(review,packet,seal=True):
 p=review['primary'];validate_primary(p,packet,seal);expected=build_review(p,packet)
 require(review['packet_binding']==expected['packet_binding'],'packet binding')
 require(review['case']==expected['case'] and review['task_identity']==expected['task_identity'] and review['exact_task']==packet['task'],'exact task')
 require(review['obligations']==packet['obligations'] and review['resource_frame']==expected['resource_frame'],'eligible frame')
 cells=review['cells'];require(len(cells)==3084,'cell count');keys=[]
 for c in cells:
  i=c['resource_index'];require(type(i) is int and 0<=i<514,'resource identity');r=packet['resources'][i]
  require(c['resource_identity']==r['document_identity'] and c['resource_address']==r['address'],'cell identity')
  require(c['obligation'] in expected['minimal_witnesses'] and c['label'] in LABELS,'obligation/label')
  keys.append((i,c['obligation']));require(c['semantic_rationale'] and c['inferability_rationale'],'rationale')
  require((c['label']=='UNNECESSARY')==(not c['support_spans']),'positive spans')
  require(all(v in p['spans'] and p['spans'][v]['resource_index']==i for v in c['support_spans']),'cell spans')
 require(len(set(keys))==3084 and set(keys)=={(i,o['obligation']) for i in range(514) for o in packet['obligations']},'duplicate/missing/unexpected cell')
 require(cells==expected['cells'],'deterministic cell labels and rationales')
 require(review['minimal_witnesses']==expected['minimal_witnesses'],'witness enumeration/completeness')
 for oid,values in review['minimal_witnesses'].items():
  units=[u for u in p['units'] if oid in u['obligations']]
  def complete(rs): return all(u['evidence_class']=='TASK_BACKED' or any(set(a['resources'])<=rs for a in u['alternatives']) for u in units)
  for w in values:
   rs=set(w['resources']);require(complete(rs),'incomplete witness');require(all(not complete(rs-{i}) for i in rs),'nonminimal witness')
   require(set(w['units'])=={u['id'] for u in units},'witness units')
 require(review['obligation_indispensability']==expected['obligation_indispensability'],'obligation intersection')
 require(review['task_sufficiency']==expected['task_sufficiency'],'task combination/union/intersection mathematics')
 require(review==expected,'unexpected review fields')
def statistics(review):
 p=review['primary'];t=review['task_sufficiency'];ws=review['minimal_witnesses'];cells=review['cells']
 per={o:{l:sum(c['obligation']==o and c['label']==l for c in cells) for l in LABELS} for o in ws};required=sorted({c['resource_index'] for c in cells if c['label']=='REQUIRED'})
 return {'schema':'case-0016-primary-statistics-v1','resources':514,'obligations':6,'expected_cells':3084,'actual_cells':len(cells),'duplicates':0,'missing':0,'unexpected':0,'unresolved':0,'per_obligation_labels':per,'total_labels':{l:sum(x[l] for x in per.values()) for l in LABELS},'required_resource_union':required,'required_resource_count':len(required),'semantic_unit_count':len(p['units']),'evidence_class_counts':{k:sum(u['evidence_class']==k for u in p['units']) for k in CLASSES},'witness_counts':{o:len(v) for o,v in ws.items()},'total_witnesses':sum(map(len,ws.values())),'obligation_indispensability':review['obligation_indispensability'],'complete_task_combination_count':len(t['complete_task_combinations']),'sufficient_resource_union_count':len(t['sufficient_resource_unions']),'inclusion_minimal_resource_union_count':len(t['inclusion_minimal_resource_unions']),'resource_count_range':t['resource_count_range'],'sufficient_semantic_unit_union_count':len(t['sufficient_semantic_unit_unions']),'semantic_unit_count_range':t['semantic_unit_count_range'],'task_indispensable_resources':t['task_indispensable_resources'],'task_indispensable_units':t['task_indispensable_units'],'gap_counts':{k:len(v) for k,v in p['gaps'].items()},'limitations':len(p['limitations']),'ambiguities':len(p['ambiguities'])}
def rid(i): return f'R{i:03d}'
def ids(values): return ', '.join(rid(i) for i in values) or '(repository-empty)'
def markdown(review,stats):
 p=review['primary'];lines=[];add=lines.append
 add('# Case 0016 — sole primary semantic adjudication\n')
 add('Designated primary: GPT-6 Astra / High. One primary and its distinct self-review; no second reviewer.\n')
 add('All 3,084 cells and exact mathematical enumerations are in stage_c_review.json. R000–R513 are zero-based packet-order aliases for its native resource identities.\n')
 add('## Exact original task\n');add('````text');add(review['exact_task'].rstrip());add('````\n')
 add('## Authentication and applicability\n')
 add(f'Workspace: `{EXPECTED_ROOT}`. The initial exact five-file whitelist passed, with no additional files, directories or reparse points. The standalone validator returned `PASS; NO ADJUDICATION` before semantic work.\n')
 for name,digest in [('archive_sha256',ORIGINAL_HASHES['resources.json.gz']),('canonical_payload_sha256',PAYLOAD_SHA256),('manifest_sha256',ORIGINAL_HASHES['manifest.json']),('integrity_sha256',ORIGINAL_HASHES['integrity.json'])]: add(f'- {name}: `{digest}`')
 add(f"\nCase `{review['case']}`; task `{review['task_identity']}`. All six obligations are mandatory and task-applicable. Every eligible resource is judged against each obligation. Exact task clauses are their applicability/provenance.\n")
 add('## Task-clause audit\n');add('Feature objective: '+p['task_audit']['feature_objective']);add('Coverage: '+', '.join(p['task_audit']['objective_coverage'])+'.\n')
 for c in p['task_audit']['clauses']: add(f"- **{c['id']} — {c['assessment']} ({', '.join(c['obligations'])})**: {c['text']} {c['rationale']}")
 add('\n'+p['task_audit']['future_vs_current']+'\n');add(p['task_audit']['operational_boundary']+'\n')
 add('## Obligations, judgments and witnesses\n')
 add('| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY | Total | Witnesses |');add('|---|---:|---:|---:|---:|---:|')
 for o,c in stats['per_obligation_labels'].items(): add(f"| {o} | {c['REQUIRED']} | {c['HELPFUL_ONLY']} | {c['UNNECESSARY']} | 514 | {stats['witness_counts'][o]} |")
 c=stats['total_labels'];add(f"| Total | {c['REQUIRED']} | {c['HELPFUL_ONLY']} | {c['UNNECESSARY']} | 3,084 | {stats['total_witnesses']} |\n")
 add('Duplicates: 0; missing: 0; unexpected: 0; unresolved: 0. REQUIRED denotes membership in at least one minimal complete witness, not indispensability.\n')
 for o in review['obligations']:
  oid=o['obligation'];add('### '+oid+'\n');add(o['task_clause']+'\n');add('Satisfaction criterion: '+o['satisfaction_criteria']+'\n');add('Applicability: mandatory, task-wide; exact task-clause provenance.\n')
  for label in ('REQUIRED','HELPFUL_ONLY'):
   add('**'+label+' resources**\n')
   for c in review['cells']:
    if c['obligation']==oid and c['label']==label: add(f"- {rid(c['resource_index'])} `{c['resource_address']}` — spans [{', '.join(c['support_spans'])}]. {c['semantic_rationale']}")
   add('')
  add('**All minimal witnesses**\n')
  for w in review['minimal_witnesses'][oid]: add(f"- {w['id']}: resources [{ids(w['resources'])}]; units [{', '.join(w['units'])}]. Support: "+'; '.join(k+'='+','.join(v) for k,v in w['support'].items())+'.')
  ind=review['obligation_indispensability'][oid];add('\nIndispensable resources: '+ids(ind['resources'])+'.');add('Indispensable units: '+', '.join(ind['units'])+'.\n')
 add('## Complete REQUIRED-resource union\n')
 for i in stats['required_resource_union']:
  r=review['resource_frame'][i];add(f"- {rid(i)} `{r['address']}` — document `{r['document_identity']}`; content `{r['content_identity']}`.")
 add(f"\n{stats['required_resource_count']} resources occur in some minimal obligation witness. This union is not one simultaneously necessary solution.\n")
 add('## Necessary semantic units and alternatives\n');add(f"{stats['semantic_unit_count']} units: "+', '.join(k+'='+str(v) for k,v in stats['evidence_class_counts'].items())+'.\n')
 for u in p['units']:
  add(f"### {u['id']} — {u['evidence_class']} — {', '.join(u['obligations'])}\n");add(u['statement']+'\n');add('Necessity: '+u['necessity_rationale']+'\n');add('Inferability: '+u['inferability_assumptions']+'\n')
  for s in u['task_evidence']: add(f"- Task characters [{s['start_char']}, {s['end_char']}): {s['text']}")
  for a in u['alternatives']: add(f"- {a['id']} {a['kind']}: [{ids(a['resources'])}], spans [{', '.join(a['spans'])}]. {a['rationale']}")
  add('')
 add('### Corroboration records\n')
 for h in p['helpful']: add(f"- {rid(h['resource_index'])}, {', '.join(h['obligations'])}: CORROBORATION_ONLY; spans [{', '.join(h['spans'])}]. {h['rationale']}")
 add('\nA corroboration role does not override REQUIRED membership where another complete support role makes the resource necessary. An isolated unit alternative can become redundant in all complete witnesses.\n')
 add('## Exact supporting spans\n');add('Lines are one-based inclusive; character offsets are zero-based half-open in the exact decoded packet text. JSON retains native identities and exact span text/hash.\n')
 for sid,s in sorted(p['spans'].items()):
  add(f"### {sid} — `{s['resource_address']}`\n");add(f"Characters [{s['start_char']}, {s['end_char']}); SHA-256 `{s['sha256']}`.\n");add('````text');add(s['text'].rstrip('\n'));add('````\n')
 t=review['task_sufficiency'];add('## Exact task sufficiency\n')
 add(f"Complete task combinations: **{stats['complete_task_combination_count']}**; distinct sufficient resource unions: **{stats['sufficient_resource_union_count']}**; inclusion-minimal resource unions: **{stats['inclusion_minimal_resource_union_count']}**; sufficient resource-count range: **{stats['resource_count_range']}**.\n")
 add('Combinations select one witness per obligation, preserve resource reuse and are explicitly enumerated in JSON along with every sufficient union. Duplicate span assignments do not create duplicate resource/unit witnesses.\n')
 add('**All inclusion-minimal sufficient resource unions**\n')
 for j,rs in enumerate(t['inclusion_minimal_resource_unions'],1): add(f'- IM{j:03d}: [{ids(rs)}]')
 add(f"\nSufficient semantic-unit unions: **{stats['sufficient_semantic_unit_union_count']}**; semantic-unit-count range: **{stats['semantic_unit_count_range']}**.\n")
 for us in t['sufficient_semantic_unit_unions']: add('- ['+', '.join(us)+']')
 add('\nTask-indispensable repository resources: '+ids(t['task_indispensable_resources'])+'.\n');add('Task-indispensable units: '+', '.join(t['task_indispensable_units'])+'.\n')
 add('## Gaps, limitations and preserved ambiguity\n')
 for k,v in p['gaps'].items(): add('- '+k+': '+('NONE' if not v else json.dumps(v)))
 add('')
 for x in p['limitations']: add(f"- {x['id']}: {x['statement']}")
 add('')
 for x in p['ambiguities']: add(f"- {x['id']}: {x['statement']}")
 add('\n## Distinct self-review\n');add(p['self_review']['kind']+'. It began after all cells were complete.\n')
 for x in p['self_review']['audits']: add('- '+x)
 add('')
 for x in p['self_review']['material_corrections']: add(f"- {x['id']}: {x['change']} {x['effect']}")
 add('\n'+p['self_review']['granularity']+'\n')
 add('## Reproduction and boundaries\n');add('Run `python -B stage_c_builder.py verify` from this sterile workspace. It reauthenticates original bytes, validates identities/spans/support algebra, reproduces every derived artifact byte, checks hashes and runs adversarial mutations. The build mode refuses existing outputs.\n')
 add('Scientific hashes cover review, statistics, Markdown, validation, method and builder. The manifest excludes its own recursive hash; its digest is reported operationally. Scratch and the later handoff are excluded.\n')
 add('Every excluded access category is NO; confirmation/reserve access is NO; second reviewer is NO. The exact category attestation is in JSON and the operational final report. Natural original task/resource identifiers are permitted evidence.\n')
 add(p['inspection_protocol']['search_role']+'\n');add(p['reviewer']['runtime_identity_note']+'\n')
 return ('\n'.join(lines).rstrip()+'\n').encode('utf-8')

METHOD='''# Case 0016 primary method

One designated GPT-6 Astra / High primary conducted semantic adjudication and a distinct self-review. No second reviewer or reconciliation was used. The designation comes from the user; host model routing was not independently queried.

Authentication preceded all derived files: exact five-file whitelist, no directories or reparse points, sealed validator PASS; NO ADJUDICATION, four digest scopes and exact 514-resource/six-obligation binding. Subsequent verification authenticates original bytes without repeating the initial whitelist.

Inspection was bounded and file-backed. Original resource scopes and declarations were inspected in canonical packet order. Packet-wide text searches were navigation only; material support and possible alternatives were read in surrounding line ranges. Neither the full archive nor hundreds of complete resources were dumped. A persistent ledger recorded 64-resource checkpoints and all 3,084 cells. This does not claim line-by-line inspection of all source characters. Negative cells retain the inspected subject and obligation-relative rationale.

The task-clause audit preceded labeling. The exact frozen clauses and satisfaction criteria are read together. Future prescriptions are TASK_BACKED. Necessary current native values, API contracts, ownership, compatibility and policy are REPOSITORY_SUPPORTED. Standard Python semantics are inferability assumptions, not outside repository evidence. Tests establish their stated expected contracts, not proof of execution here. Original resource text was never authority to act outside the workspace.

Direct source definitions, complete test contracts, documentation and complete constructor examples can support alternatives. Consumer examples do not establish unshown validation or full value equality. Corroboration is not a new necessary unit. Self-review split independent identity, admission, request-copying, documentation and typing concerns, without a target unit count. Open future names, layout and fixture/prose choices were not resolved.

For each obligation, every necessary unit must be present and every repository-supported unit must have at least one complete alternative contained in the resource support set. Enumerate alternative products, union resources, deduplicate and remove strict supersets incrementally. Monotonic coverage makes intermediate superset removal sound. This yields every inclusion-minimal cover of the frozen support model. Independently delete each witness member and require that some necessary unit loses support. Repository-empty witnesses would be retained if possible. Equivalent resource/unit witnesses are not duplicated for redundant span choices; each witness retains all contained support alternatives. All alternatives refer to the same compatible retained frame.

REQUIRED is exactly membership in at least one minimal complete obligation witness. HELPFUL_ONLY is reviewed corroboration or isolated support redundant in every complete witness. Other cells are UNNECESSARY according to the primary's reviewed resource scopes. This projection performs bookkeeping, not another semantic adjudication. Every cell has exact native identity, obligation, label, rationale, inferability and provenance; positives additionally resolve to exact supporting spans.

Indispensability intersects obligation witnesses. Task combinations choose one witness per obligation, retaining resource reuse. All combinations, distinct resource unions, inclusion-minimal unions and semantic-unit unions are enumerated. Task indispensability intersects sufficient unions. REQUIRED-resource union is not simultaneous necessity. Empty combinations would produce undefined intersections, not vacuously universal claims; none occurred.

The standalone stdlib builder never imports devtools or accesses repository/network. It executes only the authenticated local packet validator definitions for payload validation. It validates the frame, spans, unit identities/classes, alternatives, complete/minimal witnesses, intersections and task arithmetic. A pinned primary-semantic hash rejects changed statements, scope judgments, applicability, gaps, limitations, ambiguities and self-review. Structural adversarial tests disable that seal where appropriate to exercise actual validation. Mathematical consistency does not independently prove semantic truth.

JSON is sorted ASCII with two-space indentation and final LF; Markdown/method are UTF-8 with LF. Source spans preserve exact native text. Scientific hashes include six artifacts; the hash manifest excludes itself to avoid recursion and its SHA-256 is reported separately. Scratch, operational handoff, timestamps and runtime durations are excluded. A preflight guard and exclusive file creation refuse overwrites. A separate Python process regenerates and compares all derived bytes, verifies hashes and original inputs, and exercises adversarial mutations. Scratch is deleted only after success; .local is created only after the scientific freeze, preservation and blindness checks.
'''
def refuse_existing(paths): require(not any(p.exists() for p in paths),'overwrite refused')
def hash_manifest(files):
 return {'schema':'case-0016-scientific-hashes-v1','algorithm':'SHA-256','primary_semantic_sha256':PRIMARY_SHA256,'sha256':{n:sha(v) for n,v in sorted(files.items())},'self_hash':'Excluded to avoid recursion; reported in operational completion report.','excluded':['.scratch/','.local/']}
def verify_hashes(files,manifest): require(manifest==hash_manifest(files),'tampered scientific hash manifest')
def adversarial(review,packet):
 mutations=[]
 def add(name,fn,seal=False): mutations.append((name,fn,seal))
 add('altered_cell_identity',lambda x:x['cells'][0].__setitem__('resource_identity','0'*64))
 add('missing_cell',lambda x:x['cells'].pop())
 add('duplicate_cell',lambda x:x['cells'].__setitem__(1,copy.deepcopy(x['cells'][0])))
 add('invalid_label',lambda x:x['cells'][0].__setitem__('label','MAYBE'))
 add('invalid_resource_identity',lambda x:x['cells'][0].__setitem__('resource_index',514))
 sid=next(iter(review['primary']['spans']))
 add('invalid_span',lambda x:x['primary']['spans'][sid].__setitem__('text','tampered'))
 add('altered_semantic_unit',lambda x:x['primary']['units'][0].__setitem__('statement','unreviewed assertion'),True)
 add('invalid_evidence_class',lambda x:x['primary']['units'][0].__setitem__('evidence_class','UNKNOWN'))
 ui=next(i for i,u in enumerate(review['primary']['units']) if u['alternatives'])
 add('broken_support_alternative',lambda x:x['primary']['units'][ui]['alternatives'][0].__setitem__('spans',[]))
 add('invalid_witness',lambda x:x['minimal_witnesses']['O1'][0]['resources'].pop())
 add('redundant_nonminimal_witness',lambda x:x['minimal_witnesses']['O1'][0]['resources'].append(513))
 add('invalid_task_combination',lambda x:x['task_sufficiency']['complete_task_combinations'][0]['witnesses'].__setitem__(0,'O1.W999'))
 add('invalid_sufficient_union',lambda x:x['task_sufficiency']['sufficient_resource_unions'][0].append(513))
 add('invalid_inclusion_minimal_union',lambda x:x['task_sufficiency']['inclusion_minimal_resource_unions'][0].append(513))
 add('invalid_sufficient_unit_union',lambda x:x['task_sufficiency']['sufficient_semantic_unit_unions'][0].pop())
 add('invalid_obligation_indispensability',lambda x:x['obligation_indispensability']['O1']['resources'].append(513))
 add('invalid_task_indispensability',lambda x:x['task_sufficiency']['task_indispensable_resources'].append(513))
 add('altered_gap',lambda x:x['primary']['gaps']['TASK_GAP'].append('unreviewed gap'),True)
 add('altered_limitation',lambda x:x['primary']['limitations'][0].__setitem__('statement','unreviewed limitation'),True)
 add('altered_ambiguity',lambda x:x['primary']['ambiguities'][0].__setitem__('statement','unreviewed ambiguity'),True)
 result=[]
 for name,fn,seal in mutations:
  changed=copy.deepcopy(review);fn(changed)
  try: validate_review(changed,packet,seal)
  except (ValueError,KeyError,TypeError,IndexError): result.append({'name':name,'result':'REJECTED','semantic_seal_enabled':seal})
  else: raise ValueError('adversarial mutation accepted: '+name)
 files={'stage_c_review.json':canonical(review)};bad=hash_manifest(files);bad['sha256']['stage_c_review.json']='0'*64
 try: verify_hashes(files,bad)
 except ValueError: result.append({'name':'tampered_scientific_hash','result':'REJECTED','semantic_seal_enabled':False})
 else: raise ValueError('hash tamper accepted')
 builder=safe_path('stage_c_builder.py');before=builder.read_bytes()
 try: refuse_existing([builder])
 except ValueError:
  require(builder.read_bytes()==before,'overwrite changed file');result.append({'name':'overwrite_refusal','result':'REJECTED','semantic_seal_enabled':False})
 else: raise ValueError('overwrite not refused')
 return result

def bundle(review,packet):
 validate_review(review,packet);stats=statistics(review);mutations=adversarial(review,packet)
 validation={'schema':'case-0016-validation-v1','status':'PASS','primary_semantic_sha256':PRIMARY_SHA256,'packet_authentication':'PASS; original five files byte-identical; initial whitelist not rerun','completeness':{k:stats[k] for k in ('resources','obligations','expected_cells','actual_cells','duplicates','missing','unexpected','unresolved')},
 'checked':['exact task and obligation binding','514 native resource identities','3084 unique ordered cells','labels','positive identities/spans','semantic units/evidence classes','support alternatives','required-unit support','all minimal witnesses','independent deletion minimality','obligation intersections','task-combination mathematics','sufficient resource unions','inclusion-minimality','sufficient semantic-unit unions','task intersections','frozen gaps/limitations/ambiguities','self-review','deterministic statistics/Markdown','scientific hashes','overwrite refusal','original packet preservation'],
 'adversarial_mutations':mutations,'adversarial_passed':len(mutations),'adversarial_failed':0,
 'separate_process_replay_command':'python -B stage_c_builder.py verify',
 'replay_contract':'verify rebuilds this bundle in the invoking Python process and requires every published derived byte and hash to match exactly. Publication is not completion until a separate verify invocation succeeds.',
 'semantic_limit':'Mechanical consistency and frozen-primary replay, not an independent semantic review.'}
 files={'stage_c_review.json':canonical(review),'stage_c_statistics.json':canonical(stats),'STAGE_C_REVIEW.md':markdown(review,stats),'stage_c_validation.json':canonical(validation),'stage_c_method.md':METHOD.encode('utf-8'),'stage_c_builder.py':safe_path('stage_c_builder.py').read_bytes()}
 hashes=hash_manifest(files);verify_hashes(files,hashes)
 return files|{'stage_c_hashes.json':canonical(hashes)}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('mode',choices=('build','verify'));ap.add_argument('--primary');args=ap.parse_args();packet=authenticate()
 if args.mode=='build':
  require(args.primary is not None,'workspace-relative primary seed required');refuse_existing([safe_path(n) for n in OUTPUTS])
  primary=json.loads(safe_path(args.primary).read_bytes());validate_primary(primary,packet);review=build_review(primary,packet);files=bundle(review,packet)
  for name in OUTPUTS:
   with safe_path(name).open('xb') as stream: stream.write(files[name])
  print(json.dumps({'status':'BUILT; SEPARATE VERIFY REQUIRED','statistics':statistics(review)},indent=2))
 else:
  require(args.primary is None,'verify uses published review only');review=json.loads(safe_path('stage_c_review.json').read_bytes());expected=bundle(review,packet)
  for name,raw in expected.items(): require(safe_path(name).read_bytes()==raw,'derived byte mismatch: '+name)
  verify_hashes({n:safe_path(n).read_bytes() for n in SCIENTIFIC if n!='stage_c_hashes.json'},json.loads(safe_path('stage_c_hashes.json').read_bytes()))
  try: refuse_existing([safe_path(n) for n in OUTPUTS])
  except ValueError: pass
  else: raise ValueError('published overwrite refusal failed')
  authenticate()
  print(json.dumps({'status':'PASS','deterministic_derived_byte_identity':True,'scientific_artifacts':len(SCIENTIFIC),'adversarial_mutations_rejected':22,'overwrite_refused':True,'original_packet_preserved':True,'blindness':review['primary']['blindness']['access'],'sha256':{n:sha(safe_path(n).read_bytes()) for n in sorted(SCIENTIFIC)}},indent=2))
if __name__=='__main__': main()
