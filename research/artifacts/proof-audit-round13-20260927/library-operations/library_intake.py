from pathlib import Path
import hashlib
import json
import sys

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round13-20260927')
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as Corrections

Cases = [
	('round13-certificate-and-helly', 'quarantine', ['rational-envelope-certificates', 'true-curve-region-decomposition', 'helly-compactness'], 'R13-01..06 and R13-11: verify and repair current certificate statements/acceptance and missing Helly hypotheses; no automatic retraction of measurable-box or A1/A12 results.'),
	('round13-retired-decimal-engine', 'retracted', ['interval-dec-directed-rounding'], 'R13-03/05/06: original Decimal engine has false enclosure and successful-exit counterexamples. Retain it solely as frozen historical evidence, not a default trusted engine.')
]
for Name, Disposition, Cards, Summary in Cases:
	Data = dict(issue_id=Name, origin='external', reporter='sl_audit_round13', summary=Summary, disposition=Disposition, targets=[dict(location='tools/' + Card + '.md', sha256=hashlib.sha256((Root / ('tools/' + Card + '.md')).read_bytes()).hexdigest()) for Card in Cards], evidence=[dict(path='research/artifacts/proof-audit-round13-20260927/submitted/REPORT.md', locator='R13-01..06, R13-11 and boundaries'), dict(path='research/artifacts/proof-audit-round13-20260927/submitted/analytic_notes.md', locator='Exact counterexamples and hypotheses')])
	(Out / (Name + '-input.json')).write_text(json.dumps(Data, ensure_ascii=False, indent=2) + '\n')
	Result = Corrections.register_issue(Root, Data)
	(Out / (Name + '-result.json')).write_text(json.dumps(Result, ensure_ascii=False, indent=2) + '\n')
	print(Name, Result.get('verdict'), flush=True)
