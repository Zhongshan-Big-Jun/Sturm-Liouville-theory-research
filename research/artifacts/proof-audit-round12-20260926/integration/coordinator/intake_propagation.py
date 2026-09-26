from pathlib import Path
import json
import sys
Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = Root / 'research/artifacts/proof-audit-round12-20260926'
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as Corrections
Baseline = json.loads((Out / 'baseline.json').read_text())
Issue = dict(issue_id='round12-propagated-sector-labels', origin='internal', reporter='01a06f46-dd03-7c83-9267-32048412c359', disposition='quarantine', summary='Direct propagation discovered during actual R4 repair runs: sector_data raw Ke/Ko labels actually denote even/odd blocks of Kp=SKS; band-selfconsistency-equivariance repeats that split and assigns the negative rank-one criterion to the wrong raw sector. Suspend current reuse of the card until convention and dominance scope are corrected. This is an object-identity error, not evidence against total-inertia preservation or round11 residual-Jacobian anticommutation.', targets=[dict(location='tools/band-selfconsistency-equivariance.md', sha256=Baseline['tracked']['tools/band-selfconsistency-equivariance.md'])], evidence=[dict(path=str((Artifact / 'before/scripts/_gapn2_sector_decomposition.py').relative_to(Root)), locator='sector_data old He/Ho/Ee/Eo and Ke/Ko assignment'), dict(path=str((Artifact / 'before/tools/band-selfconsistency-equivariance.md').relative_to(Root)), locator='Historical sector formulas and Sherman-Morrison odd label')])
if not (Out / 'propagation-issue-result.json').exists():
	(Out / 'propagation-issue-input.json').write_text(json.dumps(Issue, ensure_ascii=False, indent=2)+'\n')
	Result = Corrections.register_issue(Root, Issue)
	(Out / 'propagation-issue-result.json').write_text(json.dumps(Result, ensure_ascii=False, indent=2)+'\n')
for Name in ['propagation-issue-input.json','propagation-issue-result.json']:
	(Artifact / Name).write_bytes((Out / Name).read_bytes())
print('Direct propagation issue registered', flush=True)
