PARTIAL

# W15 acute-threshold and collar falsification result

## Bound-input verification

All six packet inputs were verified before use. Their SHA-256 values, in packet order, are

```text
67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192
a24a0fe82e19ef6a1aeb2e29c2379bb2f8793818940d43df9d87b9abd14ef1dc
6ecc0ae44f6841414a8a8be8077ed919f1d66d285dc66abbdc79f85660c44d6d
2257a61c95cdcfa58b12cae577c5097ea4f124cd5d6077b6ebe550eb0779f8ed
bb1207baf181f37459345ed3cff4deb560b5c0acc18fdc3952b8410ffb6bd820
```

Every comparison returned equality.

## Outcome separation

- Strong max threshold `(T)`: not refuted. It is proved strictly in the full degenerate collar described below.
- Complete mass conclusion: not refuted. The same collar is proved to have strictly negative normalized mass residual, so it contains no complete tuple.
- Complete `KP-DET`: not refuted and not proved. A counterexample to `(T)` was not found, and no complete tuple with `q>E` was found.
- Floating-point searches below are `EVIDENCE` only and are not used in the collar theorem.

## STRICT collar classification

Put

```text
t=pi-alpha,
h=pi/2-theta,
z=1/m in (0,1),
c0=2/3.
```

Consider any sequence of exact strict-modal, common-`beta`, positive-lock acute tuples satisfying the accepted intrinsic angle definitions and

```text
t->0,
h->0,
c->c0.
```

The sequence may have arbitrary `m>1`, including `m->1+` or `m->infinity`. Then, uniformly after compactifying by `z in [0,1]`,

```text
h/t=1+o(1),
c=c0+[2(1-z^2)/(3 pi)]t+o(t),
beta=2zt(1+o(1)).                                  (C1)
```

For the accepted `sigma`, `D`, `q`, and `E`, define the two threshold margins

```text
TA=D-(m^2-1)(1-c^2)sin(A)^2,
Td=D-(m^2-1)(1-c^2)sin(d)^2.
```

Then

```text
t^2(q-E)=sqrt(3)/6+o(1),
TA=4/9+o(1),
Td=4/9+o(1).                                       (C2)
```

Thus every sufficiently small exact collar tuple has

```text
q>E,
D>(m^2-1)(1-c^2)max{sin(A)^2,sin(d)^2}.
```

In particular, `(T)` is true with a fixed positive margin in this collar. The coefficient dictionary then gives

```text
Acoef<0,
Bcoef<0,
Hcoef<0.
```

The `Bcoef` sign also follows directly from `sigma->infinity`, hence `sigma>1/c` eventually.

### Exact normalized mass residual

Let

```text
Mmass=
 alpha[e-JA/m^2]
 +beta[e-JA]/m
 +theta[sin(d)^2/sin(A)^2][e-Jd/m^2],
e=1-c^2.
```

This is the exact mass left side divided by the positive factor `s^2 X^2`. Indeed, the norm of the accepted first transfer pair gives

```text
X^2=P/(1+m^2 x^2),
cos(theta)^2/X^2=sin(d)^2/sin(A)^2.
```

The same uniform expansion gives

```text
t^2 Mmass=-2 pi/3+o(1).                             (C3)
```

Hence `Mmass<0` throughout a sufficiently small collar. No complete mass tuple can approach this boundary. The collar has `q>E`, equivalently `G<0`, only before imposing the exact mass equation. It is therefore not a counterexample to complete-system `G>=0` and not a counterexample to `KP-DET`.

### Proof of the uniform expansion

Define

```text
p_z(r)=atan(z tan(r))/z,
p_0(r)=tan(r).
```

This is smooth in `(z,r)` on a fixed neighborhood of `z in [0,1]` and `r in {0,pi/3}`. The four acute angles are exactly

```text
A=z p_z(t),
B=z p_z((1-c)pi+ct),
d=z p_z(h),
g=z p_z(c(pi/2-h)).
```

After division by `z`, common orientation is

```text
p_z((1-c)pi+ct)-p_z(c(pi/2-h))-c[p_z(t)+p_z(h)]=0. (C4)
```

Writing `S_z(r)=sin(z p_z(r))/z`, with the smooth extension `S_0(r)=p_0(r)`, the positive lock is the denominator-free equation

```text
S_z((1-c)pi+ct)S_z(h)
 =S_z(c(pi/2-h))S_z(t).                             (C5)
```

Uniform Taylor expansion of `(C4)-(C5)` first gives `c-c0=O(t+h)`, then `h/t=1+o(1)`. Since

```text
p_z'(pi/3)=4/(1+3z^2),
```

the linear part of `(C4)` gives the second formula in `(C1)`. The beta formula follows from `p_z(t)=t+O(t^3)`.

