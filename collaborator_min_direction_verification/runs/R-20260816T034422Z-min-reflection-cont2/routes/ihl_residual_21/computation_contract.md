# C2-P computation contract — IHL residual extraction

Status: preregistered before the residual replay.

## Object and scope

This route concerns only the conditional R17 coefficient cube on

\[
 k\in[1/64,63/64],\qquad
 t\in[63/64,1-2^{-17}],\qquad
 y\in[0,1/64].
\]

The input calculation is the C2-N IHL run capped at exactly 1,000,000 visited
boxes.  The first calculation below replays the same depth-first traversal,
same widest-coordinate split rule, same Arb evaluator, same exact dyadic root,
and the same cap.  Its only additional action is to serialize the final stack
and diagnostic intervals for its 21 members.  It does **not** increase the
search budget or re-run LHH.

## Arithmetic and validity predicates

- Partition endpoints are integers divided by `2^34`.
- Transcendentals and all R17 expressions use `python-flint` Arb at the
  upstream checker's precision.
- A leaf is validly classified only by one of the upstream predicates:
  `upper(b-a)<=0`, `upper(rB-1)<=0`, or four strictly positive conditional
  coefficient gaps.
- Stable complementary-angle diagnostics use the exact identities

  `sign(b-a)=sign(s*tan(eta)-p*tan(h))` and

  `rB = tan(h)*(1-s^2*tan(eta)^2) /
        (tan(eta)*(1+s^2)+tan(h)*p*s*(1+tan(eta)^2))`,

  where `h=pi(1-t)/2`, `eta=pi*y*(1-k)/(2*(1+k))`,
  `p=tan(k*(pi/2-h))`, and `s=tan(k*(pi/2+eta))`.

## Bounded follow-up

After freezing the residual coordinates, any second computation may start
only from those exact boxes.  It must add a mathematically different
contractor or a predeclared directed split score; it may not repeat the raw
IHL root traversal with a larger cap.  A failure result must preserve at least
one exact non-atomic residual box and the first interval dependency or pole.

The preregistered follow-up starts with the serialized 21-box forest and has a
hard cap of 1,000,000 *local* visits.  Before calling the raw R17 evaluator it
applies the stable defects

- `D_g=s*tan(eta)-p*tan(h)`; discard when `upper(D_g)<=0`;
- `D_r=tan(h)*(1-s^2*tan(eta)^2)
       -tan(eta)*(1+s^2)-tan(h)*p*s*(1+tan(eta)^2)`;
  after independently certifying the displayed positive denominator, discard
  when `upper(D_r)<=0`.

An unresolved box is split by two-child lookahead.  For each non-atomic axis,
the heuristic first maximizes the number of children immediately discarded by
these stable contractors, then minimizes the sum of their stable-defect
diameters normalized by the parent diameters, and only then uses dyadic width
and axis order to break ties.  Floating conversion is used solely for this
partition heuristic; every leaf verdict remains an Arb inequality.

The first execution exposed a non-mathematical loss: evaluating the positive
`rB` denominator as one wide natural interval made its lower endpoint negative
on 29,424 visited ancestors, despite exact positivity on IHL.  Revision v2
therefore proves denominator positivity by the domain order
`0<k*pi*t/2<pi/2` and
`0<k*(pi/2+eta)<pi/2`, with
`1-k*(1+y(1-k)/(1+k))>0`, rather than asking Arb to rediscover it on every
wide box.  It also adds the independent exact empty contractor

`k*t > (1-k)*(1-y*k/(1+k))  =>  rB<1`,

certified on a box from its monotone lower/upper endpoints.  Revision v2 keeps
the same 1,000,000 local-visit cap; this is a contractor correction, not a
budget increase.

An exact SymPy replay is also preregistered to check the two complementary-
angle algebraic identities and the factorization proving that the tangent
arguments remain below `pi/2`.  It is a symbolic consistency check, not a
replacement for the Arb cover.

## Inputs and epistemic limit

- Blueprint SHA-256:
  `358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0`.
- Inventory SHA-256:
  `b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
- Frozen R17 checker SHA-256:
  `ad1e084f40ed11a80576d2f768fe32c418db391d6d4d98700526a0b4e3b8584b`.
- C2-N annulus result is a conditional, noncanonical finite result.

No outcome in this route establishes the physical R14/R17 bridge or a
canonical reflection theorem.
