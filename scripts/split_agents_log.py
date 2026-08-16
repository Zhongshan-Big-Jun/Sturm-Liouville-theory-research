#!/usr/bin/env python3
"""Move the '## 对话记录' section of AGENTS.md into a separate archive file.

Keeps the workspace instruction file small while preserving the full session
log in the repository. Run again after AGENTS.md grows:

    py -3 scripts/split_agents_log.py --agents AGENTS.md --archive state/AGENTS_SESSION_LOG.md
"""

from __future__ import annotations

import argparse
import pathlib
import sys

MARKER = "## 对话记录"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agents", default="AGENTS.md", help="path to AGENTS.md")
    parser.add_argument(
        "--archive",
        default="state/AGENTS_SESSION_LOG.md",
        help="where to store the extracted dialogue log",
    )
    args = parser.parse_args()

    agents_path = pathlib.Path(args.agents)
    archive_path = pathlib.Path(args.archive)
    if not agents_path.is_file():
        print(f"FAIL: {agents_path} does not exist")
        return 1

    text = agents_path.read_text(encoding="utf-8")
    idx = text.find("\n" + MARKER)
    if idx == -1:
        idx = text.find(MARKER)
    if idx == -1:
        print(f"FAIL: marker '{MARKER}' not found in {agents_path}")
        return 1

    head = text[:idx].rstrip() + "\n"
    log = text[idx:]
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with open(archive_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(log)
    with open(agents_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(head)

    print(
        f"OK: moved dialogue log ({len(log.splitlines())} lines, "
        f"{len(log.encode('utf-8'))} bytes) to {archive_path}"
    )
    print(f"AGENTS.md is now {len(head.splitlines())} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
