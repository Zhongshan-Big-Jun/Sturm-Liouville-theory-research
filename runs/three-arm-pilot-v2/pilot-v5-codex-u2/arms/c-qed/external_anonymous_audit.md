# Independent blind audit

## Verdict

PARTIAL_NOT_COMPLETE

The candidate does not complete the frozen task. It rigorously proves a lower bound of order
`t^{-1/2}` and an upper bound of order `(log t)t^{-1/2}`, but it does not prove an upper bound
`C t^{-1/2}` with a constant `C` independent of `t`. The candidate states this limitation
honestly and does not promote the missing estimate to a theorem.

## First load-bearing unresolved obligation

The first unresolved obligation is STEP6, specifically the first inequality in (6.1), or any
other proof of

\[
\|Q_t^{(0)}-Q_t^{(2)}\|_{\rm TV}\leq C t^{-1/2}
\]

with an explicit absolute constant. This is a proof/dependency gap for the original target,
not a boundary-convention issue. STEP4 and STEP5 do not by themselves establish the asserted
cancellation among image sums with different periods. Since this missing statement is the
entire unproved upper half of the requested theorem, it is not a local repair. It is the main
remaining theorem-strength obligation.

There is no earlier load-bearing flaw in the claims that the candidate actually labels as
proved.

## Claim-by-claim audit

### 1. Conditional lamp law

STEP1 is correct for every `t>=1`. Conditional on a fixed nearest-neighbor base path, the
visited set is the full integer interval between its minimum and maximum. Every visited site
has at least one switch operation, and its last switch is an independent fair bit. Last
switches at distinct sites are distinct independent resampling variables. Unvisited lamps
retain their forced initial value zero. Thus the conditional final lamp law is exactly uniform
on configurations supported in the visited interval. This also correctly handles the forced
initial zero lamps at sites `0` and `2`: the starting lamp is switched before the first move,
so its initial value is overwritten when `t>=1`.

### 2. Kernel reduction and translation

STEP2 is correct. The displayed `K` is a Markov kernel, because there are exactly
`2^(u-l+1)` configurations supported in `[l,u]`. The direct `l^1` argument proves contraction
of total variation. Translation of a walk started at `2` shifts its minimum, maximum, and
endpoint by `2` without changing the all-zero initial lamp configuration.

### 3. Diagonal-variation identity and parity

STEP3 is correct. Under

\[
d=u-\ell,\qquad a=-\ell,\qquad j=z-\ell,
\]

the walk from `0` starts at `a`, while the walk from `2` starts at `a+2`. The union of the two
possible starting-coordinate supports is exactly `-2<=a<=d`, and `0<=j<=d`. A length-`t`
nearest-neighbor path has range width at most `t`, giving the stated finite sum. The parity
condition `j-a congruent to t mod 2` is correct, and shifting `a` by `2` preserves it. Thus no
opposite-parity laws are inadvertently compared.

### 4. Boundary inclusion-exclusion and image formula

STEP4 is correct. Avoiding the lower endpoint, avoiding the upper endpoint, and avoiding both
give exactly the three shifted killed kernels in the displayed inclusion-exclusion identity;
the zero-extension convention handles `d=0,1`. The image sum has the correct period
`2(d+2)`, vanishes at the exterior absorbing sites `-1` and `d+1`, has the correct time-zero
data, and satisfies the killed-walk recurrence. The induction therefore proves the formula
without an external reflection theorem.

### 5. Binomial estimates

The estimates in STEP5 are correct.

- The central-binomial recurrence proves the stated explicit bounds on `m_t`, including the
  odd-time identification `m_(2n+1)=c_(n+1)` and the separate `t=1` case.
- Unimodality on the relevant parity lattice telescopes the total first variation to `2m_t`.
- The ratio products give the stated Gaussian envelope. The odd-parity correction is bounded
  by `1/(4t)`, which is smaller than `log(sqrt(2))`.
- In the central region the exact second-difference quotient is

  \[
  \frac{4(k^2-t-2)}{(t+2)^2-k^2},
  \]

  and the candidate's denominator and numerator bounds imply the displayed estimate.
- In the outer region, monotonicity gives the factor `4p_t(k-2)`. The exponent comparison for
  `t>=8` and the finite `t=2,...,7` boundary checks cover all remaining parity-admissible
  points, including `k=t+2`; beyond that point the second difference is zero.

These second-difference estimates do not, however, supply the missing signed summation over
the different image periods in STEP6.

### 6. Reflection coupling and the logarithmic-loss upper bound

The substitute coupling in STEP6 is rigorous.

