from pathlib import Path
import hashlib
import json
import sys
Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.1/scripts')
import research_state as State
Path = Root / 'state/RESUME.md'
Raw = Path.read_bytes()
Text = Raw.decode()
At = Text.index('\n') + 1
Entry = '''
## 2026-09-26 round12 repair IN PROGRESS

Latest user input: C:\\Users\\HuangZY\\Downloads\\sl_audit_round12, workflow2.0.1, "继续修订". Reconcile F:/tools/math-audit-round12-20260926/CURRENT.json, actual agent/job state and the round12 REPORT before resuming. Do not restart round11 completed work.

Baseline be7c091,16541 tracked/134 original untracked/6 dirty/52 old SL Lean sources recorded by raw hashes. Input16 hashes and9 excerpt-function ASTs match actual whole Git blobs. Supplied34 checks normal/-O and whole old-module bug reproduction completed. Current six-program candidate covers indexed DD/DN halves, bound shared pole tables, K versus SKS sector labels and two legacy diagnostic callers. Coordinator135 checks normal/-O passed. New software reviewer01a0dcf0-d75a-71f0-9eda-40e9b5618685 running; analytic author01a0dce3-b8a0-7d83-b359-03a8073d76d4 and formal author01a0dce9-5748-7710-9a4e-adff48f38f61 running. These authors are not final reviewers.

Two native correction issues quarantine green-half-inertia, half-problem-regularized-green and band-selfconsistency-equivariance. Remaining: finish analytic proof/card edits, exact revision/issue obligations and any stale-bundle renewals; fresh analytic and blind/formal-execution reviews; original API releases/index/annotations; final maps/understanding/checkpoint and protected exact commit; push origin then fork. Preserve all old evidence, failures, canonical and original dirty/untracked. No plugin/cache/global changes. Floating guards and finite samples are not interval certification; local Lean is not whole ODE/Green/G1 formalization.

'''
if '## 2026-09-26 round12 repair' in Text:
	raise RuntimeError('Round12 progress already inserted')
Result = State.save_progress(Root, Text[:At] + Entry + Text[At:], hashlib.sha256(Raw).hexdigest())
(Out / 'progress-initial.json').write_text(json.dumps(Result, indent=2)+'\n')
print('Native progress saved', flush=True)
