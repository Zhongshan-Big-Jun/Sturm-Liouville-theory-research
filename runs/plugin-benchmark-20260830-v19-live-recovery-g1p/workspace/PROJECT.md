# v1.9 live recovery G1 prime benchmark

- **Project ID:** `MRP-20260830-v19-live-recovery-g1p-094e55`
- **Created:** 2026-08-30T01:53:39Z
- **Lifecycle state:** `ACTIVE`
- **Upstream solver:** `$rigorous-open-math-research`

## Program scope

This project isolates one bounded Sturm-Liouville research target and one
workflow property. The mathematical target is the all-finite-R negative
definiteness of the two normalized n=2 symmetric INF sector matrices. The
workflow target is a quota-safe checkpoint while one real research worker is
still in flight, followed by deterministic reconciliation without duplicate
dispatch.

The target excludes non-symmetric roots and cannot by itself close global G1
prime.

## Research objectives

1. Prove, refute, or sharply reduce the all-finite-R sector statement.
2. Test v1.9 live in-flight checkpoint and resume behavior.
3. Preserve exact open obligations and avoid repeated research after recovery.

## Literature scope and cutoff

The bounded search cutoff is 2026-08-30. It covers related Sturm-Liouville gap
papers and the parent project's accepted Blueprint snapshot. It does not claim
an exhaustive global priority search.

## Problem portfolio

The only active problem is `P-G1P-SYM-INF-ALLR`.

## Knowledge assets

Frozen parent source hashes, the accepted M3 snapshot, and the bounded novelty
preflight are stored under `refs/`.

## Research budget

No emergency reserve. Stop at a safe checkpoint boundary or experiment
completion.

## Current entry point

Read `state/RESUME.md` and `state/current.json` before continuing.
