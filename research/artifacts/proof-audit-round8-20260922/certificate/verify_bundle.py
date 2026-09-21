"""Author evidence verification, not independent mathematical final review."""
import ast
import hashlib
import json
import re
import sys
import sysconfig
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import certificate


ExpectedMessages = {
	"wrong-g-right": "ArithmeticError: G upper endpoint must have strictly negative G",
	"old-upper-endpoint": "ArithmeticError: Root upper endpoint must have strictly positive F",
	"wrong-u-enclosure": "ArithmeticError: wrong-u-enclosure: proposed enclosure does not contain certified enclosure",
	"wrong-value-enclosure": "ArithmeticError: wrong-value-enclosure: proposed enclosure does not contain certified enclosure",
	"unsafe-cot-enclosure": "ArithmeticError: unsafe-cot-enclosure: proposed enclosure does not contain certified enclosure",
	"binary-pi-enclosure": "ArithmeticError: binary-pi-enclosure: proposed enclosure does not contain certified enclosure",
	"wrong-sqrt-enclosure": "ArithmeticError: Invalid sqrt(2) enclosure",
	"omitted-taylor-remainder": "ArithmeticError: omitted-taylor-remainder: proposed enclosure does not contain certified enclosure",
	"zero-divisor": "ArithmeticError: Divisor interval contains zero",
	"reversed-interval": "ArithmeticError: Reversed interval",
	"float-input": "TypeError: Only exact int or Fraction inputs are accepted",
	"invalid-taylor-degree": "ArithmeticError: Taylor degree must be a positive integer",
	"invalid-atan-domain": "ArithmeticError: Arctan series requires 0 < x < 1",
	"wrong-ratio-bound": "ArithmeticError: Proposed scalar upper bound 0.825 is not certified",
}


def require(condition, message):
	if not condition:
		raise ArithmeticError(message)


def file_hash(path):
	return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
	return json.loads(path.read_text(encoding="utf-8"))


def check_displays(value):
	count = 0
	if isinstance(value, dict):
		if "exact" in value:
			x = Fraction(value["exact"])
			lo = Fraction(Decimal(value["display_lower"]))
			hi = Fraction(Decimal(value["display_upper"]))
			require(lo <= x <= hi, "Stored directed display misses exact rational")
			count += 1
		if "outward_display" in value:
			lo = Fraction(value["lower"]["exact"])
			hi = Fraction(value["upper"]["exact"])
			require(Fraction(Decimal(value["outward_display"][0])) <= lo <= hi <= Fraction(Decimal(value["outward_display"][1])), "Stored outward interval display is unsafe")
		for item in value.values():
			count += check_displays(item)
	elif isinstance(value, list):
		count += sum(check_displays(item) for item in value)
	return count


def interval_regressions():
	I = certificate.Interval
	require(I(-3, 2) ** 2 == I(0, 9), "Even power crossing zero")
	require(I(-3, -2) ** 3 == I(-27, -8), "Odd negative power endpoints")
	require(1 / I(-3, -2) == I(Fraction(-1, 2), Fraction(-1, 3)), "Negative reciprocal")
	require(I(2, 3) / I(-2, -1) == I(-3, -1), "Negative denominator quotient")
	require(I(-2, 3) * I(-5, -4) == I(-15, 10), "Signed product")
	require(certificate.trig_point(Fraction(0), 1) == (I(0, 0), I(1, 1)), "Taylor zero")
	s, c = certificate.trig_point(Fraction(1, 7), 11)
	NegativeSin, NegativeCos = certificate.trig_point(Fraction(-1, 7), 11)
	require(NegativeSin == -s and NegativeCos == c, "Taylor parity with odd degree")
	for x in (Fraction(-1, 3), Fraction(1, 3), Fraction(-1000001, 1000000)):
		with localcontext() as context:
			context.prec = 2
			lower = certificate.directed_decimal(x, False)
			upper = certificate.directed_decimal(x, True)
			require(Fraction(Decimal(lower)) <= x <= Fraction(Decimal(upper)), "Signed directed display or context independence")
	return 10


