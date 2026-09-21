"""Separately labelled diagnostic continuation after supplied require failures."""
import json
import sys
from pathlib import Path

import checks


def main():
	AllRows = []
	OriginalRequire = checks.require

	def record_check(condition, name, kind, **details):
		passed = bool(condition)
		AllRows.append({"name": name, "kind": kind, "condition_true": passed, "details": details})
		if passed:
			OriginalRequire(condition, name, kind, **details)
		else:
			print("DIAGNOSTIC CONDITION FALSE:", name, file=sys.stderr)

	checks.require = record_check
	try:
		checks.main()
	finally:
		Path("continuation_observations.json").write_text(json.dumps({
			"scope": "Modified require hook, diagnostic continuation only; not an unmodified 22-check replay",
			"checks": AllRows,
		}, indent=2) + "\n", encoding="utf-8")
	if any(not row["condition_true"] for row in AllRows):
		raise SystemExit(1)


if __name__ == "__main__":
	main()
