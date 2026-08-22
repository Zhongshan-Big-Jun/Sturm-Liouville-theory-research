# Final Report

Status label: `RIGOROUS_PARTIAL_RESULT`

## Summary

The run investigates the A6 open sub-problem: are there product solutions
`E_j = prod e_k` of the third-order z-scaled recurrence whose ratio `e_j` is a
rational function of `j` of degree greater than 2?

I proved a STRICT no-go theorem for the root-1 branch (`e_j -> 1`):

> For both even and odd recurrences and all `c > 0`, if `e_j` is rational,
> `e_j -> 1`, and `E_j` is a product solution, then `e_j` has degree at most 2.
> Consequently no higher-degree rational product ratio exists on the root-1
> branch.

The proof mechanism is:

1. asymptotic classification forces `u = lim j(e_j-1)` into the known free or
   rigid branch;
2. the fixed-point identity, expanded at infinity, has a triangular structure
   with nonzero diagonal coefficients: `(m-3)` on the free branch and `(m-1)`
   on the rigid branch;
3. hence the whole asymptotic expansion is uniquely determined by `(u, A_2)`;
4. the known degree-2 `E^(tau)` family realises every possible `(u,A_2)`;
5. two rational functions with the same Laurent expansion at infinity are
   identical, so any rational root-1 ratio must be that degree-2 ratio.

This closes the listed "higher-degree rational function exclusion" gap for the
root-1 branch. It does not close the root-0/minimal branch.

## Exact remaining gaps

- **Root-0/minimal branch**: rational exclusion is still only numerical
  evidence (high-precision backward iteration fits) plus a formal-asymptotic
  uniqueness argument; no complete theorem that `e_j -> 0` rational ratios
  cannot solve the fixed-point identity. This is the main open remainder of the
  A6 problem.
- **Asymptotic strictification of the minimal solution**: the constant `K(c)`
  and Birkhoff-Trjitzinsky-type rigor remain open (unchanged from the source).
- **Non-homogeneous box induction**: the source-item control gap remains open
  (unchanged).

## Artifacts produced

- `problem_contract.md`
- `status_and_literature.md`
- `approach_registry.md`
- `research_ledger.md`
- `candidate_proof.md`
- `escalation_ladder.md`
- `performance_log.md`
- `final_report.md`
- `reproducibility/verify_asymptotic_no_go.py`
