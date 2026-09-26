from pathlib import Path
import json
import sys

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = 'research/artifacts/proof-audit-round12-20260926'
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.1/scripts')
import research_state as State

Inputs = ['research_map.md', 'docs/PROJECT_UNDERSTANDING.md', 'literature/maps/FRONTIER.md', 'index/tools.json', 'reports/proof-audit-round12-20260926/REPORT.md', 'lean-proof/SL/AuditRound12.lean', Artifact + '/analytic-repair.md', Artifact + '/caller-inventory.json', Artifact + '/review-summary.json', Artifact + '/integration/library-verification.json']
Inputs.extend(['scripts/' + Name for Name in ['_sl_prufer.py', '_gapn2_half_problem_probe.py', '_gapn2_sector_decomposition.py', '_gapn2_green_inertia_probe.py', '_gapn2_half_debug2.py', '_gapn2_half_debug3.py']])
Inputs.extend(Row['location'] for Row in json.loads((Out / 'cards.json').read_text()).values())
Inputs.extend(Row['target']['location'] for Row in json.loads((Out / 'renewals.json').read_text()))
Inputs.extend(Row['bundle'] + '/report.json' for Row in json.loads((Root / Artifact / 'review-summary.json').read_text())['reviews'])
Result = State.checkpoint(Root, Inputs=Inputs)
Path = Path(Result['snapshot'])
Snapshot = json.loads(Path.read_text())
if Snapshot['inputs'] != State.input_snapshot(Root, Inputs) or State.digest(Path.read_bytes()) != Result['sha256']:
	raise RuntimeError('Checkpoint mismatch')
if Snapshot['progress_sha256'] != State.digest((Root / Snapshot['progress']).read_bytes()):
	raise RuntimeError('Progress changed')
Paths = [Path.relative_to(Root).as_posix(), '.research-state/progress/' + Snapshot['progress_sha256'] + '.md']
(Out / 'checkpoint-files.json').write_text(json.dumps(Paths, indent=2) + '\n')
Result.update(input_count=len(Snapshot['inputs']), current_inputs_match=True, progress_archive=Paths[1])
(Out / 'checkpoint-result.json').write_text(json.dumps(Result, ensure_ascii=False, indent=2) + '\n')
(Root / Artifact / 'integration/checkpoint.json').write_bytes((Out / 'checkpoint-result.json').read_bytes())
print('Checkpoint', Result['sha256'], len(Snapshot['inputs']), 'current inputs verified', flush=True)
