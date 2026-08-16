RIGOROUS_PARTIAL_RESULT

# Determinant-parity calibration for the physical minimum event matrix

## 0. Statement and scope

Fix finite `R>1`, an integer `n>=2`, and an arbitrary possibly asymmetric
premise-complete event-transverse common-terminal minimum-law relay root with
`m=2n` events.  In the relative quotient used by the accepted physical
continuant theorem, let `L_-` be its `(m-1)`-by-`(m-1)` path matrix.

Split the physical internal edges into the `n` positive odd edges and the
`n-1` negative even edges, and define the dual negative-edge Schur matrix
`H` below.  Then

```text
sign det(L_-)=sign det(H).                            (0.1)
```

Here `sign(0)=0`.  Consequently the exact local orientation required by the
accepted R7 bridge is `det(H)>0`.  For `n=2`, `H` is scalar and this agrees
with `H>0`; for `n>=3`, determinant positivity is strictly weaker than
positive definiteness.  The result does not prove `det(H)>0`, reflection
symmetry, root uniqueness, or existence.

## 1. Canonical physical input and self-contained matrix definitions

The accepted claim `CLM-NGE2-MPO3A-PHYSICAL-CONTINUANT-R7` gives positive
event coefficients

```text
a_i>0,                      i=1,...,m,
```

and the physical relative path matrix

```text
(L_-)_(ii)     =1/a_i+1/a_(i+1)+K_i,
(L_-)_(i,i+1) =-1/a_(i+1),                            (1.1)
```

for `i=1,...,m-1`.  For completeness, the physical internal-edge
coefficient is

```text
K_i={sin(theta_i)+mu sin(mu theta_i)}
    /{sqrt(rho_i) U_i U_(i+1)}.                       (1.2)
```

The trusted internal-phase theorem gives `0<theta_i<pi/mu`, so the numerator
in (1.2) is strictly positive.  The trusted alternating minimum event/nodal
allocation gives `sign(U_i U_(i+1))=(-1)^(i+1)`.  Therefore

```text
sign(K_i)=(-1)^(i+1):
K_i>0 for odd i,          K_i<0 for even i.           (1.3)
```

No `K_i` vanishes in the premise-complete event-transverse physical scope.

Define

```text
D=diag(a_1,...,a_m)>0,
K=diag(K_1,...,K_(m-1)),
```

and let `B` be the `(m-1)`-by-`m` oriented path-incidence matrix whose
`i`-th row is `e_i^T-e_(i+1)^T`.  Then (1.1) is exactly

```text
L_-=K+B D^(-1) B^T.                                  (1.4)
```

Define its algebraic dual event matrix

```text
M=D+B^T K^(-1)B.                                     (1.5)
```

Let `B_o` contain the odd rows of `B`, `B_e` the even rows, and put

```text
K_o=diag(K_i: i odd)>0,
W=diag(-K_i: i even)>0,
P=D+B_o^T K_o^(-1)B_o>0,
C=B_e.                                               (1.6)
```

The dimensions are

```text
B_o: n by 2n,        C: (n-1) by 2n,
P: 2n by 2n,         W,H: (n-1) by (n-1).
```

Equations (1.3), (1.5), and (1.6) give the exact split

```text
M=P-C^T W^(-1)C,          H=C P^(-1)C^T-W.           (1.7)
```

Thus every matrix used below is defined directly in this package.  The only
physical import is the accepted R7 representation (1.1), the trusted phase
range, and the trusted alternating event/nodal allocation used to derive
(1.3).

## 2. First determinant identity

Sylvester's identity `det(I+XY)=det(I+YX)` applied to (1.5) gives

```text
det(M)
 =det(D) det(I+D^(-1)B^T K^(-1)B)
 =det(D) det(I+K^(-1)B D^(-1)B^T)
 ={det(D)/det(K)} det(K+B D^(-1)B^T)
 ={det(D)/det(K)} det(L_-).                          (2.1)
```

There are exactly `n-1` negative diagonal entries of `K`, so

```text
sign det(K)=(-1)^(n-1).                              (2.2)
```

Since `det(D)>0`, (2.1)--(2.2) imply

```text
sign det(M)=(-1)^(n-1) sign det(L_-).                (2.3)
```

This formula remains valid if either displayed determinant is zero.

## 3. Dual Schur determinant identity

Use (1.7), `P>0`, `W>0`, and Sylvester's identity again:

```text
det(M)
 =det(P) det(I-P^(-1)C^T W^(-1)C)
 =det(P) det(I-W^(-1)C P^(-1)C^T)
 ={det(P)/det(W)} det(W-C P^(-1)C^T)
 =(-1)^(n-1){det(P)/det(W)}det(H).                   (3.1)
```

Both `det(P)` and `det(W)` are strictly positive.  Therefore

```text
sign det(M)=(-1)^(n-1) sign det(H).                  (3.2)
```

Comparing (2.3) and (3.2) proves (0.1).

## 4. Consequence for the minimum frontier

The accepted R7 orientation bridge states, in this same relative quotient,

```text
det(L_-)>0  iff  J<0  iff  partial_q A_n<0.          (4.1)
```

By (0.1), its exact matrix requirement is therefore

```text
det(H)>0.                                             (4.2)
```

The previously pursued complementary-inertia condition `H>0` implies
(4.2), but is not necessary when `dim(H)=n-1>=2`.  This calibrates the
minimum local-orientation obligation without solving it.

## 5. Audits

- **Definition audit: PASS.**  All matrices, dimensions, incidence signs,
  and odd/even partitions are defined in Section 1.  The permanent common
  scaling field is absent because `L_-` is the accepted R7 relative matrix.
- **Logic audit: PASS.**  Both determinant identities are exact and include
  the zero-determinant case.  No inertia conclusion is inferred from a
  determinant sign.
- **Parity audit: PASS.**  The internal path has `2n-1` edges: `n` positive
  odd edges and `n-1` negative even edges.  The two factors
  `(-1)^(n-1)` cancel exactly.
- **Boundary audit: PASS.**  The statement is conditional on a
  premise-complete event-transverse physical root; this does not assume
  `partial_q A_n!=0`.  `R=1`, grazing, collided
  events, incomplete words, and zero edge coefficients are outside scope.
- **Adversarial audit: PASS.**  For `n>=3`, matrices with positive
  determinant and mixed inertia are allowed.  The package does not replace
  `det(H)>0` by the stronger and still open `H>0`.

```text
determinant-parity identity: PROVED
det(H)>0 on every physical minimum root: OPEN
global minimum reflection symmetry: OPEN
unresolved_obligations_for_stated_identity: []
```
