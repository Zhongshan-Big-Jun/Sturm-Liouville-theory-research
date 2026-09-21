"""Optional durable launcher for the unchanged, frozen replay.py.

Usage: python3 -B launch_replay.py NEW_OUTPUT_DIR --job-id UNIQUE_JOB_ID
The actual checking command is still: python3 -B replay.py NEW_OUTPUT_DIR.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, subprocess, sys, uuid

Base = Path(__file__).resolve().parent
Parser = argparse.ArgumentParser(description=__doc__)
Parser.add_argument('output', type=Path)
Parser.add_argument('--job-id', required=True)
Args = Parser.parse_args()
Output = Args.output.resolve()
if Output.exists():
	raise SystemExit('Output already exists; select a fresh directory.')
StateTool = Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.0/scripts/research_state.py')
Argv = [sys.executable, '-B', str(StateTool), 'start', '--project', str(Base), '--job-id', Args.job_id]
for Name in ['freeze.json', *json.loads((Base / 'freeze.json').read_text())['files']]:
	Argv += ['--input', Name]
Argv += ['--', sys.executable, '-B', str(Base / 'replay.py'), str(Output)]
Result = subprocess.run(Argv, capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
LogDir = Base / 'launches'
LogDir.mkdir(exist_ok=True)
Prefix = LogDir / uuid.uuid4().hex
Prefix.with_suffix('.stdout.txt').write_text(Result.stdout)
Prefix.with_suffix('.stderr.txt').write_text(Result.stderr)
Prefix.with_suffix('.json').write_text(json.dumps(dict(argv=Argv, exit_code=Result.returncode, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), launcher_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), state_tool_sha256=hashlib.sha256(StateTool.read_bytes()).hexdigest()), indent=2) + '\n')
print(Result.stdout, end='')
print(Result.stderr, end='', file=sys.stderr)
sys.exit(Result.returncode)
