#!/usr/bin/env python3

import re
import sys
from pathlib import Path


def is_within(PathValue, RootValue):
	try:
		PathValue.relative_to(RootValue)
		return True
	except ValueError:
		return False


def main():
	if len(sys.argv) != 3:
		raise SystemExit("usage: qed-inline-prompt.py PROMPT WORK_ROOT")

	PromptText = sys.argv[1]
	WorkRoot = Path(sys.argv[2]).resolve()
	RawPaths = re.findall(r"/mnt/[A-Za-z0-9_./+-]+", PromptText)
	SeenPaths = set()
	Sections = []
	TotalBytes = 0

	for RawPath in RawPaths:
		CleanPath = RawPath.rstrip(" .,:;)]}`'\"")
		CandidatePath = Path(CleanPath)
		try:
			ResolvedPath = CandidatePath.resolve(strict=True)
		except (FileNotFoundError, OSError):
			continue
		if ResolvedPath in SeenPaths or not ResolvedPath.is_file():
			continue
		if not is_within(ResolvedPath, WorkRoot):
			continue
		FileBytes = ResolvedPath.read_bytes()
		if len(FileBytes) > 300000 or TotalBytes + len(FileBytes) > 900000:
			continue
		SeenPaths.add(ResolvedPath)
		TotalBytes += len(FileBytes)
		FileText = FileBytes.decode("utf-8", errors="replace")
		RelativePath = ResolvedPath.relative_to(WorkRoot)
		Sections.append(
			f"\n--- BEGIN FILE: {RelativePath.as_posix()} ---\n"
			f"{FileText}\n"
			f"--- END FILE: {RelativePath.as_posix()} ---\n"
		)

	AdapterText = """

# Offline adapter contract

All model-side tools are disabled for this blind benchmark. The exact contents of every
existing input file named above and located inside the isolated work root are appended below.
Use those contents directly. Do not attempt tool calls and do not report a tool-access blocker.
Return the requested artifact as the final response. The QED harness will save that response at
the requested output path. Preserve the requested output format, including YAML or Markdown.
"""
	sys.stdout.write(PromptText + AdapterText + "".join(Sections))


if __name__ == "__main__":
	main()
