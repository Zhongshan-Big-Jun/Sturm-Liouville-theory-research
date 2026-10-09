#!/usr/bin/env python3
"""Portable development controls; synthetic feedback is not compiler evidence."""

from __future__ import annotations

import json
import io
import os
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lean_develop import DevelopSession, declarations_in_file, feedback_passed, load_targets, make_parser, project_file, search_sources, serve, tool_hashes, verify_targets, workflow_module
from lean_runtime import LeanRuntime, background_options, bound_input_changes, full_output, hash_bytes, hash_json, run, sha256_file, source_snapshot, write_json
from lean_feedback import ProtocolFailure


class DevelopControls(unittest.TestCase):
	def setUp(self):
		self.Temp = tempfile.TemporaryDirectory(prefix="develop-unit-", dir=os.environ.get("LEAN_VERIFY_TEST_TMPDIR"))
		self.Base = Path(self.Temp.name).resolve()
		self.Root = self.Base / "project"
		self.Root.mkdir()
		self.Output = self.Base / "output"
		self.Output.mkdir()
		self.Runtime = LeanRuntime(self.Root, self.Output, "missing-lean", "missing-lake", True)
		self.Runtime.Environment = {"sha256": "environment-fixture"}

	def tearDown(self):
		self.Temp.cleanup()

	def targets(self, Items):
		PathValue = self.Root / "targets.json"
		write_json(PathValue, {"targets": Items})
		return PathValue

	def test_empty_missing_duplicate_or_uncompared_targets_rejected(self):
		Target = {"id": "one", "file": "Main.lean", "declaration": "goal", "expected_type": "∀ n : Nat, n = n"}
		for Items in ([], [dict(Target, expected_type="")], [dict(Target, declaration="missing name")], [Target, Target]):
			with self.subTest(Items=Items), self.assertRaises(ValueError):
				load_targets(self.Root, self.targets(Items))
		with self.assertRaises(ValueError):
			load_targets(self.Root, self.targets([Target]), "absent")
		Targets, Digest = load_targets(self.Root, self.targets([Target]))
		self.assertEqual(Targets[0][1]["expected_type"], Target["expected_type"])
		self.assertEqual(Digest, sha256_file(self.Root / "targets.json"))

	def test_destination_cannot_escape_project_or_use_package_tree(self):
		for Name in ("../Escape.lean", ".lake/packages/pkg/Source.lean", "notes.md"):
			with self.assertRaises(ValueError):
				project_file(self.Root, Name)

	def test_empty_candidate_rejected_and_native_gbk_json_output(self):
		Candidate = self.Output / "Empty.lean"
		Candidate.write_text("\n  \n", encoding="utf-8")
		Session = DevelopSession(self.Runtime, Backend="cli")
		try:
			with self.assertRaisesRegex(ValueError, "nonempty"):
				Session.trial("Main.lean", Candidate)
		finally:
			Session.close()
		(self.Root / "Main.lean").write_text("-- ℝ unicode fixture\ntheorem result (n : Nat) : n = n := rfl\n", encoding="utf-8")
		Script = Path(__file__).resolve().parents[1] / "lean_develop.py"
		Command = [sys.executable, str(Script), "--project", str(self.Root), "--output", str(self.Output), "--direct", "--lean", "missing-lean", "--lake", "missing-lake", "search", "--query", "unicode"]
		Result = subprocess.run(Command, capture_output=True, env=dict(os.environ, PYTHONIOENCODING="gbk"), timeout=45)
		self.assertEqual(Result.returncode, 0, Result.stderr.decode("ascii", errors="replace"))
		Data = json.loads(Result.stdout.decode("ascii"))
		self.assertIn("ℝ", Data["matches"][0]["text"])

	def test_lsp_stale_errors_and_unavailable_are_incomplete(self):
		for Data in ({"status": "stale"}, {"status": "unavailable"}, {"status": "timeout"}, {"status": "complete", "diagnostics": [{"severity": 1}]}, {"status": "passed", "diagnostics": [{"severity": "error"}]}):
			self.assertFalse(feedback_passed(Data))
		self.assertTrue(feedback_passed({"status": "complete", "diagnostics": [{"severity": 2}]}))

	def test_import_protocol_failure_retains_incomplete_candidate_receipt(self):
		Candidate = self.Output / "Candidate.lean"
		Candidate.write_text("theorem result (n : Nat) : n = n := rfl\n", encoding="utf-8")
		Session = DevelopSession(self.Runtime, Backend="cli")
		with patch.object(Session, "prepare_imports", return_value=[{"status": "passed", "exit_code": 0}]), patch.object(Session, "import_identity", side_effect=ProtocolFailure("module prefix unavailable")):
			Result = Session.trial("Main.lean", Candidate)
		self.assertEqual(Result["status"], "candidate_incomplete")
		self.assertFalse(Result["exact_root_passed"])
		self.assertIn("module prefix", Result["feedback"]["reason"])
		self.assertTrue(Path(Result["receipt"]).is_file())
		Session.close()

	def test_bound_prose_and_target_list_changes_invalidate(self):
		Source = self.Root / "contract.md"
		Source.write_text("for every natural number", encoding="utf-8")
		Contract = {"input_file_hashes": {str(Source): sha256_file(Source)}}
		self.assertEqual(bound_input_changes(self.Root, Contract), [])
		Source.write_text("for one natural number", encoding="utf-8")
		self.assertTrue(bound_input_changes(self.Root, Contract))
		Source.unlink()
		self.assertTrue(bound_input_changes(self.Root, Contract))
		with self.assertRaises(ValueError):
			bound_input_changes(self.Root, {"input_file_hashes": {"path": "not-a-hash"}})

	def test_namespace_locations_and_cross_project_mathlib_search(self):
		Local = self.Root / "Main.lean"
		Local.write_text("namespace Example\nsection\n/- theorem fake : False -/\nlemma shared_result (n : Nat) : n = n := rfl\nend\nend Example\n", encoding="utf-8")
		Package = self.Root / ".lake/packages/mathlib"
		(Package / "Mathlib").mkdir(parents=True)
		(Package / "Mathlib/Fixture.lean").write_text("lemma shared_result (n : Nat) : n = n := rfl\n", encoding="utf-8")
		write_json(self.Root / "lake-manifest.json", {"packages": [{"name": "mathlib", "rev": "frozen-fixture"}]})
		Records = declarations_in_file(Local)
		self.assertEqual([Item["candidate_name"] for Item in Records], ["Example.shared_result"])
		self.assertEqual(Records[0]["declaration_line"], 4)
		for Engine in (None, __import__("shutil").which("rg")):
			with patch("lean_develop.shutil.which", return_value=Engine):
				Result = search_sources(self.Runtime, "shared_result", 10)
			self.assertEqual({Item["scope"] for Item in Result["matches"]}, {"project", "mathlib"})
			self.assertFalse(Result["exact_root_passed"])

	def receipt(self, Status="passed"):
		Candidate = self.Output / "Candidate.lean"
		Candidate.write_text("theorem result (n : Nat) : n = n := rfl\n", encoding="utf-8")
		Receipt = {"schema": "lean-development-trial/v1", "project_root": str(self.Root), "file": "Main.lean", "candidate": str(Candidate), "candidate_sha256": sha256_file(Candidate), "disk_sha256": None, "input_hashes": source_snapshot(self.Root), "environment_sha256": "environment-fixture", "import_artifacts": {}, "tool_hashes": tool_hashes(), "feedback": {"status": Status}, "search_paths": []}
		Receipt["receipt_sha256"] = hash_json(Receipt)
		ReceiptPath = self.Output / "trial.json"
		write_json(ReceiptPath, Receipt)
		return ReceiptPath

	def test_save_rejects_stale_buffer_destination_source_and_candidate(self):
		Session = DevelopSession(self.Runtime, Backend="cli")
		for Change in ("feedback", "destination", "source", "candidate"):
			with self.subTest(Change=Change):
				ReceiptPath = self.receipt("stale" if Change == "feedback" else "passed")
				if(Change == "destination"):
					(self.Root / "Main.lean").write_text("changed destination")
				elif(Change == "source"):
					(self.Root / "Dependency.lean").write_text("changed dependency")
				elif(Change == "candidate"):
					(self.Output / "Candidate.lean").write_text("changed candidate")
				with self.assertRaises(ValueError):
					Session.save(ReceiptPath)
				for Name in ("Main.lean", "Dependency.lean"):
					(self.Root / Name).unlink(missing_ok=True)
		Session.close()

	def test_completed_job_or_written_report_not_inferred_as_root(self):
		Target = {"id": "one", "file": "Main.lean", "declaration": "result", "expected_type": "∀ n : Nat, n = n"}
		Arguments = make_parser().parse_args(["--project", str(self.Root), "--output", str(self.Output), "verify", "--targets", str(self.targets([Target]))])
		Manifest = {"exact_root_passed": False, "machine": {"status": "passed"}, "root_closure": {"status": "target_mismatch"}, "semantic": {"status": "not_supplied"}}
		ManifestPath = self.Output / "negative.json"
		write_json(ManifestPath, Manifest)
		with patch("lean_develop.verify_project", return_value=(Manifest, ManifestPath)), patch("lean_develop.recheck_manifest", return_value={"exact_root_passed": False}):
			Result = verify_targets(Arguments)
		self.assertEqual(Result["status"], "incomplete")
		self.assertFalse(Result["exact_root_passed"])

	def test_workflow_adapter_reuses_actual_local_job_interface(self):
		Workflow = workflow_module()
		self.assertTrue(callable(Workflow.start_job))
		self.assertTrue(callable(Workflow.job_status))
		self.assertTrue(callable(Workflow.atomic_write))

	def test_windows_background_flags_and_actual_child_has_no_console(self):
		self.assertEqual(background_options("nt"), {"creationflags": 0x08000000})
		self.assertEqual(background_options("posix"), {})
		Workflow = workflow_module()
		self.assertEqual(Workflow.hidden_child_options("nt"), {"creationflags": 0x08000000})
		self.assertEqual(Workflow.hidden_child_options("posix"), {})
		if(os.name == "nt"):
			Result = run([sys.executable, "-c", "import ctypes; print(ctypes.windll.kernel32.GetConsoleWindow())"], self.Root, log_dir=self.Output)
			self.assertEqual(Result["status"], "passed", Result)
			self.assertEqual(full_output(Result).strip(), "0")

	def test_warm_server_keeps_failed_requests_incomplete_and_continues(self):
		Session = DevelopSession(self.Runtime, Backend="cli")
		Output = io.StringIO()
		Requests = 'not JSON\n{"action":"unknown"}\n{"action":"restart"}\n{"action":"close"}\n'
		with patch("lean_develop.sys.stdin", io.StringIO(Requests)), patch("lean_develop.sys.stdout", Output):
			self.assertEqual(serve(Session), 0)
		Responses = [json.loads(Line) for Line in Output.getvalue().splitlines()]
		self.assertEqual([Item["status"] for Item in Responses], ["incomplete", "incomplete", "restarted", "closed"])
		self.assertTrue(all(Item["exact_root_passed"] is False for Item in Responses))
		Session.close()

	def test_loaded_python_identity_rejects_real_source_change_until_new_process(self):
		ToolSource = self.Output / "loaded-tool-fixture.py"
		ToolSource.write_text("VERSION = 1\n", encoding="utf-8")
		Loaded = {ToolSource.name: sha256_file(ToolSource)}
		with patch("lean_develop.LOADED_TOOL_HASHES", Loaded), patch("lean_develop.tool_hashes", side_effect=lambda: {ToolSource.name: sha256_file(ToolSource)}):
			Session = DevelopSession(self.Runtime, Backend="cli")
			ToolSource.write_text("VERSION = 2\n", encoding="utf-8")
			with self.assertRaisesRegex(ValueError, "new Python process"):
				Session.trial("Main.lean", "not-read-before-identity-check")
			with self.assertRaisesRegex(ValueError, "new Python process"):
				DevelopSession(self.Runtime, Backend="cli")
			Output = io.StringIO()
			with patch("lean_develop.sys.stdin", io.StringIO('{"action":"restart"}\n')), patch("lean_develop.sys.stdout", Output):
				serve(Session)
			Result = json.loads(Output.getvalue())
			self.assertEqual(Result["status"], "incomplete")
			self.assertFalse(Result["exact_root_passed"])
			Session.close()


if(__name__ == "__main__"):
	unittest.main()
