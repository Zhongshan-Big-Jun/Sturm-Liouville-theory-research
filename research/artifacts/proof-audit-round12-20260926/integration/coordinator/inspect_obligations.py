from pathlib import Path
import hashlib
import json
import sys
Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as Corrections
Store = Corrections.load_store(Root)
States, Problems = Corrections.impact_states(Root, Store)
Initial = {Item['release'] for Item in json.loads((Root / 'research/artifacts/proof-audit-round12-20260926/initial-impact.json').read_text())['review_problems']}
Invalid = []
for Problem in Problems:
	if Problem['release'] in Initial:
		continue
	Payload = Store['requests'][Problem['release']]['payload']
	Revision = Store['requests'][Payload['revision']]['payload']
	Invalid.append(dict(old_release=Problem['release'], revision=Payload['revision'], target=Revision['new'], issue=Revision['issue'], old_bundle=Payload['bundle'], problem=Problem))
Current = []
for Path in (Root / 'tools').glob('*.md'):
	Ref = dict(location=Path.relative_to(Root).as_posix(), sha256=hashlib.sha256(Path.read_bytes()).hexdigest())
	State = States.get(Corrections.key(Ref))
	if State and not State['reuse_allowed']:
		Current.append(dict(target=Ref, state=State))
(Out / 'obligations-inspection.json').write_text(json.dumps(dict(new_invalid_releases=Invalid, current_blocked=Current, all_review_problems=Problems), ensure_ascii=False, indent=2)+'\n')
print(json.dumps(dict(current_blocked=[dict(path=Row['target']['location'], issue_count=len(Row['state']['issues'])) for Row in Current], new_invalid_releases=len(Invalid), historical_review_problems=len(Problems)), ensure_ascii=False), flush=True)
