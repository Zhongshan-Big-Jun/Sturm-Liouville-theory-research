RIGOROUS_PARTIAL_RESULT

# Direct closure-first attempt on `KP-DET`

## 1. Exact claim attacked

The first open load-bearing sign obligation is

```text
KP-DET: det Kp_odd(R)>0 for every finite R>1
```

on the prescribed exact `n=2` symmetric INF branch.

Although the source record lists `trace Kp_odd<0` first, the trace is not independent after one strict inertia anchor. The determinant is the first quantity whose vanishing can change the inertia.

## 2. Strict inertia bridge

### Lemma

Let `I` be a connected interval and let `A:I->Sym_2(R)` be continuous. Suppose `A(R0)` is negative definite for some `R0 in I` and `det A(R)>0` for every `R in I`. Then `A(R)` is negative definite and `trace A(R)<0` for every `R in I`.

### Proof

The ordered eigenvalues `mu_1(R)<=mu_2(R)` of a real symmetric matrix depend continuously on its entries. Since `det A=mu_1 mu_2>0`, neither eigenvalue vanishes and they always have the same sign. At `R0` both are negative. A continuous nonzero real-valued eigenvalue cannot change sign on a connected interval. Hence both remain negative on `I`, so `A` remains negative definite and its trace is their negative sum. QED.

Applying the lemma separately to `Kp_odd` and `Ko` shows that the original four scalar sign obligations reduce to the two determinant obligations, provided the prescribed branch is connected and the matrices are continuous as stated in the contract.

## 3. Strict endpoint anchors and compact first-loss reduction

The frozen near-one theorem gives a `delta>0` such that both INF sector matrices are negative definite on `1<R<1+delta`.

For the accepted large-`R` chart, put `u=R^(-1/6)`. The exact asymptotics give

```text
(Kp_odd)11=-6 kappa(3pi^2-8)/pi^2 u^4+O(u^6),
(Kp_odd)12= 4 kappa^2/pi u^8+O(u^10),
(Kp_odd)22=-16/pi u^12+O(u^14),
det Kp_odd=128 kappa^2/pi^2 u^20+O(u^22),

Ko=-(16/pi)u^12 [[1,2],[2,4]]+O(u^14),
det Ko=2048 kappa^2/pi^4 u^26+O(u^28),
```

with `kappa>0`. Thus the diagonal entries and determinant of `Kp_odd` have the negative, negative, positive signs for all sufficiently small positive `u`, so `Kp_odd` is negative definite there. For `Ko`,

```text
trace Ko=-(80/pi)u^12+O(u^14)<0
```

and its determinant is positive for sufficiently small positive `u`, so `Ko` is negative definite there. Therefore there is a finite `R_infty` such that both matrices are negative definite for `R>R_infty`.

Consequently, any failure of the target lies in the compact middle regime

```text
[1+delta,R_infty].
```

If `Kp_odd` is the first sector to lose negative definiteness, continuity supplies a first loss `R_*` in this compact interval with

```text
det Kp_odd(R_*)=0,
Kp_odd(R)<=0 as a quadratic form at R=R_*.
```

There are two exact possibilities: a corank-one negative semidefinite matrix with a nonzero kernel vector, or the exceptional double-zero matrix `Kp_odd(R_*)=0`. Neither is excluded by endpoint information alone.

## 4. Exact first-zero equation

For INF, define

```text
d_j=-2c|W(x_j)|/(R-1)<0,
H=G_D o (e e^T)-c^2 G_N,
u=(u_2(x1),u_2(x2)).
```

The switch values `u_j` are nonzero because `f(x_j)=0` and strict Sturm interlacing excludes simultaneous zeros of `u_2` and `u_3`. The exact matrix is

```text
Kp_odd=diag(d)+2lambda_2 diag(u)Hdiag(u).
```

If `Kp_odd y=0` and `z=diag(u)y`, then `z` is nonzero and

```text
d_j z_j/u_j^2+2lambda_2(Hz)_j=0,  j=1,2.        (E-KP)
```

Taking the Euclidean inner product with `z` gives the necessary equality

```text
sum_j d_j z_j^2/u_j^2+2lambda_2 z^T H z=0.       (Q-KP)
```

Using the frozen exact spectral split, this is

```text
sum_j d_j z_j^2/u_j^2
+2lambda_2[-alpha(Ev1.z)^2+(Ez)^T Ph(Ez)
	+c^2 beta(w1.z)^2-c^2 z^T Qh z]=0,             (S-KP)
```

where `alpha,beta>0` and `Ph,Qh` are positive definite two-point tail matrices. The unresolved coercive statement is that the left side is strictly negative for every nonzero `z`, uniformly over the compact middle branch. The positive terms `(Ez)^T Ph(Ez)` and `c^2 beta(w1.z)^2` prevent a sign conclusion from positivity of the spectral tails alone.

This is an exact kernel exclusion problem. No numerical approximation occurs in the reduction.

## 5. Direct monotonicity route audit

The parent M1 evidence uses

```text
x'(R)=-J(R,x)^(-1) F_R(R,x),
d/dR det Kp_odd=partial_R det Kp_odd
	+grad_x(det Kp_odd).x'(R).
```

For `n=2`, the exact sector factorization is

```text
det J=(R-1)^4 det(Kp_odd)det(Ko).
```

Thus the displayed formula for `x'(R)` is justified only where both sector determinants are nonzero. In particular, it is unavailable at the very first singular point that a monotonicity proof is meant to exclude. This does not refute the conjecture that both determinants decrease. It proves only that the recorded `J^(-1)` calculation is not by itself a non-circular first-zero certificate. One of the following additional ingredients is required:

1. an independently regular global branch parameterization that remains differentiable when `J` is singular, together with a derivative formula in those coordinates;
2. a direct coercive or determinant identity that excludes `(E-KP)` before `J^(-1)` is used;
3. a singular-point argument showing that any kernel is incompatible with the branch equations and boundary conditions.

## 6. Cheapest falsification probe

- Exact boundary probe: both endpoint regimes have the desired strict sign. No boundary counterexample exists within their declared ranges.
- Exact dependency probe: the current monotonicity proof skeleton requires an inverse whose existence is equivalent to the combined determinant nonvanishing target. It does not close the first-zero case.
- Numerical probe: the parent finite scans survive, but they remain `EVIDENCE` and are not used in any inference above.
- Counterexample result: none found or claimed.

## 7. Strongest rigorous result

The four scalar obligations reduce to two determinant obligations. Any failure is a compact-middle sector singularity. For the earliest sector, `KP-DET`, failure is equivalent to the exact first-zero alternatives above, with a nonzero solution of `(E-KP)` in the corank-one case. The parent M1 route requires a non-circular extension at such a point.

## 8. Decision delta

The direct attempt did not close or falsify `KP-DET`. It exposed a strictly localized compact-middle kernel gap and separated two mechanism-distinct ways to attack it. This changes the control decision from direct-only work to a bounded two-task escalation.
