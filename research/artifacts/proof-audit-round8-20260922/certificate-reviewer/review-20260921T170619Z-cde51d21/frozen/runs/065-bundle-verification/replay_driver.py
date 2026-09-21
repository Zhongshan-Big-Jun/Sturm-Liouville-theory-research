"""Append-only replay evidence inside the author's directory; no OS sandbox."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

AuthorRoot = Path(__file__).resolve().parent
RoundRoot = AuthorRoot.parent


def require(condition, message):
	if not condition:
		raise RuntimeError(message)


def file_hash(path):
	return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, data):
	path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def preserve_inputs():
	InputRoot = AuthorRoot / "inputs"
	InputRoot.mkdir(exist_ok=True)
	IntakeData = json.loads((RoundRoot / "intake.json").read_text())
	OriginalRoot = Path(IntakeData["source"])
	rows = []
	for name, entry in IntakeData["files"].items():
		source = RoundRoot / "submitted" / name
		if not source.is_file():
			source = OriginalRoot / name
		require(source.is_file(), "Missing supplied artifact: " + name)
		require(file_hash(source) == entry["sha256"], "Intake hash mismatch: " + name)
		destination = InputRoot / "submitted" / name
		destination.parent.mkdir(exist_ok=True)
		if not destination.exists():
			shutil.copyfile(source, destination)
		require(file_hash(destination) == entry["sha256"], "Preserved input mismatch")
		rows.append({"source": str(source), "copy": str(destination.relative_to(AuthorRoot)), **entry})
	for name in (
		"docs/SL_gap_n1_inf_limit_proof.tex",
		"runs/rigorous-open-math-research/R-20260806T200000Z-inflimit-5B2C7D/reproducibility/05_interval_value.py",
		"runs/rigorous-open-math-research/R-20260806T200000Z-inflimit-5B2C7D/reproducibility/19_verify_lemma_A_doubleprime_chain.py",
	):
		source = RoundRoot / "sources" / name
		destination = InputRoot / "sources" / name
		destination.parent.mkdir(parents=True, exist_ok=True)
		ExpectedHash = IntakeData["sources"][name]["sha256"]
		require(file_hash(source) == ExpectedHash, "Frozen source drift: " + name)
		if not destination.exists():
			shutil.copyfile(source, destination)
		require(file_hash(destination) == ExpectedHash, "Preserved source mismatch")
		rows.append({"source": str(source), "copy": str(destination.relative_to(AuthorRoot)), "sha256": ExpectedHash})
	ManifestPath = InputRoot / "manifest.json"
	if not ManifestPath.exists():
		write_json(ManifestPath, {"files": rows, "original_failure_exit_code": None,
			"note": "The supplied initial failure log is preserved; its original process exit code and failed source revision were not supplied."})
	return InputRoot


def run_attempt(label, files, target, arguments=(), optimized=False, expected_code=0, no_site=False):
	RunsRoot = AuthorRoot / "runs"
	RunsRoot.mkdir(exist_ok=True)
	indices = [int(path.name.split("-", 1)[0]) for path in RunsRoot.iterdir() if path.is_dir() and path.name.split("-", 1)[0].isdigit()]
	RunPath = RunsRoot / (str(max(indices, default=0) + 1).zfill(3) + "-" + label)
	RunPath.mkdir()
	for name, source in {**files, "trace_execution.py": AuthorRoot / "trace_execution.py", "replay_driver.py": AuthorRoot / "replay.py"}.items():
		shutil.copyfile(source, RunPath / name)
	InputHashes = {path.name: file_hash(path) for path in RunPath.iterdir() if path.is_file()}
	command = [sys.executable, "-B"] + (["-O"] if optimized else [])
	if no_site:
		command.append("-S")
	command += ["trace_execution.py", "imports.json", target, *arguments]
	environment = dict(os.environ)
	environment["PYTHONDONTWRITEBYTECODE"] = "1"
	StartedUtc = datetime.now(timezone.utc).isoformat()
	TimedOut = False
	try:
		process = subprocess.run(command, cwd=RunPath, env=environment, capture_output=True, timeout=180)
		stdout, stderr, ReturnCode = process.stdout, process.stderr, process.returncode
	except subprocess.TimeoutExpired as error:
		stdout, stderr, ReturnCode = error.stdout or b"", error.stderr or b"", None
		TimedOut = True
	(RunPath / "stdout.txt").write_bytes(stdout)
	(RunPath / "stderr.txt").write_bytes(stderr)
	Matched = not TimedOut and ReturnCode == expected_code
	record = {
		"label": label, "command": command, "cwd": str(RunPath),
		"started_utc": StartedUtc, "finished_utc": datetime.now(timezone.utc).isoformat(),
		"return_code": ReturnCode, "timed_out": TimedOut,
		"expected_code": expected_code, "expectation_matched": Matched,
		"input_sha256": InputHashes,
		"files_sha256": {path.name: file_hash(path) for path in sorted(RunPath.iterdir()) if path.is_file()},
		"isolation": "Private copies and cwd, -B/PYTHONDONTWRITEBYTECODE; existing dependencies. No security sandbox or dependency isolation.",
	}
	write_json(RunPath / "record.json", record)
	print(json.dumps({"run": RunPath.name, "return_code": ReturnCode, "expected": expected_code, "expectation_matched": Matched}), flush=True)
	return RunPath, record


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("stage", choices=("supplied", "certificate", "verify"))
	parser.add_argument("--no-site", action="store_true")
	args = parser.parse_args()
	require(not (args.stage == "supplied" and args.no_site), "Supplied checks need existing site dependencies")
	InputRoot = preserve_inputs()
	StageRecords = []

	def capture(*PositionalArgs, **KeywordArgs):
		RunPath, record = run_attempt(*PositionalArgs, **KeywordArgs)
		StageRecords.append(record)
		return RunPath, record

	if args.stage == "supplied":
		for optimized in (False, True):
			mode = "optimized" if optimized else "normal"
			files = {"checks.py": InputRoot / "submitted" / "checks.py"}
			_, record = capture("supplied-" + mode, files, "checks.py", ("results.json",), optimized)
			if record["return_code"] != 0:
				files["continue_supplied.py"] = AuthorRoot / "continue_supplied.py"
				capture("supplied-continuation-" + mode, files, "continue_supplied.py", ("results.json",), optimized, expected_code=1)
		capture("legacy-platform-diagnostics", {
			"checks.py": InputRoot / "submitted" / "checks.py",
			"legacy_diagnostics.py": AuthorRoot / "legacy_diagnostics.py",
		}, "legacy_diagnostics.py", ("observations.json",))
	elif args.stage == "certificate":
		sys.path.insert(0, str(AuthorRoot))
		import certificate
		for optimized in (False, True):
			mode = "optimized" if optimized else "normal"
			files = {"certificate.py": AuthorRoot / "certificate.py"}
			capture("certificate-" + mode, files, "certificate.py", ("--output", "results.json"), optimized, no_site=args.no_site)
			for name in certificate.NegativeControls:
				capture("negative-" + name + "-" + mode, files, "certificate.py", ("--negative", name, "--output", "results.json"), optimized, expected_code=1, no_site=args.no_site)
	else:
		capture("bundle-verification", {
			"verify_bundle.py": AuthorRoot / "verify_bundle.py",
			"certificate.py": AuthorRoot / "certificate.py",
		}, "verify_bundle.py", (str(AuthorRoot), "verification.json"), no_site=args.no_site)
	return 0 if all(record["expectation_matched"] for record in StageRecords) else 1


if __name__ == "__main__":
	sys.exit(main())
