from pathlib import Path
import json,shutil,hashlib
O=Path('/mnt/f/tools/math-audit-round10-20260925');R=Path('/mnt/f/LaTeX/BVE research');A=R/'research/artifacts/proof-audit-round10-20260925'
if (R/'research/library/writer.lock').exists():raise RuntimeError('Library transaction still active')
Receipts=json.loads((O/'current-release-results.json').read_text())
if len(Receipts)!=4 or any(X['result']['verdict']!='RELEASED' for X in Receipts):raise RuntimeError('First unchanged-card transaction incomplete')
if json.loads((O/'math-review-received.json').read_text())['verdict']!='CHANGES_REQUIRED':raise RuntimeError('Original negative receipt not saved')
for Name in ['math-review','renewal-review']:
 D=O/(Name+'-first');D.mkdir(exist_ok=False)
 for S in ['spec','packet','spawn','completion','dispatch','received','verified']:
  P=O/(Name+'-'+S+'.json')
  if P.exists():shutil.copyfile(P,D/P.name)
for N in ['cards.json','revisions.json','current-revisions.json','renewals.json','renewal-inspection.json','current-release-results.json']:
 shutil.copyfile(O/N,O/('before-math-revision-'+N))
for N,Dest in [('analytic-repair.md',A/'analytic-repair.md'),('SL_gap_nge2_symmetry_recon.tex',R/'docs/SL_gap_nge2_symmetry_recon.tex')]:
 B=Dest.read_bytes();Old=A/'author-development/mathematical-first-review'/N;Old.parent.mkdir(parents=True,exist_ok=True);Old.write_bytes(B)
 New=(O/'mathematical-revision-candidate'/N).read_bytes();Dest.write_bytes(New)
 print('Applied',N,hashlib.sha256(New).hexdigest(),flush=True)
S=(O/'refresh_typesetting_bindings.py').read_text().replace("O/'typesetting-binding-refresh.json'", "O/'math-review-binding-refresh.json'")
(O/'refresh_math_bindings.py').write_text(S)
S=(O/'prepare_renewal.py').read_text();Old="Rows=[X for X in json.loads((O/'renewal-inspection.json').read_text())['new_invalid_releases'] if X['target']['location'] not in Changed]"
New=Old+"\n# Several historical receipts can refer to the same unchanged exact revision.\nRows=list({X['revision']:X for X in Rows}.values())"
assert Old in S;(O/'prepare_renewal_final.py').write_text(S.replace(Old,New,1))
S=(O/'release_current.py').read_text().replace("if any(D['revision']==X['revision'] for D in Done):continue", "if any(D['revision']==X['revision'] and D['bundle']==X['bundle'] for D in Done):continue")
(O/'release_current_final.py').write_text(S)
Doc='''# First mathematical review: verified amendments\n\nThe first mathematical review returned CHANGES_REQUIRED. Its actual report, completion and immutable packet remain under the original49ad935d bundle. Card-level clauses were approved but the overall bundle was not a release authorization.\n\nF1: the feasible-step argument now explicitly assumes every base width exceeds h and 0<=t for the one-sided upper bound. It also gives the full signed interval and the exact rational counterexample t=-3/20. The actual generator already required positive magnitudes; no Python change follows. F2: the experience summary now agrees with the detailed column-state composition convention and leaves the missing historical variant's failure cause unverified.\n\nThe software verdict continues to apply to its unchanged exact Python sources and actual executions. It does not approve the former unrestricted signed-step sentence. The new analytical document and source-bound card revisions receive fresh mathematical review. Four earlier unchanged-card renewals are superseded by new receipts because their shared document inputs changed; original successful receipts remain historical.\n'''
(A/'author-development/mathematical-first-review/AMENDMENTS.md').write_text(Doc)
print('Preserved first reviews and prepared exact fresh binding helpers.',flush=True)
