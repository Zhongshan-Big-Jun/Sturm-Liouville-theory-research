# Proof-obligation graph

## Root `O0`

**Statement:** There are explicit `c,C,t_0` such that the frozen two-sided total-variation estimate holds for every integer `t>=t_0`.

**Quantifiers:** one simultaneous numerical triple; all integer `t>=t_0`.

**Depends on:** `O1`, `O2`, `O3`, `O4`.

**Evidence/status:** RIGOROUS_PARTIAL_RESULT. `O1` and `O2` are closed and the logarithmic-loss upper is closed; `O3` at constant order is open, so the root target is not in the proved closure.

## `O1` Exact lamp kernel

**Statement:** For either all-zero start and every `t>=1`, conditional on the base path, final lamps on the visited interval `[L,U]` are iid `Bernoulli(1/2)`, lamps outside are zero, and the endpoint is `Z`.

**Quantifiers:** both starts, every deterministic admissible base path, every `t>=1`.

**Depends on:** direct independence/last-resampling proof.

**Evidence/status:** PROVED in `subagents/direct_coupling.md`, Section 1; pending global paper-level re-audit.

**Known edge cases:** the starting lamp is switched at time 0; arrival lamp is switched at every step; repeated visits use the last independent resampling.

## `O2` Explicit lower bound

**Statement:** Endpoint projection gives `||P_t^x-P_t^y||_TV >= p_t`, where `p_t` is the largest atom of a length-`t` simple walk; prove `p_t >= c/sqrt(t)` explicitly.

**Quantifiers:** every claimed integer time, even and odd.

**Depends on:** total-variation data processing; endpoint parity and unimodality; elementary central-mass estimate.

**Evidence/status:** PROVED in `candidate_proof.md`, Lemma 2, for every `t>=1` with `c=1/4`; pending global audit.

## `O3` Explicit upper bound

**Statement:** Prove `||P_t^x-P_t^y||_TV <= C/sqrt(t)`.

**Depends on:** `O1` and one audited mechanism below.

**Evidence/status:** PARTIAL. The explicit bound `(2 log(t)+15)/sqrt(t)` is proved for every `t>=16`; the required removal of `log(t)` remains open.

### `O3a` Range-triple gradient route

Prove the diagonal-shift estimate

`||Law_0(L,U,Z)-Law_2(L,U,Z)||_TV <= C/sqrt(t)`.

This is sufficient by `O1` and contraction under a common lamp kernel. Status: PARTIAL. Exact identity (12) in `candidate_proof.md`; `AVI` remains open. Each one-sided `(L,Z)` and `(U,Z)` marginal has TV at most `12/sqrt(t)` by hash-validated `subagents/range_translation.md`; the path-specific joint-to-marginals comparison remains open.

### `O3b` Direct successful coupling route

Construct a coupling of the two full lamplighter states with mismatch probability at most `C/sqrt(t)`, verifying exact marginals. Status: PARTIAL/route blocked for the standard reflection-then-synchronization mechanism. The hash-verified artifact `subagents/direct_coupling.md` proves that mechanism has optimal conditional mismatch of order `log(t)/sqrt(t)`; a materially different coupling could still work.

### `O3c` Exact path-count / reflection route

Express and sum the translated difference of the joint min-max-endpoint mass, with an explicit bound. Status: PARTIAL. Hash-verified `subagents/aggregate_coarea.md` proves the killed-kernel identity, an explicit periodized-binomial mixed-difference formula, and the exact coarea identity. The first gap is either

`sum_{R,K,m} c_{R,K}(m) <= C_0 binom(t,floor(t/2))`

for a fixed numerical `C_0`, or the corresponding fixed-constant bound on the explicit arrays `V_t^D+V_t^E` in that artifact.

## `O4` Interface, constants, and boundary audit

**Statement:** Check every kernel/coupling interface, select explicit `c,C,t_0`, verify `c<=C`, parity, small times, and both forced initial zeros.

**Depends on:** `O1`--`O3`.

**Evidence/status:** PARTIAL. Parity, `t=0`, small-time scope, forced initial zeros, conditional kernels, and the constants in the partial theorem passed the fresh global audit. Selection of a constant `C` for the frozen upper remains impossible until `O3` closes.
