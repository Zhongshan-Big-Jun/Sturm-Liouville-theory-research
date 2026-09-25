from pathlib import Path
import hashlib,json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925');A=R/'research/artifacts/proof-audit-round10-20260925'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as C
B=json.loads((O/'baseline.json').read_text())
def save(P,D):P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
Targets=['tools/band-selfconsistency-equivariance.md','tools/green-half-inertia.md','tools/half-problem-regularized-green.md','tools/second-variation-weighted-eigenvalues.md']
Issue=dict(issue_id='round10-indexed-spectrum-and-reflection-sectors',origin='external',reporter='sl_audit_round10; actual-source reproduction by coordinator',summary='R10-01: shared sign scanner misses four certified low roots; local residual/ordering checks do not verify mode labels. R10-02: historical asym seed assignment is -J, not a sector projector. Suspend numerical-support reuse in four directly connected cards pending scoped correction and actual caller checks; this is not a disproof of their independent analytic identities.',disposition='quarantine',targets=[dict(location=N,sha256=B['tracked'][N]) for N in Targets],evidence=[dict(path=str((A/'submitted/proof_audit_round10_20260925.md').relative_to(R)),locator='R10-01 and R10-02'),dict(path=str((A/'actual-source-failure.json').relative_to(R)),locator='Actual imported original source k=2,3,61')])
if not (O/'issue-result.json').exists():
	save(O/'issue-input.json',Issue);Result=C.register_issue(R,Issue);save(O/'issue-result.json',Result)
for N in ['issue-input.json','issue-result.json']:(A/N).write_bytes((O/N).read_bytes())
Store=C.load_store(R);States,Problems=C.impact_states(R,Store)
save(A/'initial-impact.json',dict(affected=[dict(key=K,state=S) for K,S in States.items() if not S['reuse_allowed']],review_problems=Problems))
print(json.dumps(dict(status='QUARANTINE_REGISTERED',targets=Targets,affected_versions=sum(not S['reuse_allowed'] for S in States.values()),historical_review_problems=len(Problems))),flush=True)
