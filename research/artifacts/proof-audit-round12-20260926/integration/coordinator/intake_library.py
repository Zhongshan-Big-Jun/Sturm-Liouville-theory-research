from pathlib import Path
import json
import sys

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = Root / 'research/artifacts/proof-audit-round12-20260926'
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as Corrections

def save(Path, Data):
	Path.write_text(json.dumps(Data, ensure_ascii=False, indent=2) + '\n')

Baseline = json.loads((Out / 'baseline.json').read_text())
Targets = ['tools/green-half-inertia.md', 'tools/half-problem-regularized-green.md']
Issue = dict(issue_id='round12-half-spectrum-poles-and-parity', origin='external', reporter='sl_audit_round12; supplied function excerpts independently matched to whole current Git blobs', summary='R12-01/02: the separate half-spectrum mu-grid drops low modes and changes prefix with N; position-only pole exclusion can retain the actual pole. R12-03: the historical cross-parity Green expression is the odd block of SKS (E Ke E), not the raw K odd block. Quarantine the two directly affected cards pending indexed DD/DN repair, bound pole identity and exact sector correction. No blanket retraction of unchanged reduced-kernel derivations, round11 cofinite classification, or default R4 historical data.', disposition='quarantine', targets=[dict(location=Name, sha256=Baseline['tracked'][Name]) for Name in Targets], evidence=[dict(path=str((Artifact / 'submitted/proof_audit_round12_20260926.md').relative_to(Root)), locator='R12-01, R12-02, R12-03 and scope'), dict(path=str((Artifact / 'intake-verification.json').relative_to(Root)), locator='Whole current Git blob and nine function AST identity checks'), dict(path=str((Artifact / 'before/scripts/_gapn2_half_problem_probe.py').relative_to(Root)), locator='Old half_spectrum and _spectral_green exact bytes')])
if not (Out / 'issue-result.json').exists():
	save(Out / 'issue-input.json', Issue)
	save(Out / 'issue-result.json', Corrections.register_issue(Root, Issue))
for Name in ['issue-input.json', 'issue-result.json']:
	(Artifact / Name).write_bytes((Out / Name).read_bytes())
Store = Corrections.load_store(Root)
States, Problems = Corrections.impact_states(Root, Store)
save(Artifact / 'initial-impact.json', dict(affected=[dict(key=Key, state=State) for Key, State in States.items() if not State['reuse_allowed']], review_problems=Problems))
print(json.dumps(dict(status='QUARANTINE_REGISTERED', targets=Targets, affected_versions=sum(not State['reuse_allowed'] for State in States.values()), historical_review_problems=len(Problems))), flush=True)
