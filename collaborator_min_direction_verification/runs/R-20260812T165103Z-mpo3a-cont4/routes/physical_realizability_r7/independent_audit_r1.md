APPROVE

# Independent audit of the R7-R1 relative-continuant proof package

## 0. Exact binding and verdict

Audited immutable candidate:

```text
path:
  runs/R-20260812T165103Z-mpo3a-cont4/routes/
  physical_realizability_r7/derivation_r1.md
bytes: 10017
sha256: a949934f6bfb68af9cf87a0b245c868f706d4b15b98de3c7b48a3731b9dede89
```

Bound canonical snapshot:

```text
context_id: CTX-DEFAULT
blueprint_sha256:
  sha256:3e0839c6d73e194653314ae1c456bbc77899bdc279f171f590089ad9c0f38394
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

Verdict: **approve**.  There are no blocking issues.  The original audit's
scaling-direction objection is repaired: R1 explicitly works in relative
Jacobi variables, identifies the scaling line as the zero relative vector,
and states terminal degeneracy only for the distinguished non-scaling
`log(q)` line or for an additional mode after quotienting by scaling.

The following theorem has been independently recomputed and passes:

```text
w_m=sigma product_i(a_i) det(L_sigma),
w_m=-q sigma(R-1)J,
partial_q A_n=(q^2-1)w_m/(q p^2r^2),

J<0 iff det(L_sigma)>0
    iff sign(w_m)=sigma
    iff sign(partial_q A_n)=sigma.
```

This is an exact transverse-chamber reduction.  It proves neither the
universal determinant sign nor O3a.

## 1. Premise and definition audit

The package uses only the listed accepted full-relay, structure,
symplectic-endpoint, all-cell-phase, and hybrid-twist claims together with
the active self-consistency definition.  Their semantic hashes agree with
the bound canonical snapshot.  No open obligation or numerical observation
is used as a premise.

`CLM-NGE2-MPO3A-TRANSFER-OBSTRUCTION` has correctly been removed from the
proof inputs.  It is not needed to derive the recurrence, path matrix,
continuant, or causal binding.

The quantified scope is exact: finite `R>1`, `n>=2`, either relay sign, and
an arbitrary possibly asymmetric premise-complete transverse
common-terminal root with simple terminal zeros.  The package does not
silently assume reflection invariance, equal norm, or a phase ordering
beyond the accepted all-cell phase theorem.

## 2. Quotient and scaling-direction audit

For a fixed-Dirichlet initial-slope Jacobi field, signed symplectic pairing
with the scaling field is zero.  Hence the component Wronskians agree:

```text
w=Uu_t-U_tu=Vv_t-V_tv.
```

At a relay event the relative coordinate is

```text
d_i=u(t_i)/U_i-v(t_i)/V_i.
```

The scaling field has `u=U`, `v=V`, so `d_i=0` and `w_i=0` everywhere.
It is therefore exactly invisible in these relative coordinates.  R1 no
longer equates the existence of an arbitrary nonzero two-ended Dirichlet
field with `det(L_sigma)=0`.

The distinguished `log(q)` field is not a scaling field: before the first
event it has `u/U=0`, `v/V=1`, hence `d_1=-1`.  If its terminal Wronskian
vanishes, the simple terminal zeros and the accepted symplectic identity
force both terminal position variations to vanish.  Its initial slope
variation is linearly independent of the scaling variation, so this is
precisely an additional Dirichlet direction after quotienting the permanent
scaling line.

The quotient scope in Sections 1--3 therefore resolves the sole blocking
issue in `independent_audit.md`.

## 3. Recurrence and boundary-row audit

Exact saltation and cell propagation give

```text
w_i-w_(i-1)=-sigma a_i d_i,
d_(i+1)-d_i=K_iw_i,
a_i>0,
```

with every `K_i` finite and nonzero.  Eliminating `d_i` gives

```text
(w_i-w_(i-1))/a_i-(w_(i+1)-w_i)/a_(i+1)
  -sigma K_iw_i=0.                                    (A3.1)
```

For `W=(w_1,...,w_(m-1))`, the first row of (A3.1) has boundary source
`w_0/a_1=0`.  The last row expands as

```text
(L_sigma W)_(m-1)-w_m/a_m=0.
```

Thus the inhomogeneous equation is exactly

```text
L_sigma W=(w_m/a_m)e_(m-1),
```

with a positive, not negative, terminal source.  Equation (3.2) passes.

The initial data also pass:

```text
w_0=0,
d_1=-1,
w_1=(-sigma a_1)(-1)=sigma a_1.
```

## 4. Cofactor and continuant audit

Let `N=m-1`.  The off-diagonal entries of `L_sigma` are
`b_j=-1/a_(j+1)`.  The standard tridiagonal corner inverse is

```text
(L_sigma^(-1))_(1,N)
 =(-1)^(1+N) product_(j=1)^(N-1)b_j/det(L_sigma)
 =1/[a_2...a_(m-1)det(L_sigma)].
