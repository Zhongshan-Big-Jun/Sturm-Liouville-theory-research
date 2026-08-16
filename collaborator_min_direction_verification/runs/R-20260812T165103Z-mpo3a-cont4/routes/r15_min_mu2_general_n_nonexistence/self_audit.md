CANDIDATE_COMPLETE_PROOF

# R15 author self-audit

## Audit target

Audit the exact implication

```text
strict physical mu=2 minimum-law full-relay root with n>=3
=> physical contraction 0<a<1 on both sides of cell I_3
=> a(x3,y2,r)*a(x3,y4,r)=1 and also <1
=> contradiction.
```

This is an author audit, not the independent review required for promotion.

## 1. Definition audit: pass

The event and cell indices are fixed as follows:

```text
events:         tau_1,...,tau_(2n)
internal cell:  I_j=(tau_j,tau_(j+1)), 1<=j<=2n-1
event amplitude A_i=U(tau_i)
cell ratio:     z_j=A_(j+1)/A_j.
```

The accepted allocation is odd-positive/even-negative.  A transverse event
cannot have `A_i=0`, because the switch equation also has `V(tau_i)=0` and
then its first derivative vanishes.  Thus every ratio and reciprocal exists.

The checker does not trust the displayed `a,b` formulas.  It starts from the
two half-angle oscillator solutions, normalizes the shared interface
amplitude, solves both momentum equations, and verifies

```text
a_raw-a=0,       b_raw-b=0.
```

It separately verifies `J M J=M^{-1}` for the generic oscillator transfer
matrix.  Substituting the `U` and `V` frequencies proves that both relay
equations use the same time reversal.  The reversed negative-positive pair
therefore uses `(1/z_j,1/z_(j-1))=(a,b)`, not `(z_j,z_(j-1))` and not a swap
of `a,b`.

## 2. Logic audit: pass

The local contraction is reproduced rather than imported from the R13
candidate route.  All exact residuals for

```text
N_b in natural coordinates,
D_a in natural coordinates,
a-1=(1-x^2)T/D_a,
the feasibility factorization,
kappa_D-kappa_N,
the upper-boundary T bracket
```

are zero.  On the physical domain all divided factors have fixed positive
sign.  The order `kappa<kappa_N<kappa_D` gives `D_a>0`; the `a` numerator is
positive; and the boundary-gap factorization gives `T<0`.  Hence `0<a<1`
without circular use of the desired nonexistence.

For every internal odd `j`, the left reversed and right forward descriptions
give

```text
1/z_j=a(x_j,y_(j-1),r),
z_j  =a(x_j,y_(j+1),r).
```

Their product is one.  For `n>=3`, choosing `j=3` is valid immediately.
No induction, limiting argument, endpoint equation, or global norm identity
is required.

## 3. Boundary audit: pass

- `n=2` has no positive cell with two negative internal neighbors and is
  explicitly excluded.
- `n=3` is the first admissible case and reproduces the single R13 central
  compatibility exactly.
- For every `n>3`, cells `I_2,I_3,I_4` remain internal, so word length adds no
  exception.
- Endpoint cells are outside the sharp internal phase theorem, but none is
  used.
- Reflection maps `j` to `2n-j`, preserving parity; global sign reversal
  leaves all ratios unchanged.
- `R=1`, phase endpoints, `b=0`, `a=1`, collapsed feasibility, grazing,
  colliding events, zero cells, and endpoint escape are outside the strict
  theorem.
- The maximum relay law is not claimed; only the two traversal orientations
  of the minimum law are used.

## 4. Adversarial audit: pass

The weakest step is the reciprocal at the left interface.  It was attacked
three ways:

1. label the three actual amplitudes and reverse their order, yielding
   `A_j/A_(j+1)=1/z_j` exactly;
2. verify the transfer-matrix time-reversal identity for a generic frequency,
   hence for both `U` and `V`;
3. generate every forward/reverse pair and every overlap compatibility for
   `2<=n<=12`.

The generated counts are

```text
forward pairs:                  n-1
reversed pairs:                 n-1
negative-cell compatibilities:  n-1
positive-cell compatibilities:  n-2
all overlap compatibilities:     2n-3.
```

The finite generation is not used for the universal result; the displayed
arbitrary-index proof supplies it.  The smallest case `n=2` has zero
positive-cell compatibilities, while every generated `n>=3` begins with

```text
a(x3,y2,r)*a(x3,y4,r)=1.
```

No alternate orientation, endpoint attachment, reflection, or extra global
constraint survives these checks.

## Disposition

```text
definition_audit: pass (author)
logic_audit: pass (author)
boundary_audit: pass (author)
adversarial_audit: pass (author)
mathematical_obligations_in_candidate: []
epistemic_status: CANDIDATE_COMPLETE_PROOF
next_required_action: uninvolved four-part audit on frozen hashes
```

No canonical file, proposal, R13 artifact, or earlier audit was modified.
