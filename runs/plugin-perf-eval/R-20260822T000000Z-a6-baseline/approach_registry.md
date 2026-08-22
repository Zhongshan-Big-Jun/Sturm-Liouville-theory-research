# Approach Registry

This is the run-level route portfolio for the A6 higher-degree rational
product-solution problem.

| Route | Name | State | Exact gap / result |
| --- | --- | --- | --- |
| A | Asymptotic uniqueness + rational injection (root-1) | SUCCESS (STRICT sub-result) | Proves no degree > 2 rational ratio on the root-1 branch, even and odd. Gap: proof covers root-1 only. |
| B | Petkovsek/hypergeometric solution theory | TRIAGED, NOT PURSUED | Would independently bound the degree of hypergeometric term ratios; likely gives the same no-go but is heavier. Not needed for the partial result. |
| C | Direct degree comparison in polynomial identity | TRIAGED, NOT PURSUED | Leading-degree cancellation leaves many higher equations; not as clean as route A. |
| D | Root-0/minimal-branch rationality exclusion | OPEN | Current evidence is high-precision numerical fits + formal uniqueness of asymptotic expansion; no complete rational-function injection argument because no explicit rational minimiser family is known. |
| E | Low-degree ansatz search (n=3,4) | NOT NEEDED | Route A already closes root-1; a finite solver search would only be confirmation, not a general theorem. |

## Decision log

- 2026-08-22T13:15Z: Route A chosen after reading the source document and
  noticing that the asymptotic expansion has a one-parameter family already
  realised by the degree-2 rational family. If the formal expansion is unique
  given `(u,v)`, the rational function must coincide with that degree-2 family.
- 2026-08-22T13:20Z: Formal uniqueness reduced to a diagonal-coefficient lemma.
- 2026-08-22T13:25Z: Symbolic exact verification of the diagonal coefficients
  for both parities and both branches passed (`f1 = -2` free, `0` rigid).
- Route B not started: it would require a full Petkovsek implementation, which
  is unnecessary for the bounded run.

## Avoid list

- Do not claim the whole A6 problem is solved; the root-0 branch and minimal
  constant remain open.
- Do not present numerical fits as a proof for root-0 non-rationality.
