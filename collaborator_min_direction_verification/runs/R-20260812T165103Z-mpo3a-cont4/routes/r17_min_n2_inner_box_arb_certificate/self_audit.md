FINITE_COMPUTATIONAL_RESULT

# R17 self-audit

## Verdict and exact scope

`PASS_FOR_COMPACT_SUBDOMAIN_ONLY`.

The route certifies the four R14 coefficient inequalities

```text
B_i=g Knew-p_+ N_i>0,  i=1,2,3,4,
```

only on the exact common-angle physical subset

```text
(k,t,y) in [1/64,63/64]^3,  g<1,  rB>1.
```

It is a finite certified-computation result, not a global proof of the
general-`mu`, `n=2` min interface theorem.

## Provenance freshness audit

- The calculation began against Blueprint hash `0120d1fb...` and inventory
  hash `b6286574...`.
- Before freeze, the reviewed R15 proposal was integrated and advanced the
  Blueprint to `a53684ab...`; the inventory hash stayed unchanged.
- R15's new `mu=2`, min, `n>=3` nonexistence theorem is not an input to this
  route.  R17 depends analytically only on the frozen R14 derivation, whose
  content hash is bound in the reproducibility manifest.
- The R17 statements and replay remain fresh under this advance because
  their definitions, hypotheses, and R14 dependency were not altered.

## Definition and normalization audit

1. The coordinates `k,t,y`, the common-angle phases, and the centered
   quantities are the R14 definitions reproduced in `problem_contract.md`.
2. The scaled variables `A=ka`, `B=kb`, `Q=kq`, `S=k sigma` are exact
   substitutions.  No common-angle equation is relaxed.
3. The checked quantity is
   `G_i=g Knew cp^4-Pplus Nhat_i`.  All normalization factors relating
   `G_i` to R14 `B_i` are strictly positive on the retained branch.
4. The required ratio threshold is `<1`.  The disproved auxiliary
   `<1/4` bound is nowhere used.

## Arithmetic and covering audit

1. Every root and child endpoint is an exact dyadic with denominator
   `2^34`; Arb evaluates all algebraic and transcendental expressions at
   128-bit precision with outward-rounded balls.
2. The only cancellation-sensitive term is evaluated by an alternating
   sinc-difference enclosure.  Its term magnitudes decrease because the
   first possible consecutive ratio is at most `pi^2/10<1` and subsequent
   ratios are smaller.  The union of the 16-term and 17-term enclosures
   therefore encloses the exact remainder interval.
3. A box is discarded only when its Arb upper bound proves that it cannot
   meet `g<1` or `rB>1`.
4. On a box that may meet the retained subset, the contractor intersects
   with signs already proved in R14: `ebar>=0`, `rB>=1`, and positivity of
   `X,W_i,U_i,H_i,L_i`.  These are conditional physical-branch facts, not
   assumptions about the ambient box.
5. A retained leaf is accepted only when Arb proves all four gap balls
   strictly positive.  The replay has zero singular boxes, zero unresolved
   boxes, and an empty stack.
6. The tree accounting is complete: `leaves=split+1` and
   `visited=leaves+split`.

## Adversarial and non-propagation audit

- The cross-only relaxation and the rational tangent-envelope relaxation
  are excluded; their exact no-go witnesses do not challenge this result
  because this checker keeps the full common-angle equations.
- Floating-point phase probes and the earlier apparent quarter margin are
  discovery evidence only and do not enter the certificate.
- The reported minimum gap values are directed lower endpoints converted
  to binary floats for diagnostics.  Positivity is decided before this
  conversion by Arb's rigorous comparison.
- No canonical Blueprint file, evidence inventory, proposal, or sibling
  route is edited by this route.

## Open boundary obligations

The following collars remain completely open:

```text
0<k<1/64,       63/64<k<1,
0<t<1/64,       63/64<t<1,
0<y<1/64,       63/64<y<1,
```

together with every pairwise and triple intersection of those collars.
No limiting argument, continuity propagation, or global sign conclusion is
claimed for them.  Discharging those collars is a separate future route.
