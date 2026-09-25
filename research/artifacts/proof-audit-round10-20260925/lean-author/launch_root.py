from run import *

LABEL = sys.argv[1]
STATE = Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.1/scripts/research_state.py')
INPUTS = [BASE / 'run.py', BASE / 'launch_root.py', PROJECT / 'AuditRound10.lean', PROJECT / 'lean-toolchain', PROJECT / 'lake-manifest.json', PROJECT / 'lakefile.toml', BASE / 'root-contract.json']
ARGS = [sys.executable, '-B', STATE, 'start', '--project', BASE, '--job-id', LABEL + '-durable', '--cwd', '.', '--timeout', '7200']
for P in INPUTS:
	ARGS += ['--input', str(P.relative_to(BASE))]
ARGS += ['--', sys.executable, '-B', BASE / 'run.py', 'verify', LABEL, 'root-contract.json']
RESULT = run('launch-' + LABEL, ARGS, Cwd=BASE, Inputs=INPUTS)
sys.exit(RESULT['exit_code'])
