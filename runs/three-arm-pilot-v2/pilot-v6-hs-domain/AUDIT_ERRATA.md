# Pilot v6 audit metadata errata

Status: `COORDINATOR_ERRATA`, 2026-08-28.

The original label-blind audit files are preserved byte-for-byte and are not silently rewritten.
The uniform post-unseal evaluator in `FINAL_EVALUATION.md` is authoritative for cross-arm scoring.

## Arm C degree-spectrum label

The Arm C anonymous review says that the proof establishes the bonus degree spectrum, and its
`verdict.json` contains `degree_spectrum: PASS`. Read literally as the degree spectrum of every
nonzero polynomial in the operator domain, this is incorrect. Arm C STEP6 proves the exact named
system membership index classification

```text
Q_n^(s) in D(K_c^(s/2)) iff n in {0,1},
```

and STEP8 proves polynomial graph-core density. It does not classify the degrees of all polynomials
in `C[x] intersect D(K_c^(s/2))`. The JSON field should be read as
`named_Q_membership_index_spectrum`, not `all_domain_polynomial_degree_spectrum`.

This erratum does not change C's uniform score of 97. The independent final evaluator explicitly
excluded the all-polynomial spectrum from C and awarded strict advancement only for the graph-core
theorem.

## Arm B strict-progress rationale

The Arm B anonymous review awarded 15/15 for strict progress while its prose incorrectly listed the
unproved exact all-polynomial degree spectrum among the added refinements. That bonus assertion is
not credited to B. The retained 15/15 uniform score is supported instead by B's correct closure of
the three required conclusions and its adequately sketched constrained-polynomial density
refinement. B remains `REPAIRABLE_GAP` because equation (2) omits the load-bearing regularity and
operator-power recursion details.

The later posthoc proof and audit of the all-polynomial degree spectrum are excluded from B's score.

## Posthoc audit input binding

The posthoc degree-spectrum audit binds its candidate tool input to SHA256
`59877D91F84A1D94903595EED7E35ECCCCAE23BB9591FA7FDA6AEE6D0374DD8F`. This immutable input is
exactly the Git blob

```text
d11b0aa:tools/krein-power-domain-polynomial-obstruction.md
```

verified by `git cat-file blob ... | sha256sum`. After the audit passed, the working tool file was
changed only to promote the candidate status to `STRICT` and link the archived full audit. The
audited theorem statement and parity-triangular mechanism were not changed.
