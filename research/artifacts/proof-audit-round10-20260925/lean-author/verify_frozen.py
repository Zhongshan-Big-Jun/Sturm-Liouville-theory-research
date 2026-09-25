from run import *

FROZEN = BASE / 'root-project'
LABEL = sys.argv[1]
CONTRACT = BASE / 'root-contract.json'
INPUTS = [Path(__file__), FROZEN / 'AuditRound10.lean', FROZEN / 'lean-toolchain',
	FROZEN / 'lakefile.toml', FROZEN / 'lake-manifest.json', CONTRACT]
RESULT = run(LABEL, [sys.executable, '-B', PLUGIN / 'scripts/verify_lean_project.py',
	'--project', FROZEN, '--contract', CONTRACT, '--lean', LEAN, '--lake', LAKE,
	'--direct', '--strict-exit', '--build-timeout', '1800', '--output', BASE / 'evidence' / LABEL],
	Cwd=FROZEN, Inputs=INPUTS)
sys.exit(RESULT['exit_code'])
