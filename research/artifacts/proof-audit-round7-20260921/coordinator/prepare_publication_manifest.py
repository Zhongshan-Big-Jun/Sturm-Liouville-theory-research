from pathlib import Path
import json,hashlib,datetime,subprocess,shutil
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round7-20260921');B=json.loads((O/'baseline.json').read_text());P=json.loads((O/'protection-result.json').read_text());assert P['status']=='PASS'
Target='reports/proof-audit-round7-20260921/publication-manifest.json';assert not (R/Target).exists()
Names=set(P['authorized_changed_tracked'])
for Prefix in ['reports/proof-audit-round7-20260921','research/artifacts/proof-audit-round7-20260921','research/library']:
 for F in (R/Prefix).rglob('*'):
  if F.is_file():
   Name=str(F.relative_to(R))
   if Name not in B['tracked'] and Name not in B['untracked']:Names.add(Name)
Names.update(['lean-proof/SL/AuditRound7.lean','scripts/.gitattributes','docs/.gitattributes','lean-proof/SL/.gitattributes','tools/.gitattributes'])
assert Target not in Names and not Names.intersection(B['untracked'])
Files=[]
for Name in sorted(Names):
 F=R/Name
 with F.open('rb') as Stream:H=hashlib.file_digest(Stream,'sha256').hexdigest()
 Files.append({'path':Name,'sha256':H,'bytes':F.stat().st_size})
Reviews={}
for Name in ['math','formal-v2','propagation']:
 D=json.loads((O/(Name+'-review-dispatch.json')).read_text());V=json.loads((O/(Name+'-review-receipt.json')).read_text());assert V['verdict']=='APPROVED'
 Reviews[Name]={'bundle':D['bundle'],'reviewer':D['reviewer_id'],'verdict':V['verdict']}
Record={'kind':'Reviewed candidate identity recorded before publication, not a post-push receipt','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_head':B['head'],'branch':subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip(),'push_order':['origin/main','fork/main'],'review_receipts':Reviews,'protection':P,'path_count_excluding_this_manifest':len(Files),'logical_bytes_excluding_this_manifest':sum(F['bytes'] for F in Files),'largest_file_bytes':max(F['bytes'] for F in Files),'per_file_guard_bytes':100_000_000,'storage_note':'Large exact verifier manifests are losslessly gzip-compressed with original byte hashes and reversible path mappings. Duplicate raw payloads are archived once. Derived readable indexes are labeled and do not replace the preserved complete raw evidence. Existing frozen evidence is unchanged.','software_review':{'input_packet_sha256':hashlib.sha256((O/'software-review-v2/PACKET.json').read_bytes()).hexdigest(),'verdict':json.loads((O/'software-review-v2/REVIEW.json').read_text())['verdict'],'report_sha256':hashlib.sha256((O/'software-review-v2/REVIEW.json').read_bytes()).hexdigest()},'files':Files,'post_commit_verification':'F:/tools/math-audit-round7-20260921/LOCAL_COMMIT_VERIFICATION.json','post_push_verification':'F:/tools/math-audit-round7-20260921/DELIVERY.json'}
(R/Target).write_text(json.dumps(Record,ensure_ascii=False,indent=2)+'\n');print('Candidate files',len(Files)+1,'largest',Record['largest_file_bytes'],'logical bytes',Record['logical_bytes_excluding_this_manifest'])
