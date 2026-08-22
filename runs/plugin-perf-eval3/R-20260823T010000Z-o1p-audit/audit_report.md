# Independent Adversarial Audit Report

- Audit run: `R-20260823T010000Z-o1p-audit`
- Audit root: `F:\LaTeX\BVE research\runs\plugin-perf-eval3\R-20260823T010000Z-o1p-audit`
- Target runs:
  - Baseline: `R-20260823T000000Z-o1p-baseline`
  - Light-reuse: `R-20260823T000000Z-o1p-lightreuse`
- Method: independent re-derivation; no subagents spawned; no solver results trusted.
- Overall verdict: `REPAIRABLE_GAP`
  - FATAL_GAP: 0
  - REPAIRABLE_GAP: 1 (light-reuse Lemma 3 rigor)
  - Minor omitted justification: 1 (light-reuse Theorem 5 finite + infinite combination argument)

---

## 1. Statement fidelity to the O1' problem and prior sub-results

Both runs correctly frame themselves as strict partial results on the reduced
core O1'.  They use the same sparse family, run graph, free-base/rho machinery,
and the upstream master criterion

    closure(span Q_sp) = V  <=>  V cap Q_sp^\perp = {0}.

Neither claims general O1' is closed.  Their scope restrictions are honest:
- Baseline: finite polynomial representers, real Hilbert space, bounded
  invertible moment map + banded Gram (concretely stable banded shifts).
- Light-reuse: finite polynomial representers, `H_{beta,lambda}` with
  `beta >= 0`, `|lambda| < 1`.

Both are genuine advances beyond the previously closed `H_beta` and `H_lambda`
subclasses.  The baseline extends the shift bandwidth; the light-reuse adds a
diagonal weighting and reproduces the `beta > 3/2` infinite-run threshold in a
non-Toeplitz setting.  The two families overlap only at `H_lambda`
(`m=1`, `beta=0`) and are otherwise complementary.  No claim solves general O1'.

## 2. Baseline run (Claim A)

### 2.1 Setting and Lemma 0.1 — checked

In `H_shift(m,lambda)` with

    x^k = e_k + sum_{s=1}^m lambda_s e_{k+s},

the operator `A = I + sum lambda_s S^s` is bounded; its adjoint is exactly
`J = A^*` with

    (Jw)_k = M_k(w) = w_k + sum_{s=1}^m lambda_s w_{k+s}.

Under the stability hypothesis `L(z)=1+sum lambda_s z^s` has no zeros in the
closed unit disk, `1/L(z) = sum c_j z^j` has exponentially decaying coefficients,
so `Cw = sum_j c_j w_{k+j}` is a bounded convolution inverse.  Both
`C J = I` and `J C = I` follow from the convolution identity.  Thus
`J` is a bounded invertible isomorphism onto `l^2`, `Pi` is dense, and every
`l^2` moment sequence is realizable.  This part is sound.

### 2.2 Cofinite kept set (Theorem 1.1) — checked

For a finite polynomial representer of degree `D`, the banded Gram gives
`<v_j, x^n> = 0` for `n > D + m` and hence `<v_j, p_n> = 0` for
`n > D + m + 2`.  The threshold `D+m+2` is correct.  Therefore `N` is cofinite,
there is at most one infinite run on each parity, and `B` and `B_fin` are finite.

### 2.3 Main finite-rank criterion (Theorem 2.1) — checked

The run lemma is pure linearity of moments and applies verbatim: for
`w in V cap Q_sp^\perp`,

    M_k(w) = sum_{b in B} t_b rho_b(k) 1_{k in R_b},   t_b = M_b(w).

