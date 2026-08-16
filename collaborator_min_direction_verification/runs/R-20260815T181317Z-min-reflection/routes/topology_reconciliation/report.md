RIGOROUS_PARTIAL_RESULT

# Ordered-reflection criterion and the exact limit of degree alone

## 0. Scope

Fix finite `R>1`, `n>=2`, and `mu>1`.  This report uses only the trusted
full-relay and symplectic-reflection claims.  It does not assume minimum
uniqueness, reflection symmetry, fixed-`mu` twist, or nonsingularity.

Let `X=X_min(R,n,mu)` be the set of all `q>1` for which the minimum-law
relay trajectory is a premise-complete self-consistent root: the indexed
terminal zeros coincide, the two relay integrals are equal, and the exact
`2n` transverse-event predicates hold.  At `q in X`, write

```text
p(q)=U_t(L;q),
h(q)=q_sharp=sqrt(1+(q^2-1)/p(q)^2).                 (0.1)
```

The trusted reflection theorem says that `h:X->X` is an involution and that
`h(q)=q` is equivalent to reflection invariance of the relay trajectory.

## 1. Ordered-involution lemma

**Lemma.**  If `X` is any subset of the real line and `h:X->X` is a weakly
order-preserving involution, then `h` is the identity on `X`.

**Proof.**  If `q<h(q)`, order preservation gives
`h(q)<=h(h(q))=q`, a contradiction.  If `h(q)<q`, order preservation applied
to `h(q)<q` gives `q=h(h(q))<=h(q)`, again a contradiction.  Hence
`h(q)=q` for every `q in X`. `QED`

Combining the lemma with (0.1) proves the following exact conditional
reflection theorem.

> For fixed finite `R>1`, `n>=2`, and `mu>1`, every minimum-law
> self-consistent root is reflection invariant if, for every two such roots
> `q_1<q_2` with terminal `U` slopes `p_1,p_2`,
>
> ```text
> (q_1^2-1)/p_1^2 <= (q_2^2-1)/p_2^2.               (1.1)
> ```

Indeed, the square root in (0.1) is strictly increasing, so (1.1) is
exactly weak order preservation of `h`.

This premise is strictly targeted to reflection symmetry.  It compares
only premise-complete equal-integral roots.  It imposes no sign on
`partial_q A_n` at common-terminal roots with unequal integrals, and it
allows several distinct roots at the same `mu` provided each is fixed by
reflection.  Thus it is weaker in scope and conclusion than the trusted
conditional fixed-`mu` global-order theorem, which yields at most one
common-terminal root.

## 2. Why properness and degree alone cannot prove all-root symmetry

Consider the one-parameter odd residual

```text
F_t(x)=x(x^2-(t-1)),       0<=t<=2,  -2<x<2,          (2.1)
tau(x)=-x.
```

It is reflection equivariant: `F_t(tau x)=-F_t(x)`.  Its complete zero set
over the compact parameter interval is compact and stays away from the
spatial boundary.  For `0<=t<1`, the unique zero is the fixed point `x=0`.
At `t=1`, that zero is singular.  For `1<t<=2`, the zeros are

```text
x=0,  x=+sqrt(t-1),  x=-sqrt(t-1),                   (2.2)
```

so a non-fixed reflected pair has appeared without boundary escape.  The
ordinary oriented degree on `(-2,2)` remains `+1`: for `t>1`, the index at
zero is `-1` and the two outer indices are `+1,+1`.

Therefore the following data, even together, do not imply that every zero
is reflection fixed:

- reflection equivariance;
- compactness/properness of the solution set;
- uniqueness near the initial parameter value;
- preservation of ordinary or mod-2 degree;
- persistence of at least one reflection-fixed branch.

They permit an interior symmetry-breaking pitchfork.  In the Blueprint
problem, any continuation/degree proof must additionally exclude this
mechanism, orient the reflection action on the root set, or prove a
problem-specific comparison such as (1.1).  This agrees with, but sharpens
for the reflection-only target, the trusted properness reduction: the
essential missing event is an interior singularity rather than boundary
loss.

## 3. Existing endpoint rigidity does not orient the reflection defect

For the left-oriented normalized modes put

```text
q_0=u_(n+1)'(0)/u_n'(0)>1,
q_1=u_(n+1)'(1)/u_n'(1)<-1.
```

In relay normalization `q=q_0`, `p=u_n'(1)/u_n'(0)`, and
`r/p=q_1`.  The endpoint energy identity gives

```text
p^2=(q_0^2-1)/(q_1^2-1),
p^2-1=(q_0^2-q_1^2)/(q_1^2-1).                       (3.1)
```

Thus reflection fixing is exactly the missing left-right norming equality
`q_0=|q_1|`, while the sign of the antisymmetric endpoint defect is exactly
the sign of `q_0^2-q_1^2`.  The trusted global-minimizer endpoint-rigidity
inequalities constrain each endpoint ratio relative to the spectral number
`c=1/mu`, but do not compare `q_0` with `|q_1|`.  They therefore do not
close reflection symmetry or even give a one-sided sign for the defect.
Reflection exchanges the two norming magnitudes, so any valid one-sided
comparison across the full root set would itself force equality.

## 4. Exact frontier after this route

The reflection-only target is reduced to either of two mechanism-distinct
bridges:

1. prove the pairwise endpoint order (1.1) only on complete equal-integral
   minimum roots; or
2. prove directly that no interior antisymmetric symmetry-breaking
   singularity can occur.

The first bridge does not require a universal sign for the physical
continuant on all common-terminal roots.  No trusted identity presently
signs the two-root endpoint quotient in (1.1).  The symplectic action
identity is pointwise and does not compare two disconnected roots; degree
does not supply the missing order by Section 2.

```text
ordered-involution lemma:                              PROVED
endpoint-slope criterion (1.1) => all-root reflection: PROVED
degree/properness alone => all-root reflection:         REFUTED BY EXACT MODEL
physical endpoint order (1.1) for minimum roots:        OPEN
unconditional global minimum reflection theorem:       OPEN
unresolved_obligations_for_stated_conditional_lemma:    []
```

## 5. Audits

- **Definition audit:** `X` includes the common terminal, equal integrals,
  exact event count, transversality, and minimum relay law.  It is not the
  larger zero set of `A_n` alone.
- **Logic audit:** only involutivity and the trusted fixed-point equivalence
  are imported.  The proof does not infer monotonicity from continuity.
- **Boundary audit:** no existence, finiteness, discreteness, or regularity
  of `X` is required.  Empty, singleton, multiple, and accumulating root
  sets are all covered.  The relay statement retains finite `R>1`,
  `mu>1`, and `q>1`.
- **Adversarial audit:** a decreasing involution can exchange two roots;
  Section 2 realizes exactly this obstruction.  Ordinary degree counts the
  pair with even net parity and cannot eliminate it.
- **Strength audit:** the result proves a sufficient criterion, not the
  physical inequality (1.1), existence, uniqueness, or the open canonical
  minimum O3a claim.