def main():
	AuthorRoot = Path(sys.argv[1]).resolve()
	OutputPath = Path(sys.argv[2])
	CertificateHash = file_hash(AuthorRoot / "certificate.py")
	InputManifest = read_json(AuthorRoot / "inputs" / "manifest.json")
	for row in InputManifest["files"]:
		require(file_hash(AuthorRoot / row["copy"]) == row["sha256"], "Preserved input changed")
		require(file_hash(Path(row["source"])) == row["sha256"], "Frozen upstream input changed")
	StylePaths = []
	for path in sorted(AuthorRoot.glob("*.py")):
		source = path.read_text(encoding="utf-8")
		for line in source.splitlines():
			require(not re.match(r" +\S", line), "Space indentation in " + path.name)
		for node in ast.walk(ast.parse(source)):
			if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
				require(bool(re.fullmatch(r"[a-z_][a-z0-9_]*", node.name)), "Function name not snake_case")
		StylePaths.append(path.name)
	CertificateTree = ast.parse((AuthorRoot / "certificate.py").read_text())
	require(not any(isinstance(node, ast.Assert) for node in ast.walk(CertificateTree)), "assert guard in certificate")
	require(not any(isinstance(node, ast.Constant) and isinstance(node.value, float) for node in ast.walk(CertificateTree)), "Float literal in certificate")
	DirectImports = []
	for node in ast.walk(CertificateTree):
		if isinstance(node, ast.Import):
			DirectImports.extend(item.name for item in node.names)
		elif isinstance(node, ast.ImportFrom):
			DirectImports.append(node.module)
	require(set(DirectImports) <= sys.stdlib_module_names, "Non-stdlib direct certificate import")
	StandardRoot = Path(sysconfig.get_path("stdlib")).resolve()
	RunRows, IncompleteRuns, PositiveData, NegativeRows = [], [], [], []
	DisplayCount = 0
	for RunPath in sorted((AuthorRoot / "runs").iterdir()):
		if not RunPath.is_dir():
			continue
		RecordPath = RunPath / "record.json"
		if not RecordPath.is_file():
			IncompleteRuns.append(RunPath.name)
			require(RunPath.resolve() == Path.cwd().resolve(), "Uncompleted earlier run retained: " + RunPath.name)
			continue
		record = read_json(RecordPath)
		for name, ExpectedHash in record["files_sha256"].items():
			require(file_hash(RunPath / name) == ExpectedHash, "Recorded artifact hash mismatch: " + RunPath.name + "/" + name)
		for name, ExpectedHash in record["input_sha256"].items():
			require(file_hash(RunPath / name) == ExpectedHash, "Executed input changed")
		row = {"run": RunPath.name, "return_code": record["return_code"], "command": record["command"], "record_sha256": file_hash(RecordPath)}
		label = record["label"]
		if label.startswith("certificate-"):
			require(record["return_code"] == 0, "Positive certificate execution failed")
			require(file_hash(RunPath / "certificate.py") == CertificateHash, "Positive result belongs to different certificate bytes")
			data = read_json(RunPath / "results.json")
			require(len(data["checks"]) == 19 and all(item["exact_comparison_passed"] for item in data["checks"]), "Wrong positive obligation count or result")
			require(data["optimized"] == ("-O" in record["command"]), "Optimization metadata mismatch")
			DisplayCount += check_displays(data)
			ComparableData = {key: value for key, value in data.items() if key not in ("python", "optimized")}
			if PositiveData:
				require(ComparableData == PositiveData[0], "Exact results differ across modes or site initialization")
			PositiveData.append(ComparableData)
			imports = read_json(RunPath / "imports.json")
			ExternalModules = []
			for item in imports["modules"]:
				if item["file"]:
					ModulePath = Path(item["file"]).resolve()
					if not ModulePath.is_relative_to(StandardRoot) and not ModulePath.is_relative_to(AuthorRoot):
						ExternalModules.append(item)
			if "-S" in record["command"]:
				require(not ExternalModules, "External module in no-site certificate replay")
			row["external_modules_observed"] = ExternalModules
		elif label.startswith("negative-"):
			name = label[len("negative-"):].rsplit("-", 1)[0]
			require(name in ExpectedMessages, "Unexpected negative control")
			ErrorText = (RunPath / "stderr.txt").read_text()
			require(record["return_code"] == 1 and ErrorText.rstrip().endswith(ExpectedMessages[name]), "Negative control failed for the wrong reason: " + RunPath.name)
			require(not (RunPath / "results.json").exists(), "Negative control emitted a success result file")
			require((RunPath / "stdout.txt").read_bytes() == b"", "Unexpected negative stdout")
			require(file_hash(RunPath / "certificate.py") == CertificateHash, "Negative snapshot differs from delivered certificate")
			row["intended_guard_verified"] = ExpectedMessages[name]
			NegativeRows.append(row)
		elif label in ("supplied-normal", "supplied-optimized"):
			require(record["return_code"] == 0, "Unmodified supplied replay failed on this platform")
			require(file_hash(RunPath / "checks.py") == file_hash(AuthorRoot / "inputs" / "submitted" / "checks.py"), "Supplied script changed")
			data = read_json(RunPath / "results.json")
			require(data["confirmed_groups"] == 22 and len(data["checks"]) == 22 and all(item["confirmed"] for item in data["checks"]), "Supplied 22 checks not reached")
			OriginalRows = read_json(AuthorRoot / "inputs" / "submitted" / "results.json")["checks"]
			require([(item["name"], item["kind"]) for item in data["checks"]] == [(item["name"], item["kind"]) for item in OriginalRows], "Supplied check identity changed")
		elif label == "legacy-platform-diagnostics":
			require(record["return_code"] == 0, "Legacy diagnostics failed")
			data = read_json(RunPath / "observations.json")
			require(Fraction(data["old_root_lower"]) == certificate.OldRootBracket.lo and Fraction(data["old_root_upper"]) == certificate.OldRootBracket.hi, "Pinned root witness differs from actual extraction")
			require(Fraction(data["cot_x"]) == certificate.LegacyCotX, "Pinned cot input differs")
			require(certificate.Interval(*(Fraction(x) for x in data["cot_output_exact"])) == certificate.LegacyCotBox, "Pinned cot output differs from this platform's observation")
			row["supplied_miss_reproduced_here"] = data["supplied_miss_reproduced_here"]
		RunRows.append(row)
	for optimized in (False, True):
		for name in ExpectedMessages:
			require(any(row["run"].endswith("negative-" + name + ("-optimized" if optimized else "-normal")) and "-S" in row["command"] for row in NegativeRows), "Missing no-site negative control")
	require(len(PositiveData) >= 4, "Missing initial and no-site positive modes")
	output = {
		"status": "AUTHOR_EVIDENCE_VERIFIED_NOT_FINAL_REVIEW",
		"certificate_sha256": CertificateHash,
		"preserved_input_count": len(InputManifest["files"]),
		"positive_certificate_runs": len(PositiveData), "negative_rejections": len(NegativeRows),
		"rational_display_checks": DisplayCount, "finite_interval_regressions": interval_regressions(),
		"style_paths": StylePaths, "certificate_direct_imports": DirectImports,
		"runs": RunRows, "current_run_pending_receipt": IncompleteRuns,
		"limitations": ["Author self-verification only", "No full deep-sliver proof", "No complete INF theorem audit", "sys.modules is a post-execution inventory, not an import-event sandbox"],
	}
	OutputPath.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
	print(json.dumps({key: output[key] for key in ("status", "preserved_input_count", "positive_certificate_runs", "negative_rejections", "rational_display_checks", "finite_interval_regressions")}, indent=2))


if __name__ == "__main__":
	main()