```

The total sign is positive.  Taking the first component of the boundary
equation gives

```text
sigma a_1
 =(w_m/a_m)/[a_2...a_(m-1)det(L_sigma)],
```

and therefore

```text
w_m=sigma a_1...a_m det(L_sigma).
```

The identity is valid at singular matrices by the continuant polynomial
identity (equivalently, by continuity from the nonsingular locus).  A direct
`m=2` check yields

```text
w_2=sigma[a_1+a_2-sigma K_1a_1a_2],
```

which is exactly `sigma a_1a_2 det(L_sigma)` and independently fixes the
sign convention.

Minor nonblocking observation: the two cofactor sign factors cancel for
every `m`, not only because the present `m=2n` is even.  Since `m` is in fact
even in the theorem, the sentence in R1 produces the correct sign and needs
no proof correction.

## 5. Log-q terminal equivalence and causal binding

At the common terminal,

```text
w_m=-p(q partial_q U(L)).
```

Since `q>1` and `p!=0`, `w_m=0` is equivalent to
`partial_q U(L)=0`.  The accepted terminal symplectic identity

```text
-p partial_q U(L)+r partial_q V(L)=0
```

and `r!=0` then make this equivalent to simultaneous vanishing of both
terminal position variations.  Together with the nonzero product of all
`a_i`, the equivalences in (3.5) pass exactly on the distinguished q line.

The accepted causal formula uses the unscaled derivative:

```text
p partial_q U(L)=sigma(R-1)J.
```

Because the recurrence instead uses `q partial_q`, multiplication gives

```text
w_m=-q sigma(R-1)J.
```

The independent endpoint calculation gives

```text
partial_q A_n
 =(1-q^2)partial_q U(L)/(p r^2)
 =(q^2-1)w_m/(q p^2r^2).
```

Thus both factors of `q` in (4.2)--(4.3), their signs, and all terminal
denominators are correct.  Since `q`, `R-1`, every `a_i`, and `p^2r^2` are
strictly positive, the four-way sign equivalence (4.4) follows in both max
and min cases.

## 6. Logic, boundary, and adversarial audits

Definition audit: **pass**.  Event amplitudes are nonzero under transverse
quotient crossing; `a_i>0`; cell phases give finite nonzero `K_i`; the
relative variables and scaling quotient are not conflated.

Logic audit: **pass**.  Necessity and sufficiency are shown for the exact
q-line reduction.  Positive definiteness is explicitly retained only as a
stronger sufficient condition, not substituted for final-determinant
orientation.  No numerical evidence propagates into the theorem.

Boundary audit: **pass in stated scope**.  The proof covers `n=2`, both
relay signs, all `2n` events, the left zero flux, the final boundary source,
asymmetric roots, and all finite `R>1`.  It properly excludes `R=1`, grazing,
switch collisions, unfinished IVPs, and closures where simple-root formulas
cease to be defined.  Any theorem on those closures still requires a
separate limiting argument.

Adversarial audit: **pass**.  The weakest points were attacked by inserting
the scaling field, reversing the last-row source sign, checking the smallest
continuant, and recomputing the `q` versus `log(q)` normalization.  The
scaling field is now explicitly excluded, the last-row sign is positive as
written, the small continuant agrees, and both `q` factors survive.

## 7. Blocking and nonblocking findings

```text
blocking findings: none
```

Nonblocking:

1. If this result is promoted, phrase its general conjugacy interpretation
   as occurring inside the fixed-Dirichlet initial-slope/equal-Wronskian
   relative subspace modulo scaling.  The proposed established claim may
   avoid that ancillary wording entirely and state the already proved
   distinguished-q equivalence.
2. Keep closure cases outside the proved claim unless a separate limiting
   package is supplied.
3. Keep any finite pivot scout or phase-order sample as non-propagating
   research-attempt evidence.

The R7-R1 exact reduction is ready for a scoped immutable Blueprint
proposal and formal independent proposal review.  Its research status is
still `RIGOROUS_PARTIAL_RESULT`: the minimum remaining finite-contrast
obligation is `det(L_sigma)>0` on every admissible physical word, and O3a
remains open.
