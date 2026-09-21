from pathlib import Path
import hashlib,json,subprocess
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round7-20260921');B=json.loads((O/'baseline.json').read_text())
Allowed=set('''scripts/README.md
scripts/.gitattributes
tools/band-selfconsistency-equivariance.md
tools/half-problem-regularized-green.md
tools/green-half-inertia.md
docs/SL_gap_nge2_symmetry_recon.tex
docs/SL_gap_nge2_symmetry_recon.pdf
scripts/op03_gap_fh.py
scripts/gap_n1_grad.py
scripts/_tmp_fh_paradox.py
scripts/tmp_fh_test.py
scripts/tmp_verify_endpoints.py
scripts/_gapn2_hess_verify.py
scripts/_gapn2_hess_sign_and_bigR.py
scripts/_gapn2_jacobian_analytic.py
scripts/_gapn2_o3_scan.py
scripts/_gapn2_second_variation_probe.py
AGENTS.md
README.md
README_EN.md
PROJECT.md
research_map.md
docs/.gitattributes
docs/SL_gap_nge2_symmetry_local_proof.tex
docs/SL_gap_nge2_symmetry_local_proof.pdf
docs/SL_gap_extremals.tex
docs/SL_gap_extremals.pdf
docs/PROJECT_UNDERSTANDING.md
docs/research-guide.md
state/RESUME.md
state/AGENTS_SESSION_LOG.md
lean-proof/SL/.gitattributes
lean-proof/STATUS.md
tools/.gitattributes
tools/feynman-hellmann.md
tools/gap-band-extremals.md
tools/README.md
index/tools.json
research/library/card-bindings/catalog.json
research/library/corrections-journal.json'''.splitlines())
def digest(P):
 with P.open('rb') as F:return hashlib.file_digest(F,'sha256').hexdigest()
Changed=[]
for N,H in B['tracked'].items():
 if not (R/N).is_file():raise RuntimeError('Removed original '+N)
 if digest(R/N)!=H:
  if N not in Allowed:raise RuntimeError('Outside scope '+N)
  Changed.append(N)
for N,H in B['untracked'].items():
 if not (R/N).is_file() or digest(R/N)!=H:raise RuntimeError('Changed original untracked '+N)
OldLean=[N for N in B['tracked'] if N.startswith('lean-proof/SL/') and N.endswith('.lean')]
for N in OldLean:
 if digest(R/N)!=B['tracked'][N]:raise RuntimeError('Changed old Lean '+N)
if subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()!=B['head']:raise RuntimeError('Head changed')
D=dict(status='PASS',baseline_head=B['head'],original_tracked=len(B['tracked']),unchanged_original_tracked=len(B['tracked'])-len(Changed),authorized_changed_tracked=Changed,unchanged_original_untracked=len(B['untracked']),old_Lean_sources_preserved=len(OldLean),canonical_and_old_immutable_evidence='Every original file outside the explicit active-file allowlist retains its baseline SHA256, including every prior frozen run, card version, review, correction event and canonical file.',original_dirty_preserved=['.gitattributes','index/artifacts.json','index/runs.json','research/runs/R-20260831T020156Z-g1p-kpdet/workspace/AGENTS.md','state/activity.jsonl','state/current.json'])
(O/'protection-result.json').write_text(json.dumps(D,indent=2)+'\n');print({K:V for K,V in D.items() if K not in ['authorized_changed_tracked','canonical_and_old_immutable_evidence']})
