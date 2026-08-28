INDEPENDENTLY_AUDITED_PROOF

# Degree-spectrum audit

## Verdict

`PASS`.

For every `c>0` and integer `s>=4`, with `r=floor(s/2)`, the claimed spectrum is exact:

```text
{deg p: 0!=p in C[x] intersect D(K_c^(s/2))}
= {0,1} union {N:N>=2r+2}.
```

There is no failing step. The parity-triangular argument closes the general-r gap left open in
the older hidden-gold run. This is a posthoc audit and is excluded from every benchmark arm
score.

## Exact operator-domain trace characterization

Write `A=K_c`, `T=c-D^2`, and

```text
delta(f)=(f(1)-f(-1))/2.
```

The closed form of `A` has domain `H^1[-1,1]` and satisfies

```text
a(f,f)=c||f||_2^2+||f'-delta(f)||_2^2.
```

In particular `A>=cI`, `D(A^(1/2))=H^1`, and the spectral calculus gives

```text
D(A^r)={f:T^j f is in D(A), 0<=j<r},
D(A^(r+1/2))={f in D(A^r):A^r f is in D(A^(1/2))}.
```

For a polynomial, the last condition in the second line is automatic once the first `r`
operator-domain conditions hold, because `A^r p=T^r p` is again a polynomial and hence is in
`H^1`. Therefore, for both `s=2r` and `s=2r+1`,

```text
p in C[x] intersect D(A^(s/2))
iff T^j p satisfies the Krein boundary conditions for 0<=j<r.        (1)
```

The two endpoint signs produce exactly the claimed parity split. If `e` is even, then
`delta(e)=0`, `e'(-1)=-e'(1)`, and the two boundary conditions are equivalent to `e'(1)=0`.
If `o` is odd, then `delta(o)=o(1)`, `o'(-1)=o'(1)`, and both conditions are equivalent to
`o'(1)=o(1)`. For a general polynomial `p=e+o`, adding and subtracting the two endpoint
conditions shows that they hold if and only if these even and odd conditions hold separately.
Thus opposite parities cannot cancel a boundary defect.

For `0<=j<r`, expand `T^j` by the binomial theorem. On the even part,

```text
(T^j e)'(1)
= sum_{k=0}^j binom(j,k)c^(j-k)(-1)^k e^(2k+1)(1).
```

On the odd part,

```text
(T^j o)'(1)-(T^j o)(1)
= sum_{k=0}^j binom(j,k)c^(j-k)(-1)^k
  [o^(2k+1)(1)-o^(2k)(1)].
```

Each system is lower triangular in the raw traces, with diagonal coefficient `(-1)^j`.
Consequently (1) is equivalent to the c-independent constraints

```text
E_j(e):=e^(2j+1)(1)=0,
O_j(o):=o^(2j+1)(1)-o^(2j)(1)=0,
0<=j<r.                                                        (2)
```

This proves the exact trace characterization for both even and odd `s`; no unmentioned
regularity or c-dependent condition remains.

## Exclusion of every degree from 2 through 2r+1

Suppose first that an even polynomial has exact degree `2m`, where `1<=m<=r`. In the equation
`E_(m-1)=0`, the derivative of order `2m-1` annihilates every lower even monomial, while its
value on the leading monomial `x^(2m)` is `(2m)!`. The leading coefficient must therefore be
zero, a contradiction.

Now suppose that an odd polynomial has exact degree `2m+1`, where `1<=m<=r`. In the equation
`O_(m-1)=0`, all odd monomials below `x^(2m-1)` vanish. The contribution of `x^(2m-1)` is also
zero because its derivatives of orders `2m-1` and `2m-2` both equal `(2m-1)!` at 1. The
contribution of the leading monomial is

```text
(2m+1)!/2!-(2m+1)!/3!=(2m+1)!/3 != 0.
```

Hence its leading coefficient must also vanish. Since the constraints split by parity, lower
terms of the opposite parity cannot change either conclusion. Thus no exact degree in
`{2,...,2r+1}` occurs.

## Existence in every degree at least 2r+2

For the even correction space

