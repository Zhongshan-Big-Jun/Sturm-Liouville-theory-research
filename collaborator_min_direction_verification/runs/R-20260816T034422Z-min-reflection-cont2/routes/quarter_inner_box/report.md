FINITE_COMPUTATIONAL_RESULT

# C2-O: rigorous uniform-quarter certificate on the exact inner cube

The frozen R17 directed-Arb evaluator was replayed on

```text
(k,t,y) in [1/64,63/64]^3,
g<1, rB>1,
```

with the stronger target

```text
Pplus*Nhat_i/(g*Knew*cp^4) < 1/4,  i=1,...,4.
```

Equivalently, the checker certifies

```text
g*Knew*cp^4/4-Pplus*Nhat_i > 0
```

by directed 128-bit Arb arithmetic.  The complete run visited 5,848,407
boxes, with 117,875 exact `g` discards, 61,610 exact `rB` discards,
2,744,719 proved leaves, 2,924,203 splits, zero singular boxes, zero atomic
unresolved boxes, and an empty final stack.  The four smallest directed
lower endpoints were

```text
0.017210393145654746,
8.02367958724354e-6,
4.283843323617724e-7,
1.8713493338293328e-8.
```

This is a finite exact-cube result, not a full coefficient theorem.  It
does not cover any of the six boundary collars.  It also does not by itself
propagate through the physical reflection bridge; that bridge is separately
proved in C2-J and remains conditional on complete retained-cube coverage.

Artifacts:

```text
quarter_cover.py
sha256:b3550003da0155d3d52744105e9e5c64c5180fb53b9c0a4cd0a1916eecbee386

quarter_cover_output.json
```

The output JSON is a verbatim structured freeze of the successful terminal
run.  No floating scout value is used in any proof decision.

```text
inner quarter bound: PROVED BY FINITE DIRECTED COVER
boundary quarter bounds: OPEN
full coefficient cube: OPEN
physical n=2 reflection: OPEN
formalization_status: not_requested
```
