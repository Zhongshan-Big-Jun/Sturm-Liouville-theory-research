# Exact full-interval relay reduction for multiphase O3a

## 1. Scope

Fix an integer `n>=2`, a finite contrast `R>1`, and one saturation sign
`e in {max,min}`.  This note concerns the complete self-consistent class; no
reflection symmetry is assumed.  It proves an exact finite-dimensional
equivalence, not uniqueness.

The accepted structure theorem is used in the forward direction only to
identify the complete switch set and endpoint material.  The reverse
direction independently recovers those facts from Sturm oscillation,
Wronskian monotonicity, and the relay energy.

## 2. Relay definition

For parameters

```text
mu>1, q>0, L>0,
```

let `(U,V,rho)` be a finite-switch piecewise-classical solution on `[0,L]`
of

```text
U_tt=-rho U,          U(0)=0, U_t(0)=1,
V_tt=-mu^2 rho V,     V(0)=0, V_t(0)=q,              (2.1)
S=U^2-mu^2 V^2.                                      (2.2)
```

The relay law holds almost everywhere:

```text
max: rho=R on {S>0}, rho=1 on {S<0},
min: rho=1 on {S>0}, rho=R on {S<0}.                 (2.3)
```

Values of `rho` on `{S=0}` are irrelevant.  At this definition stage no
event count, transversality, endpoint phase, or symmetry is imposed.  Put

```text
I_U(T)=integral_0^T rho U^2 dt,
I_V(T)=integral_0^T rho V^2 dt.                       (2.4)
```

Let `Theta_U,Theta_V` be the continuous Prüfer lifts of
`atan2(U,U_t)` and `atan2(V,V_t)`, both starting from zero.

A relay triple means the labelled finite-switch trajectory
`(mu,q,L;U,V,rho)`, modulo a.e. changes of `rho`, with the orientation fixed
by `U_t(0)=1` and `V_t(0)=q>0`.  At a solution of (3.1), (3.8) below gives
`q>1`, so `S<0` initially, and the quotient proof makes all events simple.
Cellwise IVP uniqueness and induction across those sign-changing events show
that fixed `(mu,q,L,R,e)` supports at most one such oriented trajectory.
Thus the trajectory-level equivalence below descends to a bijection with the
three scalar labels.

## 3. Full relay theorem

### Theorem 3.1 (three-scalar bijection)

Self-consistent `2n`-switch points of sign `e`, modulo a.e. equality and the
positive left orientation of both consecutive modes, are in bijection with
relay triples `(mu,q,L)` satisfying

```text
Theta_U(L)=n*pi,
Theta_V(L)=(n+1)*pi,
I_U(L)=I_V(L).                                        (3.1)
```

Every triple satisfying (3.1) automatically has

```text
q>1,                                                   (3.2)
```

and its switching function `S` has exactly `2n` simple zeros in `(0,L)`.
Thus neither the event count nor transversality is an extra premise in
Theorem 3.1.

### Forward proof

Let `rho(x)` be any self-consistent point and take the normalized,
left-oriented consecutive modes

```text
u=u_n, v=u_{n+1},
a=lambda_n, b=lambda_{n+1}, mu=sqrt(b/a),
A=u'(0)>0, q=v'(0)/u'(0), L=sqrt(a).                  (3.3)
```

With `t=sqrt(a)x`, define

```text
U(t)=sqrt(a)u(x)/A,  V(t)=sqrt(a)v(x)/A.              (3.4)
```

Then (2.1) holds and the physical switching function is

```text
a u^2-b v^2=A^2 S.                                    (3.5)
```

Hence self-consistency is exactly (2.3).  Sturm indexing gives the two
endpoint phases in (3.1).  Finally

```text
1=integral_0^1 rho u^2 dx=A^2 I_U(L)/a^(3/2),
1=integral_0^1 rho v^2 dx=A^2 I_V(L)/a^(3/2),         (3.6)
```

so the two relay integrals are equal.  The accepted structural theorem gives
the exact `2n` simple switch events, although this count will also follow in
the converse direction.

### Reverse proof

Conversely, suppose a relay triple satisfies (3.1), and write

```text
I=I_U(L)=I_V(L)>0.
```

The relay energy

```text
E=U_t^2+rho U^2-(V_t^2+mu^2 rho V^2)                 (3.7)
```

is constant on each material cell.  Its jump at a relay interface is
`Delta rho*S=0`, so it is global and `E=1-q^2`.  Integration by parts, using
the two endpoint phase conditions (hence `U(L)=V(L)=0`), gives

```text
integral U_t^2=I_U(L),
integral V_t^2=mu^2 I_V(L).
```

Therefore

```text
L(1-q^2)=2I-2mu^2 I,
L(q^2-1)=2(mu^2-1)I>0.                               (3.8)
```

This proves (3.2).  Now set

```text
a=L^2, b=mu^2 L^2, A^2=L^3/I,
x=t/L,
u(x)=A U(t)/L, v(x)=A V(t)/L, rho_x(x)=rho(Lx).       (3.9)
```

Equations (2.1) become

```text
-u''=a rho_x u,  -v''=b rho_x v,
u(0)=u(1)=v(0)=v(1)=0.                               (3.10)
```

