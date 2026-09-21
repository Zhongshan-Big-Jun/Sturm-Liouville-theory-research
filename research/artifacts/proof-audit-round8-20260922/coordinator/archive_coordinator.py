from pathlib import Path
import hashlib,json,shutil,datetime
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922');A=R/'research/artifacts/proof-audit-round8-20260922'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy(s,t):
	t.parent.mkdir(parents=True,exist_ok=True)
	if t.exists() and sha(s)!=sha(t):raise RuntimeError('Existing archived coordinator evidence differs '+str(t))
	if not t.exists():shutil.copyfile(s,t)
for n in ['certificate-review','math-review','formal-readback','formal-semantic','renewal-review','summary-review']:
	d=json.loads((O/(n+'-received.json')).read_text())
	if d['verdict']!='APPROVED':raise RuntimeError('Pending independent review '+n)
	for suffix in ['spec','packet','spawn','dispatch','completion','received']:
		copy(O/(n+'-'+suffix+'.json'),A/'orchestration'/(n+'-'+suffix+'.json'))
for p in (O/'pdf-build').rglob('*'):
	if p.is_file():copy(p,A/'pdf-build'/p.relative_to(O/'pdf-build'))
for p in (O/'pdf-visual').iterdir():
	if p.is_file():copy(p,A/'pdf-visual'/p.name)
for p in list(O.glob('*.py'))+list(O.glob('*-repair.tex'))+list(O.glob('*-card.md'))+[O/'coordinator-math.md']:
	copy(p,A/'coordinator'/p.name)
for n in ['cards.json','revisions.json','release-results.json','renewals.json','renewal-release-results.json','annotations.json','library-final.json','final-query-result.json','integrated-proof-sources.json','pdf-page-selection.json','native-operations.jsonl','protection-result.json','final-document-check.json','whitespace-check.json','baseline-markdown.json','session-log-prefix-preservation.json','pre-final-document-check.json']:
	copy(O/n,A/'coordinator'/n)
for n in ['cot-series-certificate','delta-bracketing','lemma-A-doubleprime','inf-limit-comparison']:
	copy(O/(n+'-requirements.json'),A/'coordinator'/(n+'-requirements.json'))
plugin=json.loads((O/'source-verification.json').read_text())['plugin_sources']
(A/'library-runtime.json').write_text(json.dumps({'status':'EXISTING_RUNTIME_REUSED','plugin_sources':plugin,'checkout':'_xsoc1_work','module_scope':'Existing maintained library/correction/review APIs; no plugin code or cache edit','private_runtime_provenance':'research/artifacts/proof-audit-round7-20260921/library-runtime','new_wrapper':'coordinator/run_native_posix.py','new_operations':'coordinator/native-operations.jsonl','global_configuration_modified':False,'canonical_modified':False},indent=2)+'\n')
(A/'coordinator/README.md').write_text('''# Coordinator maintenance evidence

The current accepted proof is the hash-bound TeX referenced by the round8 review packet. The fragments and draft notes here preserve author development and maintenance choices; they are not independent approvals. Final acceptance uses native fresh-review dispatch/completion bundles under research/library/reviews.

The library runtime wrapper reuses the previously verified private POSIX runtime without changing the three plugin modules, frozen absolute paths, journal semantics or global configuration. New operations are logged separately. Current query/release results, not runtime choice, establish retrieval eligibility.

The original author sliver completion notification was followed by a queued follow-up and a timed-out collection. That exact wait remains history; the coordinator note explicitly records the race. It is not a review receipt. Final mathematical review was performed by another fresh stateless session.

PDF rendering initially found Pillow unavailable and used the existing PyMuPDF renderer; this did not change any mathematical source. An early formal packet-preparation path expected summary.json, and failed before dispatch; the actual author file evidence.json was selected. These maintenance failures are not certificate passes.
''')
rows=[]
for prefix in ['orchestration','pdf-build','pdf-visual','coordinator']:
	for p in sorted((A/prefix).rglob('*')):
		if p.is_file():rows.append({'path':str(p.relative_to(A)),'sha256':sha(p)})
(A/'coordinator-archive.json').write_text(json.dumps({'kind':'coordinator_exact_copy_check','files':rows},ensure_ascii=False,indent=2)+'\n')
print('Coordinator evidence archived',len(rows),'files',flush=True)
