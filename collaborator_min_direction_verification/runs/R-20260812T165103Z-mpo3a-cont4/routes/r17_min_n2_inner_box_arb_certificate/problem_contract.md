FINITE_COMPUTATIONAL_RESULT

# R17 problem contract: compact physical common-angle certificate

## Canonical binding and concurrent advance

- Blueprint SHA-256 at freeze:
  `a53684ab115d53756d4dc9bd3af7fb1ef56c8cee3b90fc303070ce0503223c46`.
- Evidence inventory SHA-256: `b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
- The calculation started from Blueprint snapshot
  `0120d1fb32af1a30449575995efccb6d1afcce416ee671ad00a5f296400fd799`.
  During the calculation, the independently reviewed R15 proposal was
  deterministically integrated, advancing the canonical Blueprint to the
  freeze hash above without changing the inventory.
- R15 adds the `mu=2`, min, `n>=3` nonexistence theorem.  That theorem is
  disjoint from and is not used by this compact general-`mu`, `n=2`
  coefficient certificate.
- Trusted analytic input: R14, route
  `runs/R-20260812T165103Z-mpo3a-cont4/routes/r14_min_n2_ratio_bernstein`.

## Objects and quantifiers

Let

```text
k=(mu-1)/(mu+1),
Aplus=(mu+1)alpha/2,
Aminus=(mu+1)beta/2,
t=2 Aplus/pi,
y=(Aminus-pi/2)/(pi/(1+k)-pi/2).
```

This route quantifies over the exact common-angle compact box

```text
(k,t,y) in [1/64,63/64]^3,
```

restricted to the physical retained branch

```text
g<1,   rB>1.
```

All centered quantities, `Knew`, and the Bernstein data `N_i` are those of
R14.  The target is exactly

```text
B_i=g Knew-p_+ N_i>0,       i=1,2,3,4.
```

In the centered normalization checked here this is

```text
g Knew cp^4-Pplus Nhat_i>0.
```

The true ratio threshold is `<1`; no auxiliary `<1/4` estimate is assumed.

## Allowed inputs

- R14 exact reductions and its proved physical signs, including positivity
  of `X,W_i,U_i,H_i,L_i` on the retained branch.
- Exact algebraic transformations reproduced in `exact_checker.py`.
- Arb directed ball arithmetic with exact dyadic box endpoints.

## Forbidden substitutes

- Floating-point sampling as proof.
- The false cross-only relaxation.
- Replacing the full common-angle equations by a rational `T` envelope and
  tangent-convexity slacks.
- Propagating this compact result to any omitted boundary collar.

## Completion and non-completion

This route is complete exactly when every dyadic subbox is either proved to
contain no retained physical point or has all four coefficient gaps bounded
strictly above zero, with no unresolved boxes.  It does **not** complete the
global `0<k,t,y<1` theorem.  The collars

```text
k<1/64, k>63/64, t<1/64, t>63/64,
y<1/64, y>63/64,
```

and all of their intersections remain open.
