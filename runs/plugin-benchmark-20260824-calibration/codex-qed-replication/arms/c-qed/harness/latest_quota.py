#!/usr/bin/env python3

import json
import pathlib
import sys


def main():
	sessions_root = pathlib.Path(sys.argv[1])
	latest_timestamp = ""
	latest_used_percent = -1

	if not sessions_root.exists():
		print(latest_used_percent)
		return

	for path in sessions_root.rglob("*.jsonl"):
		with path.open("r", encoding="utf-8") as handle:
			for line in handle:
				row = json.loads(line)
				payload = row.get("payload", {})
				if row.get("type") != "event_msg" or payload.get("type") != "token_count":
					continue
				timestamp = row.get("timestamp", "")
				primary = payload.get("rate_limits", {}).get("primary") or {}
				used_percent = primary.get("used_percent")
				if used_percent is not None and timestamp >= latest_timestamp:
					latest_timestamp = timestamp
					latest_used_percent = used_percent

	print(latest_used_percent)


if __name__ == "__main__":
	main()
