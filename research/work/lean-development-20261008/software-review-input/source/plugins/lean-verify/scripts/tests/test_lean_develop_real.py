#!/usr/bin/env python3
"""Opt-in actual compiler integration for the same generic development entrance."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import subprocess
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lean_develop import DevelopSession, make_parser, start_verification, verification_status, verify_targets
from lean_evidence import recheck_manifest
from lean_runtime import LeanRuntime, background_options, sha256_file, write_json

LEAN = os.environ.get("LEAN_VERIFY_REAL_LEAN")
LAKE = os.environ.get("LEAN_VERIFY_REAL_LAKE", "lake")


@unittest.skipUnless(LEAN, "set LEAN_VERIFY_REAL_LEAN for actual compiler integration")
class RealDevelopControls(unittest.TestCase):
	@classmethod
	def setUpClass(Class):
		Class.Temp = tempfile.TemporaryDirectory(prefix="develop-real-", dir=os.environ.get("LEAN_VERIFY_TEST_TMPDIR"))
		Class.Base = Path(Class.Temp.name).resolve()
		Class.Results = []
		Class.Counter = 0

	@classmethod
	def tearDownClass(Class):
		Output = os.environ.get("LEAN_DEVELOP_TEST_REPORT")
		if(Output):
			write_json(Output, {"scope": "generic actual Lean development fixture; no SL or full Mathlib build", "results": Class.Results})
		if(os.environ.get("LEAN_VERIFY_KEEP_TEST_ARTIFACTS")):
			Class.Temp._finalizer.detach()
		else:
			Class.Temp.cleanup()

	def project(self):
		type(self).Counter += 1
		Base = self.Base / str(self.Counter)
		Root = Base / "project"
		Root.mkdir(parents=True)
		(Root / "lean-toolchain").write_text("leanprover/lean4:v4.31.0\n", encoding="utf-8")
		Output = Base / "output"
		Runtime = LeanRuntime(Root, Output, LEAN, LAKE, True)
		self.assertIn("4.31.0", Runtime.environment()["lean_version"])
		return Root, Output, Runtime

	def arguments(self, Root, Output, Targets, Action="verify", Extra=()):
		return make_parser().parse_args(["--project", str(Root), "--output", str(Output), "--lean", LEAN, "--lake", LAKE, "--direct", "--timeout", "60", Action, "--targets", str(Targets), *Extra])

	def target_list(self, Root, Expected="∀ n : Nat, n + 0 = n", Declaration="Generic.result"):
		PathValue = Root / "targets.json"
		write_json(PathValue, {"targets": [{"id": "natural-addition", "file": "Main.lean", "declaration": Declaration, "expected_type": Expected}]})
		return PathValue

	def test_candidate_failure_revision_save_new_target_and_old_entry(self):
		Root, Output, Runtime = self.project()
		Candidate = Root.parent / "Candidate.lean"
		Candidate.write_text("namespace Generic\ntheorem result (n : Nat) : n + 0 = n := by\n  exact Nat.zero_add n\nend Generic\n", encoding="utf-8")
		Session = DevelopSession(Runtime, 60, "cli")
		try:
			Probe = Session.probe(["Nat.add_zero"], [])
			self.assertEqual(Probe["status"], "checked", Probe)
			self.assertIn("Nat", Probe["declarations"][0]["actual_type"])
			Bad = Session.trial("Main.lean", Candidate)
			# Nat.zero_add has a different syntactic expression but Lean may reduce both.
			if(Bad["status"] == "candidate_checked"):
				Candidate.write_text("namespace Generic\ntheorem result (n : Nat) : n + 0 = n := by\n  exact False.elim (by contradiction)\nend Generic\n", encoding="utf-8")
				Bad = Session.trial("Main.lean", Candidate)
			self.assertEqual(Bad["status"], "candidate_incomplete", Bad)
			with self.assertRaises(ValueError):
				Session.save(Bad["receipt"])
			Candidate.write_text("namespace Generic\ntheorem result (n : Nat) : n + 0 = n := by\n  exact Nat.add_zero n\nend Generic\n", encoding="utf-8")
			Good = Session.trial("Main.lean", Candidate)
			self.assertEqual(Good["status"], "candidate_checked", Good)
			Saved = Session.save(Good["receipt"])
			self.assertFalse(Saved["exact_root_passed"])
			self.assertEqual((Root / "Main.lean").read_bytes(), Candidate.read_bytes())
		finally:
			Session.close()
		Targets = self.target_list(Root)
		Result = verify_targets(self.arguments(Root, Output, Targets))
		self.assertTrue(Result["exact_root_passed"], Result)
		Manifest = Result["targets"][0]["manifest"]
		self.assertTrue(recheck_manifest(Manifest)["exact_root_passed"])
		# The existing entry still works, without this tool's orchestration.
		from verify_lean_project import make_parser as old_parser, verify_project
		Arguments = old_parser().parse_args(["--project", str(Root), "--output", str(Output / "old-entry"), "--lean", LEAN, "--lake", LAKE, "--direct", "--target-file", "Main.lean", "--declaration", "Generic.result", "--expected-type", "∀ n : Nat, n + 0 = n", "--strict-exit"])
		Old, _ = verify_project(Arguments)
		self.assertTrue(Old["exact_root_passed"], Old)
		write_json(Targets, {"targets": [{"id": "natural-addition", "file": "Main.lean", "declaration": "Generic.result", "expected_type": "∀ n : Nat, 0 + n = n"}]})
		Stale = recheck_manifest(Manifest)
		self.assertFalse(Stale["exact_root_passed"])
		self.assertTrue(any("contract_input:" in Reason for Reason in Stale["reasons"]))
		self.Results.append({"test": self.id(), "probe": Probe, "failed_trial": Bad, "revised_trial": Good, "save": Saved, "verification": Result, "contract_changed": Stale})

	def test_wrong_extra_hypotheses_missing_roots_and_transitive_assumptions(self):
		Root, Output, _ = self.project()
		Cases = [
			("theorem wrong (n : Nat) (h : n = 0) : n + 0 = n := Nat.add_zero n\n", "wrong", "∀ n : Nat, n + 0 = n"),
			("theorem leaf (n : Nat) : n + 0 = n := Nat.add_zero n\n", "missing_root", "∀ n : Nat, n + 0 = n"),
			("theorem unproved : False := by sorry\ndef hidden : False := unproved\ntheorem wrong (n : Nat) : n + 0 = n := False.elim hidden\n", "wrong", "∀ n : Nat, n + 0 = n"),
			("axiom extra : False\ndef hidden : False := extra\ntheorem wrong (n : Nat) : n + 0 = n := False.elim hidden\n", "wrong", "∀ n : Nat, n + 0 = n"),
			("def model : Prop := True\ntheorem wrong : model := True.intro\n", "wrong", "∀ n : Nat, n + 0 = n")]
		for Index, (Code, Declaration, Expected) in enumerate(Cases):
			with self.subTest(Index=Index):
				(Root / "Main.lean").write_text(Code, encoding="utf-8")
				Targets = self.target_list(Root, Expected, Declaration)
				Result = verify_targets(self.arguments(Root, Output / str(Index), Targets))
				self.assertFalse(Result["exact_root_passed"], Result)
				self.Results.append({"test": self.id(), "case": Index, "verification": Result})

	def test_actual_buffer_freshness_and_unavailable_compiler(self):
		Root, Output, Runtime = self.project()
		Candidate = Root.parent / "Candidate.lean"
		Candidate.write_text("theorem result (n : Nat) : n = n := rfl\n", encoding="utf-8")
		Session = DevelopSession(Runtime, 60, "cli")
		try:
			Trial = Session.trial("Main.lean", Candidate)
			self.assertEqual(Trial["status"], "candidate_checked", Trial)
			(Root / "Dependency.lean").write_text("def changed : Nat := 1\n", encoding="utf-8")
			with self.assertRaisesRegex(ValueError, "source or configuration changed"):
				Session.save(Trial["receipt"])
		finally:
			Session.close()
		Missing = DevelopSession(LeanRuntime(Root, Output / "missing", str(Root / "missing-lean"), str(Root / "missing-lake"), True), 1, "cli")
		try:
			Trial = Missing.trial("Main.lean", Candidate)
			self.assertEqual(Trial["status"], "candidate_incomplete")
			self.assertFalse(Trial["exact_root_passed"])
		finally:
			Missing.close()
		self.Results.append({"test": self.id(), "unavailable": Trial})

	def test_real_workflow_resume_and_duplicate_dispatch(self):
		Root, Output, _ = self.project()
		(Root / "Main.lean").write_text("namespace Generic\ntheorem result (n : Nat) : n + 0 = n := Nat.add_zero n\nend Generic\n", encoding="utf-8")
		Targets = self.target_list(Root)
		Arguments = self.arguments(Root, Output, Targets, "start", ("--job-id", "generic-root", "--job-timeout", "120"))
		Started = start_verification(Arguments)
		Duplicate = start_verification(Arguments)
		self.assertTrue(Started["dispatched"])
		self.assertFalse(Duplicate["dispatched"])
		StatusArgs = make_parser().parse_args(["--project", str(Root), "--output", str(Output), "status", "--job-id", "generic-root"])
		Deadline = time.monotonic() + 150
		while(time.monotonic() < Deadline):
			Status = verification_status(StatusArgs)
			if(Status["state"] not in ("STARTING", "RUNNING")):
				break
			time.sleep(0.2)
		self.assertEqual(Status["state"], "SUCCEEDED", Status)
		self.assertTrue(Status["exact_root_passed"], Status)
		self.Results.append({"test": self.id(), "dispatch": Started, "duplicate": Duplicate, "resumed": Status})

	def test_actual_warm_entrance_and_target_extension(self):
		Root, Output, _ = self.project()
		(Root / "Pair/Left").mkdir(parents=True)
		(Root / "Pair/Right").mkdir(parents=True)
		(Root / "Pair/Left/One.lean").write_text("namespace Generic\ntheorem helper (n : Nat) : n + 0 = n := Nat.add_zero n\nend Generic\n", encoding="utf-8")
		(Root / "Pair/Right/Two.lean").write_text("namespace Generic\ntheorem second_helper (n : Nat) : n = n := rfl\nend Generic\n", encoding="utf-8")
		Candidate = Root.parent / "Candidate.lean"
		Code = "import Pair.Left.One\nimport Pair.Right.Two\nnamespace Generic\ntheorem result (n : Nat) : n + 0 = n := (helper n).trans (second_helper n)\nend Generic\n"
		Candidate.write_text(Code.replace("(helper n)", "(Nat.zero_add n)"), encoding="utf-8")
		Script = Path(__file__).resolve().parents[1] / "lean_develop.py"
		ErrorPath = Root.parent / "serve.stderr.log"
		Responses = []
		with ErrorPath.open("wb") as ErrorLog:
			Process = subprocess.Popen([sys.executable, str(Script), "--project", str(Root), "--output", str(Output), "--lean", LEAN, "--lake", LAKE, "--direct", "--timeout", "60", "serve", "--backend", "cli"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=ErrorLog, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="gbk"), **background_options())
			def request(Data):
				Process.stdin.write(json.dumps(Data) + "\n")
				Process.stdin.flush()
				Line = Process.stdout.readline()
				self.assertTrue(Line, ErrorPath.read_text(encoding="utf-8", errors="replace"))
				Response = json.loads(Line)
				Responses.append(Response)
				return Response
			try:
				Bad = request({"action": "trial", "file": "Main.lean", "candidate": str(Candidate)})
				self.assertEqual(Bad["status"], "candidate_incomplete", Bad)
				Candidate.write_text(Code, encoding="utf-8")
				Good = request({"action": "trial", "file": "Main.lean", "candidate": str(Candidate)})
				self.assertEqual(Good["status"], "candidate_checked", Good)
				Receipt = json.loads(Path(Good["receipt"]).read_text(encoding="utf-8"))
				self.assertTrue(any(Item.get("kind") == "development_import_cache" for Item in Receipt["preparation_commands"]))
				self.assertEqual(request({"action": "save", "receipt": Good["receipt"]})["status"], "saved")
				request({"action": "close"})
				self.assertEqual(Process.wait(timeout=10), 0)
			finally:
				if(Process.poll() is None):
					Process.kill()
					Process.wait(timeout=10)
				Process.stdin.close()
				Process.stdout.close()
		Targets = self.target_list(Root)
		First = verify_targets(self.arguments(Root, Output / "first-root", Targets))
		self.assertTrue(First["exact_root_passed"], First)
		Candidate.write_text(Code + "namespace Generic\ntheorem extended (n : Nat) : n + 0 + 0 = n := by\n  exact (result (n + 0)).trans (result n)\nend Generic\n", encoding="utf-8")
		Session = DevelopSession(LeanRuntime(Root, Output / "extension", LEAN, LAKE, True), 60, "cli")
		try:
			Extended = Session.trial("Main.lean", Candidate)
			self.assertEqual(Extended["status"], "candidate_checked", Extended)
			Session.save(Extended["receipt"])
		finally:
			Session.close()
		ListData = json.loads(Targets.read_text(encoding="utf-8"))
		ListData["targets"].append({"id": "addition-composition", "file": "Main.lean", "declaration": "Generic.extended", "expected_type": "∀ n : Nat, n + 0 + 0 = n"})
		write_json(Targets, ListData)
		Expanded = verify_targets(self.arguments(Root, Output / "two-roots", Targets))
		self.assertTrue(Expanded["exact_root_passed"], Expanded)
		self.assertEqual(len(Expanded["targets"]), 2)
		self.Results.append({"test": self.id(), "warm_responses": Responses, "first_root": First, "extension_trial": Extended, "expanded_targets": Expanded})


if(__name__ == "__main__"):
	unittest.main()
