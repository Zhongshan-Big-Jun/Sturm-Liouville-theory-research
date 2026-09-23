from pathlib import Path
import hashlib,json,shutil
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A=R/'research/artifacts/proof-audit-round9-20260923';S=O/'software-author'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
B=json.loads((O/'baseline.json').read_text());D=json.loads((S/'DELIVERY.json').read_text());Target=R/'scripts/_gapn2_second_variation_probe.py'
if sha(Target)!=B['tracked']['scripts/_gapn2_second_variation_probe.py']:raise RuntimeError('Original probe drift')
for N,H in D['file_sha256'].items():
	if sha(S/N)!=H:raise RuntimeError('Author delivery changed '+N)
for P in S.rglob('*'):
	if not P.is_file():continue
	if '__pycache__' in P.parts or P.suffix=='.pyc':raise RuntimeError('Unintended cache')
	Q=A/'software-author'/P.relative_to(S);Q.parent.mkdir(parents=True,exist_ok=True)
	if Q.exists():raise RuntimeError('Archive already exists '+str(Q))
	shutil.copyfile(P,Q)
Target.write_bytes((S/'_gapn2_second_variation_probe.py').read_bytes())
if sha(Target)!=D['candidate_sha256']:raise RuntimeError('Integrated candidate differs')
Attrs=R/'scripts/.gitattributes'
with Attrs.open('ab') as F:F.write(b'\n# Ninth-round hash-bound numerical repair.\n_gapn2_second_variation_probe.py -text\n_gapn2_k_global_rank2.py -text\n')
Evidence=dict(candidate_sha256=D['candidate_sha256'],integrated_path='scripts/_gapn2_second_variation_probe.py',dependencies={N:sha(R/N) for N in ['scripts/_gapn2_symmetry_recon.py','scripts/_gapn2_jacobian_probe.py','scripts/_gapn2_jacobian_analytic.py','scripts/op03_gap_table.json']},author='01a0cbe7-3a93-7ec3-94d5-1481aa88a92d',status='AUTHOR_EVIDENCE_AWAITING_INDEPENDENT_REVIEW')
(A/'software-integration.json').write_text(json.dumps(Evidence,indent=2)+'\n')
(A/'software-reproduction.md').write_text('''# Frozen numerical repair reproduction

This packet contains the actual current probe, its three local imported modules and input table, the original probe snapshot, and author test scripts/logs. External numerical dependencies are the installed NumPy, SciPy, mpmath; input_manifest.json records versions. These tests are finite numerical checks, not universal certificates.

For independent execution, copy the packet's listed input snapshots preserving their original relative paths to a NEW private directory outside the source project. Work with that copied input root as cwd. Do not read the author's live work directory or alter the frozen packet. The current script in scripts/ uses its sibling dependencies. The identical author copy falls back to cwd/scripts; its tests locate that adjacent author copy. All required local imports and table are supplied.

Run the copied test_candidate.py with -B normally and with -B -O, passing --output to a fresh reviewer output path. The copied current probe retains positional arguments n R mode and --output; rerun the four listed cases and the R=1 compatibility example as useful. sensitivity.py writes beside its own copy, so run ONLY the private copied version. regression_projection.py accepts a source path, and the old original projection should produce the recorded nonzero failure while the new projection passes. No original-source read is needed.

Independently inspect the implementation and choose additional counterexamples instead of relying only on an author PASS label. Inspect cutoff/FD errors, actual residuals, path positivity, normalization, real endpoints and the distinction between arbitrary density direction and box feasibility. P3 remains a fixed-width finite experiment. The separate mathematical packet handles the universal analytic proof; no numerical packet establishes G1/O1/O2.
''')
print('Integrated and archived',D['candidate_sha256'],flush=True)