```text
V_e=span{x^2,x^4,...,x^(2r)},
```

consider the `r` by `r` matrix `M_e=(E_j(x^(2k)))`, with `0<=j<r` and `1<=k<=r`.
Its entries vanish for `k<=j`, and the first possible entry in row `j`, at `k=j+1`, is
`(2j+2)!`. Hence `M_e` is triangular with nonzero diagonal and has rank `r`.

For the odd correction space

```text
V_o=span{x^3,x^5,...,x^(2r+1)},
```

the matrix `M_o=(O_j(x^(2k+1)))` has entries zero for `k<=j`. At `k=j+1`, its diagonal
entry is

```text
(2j+3)!/2!-(2j+3)!/3!=(2j+3)!/3 != 0.
```

Thus `M_o` also has rank `r`.

Let `N>=2r+2`. If `N` is even, solve the full-rank even system for `q in V_e` such that
all `E_j(x^N+q)` vanish. Since `deg q<=2r<N`, the corrected polynomial has exact degree `N`.
If `N` is odd, necessarily `N>=2r+3`; solve analogously for `q in V_o`. Again the degree is
unchanged. This constructs an admissible polynomial of every degree at or above the threshold.

Finally, every nonzero constant has degree 0, and every affine polynomial with nonzero slope has
degree 1 and satisfies the Krein condition at every iterate. This completes both inclusions.

## Four mandatory audits

### Definition audit

`PASS`. The audit uses the operator power domain, not the abstract polynomial completion. The
spectral recursion is stated for the positive self-adjoint realization, and the polynomial
differential expression is used only after the preceding iterates satisfy the operator boundary
conditions. Even and odd parts are shown to decouple from the actual two-endpoint Krein
condition. The trace functionals, derivative orders, and degree convention for nonzero
polynomials match the claim.

### Logic audit

`PASS`. Necessity follows from the domain recursion and the highest surviving raw trace.
Sufficiency follows from invertibility of explicit finite triangular matrices. The correction
uses only strictly lower-degree monomials, so it cannot cancel the prescribed leading term.
Both implications and both parities are closed for every `r=floor(s/2)`.

### Boundary audit

`PASS`. Constants and affine polynomials are included. For the minimal cases `s=4` and `s=5`,
`r=2`, the forbidden degrees are exactly 2, 3, 4, and 5. The first two permitted higher degrees
are witnessed by

```text
p_6=x^6-5x^4+7x^2,
p_7=x^7-(21/5)x^5+(27/5)x^3.
```

They satisfy `E_0=E_1=0` and `O_0=O_1=0`, respectively, so both lie in `D(K_c^2)` and, because
`T^2p` is polynomial, also in `D(K_c^(5/2))`, for every `c>0`. These examples attain the sharp
thresholds 6 and 7 in the two parities.

### Adversarial audit

`PASS`. The attack checked possible cancellation between parities, cancellation by the next
lower odd monomial, both endpoint signs, the smallest allowed and forbidden degrees, and the
dependence on `c`. The apparent odd cancellation at degree `2m-1` is real, but the leading
degree `2m+1` has coefficient `(2m+1)!/3`, so it cannot evade the trace. All powers of `c`
disappear only after an invertible triangular change of trace coordinates, which justifies the
claimed c-independence rather than assuming it.

## Smallest failing step

None. `critical_errors=[]` and `gaps=[]`.

## Provenance and reproducibility

- Network access: not used.
- Frozen task SHA256: `359D335803EAE43F45120E3CA3995B8F12EC2F98B357E2B10116EAFE2D8C6332`.
- Candidate tool SHA256: `59877D91F84A1D94903595EED7E35ECCCCAE23BB9591FA7FDA6AEE6D0374DD8F`.
- Prior Arm B audit SHA256: `486CE4FFAC8544990BA6450363F738E1CBA631E98CE0C8F820DD434A5E33C4BE`.
- The hidden-gold record at commit `0f9b2b0` was inspected only after the independent derivation;
  it records this same general-r statement as an open evidence-level gap and was not used as a
  proof premise.
- Novelty status: `UNKNOWN`. This audit establishes correctness, not literature novelty.
