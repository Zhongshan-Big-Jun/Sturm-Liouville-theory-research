# Problem contract

## Authority and frozen inputs

- Task ID: `Q-20260831-g1p-kpdet`.
- Contract date: `2026-08-31`.
- Source record SHA256: `45f844a99eb64994ec86a94746ba85e8b619eeea60322ccb3e60d50b3da1658b`.
- Parent Blueprint SHA256: `3b99f2090d73029fa77498a897979e614ddccbb205b613449fdd2181ce6ccc48`.
- Prior candidate SHA256: `4e688ad5d7c0e3f4869e4aa43cad823549fc66db76bcd9293341eb85b0d8e556`.
- Prior independent audit SHA256: `5682b7c1c0fa7b881cb71c28d993966c8bc26e099a2641622a90b4facc3db93e`.

## Objects and normalization

Let `R>1`, `tau=R-1`, and `L=1/2`. Work on the prescribed finite-interior,
band-consistent, n=2 symmetric INF branch with half switches

```text
0<a<b<L.
```

Let `lambda_2<lambda_3`, `c^2=lambda_2/lambda_3`, and let

```text
v=sqrt(2)u_2|_[0,L],
w=sqrt(2)u_3|_[0,L].
```

Then `v` is the positive first Dirichlet-Dirichlet half mode, `w` is the
second Dirichlet-Neumann half mode, and

```text
w(a)=c v(a),
w(b)=-c v(b).
```

With `U=diag(u_2(a),u_2(b))`, the audited reduction gives

```text
U^(-1) H U^(-1)=[[a_0,b_0],[b_0,b_0]],
b_0>0,
M=(2lambda_2)^(-1)U^(-2)Kp_odd U^(-2)
  =[[a_0-gamma_1,b_0],[b_0,b_0-gamma_2]],
gamma_j=c|W(x_j)|/[lambda_2 tau u_2(x_j)^4]>0.
```

The symbols `a_0,b_0` are matrix coefficients and are not switch positions.

## Exact target

Decide the branch-local claim

```text
KP-DET: det Kp_odd(R)>0 for every finite R>1.
```

Equivalently, exclude every branch-realizable equality

```text
(gamma_1-a_0)(gamma_2-b_0)=b_0^2
```

at a first loss from the strict near-one negative-inertia component.

## Permitted premises

1. The prior audited semiseparable, Jacobi, transfer, and strict off-diagonal reductions.
2. Strict near-one negative definiteness and the accepted large-R finite-interior chart.
3. Standard one-dimensional Sturm comparison, separation, Green factorization, and analytic perturbation, with hypotheses checked in the proof.
4. Exact three-layer transfer formulas derived within this run.

## Excluded scope

- KO-DET and simultaneous sector singularity, unless an exact KP-DET implication forces them.
- Non-symmetric roots, SUP, n greater than 2, switch collision, and global G1 prime.
- Numerical scans as proof.

## Completion and falsification criteria

- `PROVED`: a strict branch-uniform exclusion of the scalar equality.
- `REFUTED`: an exact branch witness satisfying all transfer, band, normalization, and mode-index conditions with nonpositive determinant.
- `RIGOROUS_PARTIAL_RESULT`: a strictly smaller exact scalar or phase inequality, with all equivalences proved and remaining equality cases explicit.

An abstract two-by-two matrix or finite numerical ladder is not a counterexample.

## Contract audit

This contract narrows the prior branch problem to its earliest named open
obligation. It preserves the normalized `Kp_odd` convention and does not infer
KP-DET from the previous partial PASS.
