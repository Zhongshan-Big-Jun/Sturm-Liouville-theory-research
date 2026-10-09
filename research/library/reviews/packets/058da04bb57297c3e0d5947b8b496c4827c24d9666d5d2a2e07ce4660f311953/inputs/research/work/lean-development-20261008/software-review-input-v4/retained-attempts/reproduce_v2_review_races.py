from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
from unittest.mock import patch


Base = Path(r"F:\tools\lean-joint-20261008\plugin")
Frozen = Base / "source-freeze-v2"
Destination = Base / "review-v2-race-reproduction"
if(Destination.exists()):
	raise SystemExit("retain prior reproduction; choose a fresh destination")
Replica = Destination / "replica"
shutil.copytree(Frozen, Replica, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
sys.path.insert(0, str(Replica / "plugins/lean-verify/scripts"))
import lean_develop as develop
from lean_runtime import LeanRuntime, source_snapshot, write_json
from lean_evidence import recheck_manifest


LEAN = r"C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
LAKE = r"C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe"


def project(Name):
	Root = Destination / Name / "project"
	Root.mkdir(parents=True)
	(Root / "Src").mkdir()
	(Root / "lean-toolchain").write_text("leanprover/lean4:v4.31.0\n", encoding="utf-8")
	return Root


def arguments(Root, Output, Targets):
	return develop.make_parser().parse_args(["--project", str(Root), "--output", str(Output), "--lean", LEAN,
		"--lake", LAKE, "--direct", "--timeout", "60", "verify", "--targets", str(Targets)])


Root = project("save-output-root")
Helper = Root / "Src/Helper.lean"
Helper.write_text("theorem helper (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
Candidate = Root.parent / "Candidate.lean"
Candidate.write_text("import Src.Helper\ntheorem result (n : Nat) : n + 0 = n := helper n\n", encoding="utf-8")
Session = develop.DevelopSession(LeanRuntime(Root, Root, LEAN, LAKE, True), 60, "cli")
try:
	Trial = Session.trial("Src/Main.lean", Candidate)
	assert Trial["status"] == "candidate_checked", Trial
	Helper.write_text("theorem helper (n : Nat) : n + 0 = n := by sorry\n", encoding="utf-8")
	Saved = Session.save(Trial["receipt"])
	assert Saved["status"] == "saved", Saved
	write_json(Destination / "overlap-save.json", {"trial": Trial, "saved_after_nested_source_changed": Saved, "observed_snapshot": source_snapshot(Root, [Root])})
	print("V2-OUTPUT-COVERAGE save reproduced: nested source changed, output=root snapshot omitted it, save returned saved", flush=True)
finally:
	Session.close()

Root = project("batch-output-root")
First = Root / "Src/First.lean"
First.write_text("theorem first (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
(Root / "Src/Second.lean").write_text("theorem second (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
Targets = Root / "targets.json"
write_json(Targets, {"targets": [{"id": "first", "file": "Src/First.lean", "declaration": "first", "expected_type": "∀ n : Nat, n + 0 = n"}, {"id": "second", "file": "Src/Second.lean", "declaration": "second", "expected_type": "∀ n : Nat, n + 0 = n"}]})
Calls = []
def actual_recheck_then_nested_source_edit(PathValue):
	Result = recheck_manifest(PathValue)
	Calls.append(Result)
	if(len(Calls) == 2):
		First.write_text("theorem first : False := by sorry\n", encoding="utf-8")
	return Result
with patch("lean_develop.recheck_manifest", side_effect=actual_recheck_then_nested_source_edit):
	Batch = develop.verify_targets(arguments(Root, Root, Targets))
Terminal = [recheck_manifest(Item["manifest"]) for Item in Batch["targets"]]
assert Batch["exact_root_passed"] is True and all(not Item["exact_root_passed"] for Item in Terminal), (Batch, Terminal)
write_json(Destination / "overlap-batch.json", {"batch": Batch, "actual_final_checks": Terminal})
print("V2-OUTPUT-COVERAGE batch reproduced: nested First changed after true rechecks; batch true, post rechecks false", flush=True)

ToolResults = []
for ToolName in ("lake_build_guard.py", "run_manifest.schema.json"):
	Root = project("tool-" + ToolName.replace(".", "-"))
	(Root / "Src/First.lean").write_text("theorem first (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
	(Root / "Src/Second.lean").write_text("theorem second (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
	Targets = Root / "targets.json"
	write_json(Targets, {"targets": [{"id": "first", "file": "Src/First.lean", "declaration": "first", "expected_type": "∀ n : Nat, n + 0 = n"}, {"id": "second", "file": "Src/Second.lean", "declaration": "second", "expected_type": "∀ n : Nat, n + 0 = n"}]})
	ToolPath = Path(develop.__file__).parent / ToolName
	RawTool = ToolPath.read_bytes()
	Calls = []
	def actual_recheck_then_tool_edit(PathValue):
		Result = recheck_manifest(PathValue)
		Calls.append(Result)
		if(len(Calls) == 2):
			ToolPath.write_bytes(RawTool + b"\n")
		return Result
	try:
		with patch("lean_develop.recheck_manifest", side_effect=actual_recheck_then_tool_edit):
			Batch = develop.verify_targets(arguments(Root, Root.parent / "output", Targets))
		Terminal = [recheck_manifest(Item["manifest"]) for Item in Batch["targets"]]
		assert Batch["exact_root_passed"] is True and all(not Item["exact_root_passed"] for Item in Terminal), (Batch, Terminal)
		Item = {"tool": ToolName, "batch": Batch, "actual_final_checks": Terminal}
		ToolResults.append(Item)
		write_json(Destination / ("tool-" + ToolName + ".json"), Item)
		print("V2-TOOLS-COVERAGE reproduced for " + ToolName + ": batch true, actual final rechecks stale tool", flush=True)
	finally:
		ToolPath.write_bytes(RawTool)
write_json(Destination / "REPRODUCTION.json", {"scope": "original v2 replica, real native Lean checks; frozen v1/v2 never edited", "original_source": str(Frozen), "replica": str(Replica), "actual_lean": LEAN, "actual_lake": LAKE, "cases": ["output=root save", "output=root batch", "guard late change", "schema late change"]})