Equation (3.9) and (2.4) give both weighted norms equal to one.  The lifted
phases in (3.1), together with regular Sturm oscillation, identify `a` and
`b` as `lambda_n(rho_x)` and `lambda_{n+1}(rho_x)`.  Equation (3.5), read in
reverse, makes (2.3) the required saturation law.

It remains only to show that no hidden relay pathology was admitted.
Because (3.8) gives `q>1`, the endpoint energy relation gives

```text
V_t(0)^2-U_t(0)^2=q^2-1,
V_t(L)^2-U_t(L)^2=q^2-1.                             (3.11)
```

Sturm nodal parity fixes the terminal derivative ratio to be negative, with
absolute value greater than one.  For

```text
W=V_t U-V U_t,
```

one has `W'=-(mu^2-1)rho U V`.  Strict interlacing of the now-identified
consecutive modes gives `W<0` in `(0,L)`.  Thus `V/U` is strictly decreasing
on every nodal interval of `U`.  Its endpoint ranges, together with (3.11),
show that

```text
S=U^2-mu^2 V^2
```

has exactly two zeros on each of the `n` nodal intervals of `U`, hence
exactly `2n` interior zeros.  At each crossing `V/U=+/-1/mu`, differentiation
shows `S'!=0`.  These are all the relay interfaces because (2.3) can change
material only when the sign changes.  The sign of `S` is negative on both
endpoint cells, so the endpoint materials and alternating word are exactly
the max or min word.  The reconstructed coefficient is therefore a member
of the frozen self-consistent class.

The transformations (3.3)--(3.4) and (3.9) are inverse, proving the
bijection.

## 4. Two-scalar zero-time formulation

For each selected relay chamber on which `q>0`, the finite effective material
word up to `max(T_U^(n),T_V^(n+1))` is constant, every encountered `S` event
is transverse, neither indexed zero-time endpoint coincides with an
unresolved grazing event, and the selected relay IVP branch and indexed
simple zero times depend continuously on `(mu,q)`, let

```text
T_U^(n)(mu,q)       = the n-th positive zero time of U,
T_V^(n+1)(mu,q)     = the (n+1)-st positive zero time of V.              (4.1)
```

On every such premise-complete chamber, Theorem 3.1 is equivalent to the two
equations

```text
A_n(mu,q)=T_U^(n)-T_V^(n+1)=0,                       (4.2)
B_n(mu,q)=I_U(T_U^(n))-I_V(T_U^(n))=0.               (4.3)
```

At a zero of (4.2), the common zero time is `L`; (4.3) is exactly the norm
condition.  Theorem 3.1 then supplies `q>1`, transversality, and the exact
event count.  Conversely every self-consistent point maps to a zero of
(4.2)--(4.3).

The union is taken over all such chambers.  At any common zero, Theorem 3.1
proves `q>1` and all `2n` events transverse, so the root lies on a
deterministic branch.  A global uniqueness proof must range over every
chamber and identify duplicate descriptions at overlapping chamber closures.
With this convention, this is an exact reduction of the full, potentially
asymmetric, `2n`-switch problem from `2n` switch coordinates plus spectral
variables to two scalar equations in `(mu,q)`.  The dependence on `n` occurs
only through the two zero indices.

## 5. Reflection and the remaining target

For a relay triple satisfying (3.1), put `p=U_t(L)` and `r=V_t(L)`.  The
reflected, positively reoriented trajectory is

```text
U#(s)=[-sign(p)] U(L-s)/|p|,
V#(s)=[-sign(r)] V(L-s)/|p|,
rho#(s)=rho(L-s),
q#=|r|/|p|>1.                                         (5.1)
```

Thus both modes use the same scale magnitude but independent harmless signs.
Their equations, `S`, norm equality, relay law, and indexed endpoint phases
are preserved.  Therefore uniqueness of (4.2)--(4.3) across all
premise-complete chambers would imply reflection symmetry and full
multiphase O3a.

No injectivity theorem is proved here.  The precise next obligation is:

```text
For every n>=2, R>1 and sign e, prove that (A_n,B_n) has exactly one zero
in its premise-complete finite-switch relay chambers, or certify two distinct
zeros with their indexed phases, norm equality, and relay sign law.
```

This obligation is lower-dimensional than `det D_x G_e!=0` and is logically
independent of an assumption that all solutions are symmetric.

## 6. Boundary and definition audit checklist

- `n=2` is included; the quotient count gives four simple events.
- `R->1+` is not replaced by `R=1`; at `R=1` material labels merge.
- Every finite `R>1` is admitted; no `R=infinity` claim is made.
- Point values of `rho` at `S=0` are a.e. irrelevant.
- Possible grazing in the initial relay definition is removed a posteriori
  at every zero of (3.1), rather than silently excluded from the target.
- The common endpoint `(U,V)=(0,0)` is not counted as an interior relay event.
- The two-scalar form is chamberwise because relay trajectories can change
  combinatorics away from actual solutions; a global proof must audit these
  chamber boundaries.
- No numerical computation is used in this derivation.

Epistemic status: `RIGOROUS_PARTIAL_RESULT`, pending independent audit.
