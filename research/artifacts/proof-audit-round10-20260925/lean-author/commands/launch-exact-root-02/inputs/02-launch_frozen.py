from run import *

LABEL = sys.argv[1]
FROZEN = BASE / 'root-project'
STATE = Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.1/scripts/research_state.py')
INPUTS = [BASE / 'run.py', BASE / 'verify_frozen.py', BASE / 'launch_frozen.py', BASE / 'root-contract.json',
	FROZEN / 'AuditRound10.lean', FROZEN / 'lean-toolchain', FROZEN / 'lakefile.toml', FROZEN / 'lake-manifest.json']
ARGS = [sys.executable, '-B', STATE, 'start', '--project', BASE, '--job-id', LABEL + '-durable', '--cwd', '.', '--timeout', '7200']
for P in INPUTS:
	ARGS += ['--input', str(P.relative_to(BASE))]
ARGS += ['--', sys.executable, '-B', BASE / 'verify_frozen.py', LABEL]
RESULT = run('launch-' + LABEL, ARGS, Cwd=BASE, Inputs=INPUTS)
sys.exit(RESULT['exit_code'])
