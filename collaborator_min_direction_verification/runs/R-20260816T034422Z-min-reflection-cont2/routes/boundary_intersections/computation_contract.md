# Conditional Arb boundary-intersection computation contract

Status: PREREGISTERED

## Mathematical object and exact predicate

The object is the frozen R17 exact common-angle evaluator for the four R14
coefficient gaps

```text
G_i=g Knew cp^4-Pplus Nhat_i, i=1,2,3,4,
```

on exact dyadic boxes in `(k,t,y)`. A retained leaf is valid only if outward
rounded Arb balls prove every `G_i>0`. A leaf may be discarded only when an
Arb upper bound proves `g>=1` is impossible for the retained half-domain or
`rB<=1`. `complete=true`, zero unresolved leaves, an empty stack, and
`leaves=splits+1` are separate validity predicates from diagnostic gap
margins.

## Scope and epistemic limitation

The run targets the twelve collar-intersection boxes not covered by the old
inner/single-face union when `t` is inner or high. States are

```text
L=[0,1/64], I=[1/64,63/64], H=[63/64,1].
```

The target triples are

```text
LIL, LIH, HIL, HIH,
LHL, LHI, LHH, IHL, IHH, HHL, HHI, HHH,
```

where the letters are `(k,t,y)`. The result remains conditional on the
noncanonical R14/R17 physical reduction. It is not a universal n=2 theorem,
and it does not quantify the new analytic small-`t` neighborhood.

## Arithmetic, software, and frozen inputs

- Python 3.12.13
- python-flint 0.9.0 / Arb, 128-bit evaluator precision
- exact dyadic denominator and alternating-sinc enclosure inherited without
  modification from the frozen R17 checker
- frozen R17 checker SHA-256:
  `ad1e084f40ed11a80576d2f768fe32c418db391d6d4d98700526a0b4e3b8584b`
- frozen collar driver SHA-256:
  `6c3a4af844a4730b6df577b28c26ded3ac23e1e86f59538ce824c740708c97c2`
- no random seed; subdivision is deterministic

## Limits and stopping rule

- first pass: at most 500,000 visited boxes per intersection;
- one bounded escalation to 2,000,000 only when the first pass has no
  singular/unresolved atomic leaf and the remaining stack is shrinking;
- repeated blow-up near a boundary must be frozen and handed to an analytic
  normalization route, not attacked by unbounded subdivision;
- a negative or zero lower interval is not a counterexample; only a fully
  retained box with a rigorously nonpositive upper bound could be a
  certificate candidate, and every physical bridge would still need audit.

## Replay

Use the project-local `tmp/r12-flint312` python-flint package and run
`intersection_driver.py` with one or more three-letter state codes.