Because `J` is a bounded invertible map onto `l^2`, `M(w) = Jw` must be an
`l^2` sequence.  Infinite-run moment vectors grow linearly, hence are not in
`l^2`; therefore all `t_b` with `b in B_inf` vanish.  Membership in `V`
then becomes `T|_{B_fin} t = 0`.  Conversely, a kernel vector `t` produces a
finitely supported `M` (all finite runs are below the infinite tails), so
`w = J^{-1}M` exists in `H`, lies in `V`, and is orthogonal to all kept `p_n`
because the rho recursions hold on finite-run kept edges and the tail moments
vanish.  The correspondence is injective by density of `Pi`.  The criterion
is correct in this family.

### 2.4 Abstract band-invertible structure theorem (Theorem 2.3) — checked

The proof only uses:
- `J = A^*` bounded invertible,
- `l^2` realizability of a moment sequence,
- bandedness of `G` to make `N` cofinite,
- the same run/rho algebra.

All these are satisfied under the stated hypotheses.  The theorem is not
claimed for arbitrary banded Gram without an invertible moment map; the
hypothesis `A` bounded invertible is essential and is stated.  No flaw found.

### 2.5 Bandwidth-2 example (Theorem 4.1) — checked

For `m=2`, `v_1=x^4`:

    a_2 = G_{4,2} = lambda_2,
    a_4 = G_{4,4} = 1 + lambda_1^2 + lambda_2^2,
    a_n = 0 for n > 6.

Thus

    <v_1, p_4> = a_4 - 2 a_2
               = lambda_1^2 + (lambda_2 - 1)^2.

The only way this vanishes is `lambda_1=0, lambda_2=1`, which gives
`L(z) = 1 + z^2` with zeros at `z = ±i` on the unit circle, contradicting
stability.  Therefore `4 notin N`.  The finite-support moment sequence
`delta_2` is in `l^2`, so it is realizable via `J^{-1}`; its moments are
`M_0=M_1=M_4=0`, and every kept `p_n` uses degrees `{n,n-2}` with
`n != 4`, so it is orthogonal to the whole kept family.  This is a rigorous
non-density certificate.  No flaw found.

### 2.6 Baseline verdict

**No FATAL_GAP or REPAIRABLE_GAP found in the baseline run.**  The internal
baseline audit was honest that it was not independent; this external audit
resolves that limitation for the stated scope.

---

## 3. Light-reuse run (Claim B)

### 3.1 Setting, density of Pi, Theorem 1 — checked

The telescoping identity

    e_k = sum_{j=0}^{N} (-lambda)^j C_j x^{k+j}
          + (-lambda)^{N+1} C_N e_{k+N+1},
    C_j = prod_{i=0}^{j} (k+1+i)^{-beta},

is correct (with the corrected `j+1`-factor denominator).  The remainder
goes to zero because `|lambda| < 1` and `C_N -> 0` for `beta >= 0`.  Hence
`Pi` is dense.  The Gram matrix has bandwidth 1, and the cofinite threshold
`n > D+3` is correct as a restatement of the H_lambda threshold.

### 3.2 Moment parameterization (Theorem 2) — checked

This is the same pure-moment algebra as the upstream runs and is correct:
a vector `w` lies in `V cap Q_sp^\perp` exactly when its moment sequence has
the run/free-base parameterization and the membership matrix `T` annihilates
the parameter vector.  The theorem does not assert every formal parameter
vector is realizable, which is the right separation of concerns.

### 3.3 Realizability lemma (Lemma 3) — REPAIRABLE_GAP

This is the load-bearing new input.  The claimed result,

    an infinite-run moment vector is realizable in H_{beta,lambda}
    iff  beta > 3/2,

is almost certainly true and is consistent with the H_beta limit `lambda=0`.
However the proof as written is not fully rigorous:

1. **Formal series convergence/remainder.**  The candidate writes
   `w_k = sum (-lambda)^j m_{k+j} / prod_{i=0}^{j} (k+1+i)^beta`
   and then gives asymptotic estimates.  It is not proved that the series
   converges absolutely for every `beta >= 0`, `|lambda| < 1`, and every run
   vector, nor that the truncated-series remainder tends to zero so that this
   particular series is a genuine solution of the moment equation.

