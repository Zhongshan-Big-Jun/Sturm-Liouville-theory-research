from pathlib import Path
import json,hashlib,shutil,gzip
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925');A=R/'research/artifacts/proof-audit-round10-20260925'
def sha(B):return hashlib.sha256(B).hexdigest()
Rows=[]
def copy(S,D):
 B=S.read_bytes();D.parent.mkdir(parents=True,exist_ok=True)
 if D.exists() and D.read_bytes()!=B:raise RuntimeError('Immutable archive drift '+str(D))
 if not D.exists():D.write_bytes(B)
 Rows.append(dict(path=str(D.relative_to(A)),sha256=sha(B),bytes=len(B)))
for N in ['cards.json','current-revisions.json','renewals.json','current-release-results.json','annotations.json','index-result.json','retrieval-result.json','library-verification.json','native-operations.jsonl','revision-pipeline.jsonl','final-library-pipeline.jsonl','math-review-binding-refresh.json','signed-step-counterexample.json','pdf-reviewed-visual-check.json']:
 copy(O/N,A/'integration'/N)
for Folder in ['math-review-first','renewal-review-first','math-preparation-v1']:
 for P in sorted((O/Folder).iterdir()):
  if P.is_file():copy(P,A/'author-development'/Folder/P.name)
for N in ['math-first-receive.log','math-first-receive-serial.log','release-renewals.log','revision-pipeline.log','release-current-final.log','annotate-index.log','query-library.log','formal-finalization-coordinator.log']:
 if (O/N).is_file():copy(O/N,A/'integration/logs'/N)
for P in sorted(O.glob('before-math-revision-*.json')):copy(P,A/'author-development'/P.name)
Scripts=['capture_baseline.py','intake_library.py','save_cards.py','refresh_bindings.py','refresh_typesetting_bindings.py','refresh_math_bindings.py','prepare_math_review.py','prepare_math_review_final.py','prepare_renewal.py','prepare_renewal_final.py','prepare_software_review.py','prepare_blind.py','prepare_formal_comparison.py','review_ops.py','run_native_posix.py','run_case.py','build_pdf.py','apply_math_revision.py','revision_pipeline.py','release_current.py','release_current_final.py','final_library_pipeline.py','annotate_index.py','query_library.py','finalize_docs.py','finish_checkpoint.py','final_document_check.py','publication.py','archive_final_evidence.py','archive_formal_execution.py','archive_coordinator_final.py']
Scripts.append('check_evidence_archives.py')
for N in Scripts:copy(O/N,A/'coordinator'/N)
for N in ['REPORT.final-template.md','commit-message.txt']:copy(O/N,A/'coordinator'/N)
for N in ['math-review-final-close.json','renewal-review-final-close.json']:
 copy(O/N,A/'integration'/N)
Source=R/'docs/SL_gap_nge2_symmetry_recon.tex';Digest=sha(Source.read_bytes());D=O/'pdf-build/SL_gap_nge2_symmetry_recon'/Digest[:12]
for P in D.iterdir():
 if P.is_file() and P.suffix not in ['.aux','.toc','.out','.pdf','.synctex']:copy(P,A/'pdf-reviewed-final'/P.name)
for N in ['reviewed-pdf-page1.png','reviewed-pdf-page3.png','reviewed-pdf-page5.png']:
 copy(O/N,A/'pdf-reviewed-final'/N)
Reviewer=O/'formal-reviewer/independent-35c0ed5b7a9f'
for P in sorted(Reviewer.rglob('*')):
 if not P.is_file() or any(X in P.relative_to(Reviewer).parts for X in ['objects','lib','tmp','__pycache__']) or P.suffix in ['.olean','.ilean','.pyc']:continue
 B=P.read_bytes();Dest=A/'formal-execution'/P.relative_to(Reviewer)
 if len(B)>2000000:
  Encoded=gzip.compress(B,mtime=0);Dest=Dest.with_suffix(Dest.suffix+'.gz');Dest.parent.mkdir(parents=True,exist_ok=True)
  if Dest.exists() and Dest.read_bytes()!=Encoded:raise RuntimeError('Compressed archive drift')
  Dest.write_bytes(Encoded);Rows.append(dict(path=str(Dest.relative_to(A)),sha256=sha(Encoded),bytes=len(Encoded),encoding='gzip',original_sha256=sha(B),original_bytes=len(B),original_path=str(P.relative_to(Reviewer))))
 else:copy(P,Dest)
(A/'delivery-evidence-manifest.json').write_text(json.dumps({'files':Rows,'scope':'Exact current library result and coordinator/independent-formal evidence. Original large JSON is losslessly compressed. Local compiled objects and temporary caches remain outside the repository; their recorded identities and reproduction sources are retained.'},ensure_ascii=False,indent=2)+'\n')
(A/'README.md').write_text('''# Round10 evidence entry

Current conclusions and limits are in [the report](../../../reports/proof-audit-round10-20260925/REPORT.md). This directory preserves submitted evidence, actual old failures, author attempts, current proof, independent checks and correction receipts separately.

- `analytic-repair.md`: current analytical contract; old rejected text remains under `author-development/mathematical-first-review/` and its original frozen packet.
- `software-review/`, `software-execution/`: independent review and actual executions of the unchanged final Python sources. Its older analytical snapshot is not approval of the subsequently corrected signed-step sentence.
- `formal-readback/`: blind38-declaration translation; `formal-comparison/` and `formal-execution/`: different reviewer's actual compilation and semantic comparison. Local scope only.
- `lean-author/`: original author machine evidence, including stale first exact-root run. Large JSON evidence uses lossless gzip with both hashes recorded in manifests.
- `pdf-reviewed-final/`: build record and inspected pages for the current active PDF. Earlier `pdf-final/` and `pdf-evidence/` are superseded build evidence, retained as history.
- `integration/`: original API results,15 current exact obligations, actual query, warnings and version-bound annotations. Earlier unchanged-card releases became stale after the independent mathematical review's document corrections and were renewed.
- `replays/`, `checks/`, `caller-inventory.json`: actually rerun configurations and exact current static caller identities. Historical experiments outside this scope are not revalidated.
- `coordinator/`: task-specific external helpers as used; they are not new generic plugin infrastructure. Replay into a new private output directory, following each command's inputs/environment, rather than overwriting old paths.

The final scoped publication manifest lives with the report. Canonical and historical project artifacts retain baseline bytes. Compiler success, blind readback, analytic review, numerical observations and library release are distinct evidence levels.
''')
print('Archived final coordinator/formal/library evidence',len(Rows),'files',sum(X['bytes'] for X in Rows),'bytes')
