CANDIDATE_COMPLETE_PROOF

# R15: exact minimum-law nonexistence for `mu=2` and every `n>=3`

## 0. Result and scope

Fix a finite `R>1`, put `r=sqrt(R)>1`, and set `mu=2`.

> **Candidate theorem.** For every integer `n>=3`, no strict,
> premise-complete, transverse, common-terminal full-relay root with `2n`
> events obeys the minimum saturation law.

The result allows arbitrary asymmetry.  It is a direct internal-composition
obstruction; neither reflection, the endpoint equations, the global norm
equation, nor the desired inertia sign is assumed.  The theorem is only for
the minimum law and only for `mu=2`.  It does not cover `n=2`, the maximum
law, general `mu`, or boundary/grazing words.

This route is bound to canonical Blueprint SHA-256
`0120d1fb32af1a30449575995efccb6d1afcce416ee671ad00a5f296400fd799`
and inventory SHA-256
`b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.

## 1. Arbitrary word and event-amplitude ratios

Let the `2n` simple relay events be

```text
tau_1<...<tau_(2n).
```

There are `2n-1` internal cells

```text
I_j=(tau_j,tau_(j+1)),       1<=j<=2n-1.
```

The trusted structure and sharp-phase theorems give the same allocation for
every possibly asymmetric root:

```text
j odd:  positive internal cell, 0<theta_j<pi/3,
j even: negative internal cell, pi/3<theta_j<pi/2.       (1.1)
```

Define

```text
x_j=tan(theta_j/2),       j odd,
y_j=tan(theta_j/2),       j even.
```

Then

```text
0<x_j<1/sqrt(3)<y_j<1.                              (1.2)
```

Put

```text
A_i=U(tau_i),
z_j=A_(j+1)/A_j.                                    (1.3)
```

Every `A_i` is nonzero.  Indeed, at an internal event `U=V=0` would force
both the switching function and its first derivative to vanish, contrary to
transversality.  Hence every ratio in (1.3) and every reciprocal used below
is defined.

## 2. Standalone one-interface contraction

For a physical positive cell with half-angle tangent `x`, followed by a
negative cell with half-angle tangent `y`, solve the two continuous-momentum
equations after normalizing the shared event amplitude to one.  The two cell
ratios are

```text
a=-y(x-y)(x+y)(1+x^2)/D_a,
b=N_b/[r x(x-y)(x+y)(1+y^2)],                       (2.1)

D_a=3r x^3y^2-rx^3-3rxy^2+rx
    +x^4y+2x^2y^3-4x^2y+y,

N_b=2r x^3y^2+rxy^4-4rxy^2+rx
    +3x^2y^3-3x^2y-y^3+y.
```

The companion exact checker reconstructs (2.1) from the raw half-angle
oscillator matrices and obtains zero residual for both amplitudes.  Thus
`a` is the forward positive-cell ratio and `b` the following negative-cell
ratio; these meanings are not assigned from their signs.

For completeness, the contraction is reproved here.  Put

```text
X=x^2,       Y=y^2,
kappa=r x(3Y-1)/[y(1-3X)],

C=(3Y-1)(1-Y),
E=C+2Y(Y-X),
kappa_0=sqrt(X/Y)(3Y-1)/(1-3X),
kappa_N=C/E.                                        (2.2)
```

The strict physical branch has

```text
1/3<Y<1,
0<X<(1-Y)^2/(4Y),
kappa_0<kappa<kappa_N.                              (2.3)
```

Here `kappa=r kappa_0`, so the lower bound is exactly `r>1`.  The upper
bound is the physical `b<0` boundary: direct substitution in (2.1) gives

```text
N_b=y(1-3X)(C-kappa E)/(3Y-1),                      (2.4)
```

and all factors outside the last bracket are positive.  The feasibility
condition in (2.3) is also forced by the nonempty contrast interval.  Exact
factorization gives

```text
Y(1-Y)^2(1-3X)^2-XE^2
 =-(X-Y)(XY-1)[4XY-(1-Y)^2].                       (2.5)
```

Since `X<1/3<Y<1`, the inequality `kappa_0<kappa_N` is equivalent to the
strict positivity of the left side of (2.5), and hence to
`4XY<(1-Y)^2`.

Substitution in the remaining denominator gives

```text
D_a=y[X^2+2XY-4X+1-kappa(1-X)(1-3X)].             (2.6)
```

Its zero is

```text
kappa_D=(X^2+2XY-4X+1)/[(1-X)(1-3X)],

kappa_D-kappa_N
 =2(Y-X)^2(1-XY)/[(1-X)(1-3X)E] >0.               (2.7)
```

Thus every physical `kappa<kappa_N` also satisfies
`kappa<kappa_D`, and (2.6) gives `D_a>0`.  Because `x<y`, the numerator of
`a` in (2.1) is positive, so `a>0`.

Direct subtraction gives

```text
a-1=(1-x^2)T/D_a,

T=y[kappa(1-3X)+2X+Y-1].                           (2.8)
```

At the upper physical boundary,

```text
kappa_N(1-3X)+2X+Y-1
 =-(Y-X)[(1-Y)^2-4XY]/E <0.                        (2.9)
