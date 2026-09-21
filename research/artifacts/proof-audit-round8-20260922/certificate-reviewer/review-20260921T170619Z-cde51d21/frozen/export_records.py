"""Copy verified results and inventory actual artifacts, without rewriting runs."""
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path


def file_hash(path):
	return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
	if not condition:
		raise RuntimeError(message)


def write_json(path, data):
	path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
	AuthorRoot = Path(__file__).resolve().parent
	RunPaths = sorted(path for path in (AuthorRoot / "runs").iterdir() if path.is_dir())
	RunRecords = [(path, json.loads((path / "record.json").read_text())) for path in RunPaths]
	CertificateHash = file_hash(AuthorRoot / "certificate.py")
	SelectedRuns = {}
	for mode in ("normal", "optimized"):
		candidates = [(path, record) for path, record in RunRecords if record["label"] == "certificate-" + mode and "-S" in record["command"] and record["return_code"] == 0 and record["input_sha256"].get("certificate.py") == CertificateHash]
		require(bool(candidates), "No matching successful certificate: " + mode)
		path, record = candidates[-1]
		OutputName = "results.json" if mode == "normal" else "results_optimized.json"
		shutil.copyfile(path / "results.json", AuthorRoot / OutputName)
		SelectedRuns[mode] = {"run": path.name, "result_sha256": file_hash(path / "results.json"), "record_sha256": file_hash(path / "record.json")}
	VerifierRuns = [(path, record) for path, record in RunRecords if record["label"] == "bundle-verification" and record["return_code"] == 0 and record["input_sha256"].get("verify_bundle.py") == file_hash(AuthorRoot / "verify_bundle.py")]
	require(bool(VerifierRuns), "No matching successful bundle verification")
	VerifierPath, _ = VerifierRuns[-1]
	VerificationData = json.loads((VerifierPath / "verification.json").read_text())
	require(VerificationData["certificate_sha256"] == CertificateHash, "Verifier certificate mismatch")
	shutil.copyfile(VerifierPath / "verification.json", AuthorRoot / "verification.json")
	rows = []
	for path, record in RunRecords:
		for name, ExpectedHash in record["files_sha256"].items():
			require(file_hash(path / name) == ExpectedHash, "Stored execution artifact changed")
		rows.append({
			"run": path.name, "role": record["label"], "command": record["command"],
			"return_code": record["return_code"], "expected_code": record["expected_code"],
			"expectation_matched": record["expectation_matched"],
			"record": str((path / "record.json").relative_to(AuthorRoot)),
			"record_sha256": file_hash(path / "record.json"),
			"stdout_sha256": file_hash(path / "stdout.txt"), "stderr_sha256": file_hash(path / "stderr.txt"),
		})
	SummaryData = {
		"role": "scoped certificate author, awaiting independent final review",
		"certificate_sha256": CertificateHash, "selected_result_runs": SelectedRuns,
		"verification_run": VerifierPath.name,
		"verification_record_sha256": file_hash(VerifierPath / "record.json"),
		"actual_exit_code_counts": dict(Counter(str(row["return_code"]) for row in rows)),
		"intentional_negative_failures": sum(row["role"].startswith("negative-") and row["return_code"] == 1 for row in rows),
		"unexpected_execution_results": [row for row in rows if not row["expectation_matched"]],
		"supplied_initial_failure": {"path": "inputs/submitted/initial_symbolic_check_failure.log", "sha256": file_hash(AuthorRoot / "inputs/submitted/initial_symbolic_check_failure.log"), "actual_original_exit_code": None, "failed_source_revision_available": False},
		"author_provenance_correction": {"retained_draft": "development/README-before-import-provenance-correction.md", "explanation": "Initial imports included distro startup hooks; claim corrected and -S replays added, original receipts retained."},
		"verification_receipt_note": "The verifier's current_run_pending_receipt names its own executing child; its now-complete outer record is included in this summary.",
		"runs": rows,
	}
	write_json(AuthorRoot / "replay_summary.json", SummaryData)
	ChangedPaths = sorted({str(path.relative_to(AuthorRoot)) for path in AuthorRoot.rglob("*") if path.is_file()} | {"changed_paths.txt", "artifact_hashes.json"})
	(AuthorRoot / "changed_paths.txt").write_text("\n".join(str(AuthorRoot / path) for path in ChangedPaths) + "\n", encoding="utf-8")
	InventoryData = {
		"algorithm": "SHA-256", "root": str(AuthorRoot),
		"excludes": ["artifact_hashes.json (this manifest cannot contain its own hash)"],
		"files": {name: {"sha256": file_hash(AuthorRoot / name), "size_bytes": (AuthorRoot / name).stat().st_size} for name in ChangedPaths if name != "artifact_hashes.json"},
	}
	write_json(AuthorRoot / "artifact_hashes.json", InventoryData)
	print(json.dumps({"selected_runs": SelectedRuns, "verification_run": VerifierPath.name,
		"exit_codes": SummaryData["actual_exit_code_counts"], "file_count": len(ChangedPaths),
		"manifest_sha256": file_hash(AuthorRoot / "artifact_hashes.json")}, indent=2))


if __name__ == "__main__":
	main()