2. **No epsilon-level error bounds.**  The asymptotic statements
   `w_{2n} = n/[a(2n+1)^beta] + O(n^{1-2beta})` and
   `w_{2n+1} = O(n^{1-2beta})` are used as the basis for the `l^2`
   classification, but no uniform constants or explicit remainder bounds are
   supplied.  A STRICT theorem cannot rest on an unproved `~`/`O` claim.

3. **Mixed even/odd cancellation.**  The proof that a nonzero combination of
   even and odd infinite-run vectors has no `l^2` cancellation for
   `beta <= 3/2` is stated asymptotically; for `beta = 0` a 2x2 leading-vector
   cancellation argument is given, but the `beta > 0` case again relies on
   unproved `O(n^{1-2beta})` upper bounds on the opposite parity.  This is
   repairable by parity-separated lower bounds.

4. **Finite + infinite combinations.**  Lemma 3 only explicitly discusses the
   pure infinite-run combination.  Theorem 5 then asserts that a full
   `M(t) = sum_b t_b m_b` is realizable iff all `B_inf` coefficients vanish
   when `beta <= 3/2`.  This follows because finite-run moment sequences are
   finitely supported and cannot cancel an unbounded infinite tail, and because
   all finite-run moment vectors are realizable; but this step is not written
   in the proof.

**Repair.**  Replace the asymptotic sketch with a rigorous two-sided bound:
e.g. show for the even-run solution that
`|w_{2n}| <= C n^{1-beta}` and `|w_{2n+1}| <= C n^{1-2beta}` uniformly, and
`|w_{2n}| >= c n^{1-beta}` for large `n`; then `||w||^2` is comparable to
`sum n^{2-2beta}`, which converges exactly when `beta > 3/2`.  For mixed runs,
prove the opposite-parity contributions are of strictly smaller order, or use
a matrix/determinant argument to exclude leading-order cancellation.
This is a repairable, not a fatal, gap.

### 3.4 Theorem 5 and Section 5 example — structurally correct

Assuming Lemma 3 is repaired, Theorem 5 is the correct consequence of the
run parameterization plus the realizability classification.  The concrete
`v_1 = x^4` example is correct:
`G_{4,4}=5^{2beta}+lambda^2`, `G_{4,2}=0`, so `p_4 notin N`; the
finite-support `delta_2` moment sequence is realizable and gives the same
non-density certificate as in H_lambda.

### 3.5 Regressions and complementarity — checked

- `lambda = 0` is unitarily equivalent to the diagonal `H_beta`; the
  `beta > 3/2` infinite-run admissibility agrees with the prior H_beta result.
- `beta = 0` is exactly `H_lambda`; `B_adm` reduces to `B_fin`.
- The two runs are complementary: baseline widens shift bandwidth in a
  Toeplitz bounded-invertible setting; light-reuse adds diagonal weighting
  with unbounded moment map.  They overlap only at `H_lambda`.

---

## 4. Critical/gap counts

- FATAL_GAP: 0
- REPAIRABLE_GAP: 1
  - Light-reuse Lemma 3: realizability `iff beta > 3/2` needs a rigorous
    convergence + asymptotics proof.
- Minor omitted justification: 1
  - Light-reuse Theorem 5: explicit finite-run + infinite-run combination
    argument should be added (fold into the same repair).
- Baseline: no gap found.

## 5. Registration decision

- **Baseline**: can be registered as a strict partial result now.  It may be
  formally labeled `RIGOROUS_PARTIAL_RESULT` after this independent audit.
- **Light-reuse**: should be held at `REPAIRABLE_GAP` until Lemma 3 is
  rewritten with rigorous bounds and the finite+infinite argument is made
  explicit.  After that repair, it can be registered as a strict partial result.
- Neither run solves general O1'; both are correctly scoped.
