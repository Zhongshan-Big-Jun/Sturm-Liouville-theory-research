import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2) + "\n")

argv = ["/usr/bin/python3", "-B", "run_checks.py"]
receipt_dir = ROOT / "receipts"
if receipt_dir.is_symlink():
    raise RuntimeError("Refusing a symlink output directory")
created_receipts = not receipt_dir.exists()
receipt_dir.mkdir(exist_ok=True)
names = ["normal", "optimized", "negative-normal-old-fh", "negative-optimized-old-fh"]
expected_outputs = ["outputs.json", "outputs.optimized.json", "receipts/execution-summary.json"]
expected_outputs += ["receipts/" + n + suffix for n in names for suffix in [".stdout.log", ".stderr.log", ".execution.json"]]
# Inspect metadata only, never read previous executions' contents.
before = {}
for rel in expected_outputs:
    path = ROOT / rel
    if path.is_symlink():
        raise RuntimeError("Refusing a symlink output: " + rel)
    before[rel] = path.stat().st_mtime_ns if path.exists() else None
start_ns = time.time_ns()
started = now()
t0 = time.monotonic()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
with (OUT / "outer.stdout.log").open("wb") as stdout, (OUT / "outer.stderr.log").open("wb") as stderr:
    process = subprocess.Popen(argv, cwd=ROOT, stdout=stdout, stderr=stderr, env=env)
    initial = {"execution_role": "fresh independent finite-check verifier", "argv": argv, "cwd": str(ROOT), "pid": process.pid, "started_at_utc": started, "start_time_ns": start_ns, "environment_override": {"PYTHONDONTWRITEBYTECODE": "1"}, "created_receipts_output_directory": created_receipts, "preexisting_output_mtime_ns": before}
    write("outer.started.json", initial)
    timeout = False
    try:
        code = process.wait(timeout=1020)
    except subprocess.TimeoutExpired:
        timeout = True
        process.kill()
        code = process.wait()
ended = now()
stdout_bytes = (OUT / "outer.stdout.log").read_bytes()
stderr_bytes = (OUT / "outer.stderr.log").read_bytes()
new_outputs, not_observed = [], []
for rel in expected_outputs:
    path = ROOT / rel
    stat = path.stat() if path.exists() else None
    if stat is not None and stat.st_mtime_ns >= start_ns and stat.st_mtime_ns != before[rel]:
        data = path.read_bytes()
        new_outputs.append({"path": rel, "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "mtime_ns": stat.st_mtime_ns})
    else:
        not_observed.append(rel)
receipt = dict(initial, ended_at_utc=ended, elapsed_seconds=time.monotonic()-t0, returncode=code, outer_timeout=timeout, stdout_path=str((OUT/"outer.stdout.log").relative_to(ROOT)), stderr_path=str((OUT/"outer.stderr.log").relative_to(ROOT)), stdout=stdout_bytes.decode("utf-8", errors="replace"), stderr=stderr_bytes.decode("utf-8", errors="replace"), stdout_sha256=hashlib.sha256(stdout_bytes).hexdigest(), stderr_sha256=hashlib.sha256(stderr_bytes).hexdigest(), generated_outputs=new_outputs, expected_outputs_not_observed_as_fresh=not_observed)
write("outer.execution.json", receipt)
print(json.dumps(receipt, indent=2), flush=True)
