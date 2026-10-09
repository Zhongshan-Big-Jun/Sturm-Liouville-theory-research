#!/usr/bin/env python3
"""Restore losslessly packaged evidence without overwriting existing files."""

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import tempfile


def file_sha(PathValue):
	Hash = hashlib.sha256()
	with PathValue.open("rb") as Handle:
		for Block in iter(lambda: Handle.read(1024 * 1024), b""):
			Hash.update(Block)
	return Hash.hexdigest()


def contained_path(Root, Location):
	Relative = Path(Location)
	if(Relative.is_absolute() or ".." in Relative.parts):
		raise ValueError("invalid relative evidence path: " + Location)
	Target = (Root / Relative).resolve()
	if(not Target.is_relative_to(Root.resolve()) or Target == Root.resolve()):
		raise ValueError("evidence path escapes its root: " + Location)
	return Target


def restore_files(EvidenceRoot, TargetRoot, Mapping, Check=False, Only=()):
	if(Mapping.get("schema") != "lossless-large-evidence/v1"):
		raise ValueError("unsupported evidence packaging schema")
	Known = {Row["path"] for Row in Mapping["files"]}
	if(set(Only) - Known):
		raise ValueError("unknown evidence selection")
	Results, CheckedArchives = [], set()
	for Row in Mapping["files"]:
		if(Only and Row["path"] not in Only):
			continue
		Archive = contained_path(EvidenceRoot, Row["archive"])
		Target = contained_path(TargetRoot, Row["path"])
		if(Archive not in CheckedArchives):
			if(file_sha(Archive) != Row["archive_sha256"]):
				raise ValueError("compressed evidence identity mismatch")
			CheckedArchives.add(Archive)
		if(Target.exists()):
			if(not Target.is_file() or Target.stat().st_size != Row["original_bytes"] or file_sha(Target) != Row["original_sha256"]):
				raise FileExistsError("refusing to replace different existing evidence: " + str(Target))
			Results.append(dict(path=Row["path"], state="EXISTING_BYTES_MATCH"))
			continue
		if(Check):
			raise FileNotFoundError("restore the missing evidence first: " + str(Target))
		Target.parent.mkdir(parents=True, exist_ok=True)
		Hash, Size = hashlib.sha256(), 0
		with tempfile.NamedTemporaryFile(prefix=".restore-evidence-", dir=Target.parent, delete=False) as Handle:
			Temporary = Path(Handle.name)
			try:
				with gzip.open(Archive, "rb") as Source:
					for Block in iter(lambda: Source.read(1024 * 1024), b""):
						Size += len(Block)
						if(Size > Row["original_bytes"]):
							raise ValueError("decompressed evidence exceeds its recorded size")
						Hash.update(Block)
						Handle.write(Block)
				if(Size != Row["original_bytes"] or Hash.hexdigest() != Row["original_sha256"]):
					raise ValueError("decompressed evidence identity mismatch")
				Handle.flush()
				os.fsync(Handle.fileno())
			except Exception:
				Handle.close()
				Temporary.unlink()
				raise
		try:
			# Creating the hard link is atomic and fails if another writer creates Target.
			os.link(Temporary, Target)
		finally:
			Temporary.unlink()
		Results.append(dict(path=Row["path"], state="RESTORED_EXACT_BYTES"))
	return Results


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument("--check", action="store_true", help="check all selected original and compressed identities without writing")
	Parser.add_argument("--target-dir", type=Path, help="restore into a separate explicit directory instead of this evidence directory")
	Parser.add_argument("--only", action="append", default=[], help="select an exact relative original path; repeat for more than one")
	Arguments = Parser.parse_args()
	EvidenceRoot = Path(__file__).resolve().parent
	TargetRoot = (Arguments.target_dir or EvidenceRoot).resolve()
	Mapping = json.loads((EvidenceRoot / "large-evidence.json").read_text(encoding="utf-8"))
	Results = restore_files(EvidenceRoot, TargetRoot, Mapping, Arguments.check, Arguments.only)
	print(json.dumps(dict(files=len(Results), results=Results, scope="Exact byte restoration only; no Lean execution or review acceptance."), ensure_ascii=False))


if(__name__ == "__main__"):
	main()
