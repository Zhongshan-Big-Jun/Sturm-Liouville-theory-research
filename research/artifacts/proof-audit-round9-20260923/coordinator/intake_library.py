from pathlib import Path
import hashlib,json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A=R/'research/artifacts/proof-audit-round9-20260923'
P=Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
sys.path.insert(0,str(P))
import research_library as L
import research_corrections as C
B=json.loads((O/'baseline.json').read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
Targets=['tools/second-variation-weighted-eigenvalues.md','tools/secular-chebyshev-jacobi-rootcount.md','tools/bloch-band.md']
for n in Targets+['docs/SL_fixed_n_supremum.tex','docs/SL_fixed_n_supremum.pdf','docs/SL_spectral_topics_summary.tex','docs/SL_spectral_topics_summary.pdf','scripts/_gapn2_second_variation_probe.py','scripts/_gapn2_k_global_rank2.py','AGENTS.md','research_map.md','docs/PROJECT_UNDERSTANDING.md']:
	p=A/'before'/n;p.parent.mkdir(parents=True,exist_ok=True);Raw=(R/n).read_bytes()
	if hashlib.sha256(Raw).hexdigest()!=B['tracked'][n]:raise RuntimeError('Baseline changed '+n)
	if p.exists() and p.read_bytes()!=Raw:raise RuntimeError('Snapshot changed '+n)
	if not p.exists():p.write_bytes(Raw)
Finding=A/'propagation-findings.md'
if not Finding.exists():Finding.write_text('''# Round9 source propagation and intake observations

F01-F03 affect the second-variation card and the active probe. The fixed historical R-206 addendum retains its original bytes; the new proof and report supersede its erroneous kernel equality, alleged inevitable Green divergence and block-tangency claims. Its separate K identity is not recertified by this repair.

F04 also appears in the active summary at the fixed-n paragraph and in the root-count card's F_n = sin(y) Q_n notation. Correct physical F_n and normalized Fhat_n simultaneously. The historical B3 proof explicitly uses omega F_n; its root count is not refuted by the missing physical prefactor.

The bloch-band card is placed under review for an explicit, proof-supported upgrade of the prescribed balanced candidate sequence only. No equality with the all-density global supremum is implied.

The general-alternating Chebyshev card already uses normalized matrices and its derivation is independent; balanced-phase lists candidate root equations and correct scope, not the false physical function-value identity. The half-problem Green card only links the second-variation card for the historical K identity; it contains no assertion of divergence and no false normalized derivative equality. These link-only neighbors are not mathematically invalidated by the findings. No missing declared dependency was discovered that uses the erroneous claims.

Whole-summary hash bindings can invalidate unrelated existing releases even when their mathematical passages are unchanged. Their statuses must be examined and, where needed, renewed by a fresh isolated review. This text records author observations, not acceptance.
''')
Issue=dict(issue_id='round9-variation-and-normalization',origin='external',reporter='sl_audit_round9 supplied audit with coordinator source propagation inspection',summary='F01 wrong block-average tangent projection; F02 incorrect Green divergence obstruction; F03 missing normalized kernel component; F04 physical secular reflection factor and propagated notation. Review the separately supplied balanced-candidate monotonicity theorem within its restricted scope.',disposition='quarantine',targets=[dict(location=n,sha256=B['tracked'][n]) for n in Targets],evidence=[dict(path=str((A/'submitted/proof_audit_round9_20260923.md').relative_to(R)),locator='F01-F04 and constructive supplement'),dict(path=str(Finding.relative_to(R)),locator='Direct active source propagation and explicit unchanged neighbors')])
if not (O/'issue-result.json').exists():
	save(O/'issue-input.json',Issue);print('Register issue',flush=True);Result=C.register_issue(R,Issue);save(O/'issue-result.json',Result)
for n in ['issue-input.json','issue-result.json']:(A/n).write_bytes((O/n).read_bytes())
Store=C.load_store(R);States,Problems=C.impact_states(R,Store)
save(A/'initial-impact.json',dict(affected=[dict(key=k,state=s) for k,s in States.items() if not s['reuse_allowed']],review_problems=Problems))
print(json.dumps(dict(status='QUARANTINE_REGISTERED',targets=Targets,affected_versions=sum(not s['reuse_allowed'] for s in States.values()),historical_review_problems=len(Problems))),flush=True)
