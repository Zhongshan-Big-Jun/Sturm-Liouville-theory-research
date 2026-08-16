# Archive policy for runs/ and misc/

Long-running research projects accumulate run roots and throwaway artifacts.
Keep the working tree navigable without deleting history.

## Policy

- `runs/rigorous-open-math-research/<RUN_ID>/` directories older than the
  configured cutoff are zipped into `archive/runs/<RUN_ID>.zip` and removed
  from the live tree.
- `misc/` files older than the cutoff are zipped into
  `archive/misc/misc-old-<YYYYMMDD>.zip` and removed.
- Default cutoff is 90 days. Adjust with `--days`.
- The script is **dry-run by default**; pass `--apply` to execute.

## Usage

```text
py -3 scripts/archive_old_runs.py --days 90            # preview
py -3 scripts/archive_old_runs.py --days 90 --apply    # execute
```

## Notes

- Archives live in `archive/` so they remain in the repository (or can be
  pushed to a release/backup location) instead of being lost.
- Do not archive active runs. The script uses file modification time; an
  active run is usually recent. For a run you want to keep live, touch its
  directory or move it out of the scanned root.
- This is a maintenance convenience, not a research artifact. It never deletes
  without `--apply` and never touches `docs/`, `scripts/`, `tools/`, or
  `lean-proof/`.