```

Since the bracket is strictly increasing in `kappa`, equations
`kappa<kappa_N` and `1-3X>0` make the bracket in (2.8) strictly negative.
Therefore `T<0`.  Together with `1-x^2>0` and `D_a>0`, (2.8) proves

```text
0<a(x,y,r)<1                                      (2.10)
```

on every strict physical minimum-law `mu=2` positive-negative interface.

## 3. The two interface orientations

The only delicate point in the generalization is the left interface of an
internal positive cell.  Both relay equations are time-reversal invariant:

```text
U_tt=-rho U,       V_tt=-4rho V.                   (3.1)
```

For the minimum law, `rho=1` on a positive cell and `rho=R` on a negative
cell.  Hence a forward negative-positive material sequence `(R,1)` becomes
the canonical positive-negative sequence `(1,R)` after reversal; the
contrast remains the same `r=sqrt(R)` rather than becoming `1/r`.

For either oscillator the constant-cell transfer matrix is

```text
M_omega(t)=[ cos(omega t)       sin(omega t)/omega ]
           [-omega sin(omega t) cos(omega t)       ].
```

With `J=diag(1,-1)`, exact multiplication gives

```text
J M_omega(t) J=M_omega(t)^(-1).                   (3.2)
```

Thus reversal preserves the positions, reverses both momenta, and turns a
physical negative-positive pair into the canonical positive-negative pair
with the same phases and the same `r`.  No material reciprocal or different
interface function appears.

Now take an odd internal index

```text
3<=j<=2n-3.                                        (3.3)
```

The right pair `(I_j,I_(j+1))` is already positive-negative.  By the
definition of `a,b`,

```text
z_j    =a(x_j,y_(j+1),r),
z_(j+1)=b(x_j,y_(j+1),r).                          (3.4)
```

The left pair `(I_(j-1),I_j)` is negative-positive.  Reverse this two-cell
segment.  Its event amplitudes, in reversed order, are

```text
A_(j+1), A_j, A_(j-1).
```

Therefore the two reversed ratios are

```text
A_j/A_(j+1)=1/z_j,
A_(j-1)/A_j=1/z_(j-1).
```

Applying the same canonical positive-negative map gives

```text
1/z_j    =a(x_j,y_(j-1),r),
1/z_(j-1)=b(x_j,y_(j-1),r).                        (3.5)
```

Equations (3.4)--(3.5) prove the exact positive-cell compatibility

```text
a(x_j,y_(j-1),r)*a(x_j,y_(j+1),r)=1.              (3.6)
```

This also fixes the companion negative-cell compatibility, for every even
`j`:

```text
b(x_(j-1),y_j,r)*b(x_(j+1),y_j,r)=1.              (3.7)
```

The full internal word has `n-2` equations of type (3.6) and `n-1` equations
of type (3.7).  Their total is `2n-3`, exactly the number of overlaps between
the `2n-2` adjacent two-cell descriptions.  Hence no interface or amplitude
ratio has been omitted or counted twice.

## 4. Arbitrary-`n` contradiction

For every `n>=3`, the fixed index `j=3` satisfies (3.3): the cells
`I_2,I_3,I_4` exist and have signs negative-positive-negative.  Both adjacent
two-cell segments are physical interfaces inherited from the assumed full
trajectory.  Applying (2.10) twice gives

```text
0<a(x_3,y_2,r)<1,
0<a(x_3,y_4,r)<1.                                  (4.1)
```

Their product is strictly between zero and one, contradicting (3.6).  Thus
the internal amplitude system is empty for every `n>=3`.  A fortiori it
cannot be completed by the two common-terminal endpoint equations or the
global norm equation.  This proves the candidate theorem.

No induction is needed: the same three-cell obstruction occurs verbatim in
every longer word.  In fact every odd `j` in (3.3) supplies its own
contradiction.

## 5. Boundary, parity, endpoint, and law audit

### The minimal exception `n=2`

For `n=2`, the internal word has cells `I_1,I_2,I_3`.  There is one negative
cell compatibility of type (3.7), but no odd positive cell with two negative
neighbors.  The set in (3.3) is empty.  Therefore this proof makes no claim
for `n=2`, consistently with the established nonvacuous `mu=2,n=2` theory.

### Endpoint cells and common terminal

The cells from the left common zero to `tau_1` and from `tau_(2n)` to the
right common zero are not among the internal cells and need not satisfy the
sharp threshold (1.1).  They affect only the endpoint equations and the
global norm balance.  Since the contradiction uses only `I_2,I_3,I_4`, no
endpoint choice can repair it.

### Reflection and global sign

Reflection sends the internal index `j` to `2n-j`, which has the same parity.
It also replaces cell ratios by reciprocals in reversed order, exactly as in
(3.5).  Thus reflection creates no exceptional orientation.  Multiplying
both eigenfunctions by `-1` leaves every ratio `z_j` unchanged.

### Relay-law scope

The proof uses the minimum-law material allocation behind (2.1)--(2.4).
It verifies both traversal orientations of that law, positive-negative and
negative-positive.  It does not assert the same contraction for the maximum
law, where the material allocation and interface formula must be rederived.

### Strict boundaries

The argument excludes `R=1`, collapsed feasibility
`4XY=(1-Y)^2`, `b=0`, `a=1`, phase endpoints, grazing, colliding events,
zero-length cells, and endpoint escape.  These are outside the stated
premise-complete transverse scope and are not promoted by continuity.

## 6. Verification and remaining status

The exact checker independently performs all of the following:

1. reconstructs `a,b` from the two raw momentum equations;
2. verifies (2.5)--(2.9) and the denominator gap with zero residual;
3. verifies the transfer time-reversal identity (3.2);
4. generates the forward, reversed, and compatibility index tables for
   `2<=n<=12`, checking counts and the `n=2/n=3` threshold.

The finite table is only an adversarial indexing test.  Equations
(3.3)--(3.6) provide the arbitrary-`n` proof.

There is no unresolved mathematical obligation in this candidate package.
It remains `CANDIDATE_COMPLETE_PROOF` until an uninvolved reviewer passes the
definition, logic, boundary, and adversarial audits on the frozen hashes.