Before meeting, `Y_s=2-X_s`; both walks meet when `X` first hits `1`. At each pre-meeting step,
the sign used for the increment of `Y` is a predictable sign change of a fresh fair increment.
After meeting, a fresh independent fair-increment sequence is used for both walks. Hence each
marginal is a simple symmetric random walk, while the endpoints agree after the meeting.

If `M` is the pre-meeting minimum and `K=1-M`, the pre-meeting ranges are `[1-K,1]` and
`[1,1+K]`. If the common continuation hits both `-K` and `K`, its translated range contains
both pre-meeting ranges, so the final range-endpoint triples coincide. This implication is
correct.

For a fresh walk `S` and `T_K=inf{s:S_s=K}`, reflection gives the exact cancellation

\[
\mathbb P(T_K>s)
=\sum_{j<K}p_s(j)-\sum_{j>K}p_s(j)
=\sum_{-K\leq j<K}p_s(j).
\]

The last interval contains exactly `K` points of the time-`s` parity lattice, so this is at
most `K m_s`. This verifies (6.3), including its parity convention. Taking `K=1` verifies
(6.4).

The gambler's-ruin calculation in (6.5) is also correct: `K>=k` is exactly the event of hitting
`1-k` before `1`, and the affine harmonic function gives probability `1/k`. The exit time is
almost surely finite by the stated uniform block argument.

With `N=floor(t/2)`, on `tau<=N` the continuation has at least `t/2` steps and is independent
of the stopped pre-meeting path. Conditioning on the pre-meeting information therefore gives
failure probability at most `3K/sqrt(t)`. Moreover, `K<=N+1` on this event and

\[
\mathbb E[K;\tau\leq N]
\leq\sum_{k=1}^{N+1}\frac1k
\leq1+\log t.
\]

Together with `P(tau>N)<=2/sqrt(t)`, this proves

\[
A_t\leq\frac{5+3\log t}{\sqrt t}\qquad(t\geq4).
\]

Kernel contraction then proves the same bound for the lamplighter laws. For `t=1,2,3`, its
right-hand side exceeds `1`, so extension to all `t>=1` by the trivial total-variation bound
is valid.

### 7. Lower bound

STEP8 is correct. Endpoint projection is a deterministic Markov kernel, hence

\[
\|P_t^x-P_t^y\|_{\rm TV}
\geq \tfrac12\sum_k|p_t(k)-p_t(k-2)|
=m_t
\geq\frac1{2\sqrt t}
\]

for every `t>=1`. The two endpoint laws live on the same parity lattice because the starting
positions differ by `2`.

### 8. Small times

STEP9 is correct. At `t=0` the two point masses are distinct, so total variation is `1`. At
`t=1` overlap is possible only at base endpoint `1`. Equality of final lamp configurations
then forces the lamp at `0` on the first path and the lamp at `2` on the second path to be zero,
while the common lamp at `1` can take either value. There are two common states, each of mass
`1/8` under both laws, so the overlap mass is `1/4` and total variation is `3/4`.

## Rigorously established result

The candidate rigorously establishes the following explicit partial theorem:

\[
\boxed{
\frac1{2\sqrt t}
\leq\|P_t^x-P_t^y\|_{\rm TV}
\leq\frac{5+3\log t}{\sqrt t}
\quad\text{for every integer }t\geq1.
}
\]

It also rigorously establishes the exact range-endpoint reduction, the diagonal-variation
identity, the killed-walk image formula, the stated binomial estimates, and the exact values
at `t=0,1`.

## Why the original task is not complete

The factor `5+3 log t` is unbounded and therefore cannot be replaced by a fixed constant merely
by enlarging `C` or `t_0`. The proposed constants `c=1/2`, `C=144`, `t_0=1` depend on the
unproved estimate (6.1). Consequently the required constant-order upper bound, and hence the
original two-sided theorem, remains open in this candidate.

## Structured audit record

```json
{
  "verdict": "PARTIAL_NOT_COMPLETE",
  "first_error": {
    "location": "STEP6, first inequality in (6.1)",
    "layer": "proof/dependency",
    "issue": "The signed diagonal-variation estimate O(t^{-1/2}) is not proved; STEP4 and STEP5 do not provide the required cross-period cancellation."
  },
  "critical_errors": [],
  "gaps": [
    {
      "location": "STEP6 -> STEP7 -> STEP10 -> GOAL",
      "issue": "No explicit constant C independent of t is established for the upper bound required by the frozen task."
    }
  ],
  "repair_hints": "Supply a complete signed summation-by-parts identity for the diagonal variation, with all d=0,1 and a-boundary terms checked, or give a different coupling or analytic argument proving an explicit C/sqrt(t) upper bound. The existing pathwise range-equality coupling inherently yields the harmonic logarithm and does not close this obligation."
}
```
