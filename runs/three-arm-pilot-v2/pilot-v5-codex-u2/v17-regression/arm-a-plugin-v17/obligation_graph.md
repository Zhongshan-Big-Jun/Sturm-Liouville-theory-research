# Proof-obligation graph

## O0 — Frozen target

- **Statement:** There exist explicit `c,C,t_0` such that the requested two-sided TV estimate
  holds for every integer `t>=t_0`.
- **Quantifiers:** one simultaneous numerical triple; every integer `t>=t_0`.
- **Depends on:** `O1`, `O2`, `O3`, `O4`.
- **Evidence/status:** OPEN.
- **Known edge cases:** `t=0` has TV one; both chains have the same base parity at every time.

## O1 — Conditional lamp law

- **Statement:** For a fixed base path `S_0,...,S_t`, its visited set is the integer interval
  `[L_t,U_t]`; conditional on the path, the final lamps on that interval are mutually
  independent fair bits and all lamps outside it are zero.
- **Quantifiers:** every integer `t>=0` and every admissible nearest-neighbour path.
- **Depends on:** only the transition definition.
- **Evidence/status:** PROVED in `closure_gate.md`; paper-level expansion pending.
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
  integer `t>=1`; independent audit pending.

## O3 — Explicit full-state upper bound

- **Statement:** `||P_t^x-P_t^y||_TV <= C/sqrt(t)` with numerical `C` for all `t>=t_0`.
- **Quantifiers:** as in `O0`.
- **Depends on:** `O1` and either an exact state-level coupling/comparison (`O3a`) or a verified
  theorem specialized with all constants (`O3b`).
- **Evidence/status:** OPEN and load-bearing.
- **Known edge cases:** coupling only the base endpoints is insufficient; range-only coupling
  is sufficient if the full `(L_t,U_t,S_t)` triples agree and lamp bits are then shared.

## O4 — Independent audit

- **Statement:** the integrated proof has zero critical errors and zero gaps under the frozen
  conventions.
- **Depends on:** completed candidate proof for `O1`–`O3`.
- **Evidence/status:** OPEN.

## O1b — Visible-hull sufficiency

- **Statement:** For every `t>=1`, the TV distance of the full state laws equals the TV
  distance of `(min(supp eta union {z}), max(supp eta union {z}), z)` under those laws.
- **Quantifiers:** both specified starts and every integer `t>=1`.
- **Depends on:** `O1` and the exact mixture formula (3.1).
- **Evidence/status:** PROVED in Section 3 of `candidate_proof.md`; independent audit pending.
- **Verifier notes:** fibers are finite; likelihoods, not merely conditional lamp laws, are
  constant on each fiber.

## Shortest live dependency chain

Transition definition -> `O1` -> `O3` -> `O0`, in parallel with `O2`, followed by `O4`.
