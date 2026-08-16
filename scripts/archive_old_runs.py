#!/usr/bin/env python3
"""Archive old solver runs and misc artifacts to keep the working tree lean.

Default mode is a dry run. Pass --apply to actually zip and remove.

Examples:
    py -3 scripts/archive_old_runs.py --days 90
    py -3 scripts/archive_old_runs.py --days 30 --apply
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[1]
RUNS_ROOT = REPO / "runs" / "rigorous-open-math-research"
MISC_ROOT = REPO / "misc"
ARCHIVE_ROOT = REPO / "archive"


def is_old(path: pathlib.Path, cutoff: dt.datetime) -> bool:
    mtime = dt.datetime.fromtimestamp(path.stat().st_mtime)
    return mtime < cutoff


def archive_run_dir(run_dir: pathlib.Path, archive_root: pathlib.Path, apply: bool, dry: bool) -> None:
    zip_path = archive_root / "runs" / f"{run_dir.name}.zip"
    if dry:
        print(f"would archive run: {run_dir.relative_to(REPO)} -> {zip_path.relative_to(REPO)}")
        return
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(run_dir.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(run_dir.parent).as_posix())
    # sanity: zip must contain at least one file
    with zipfile.ZipFile(zip_path) as zf:
        if len(zf.namelist()) == 0:
            print(f"FAIL: {zip_path} is empty; keeping {run_dir}")
            return
    import shutil

    shutil.rmtree(run_dir)
    print(f"archived run: {run_dir.relative_to(REPO)} -> {zip_path.relative_to(REPO)}")


def archive_misc_files(cutoff: dt.datetime, archive_root: pathlib.Path, apply: bool, dry: bool) -> None:
    old_files = [p for p in MISC_ROOT.rglob("*") if p.is_file() and is_old(p, cutoff)]
    if not old_files:
        print("no old misc files to archive")
        return
    zip_path = archive_root / "misc" / f"misc-old-{cutoff.strftime('%Y%m%d')}.zip"
    if dry:
        print(f"would archive {len(old_files)} old misc files -> {zip_path.relative_to(REPO)}")
        for p in old_files[:5]:
            print(f"  {p.relative_to(REPO)}")
        if len(old_files) > 5:
            print(f"  ... and {len(old_files) - 5} more")
        return
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in old_files:
            zf.write(p, p.relative_to(REPO).as_posix())
    for p in old_files:
        p.unlink()
    print(f"archived {len(old_files)} misc files -> {zip_path.relative_to(REPO)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=90, help="archive entries older than this many days")
    parser.add_argument("--apply", action="store_true", help="actually zip and remove (default is dry run)")
    args = parser.parse_args()

    cutoff = dt.datetime.now() - dt.timedelta(days=args.days)
    dry = not args.apply

    if RUNS_ROOT.is_dir():
        old_runs = [p for p in RUNS_ROOT.iterdir() if p.is_dir() and is_old(p, cutoff)]
        for run_dir in sorted(old_runs):
            archive_run_dir(run_dir, ARCHIVE_ROOT, args.apply, dry)
    else:
        print(f"note: {RUNS_ROOT.relative_to(REPO)} not found; skipping runs")

    if MISC_ROOT.is_dir():
        archive_misc_files(cutoff, ARCHIVE_ROOT, args.apply, dry)
    else:
        print(f"note: {MISC_ROOT.relative_to(REPO)} not found; skipping misc")

    if dry:
        print("\nDry run: no changes made. Re-run with --apply to execute.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
