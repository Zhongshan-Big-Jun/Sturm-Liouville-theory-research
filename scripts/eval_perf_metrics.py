#!/usr/bin/env python3
"""Collect performance metrics for the A6 plugin A/B experiment.

Usage:
  python3 scripts/eval_perf_metrics.py \
      --name baseline --session 97ba72f7-f850-4df8-a47f-ff87d74d97a3 \
      --run "runs/plugin-perf-eval/R-20260822T000000Z-a6-baseline"
  python3 scripts/eval_perf_metrics.py \
      --name reuse --session c13dd1f0-0873-4e9e-8c47-3f4be259183d \
      --run "runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse"

The script reads DSH session statistics from the local session cache and the
raw session log, plus the agent-written performance_log.md and run artifacts.
It prints a compact table and writes metrics.json next to the run root.
"""

import argparse
import json
import os
import subprocess
from pathlib import Path

DSH_HOME = Path(os.environ.get("DSH_HOME", "/mnt/c/Users/HuangZY/.dsh"))
SESSION_DIRS = [
    DSH_HOME / "sessions" / "--F-LaTeX-BVE~0020research--",
]
CACHE = DSH_HOME / "storages" / "session_projcache.json"
PROJECT_ROOT = Path("/mnt/f/LaTeX/BVE research")


def load_cache():
    if not CACHE.exists():
        return {}
    with open(CACHE, encoding="utf-8") as f:
        return json.load(f)


def session_stats(session_id):
    data = load_cache()
    rec = data.get("tables", {}).get("sessions", {}).get(session_id, {})
    rows = rec.get("rows", {})
    stats = rows.get("sessionStats", {}).get("val") or {}
    tokens = rows.get("tokenUsage", {}).get("val") or {}
    title = rows.get("title", {}).get("val")
    return {"title": title, "stats": stats, "tokens": tokens}


def find_session_log(session_id):
    for base in SESSION_DIRS:
        p = base / session_id / "session.jsonl.zstd"
        if p.exists():
            return p
    return None


def count_session_events(session_id):
    """Count raw events from the zstd JSONL session file using zstd CLI."""
    path = find_session_log(session_id)
    counts = {"assistant_messages": 0, "tool_calls": 0, "tool_results": 0,
              "user_messages": 0, "steps": 0, "turns": 0}
    if path is None:
        return counts
    proc = subprocess.Popen(["zstd", "-dc", str(path)], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)
    import json as j
    for raw in proc.stdout:
        try:
            obj = j.loads(raw.decode("utf-8", "replace"))
        except ValueError:
            continue
        typ = obj.get("type")
        if typ == "assistant/message":
            counts["assistant_messages"] += 1
        elif typ == "tool/call":
            counts["tool_calls"] += 1
        elif typ == "tool/result":
            counts["tool_results"] += 1
        elif typ == "user/message":
            counts["user_messages"] += 1
        elif typ == "step/start":
            counts["steps"] += 1
        elif typ == "turn/start":
            counts["turns"] += 1
    proc.stdout.close()
    return counts


def read_performance_log(run_path):
    p = Path(PROJECT_ROOT) / run_path / "performance_log.md"
    if not p.exists():
        return {"exists": False}
    text = p.read_text(encoding="utf-8", errors="replace")
    return {
        "exists": True,
        "bytes": len(text.encode("utf-8")),
        "reuse_lines": text.count("REUSE:"),
        "reuse_miss_lines": text.count("REUSE_MISS:"),
        "lines": text.count("\n") + 1,
    }


def artifact_summary(run_path):
    root = Path(PROJECT_ROOT) / run_path
    if not root.exists():
        return {"exists": False, "files": []}
    files = []
    for f in sorted(root.rglob("*")):
        if f.is_file():
            files.append({"path": str(f.relative_to(root)), "bytes": f.stat().st_size})
    return {"exists": True, "files": files}


def aggregate(session_id, run_path, name):
    stats = session_stats(session_id)
    events = count_session_events(session_id)
    perf = read_performance_log(run_path)
    arts = artifact_summary(run_path)
    total_tokens = stats["tokens"].get("totals", {})
    s = stats["stats"]
    return {
        "name": name,
        "session_id": session_id,
        "run_path": run_path,
        "title": stats["title"],
        "session": {
            "turns": s.get("turns"),
            "steps": s.get("steps"),
            "llmMs": s.get("llmMs"),
            "toolMs": s.get("toolMs"),
            "decodeTokens": s.get("decodeTokens"),
        },
        "tokens": total_tokens,
        "events": events,
        "performance_log": perf,
        "artifacts": arts,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--session", required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    data = aggregate(args.session, args.run, args.name)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    out_path = args.out
    if out_path is None:
        out_path = str(Path(PROJECT_ROOT) / args.run / "metrics.json")
    Path(out_path).write_text(json.dumps(data, ensure_ascii=False, indent=2),
                              encoding="utf-8")


if __name__ == "__main__":
    main()
