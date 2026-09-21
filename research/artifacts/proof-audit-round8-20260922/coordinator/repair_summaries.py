from pathlib import Path
import json,sys,hashlib,re,copy,shutil
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922');A=R/'research/artifacts/proof-audit-round8-20260922';D=A/'summary-recovery'
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_library as L
import research_review as V
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def rows(d):return {x['location']:x for x in d['items']+d['blocked_items']}
targets={x['target']['location']:x['target'] for x in json.loads((O/'renewals.json').read_text())}
index=R/'index/tools.json'
if sys.argv[1]=='prepare':
 D.mkdir(exist_ok=True)
 before=D/'index-before.json'
 if before.exists():raise RuntimeError('Recovery evidence already exists; reconcile instead of overwrite')
 shutil.copyfile(index,before);shutil.copyfile(O/'finish_library.py',O/'finish_library_before_summary_repair.py')
 before_data=json.loads(before.read_text());seed=copy.deepcopy(before_data);seedrows=rows(seed)
 for loc,ref in targets.items():
  if sha(R/loc)!=ref['sha256']:raise RuntimeError('Card drift '+loc)
  seedrows[loc].pop('summary',None)
  seedrows[loc].pop('sha256',None) # Force documented parser re-entry; never change the actual card identity.
 save(D/'recovery-seed.json',seed)
 result=L.make_index(R,IndexPath=str((D/'candidate-index.json').relative_to(R)),PreviousIndex=str((D/'recovery-seed.json').relative_to(R)))
 save(D/'build-result.json',result)
 candidate=json.loads((D/'candidate-index.json').read_text());oldrows=rows(before_data);newrows=rows(candidate);changes=[]
 if set(oldrows)!=set(newrows):raise RuntimeError('Index membership changed')
 for loc,old in oldrows.items():
  new=newrows[loc]
  changed={k for k in old.keys()|new.keys() if old.get(k)!=new.get(k)}
  if loc not in targets and changed:raise RuntimeError('Unrelated row changed '+loc+' '+str(changed))
  if loc in targets:
   if changed-{'summary','inherited_metadata'}:raise RuntimeError('Non-summary change '+loc+' '+str(changed))
   if old.get('inherited_metadata')!=new.get('inherited_metadata'):raise RuntimeError('Metadata inheritance changed '+loc)
   front,body,_=L.read_metadata((R/loc).read_bytes());expected=str(front.get('summary') or re.sub(r'\s+',' ',body).strip())[:500]
   if new['summary']!=expected:raise RuntimeError('Summary is not exact current text '+loc)
   changes.append(dict(location=loc,sha256=sha(R/loc),before_summary=old['summary'],after_summary=new['summary'],changed=bool(changed)))
 if len(candidate['items'])!=78 or len(candidate['blocked_items'])!=1:raise RuntimeError('Correction gate changed')
 for k in before_data.keys()|candidate.keys():
  if k not in ['items','blocked_items','updated_at'] and before_data.get(k)!=candidate.get(k):raise RuntimeError('Index global field changed '+k)
 result=dict(status='CANDIDATE_EXACT_SUMMARY_REFRESH',before_sha256=sha(before),candidate_sha256=sha(D/'candidate-index.json'),cards=changes,source_cards_unchanged=True,gate_fields_unchanged=True,non_target_rows_unchanged=True,available=78,blocked=1)
 save(D/'comparison.json',result)
 author_ids=json.loads((O/'renewal-review-spec.json').read_text())['author_ids']
 inputs=[dict(path=loc,role='approved-current-card') for loc in targets]
 for name in ['index-before.json','candidate-index.json','comparison.json']:
  inputs.append(dict(path=str((D/name).relative_to(R)),role='derived-index-before-after'))
 claim=dict(id='R8-summary-recovery',verification='analytic',statement='Review only the eight unchanged current cards and their derived query summaries. Confirm each candidate summary is literally the first 500 characters of the whitespace-collapsed current body (or explicit summary if present), and thus removes obsolete content retained by the old index. In particular the Krein boundary uses first derivatives and the original-family H2/H3 completeness is not open. Confirm no card hash, dependency, correction status, reuse eligibility, index membership, non-target row or global gate metadata changes; only derived summaries and the index update timestamp may change. This is a retrieval presentation repair, not a new theorem, card version, correction release or fresh approval of all historical mathematics. Do not infer proof approval from a query count.')
 spec=dict(kind='mathematics',author_ids=author_ids,inputs=inputs,claims=[claim]);save(O/'summary-review-spec.json',spec);save(O/'summary-review-packet.json',V.create_packet(R,spec))
 print('Frozen derived-summary candidate:',len(changes),'cards;',sum(x['changed'] for x in changes),'summaries changed; mathematical and gate identities unchanged.',flush=True)
elif sys.argv[1]=='promote':
 bundle=json.loads((O/'summary-review-dispatch.json').read_text())['bundle']
 if V.verify_review_bundle(R,bundle)['verdict']!='APPROVED':raise RuntimeError('Summary review not approved')
 comp=json.loads((D/'comparison.json').read_text())
 with L.writer_lock(L.library_root(R)):
  if sha(index)!=comp['before_sha256'] or sha(D/'candidate-index.json')!=comp['candidate_sha256']:raise RuntimeError('Index drift during review')
  for loc,ref in targets.items():
   if sha(R/loc)!=ref['sha256']:raise RuntimeError('Card drift before promotion '+loc)
  L.immutable_write(L.library_root(R)/'index-history'/(comp['before_sha256']+'.json'),index.read_bytes())
  L.atomic_write(index,(D/'candidate-index.json').read_bytes())
 save(D/'promotion.json',dict(status='PROMOTED_REVIEWED_DERIVED_SUMMARIES',before_sha256=comp['before_sha256'],after_sha256=sha(index),bundle=bundle,card_bytes_changed=False,gate_bypassed=False))
 print('Reviewed derived summaries promoted; final live query still required.',flush=True)
else:raise ValueError(sys.argv[1])