At the collar base point, put

```text
p=atan(sqrt(3)z),
S=sin(p),
C=cos(p),
Q0=C^2+z^(-2)S^2.
```

The expressions extend continuously to `z=0`, and direct substitution in the accepted denominator-safe formulas gives

```text
lim t^2(q-E)=c0 (S/z)C/Q0.
```

Because

```text
S/z=sqrt(3)/sqrt(1+3z^2),
C=1/sqrt(1+3z^2),
Q0=4/(1+3z^2),
```

the limit is identically `sqrt(3)/6`, proving the first part of `(C2)` uniformly in `z`. Also `sigma^(-2)=O(t^2)` and

```text
(m^2-1)sin(A)^2=(1-z^2)t^2+o(t^2),
(m^2-1)sin(d)^2=(1-z^2)h^2+o(t^2),
```

which proves the two threshold limits. Finally,

```text
JA/m^2=c0^2/t^2+O(1/t),
Jd/m^2=c0^2/h^2+O(1/t),
sin(d)^2/sin(A)^2=(h/t)^2[1+o(1)].
```

The `alpha` and `theta` mass terms therefore contribute `-pi c0^2/t^2` and `-(pi/2)c0^2/t^2`; the beta term is only `O(1/t)`. This proves `(C3)` since `(3pi/2)c0^2=2pi/3`.

## Bounded floating-point search, EVIDENCE

All calculations in this section used IEEE binary64 and SciPy `1.15.3`. They are non-exhaustive `EVIDENCE`.

### Acute branch scan

With PCG64 seed `20260901`, `360` pairs were sampled with log-uniform

```text
1.001<=m<=1000
```

and uniform

```text
0.666667<=c<=0.9995.
```

For each pair, two bounded least-squares starts solved `(C4)-(C5)`. Residual tolerance was `1e-8`; strict modal, acute, common-`beta`, positive-lock, and `sigma>1/c` checks were imposed. There were `605` admissible convergences, including repeated convergence to the same root, and `75` had `q-E>1e-8`. Among those `75`, the smallest observed threshold margin was

```text
min(TA,Td)=0.44650316370652032.
```

The smallest observed positive `q-E` was

```text
q-E=0.016673604190749813,
TA=0.45918454661640129,
Td=0.47301811448099113,
Mmass=-27.51560981555626.
```

No strong-threshold counterexample was observed.

### Complete mass scan

For `80` logarithmically spaced values

```text
1.0005<=m<=1000,
```

five bounded starts solved common orientation, positive lock, and `Mmass=0` simultaneously in `(c,t,h)`. There were `398` admissible convergences, including duplicates, and none had `q-E>0`. The largest observed value was approximately

```text
q-E=-6.866719279e-5
```

at

```text
m=1000,
c=0.9999567841,
t=1.5650006606,
h=0.78251112579.
```

This does not certify complete-system `q<=E`.

## First certification gap and plan

The first gap is an exhaustive enclosure of the exact acute solution manifold away from the proved collar. The binary64 convergences do not exclude missed components, near-singular roots, or a narrow intersection of `q>E` with either `TA<=0`, `Td<=0`, or `Mmass=0`.

A certification pass should use outward-rounded interval arithmetic in compact variables `(z,c,t,h)` and the denominator-free equations `(C4)-(C5)`:

1. Remove a small `t` collar using `(C1)-(C3)` with explicit Taylor remainder bounds.
2. Subdivide the remaining compact domain and reject boxes by interval signs for `(C4)-(C5)`.
3. Where the `(t,h)` Jacobian is interval-invertible, use a parameterized interval Newton or Krawczyk operator over `(z,c)` to enclose the whole two-dimensional branch, then bound `q-E`, `TA`, and `Td` on each enclosure.
4. For the complete mass question, add `Mmass=0`, validate the resulting one-dimensional set by a rank-certified interval Newton step, and prove `q-E<0` on every segment.
5. Treat the observed escape toward `z=0`, `c=1` by a separate blow-up chart before claiming global coverage. This large-`m`, right-boundary chart is the first unresolved boundary certification problem after the collar handled here.

Exact gap: `(T)` and complete-system `q<=E` remain open outside the proved collar; no exact or interval-certified counterexample was obtained.

decision_delta: Proved a uniform all-`m` blow-up classification at the `(pi,0,pi/2,2/3)` collar, where `q-E~sqrt(3)/(6t^2)>0`, both strong-threshold margins tend to `4/9`, and the normalized mass residual is `~-2pi/(3t^2)<0`; therefore this collar supports `(T)` and cannot refute complete `KP-DET`, while bounded EVIDENCE found no counterexample elsewhere.
