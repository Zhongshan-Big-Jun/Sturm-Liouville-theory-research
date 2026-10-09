from __future__ import annotations

import json
from pathlib import Path
import sys
from unittest.mock import patch


Base = Path(r"F:\tools\lean-joint-20261008\plugin")
Frozen = Base / "source-freeze-v1"
sys.path.insert(0, str(Frozen / "plugins/lean-verify/scripts"))
import lean_develop as develop
from lean_runtime import LeanRuntime, sha256_file, source_snapshot, write_json
from lean_evidence import recheck_manifest


LEAN = r"C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
LAKE = r"C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe"
Destination = Base / "review-v1-race-reproduction"
if(Destination.exists()):
	raise SystemExit("retain prior reproduction; choose a fresh destination")
Destination.mkdir()


def arguments(Root, Output, Targets):
	return develop.make_parser().parse_args(["--project", str(Root), "--output", str(Output), "--lean", LEAN,
		"--lake", LAKE, "--direct", "--timeout", "60", "verify", "--targets", str(Targets)])


Root = Destination / "save/project"
Root.mkdir(parents=True)
(Root / "lean-toolchain").write_text("leanprover/lean4:v4.31.0\n", encoding="utf-8")
Helper = Root / "Helper.lean"
Helper.write_text("theorem helper (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
Candidate = Root.parent / "Candidate.lean"
Candidate.write_text("import Helper\ntheorem result (n : Nat) : n + 0 = n := helper n\n", encoding="utf-8")
Runtime = LeanRuntime(Root, Root.parent / "output", LEAN, LAKE, True)
Session = develop.DevelopSession(Runtime, 60, "cli")
try:
	Trial = Session.trial("Main.lean", Candidate)
	assert Trial["status"] == "candidate_checked", Trial
	Before = source_snapshot(Root, [Runtime.LogDir])
	Environment = Runtime.environment
	Events = []
	def change_dependency_during_environment_check():
		if(not Events):
			Helper.write_text("theorem helper (n : Nat) : n + 0 = n := by sorry\n", encoding="utf-8")
			Events.append({"event": "real dependency source changed during environment check", "source_sha256": sha256_file(Helper)})
		return Environment()
	with patch.object(Runtime, "environment", side_effect=change_dependency_during_environment_check):
		Saved = Session.save(Trial["receipt"])
	After = source_snapshot(Root, [Runtime.LogDir])
	assert Before != After and Saved["status"] == "saved", (Before, After, Saved)
	Targets = Root / "targets.json"
	write_json(Targets, {"targets": [{"id": "save-root", "file": "Main.lean", "declaration": "result", "expected_type": "∀ n : Nat, n + 0 = n"}]})
	Final = develop.verify_targets(arguments(Root, Root.parent / "strict", Targets))
	assert Final["exact_root_passed"] is False, Final
	SaveRace = {"events": Events, "trial": Trial, "saved": Saved, "source_before": Before, "source_after": After, "strict_after_save": Final}
	write_json(Destination / "save-race.json", SaveRace)
	print("F1 reproduced: stale dependency source accepted by save; actual strict verification rejected", flush=True)
finally:
	Session.close()

Root = Destination / "batch/project"
Root.mkdir(parents=True)
(Root / "lean-toolchain").write_text("leanprover/lean4:v4.31.0\n", encoding="utf-8")
First = Root / "First.lean"
First.write_text("theorem first (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
(Root / "Second.lean").write_text("theorem second (n : Nat) : n + 0 = n := Nat.add_zero n\n", encoding="utf-8")
Targets = Root / "targets.json"
write_json(Targets, {"targets": [{"id": "first", "file": "First.lean", "declaration": "first", "expected_type": "∀ n : Nat, n + 0 = n"}, {"id": "second", "file": "Second.lean", "declaration": "second", "expected_type": "∀ n : Nat, n + 0 = n"}]})
RealVerify = develop.verify_project
Calls = []
def change_first_before_second(Arguments):
	Calls.append(Arguments)
	if(len(Calls) == 2):
		First.write_text("theorem first : False := by sorry\n", encoding="utf-8")
	return RealVerify(Arguments)
with patch("lean_develop.verify_project", side_effect=change_first_before_second):
	Result = develop.verify_targets(arguments(Root, Root.parent / "output", Targets))
FinalChecks = [recheck_manifest(Item["manifest"]) for Item in Result["targets"]]
assert Result["exact_root_passed"] is True and [Check["exact_root_passed"] for Check in FinalChecks] == [False, True], (Result, FinalChecks)
write_json(Destination / "batch-race.json", {"batch": Result, "actual_terminal_checks": FinalChecks})
print("F2 reproduced: actual batch summary true while terminal manifest rechecks are [false, true]", flush=True)
write_json(Destination / "REPRODUCTION.json", {"scope": "deterministic editor mutations at real native Lean check boundaries, original v1 source", "source": str(Frozen), "save_race": str(Destination / "save-race.json"), "batch_race": str(Destination / "batch-race.json"), "actual_lean": LEAN, "actual_lake": LAKE})
