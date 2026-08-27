# Proof-obligation graph

## O0 — Frozen target

- **Statement:** There exist explicit `c,C,t_0` such that the requested two-sided TV estimate
  holds for every integer `t>=t_0`.
- **Quantifiers:** one simultaneous numerical triple; every integer `t>=t_0`.
- **Depends on:** `O1`, `O2`, `O3`, `O4`.
- **Evidence/status:** OPEN.  The stopping package proves only the two-sided partial estimate
  in `O5`; the fixed-constant upper half is not closed.
- **Known edge cases:** `t=0` has TV one; both chains have the same base parity at every time.

## O1 — Conditional lamp law

- **Statement:** For a fixed base path `S_0,...,S_t` with `t>=1`, its visited set is the integer interval
  `[L_t,U_t]`; conditional on the path, the final lamps on that interval are mutually
  independent fair bits and all lamps outside it are zero.
- **Quantifiers:** every integer `t>=1` and every admissible nearest-neighbour path.
- **Depends on:** only the transition definition.
- **Evidence/status:** PROVED in Section 1 of `candidate_proof.md`; coordinator audit passed.
- **Proof:** take the chronologically last independent resampling bit at each visited site.
- **Known edge cases:** at `t=0` the initial site is not resampled because no step occurs;
  therefore the statement is used for `t>=1`.  For `t>=1`, the initial site is switched before
  the first move and every arrival site is switched.

## O2 — Explicit lower bound

- **Statement:** The endpoint projection gives TV at least the maximum atom of
  `Binomial(t,1/2)`, hence at least an explicit constant times `t^{-1/2}`.
- **Quantifiers:** every integer `t` in the final range.
- **Depends on:** exact endpoint translation and an explicit central-binomial estimate.
- **Evidence/status:** PROVED in Section 4 of `candidate_proof.md`, with `c=1/4` for every
  integer `t>=1`; coordinator audit passed.

## O3 — Explicit full-state upper bound

- **Statement:** `||P_t^x-P_t^y||_TV <= C/sqrt(t)` with numerical `C` for all `t>=t_0`.
- **Quantifiers:** as in `O0`.
- **Depends on:** `O1` and either an exact state-level coupling/comparison (`O3a`) or a verified
  theorem specialized with all constants (`O3b`).
- **Evidence/status:** OPEN and load-bearing.  Route A proves only
  `sqrt(2)[3+2 log(t+1)]/sqrt(t)` for `t>=2`.  Route C gives the sufficient open array
  inequality `O3c` and falsifies its naive unimodality proof.
- **Known edge cases:** coupling only the base endpoints is insufficient; range-only coupling
  is sufficient if the full `(L_t,U_t,S_t)` triples agree and lamp bits are then shared.

## O4 — Independent audit

- **Statement:** the integrated proof has zero critical errors and zero gaps under the frozen
  conventions.
- **Depends on:** completed candidate proof for `O1`–`O3`.
- **Evidence/status:** BLOCKED at this stopping boundary: no independent audit agent return is
  available and the frozen target itself is incomplete.  `audit_report.md` performs a fresh
  adversarial coordinator audit of the partial package only.

## O1b — Visible-hull sufficiency

- **Statement:** For every `t>=1`, the TV distance of the full state laws equals the TV
  distance of `(min(supp eta union {z}), max(supp eta union {z}), z)` under those laws.
- **Quantifiers:** both specified starts and every integer `t>=1`.
- **Depends on:** `O1` and the exact mixture formula (3.1).
- **Evidence/status:** PROVED in Section 3 of `candidate_proof.md`; coordinator audit passed.
- **Verifier notes:** fibers are finite; likelihoods, not merely conditional lamp laws, are
  constant on each fiber.

## O3p — Explicit logarithmic-loss upper bound

- **Statement:** For every integer `t>=2`, with `n=floor(t/2)`, full-state TV is at most
  `1/sqrt(n+1)+2H_(n+1)/sqrt(t-n+1)`, hence at most
  `sqrt(2)[3+2log(t+1)]/sqrt(t)`.
- **Depends on:** `O1`, the reflected/coalescing base coupling, the one-sided reflection
  identity, and the exact pre-meeting depth law.
- **Evidence/status:** PROVED in Section 5 of `candidate_proof.md` and
  `subagents/route_a.md`; coordinator audit passed.
- **Strength relative to target:** strictly weaker by a logarithmic factor.

## O3c — Sufficient normalized-range array inequality

- **Statement:** There are explicit fixed `C_*` and `t_*` such that, for `t>=t_*`,
  `sum_{r,j,a}|h_t^r(a,j)-h_t^r(a+2,j)| <= 2C_*2^t/sqrt(t)`.
- **Depends on:** exact path counts only.
- **Evidence/status:** OPEN.  Formula (6.2) proves it is sufficient for `O3`.
- **Known obstruction:** parity-class unimodality is false: the exact `t=10,r=4,j=2` slice
  is `(26,16,26)`.

## O5 — Strongest exact partial theorem

- **Statement:** For every integer `t>=2`,
  `1/(4sqrt(t)) <= TV <= 1/sqrt(floor(t/2)+1)
  +2H_(floor(t/2)+1)/sqrt(ceil(t/2)+1)`.
- **Depends on:** `O2`, `O3p`.
- **Evidence/status:** PROVED; exact statement is (7.1) in `candidate_proof.md`.
- **Strength relative to target:** lower bound has the requested scale; upper bound has one
  extra factor `log(t)`.

## Shortest live dependency chain

Transition definition -> `O1` -> `O3` -> `O0`; `O2` is closed, `O3p` closes only `O5`, and
`O3` remains the first unresolved load-bearing node.  A future completion would then require
an independent `O4` audit.
