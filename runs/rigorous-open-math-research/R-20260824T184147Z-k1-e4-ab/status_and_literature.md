# Status and Literature - K(1) strict anchor run

## Status after audit

The `c=1` even minimal-solution anchor is now `STRICT`:

```text
lim_(j -> infinity) j^3 mu*_j = e/4.
```

The proof is self-contained from the frozen recurrence, terminal data, and
elementary factorial and exponential series identities.  It does not import
an external theorem.

The following remain open or outside this run:

- a closed form for `K(c)` for general `c`;
- source-term control in the broader third-order box-induction program;
- the general coefficient-family product classification;
- formal Lean verification of this new proof.

## Literature and source status

The repository source at commit `db7e597` contained a 25-digit numerical match
for `K(1)=e/4` and explicitly labeled the corresponding proof gap as open.
The source files and hashes used by the benchmark are recorded in
`reproducibility/source_manifest.json`.

No priority claim is made.  The result is registered as a project proof based
on the repository's own recurrence and is subject to future independent
literature comparison.
