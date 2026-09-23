# Comparative extension: what the weighted descent suggests and what it does not

This is original author analysis prompted by L06 Section 9, not a replacement domain theorem for K_c. Independent review is pending.

A local endpoint model explains the loss of ordinary derivatives in a degenerate operator. Put t=1-x and F(t)=t^n log(t). For j>=1,
\[
\left|\frac{d^{n+j}}{dt^{n+j}}F(t)\right|=n!(j-1)!t^{-j}.
\]
The n-th derivative is a constant multiple of log(t) plus a constant, hence square integrable near zero. The (n+1)-st derivative behaves as t^{-1} and is not square integrable. The 2n-th derivative times t^n is bounded. Thus a weighted highest derivative condition can coexist with precisely the n-th ordinary-derivative threshold.

On (-1,1) define the right piece by (1-x)^n log(1-x). For x<=0 choose its Taylor polynomial at zero through order 2n-1. All derivatives through order 2n-1 then match at zero; on compact subintervals the last one is absolutely continuous piecewise and continuous across zero, hence absolutely continuous across the junction. This supplies the full local regularity required by the consistent Legendre domain formula. The lower endpoint is harmless because that piece is polynomial. This corrects the sufficiency of the stated matching choice, without alleging that the source theorem itself is false.

For the nondegenerate project operator, the situation is different: already D(K_c) requires Bf=0. A smooth polynomial x^2 has every unweighted derivative integrable but fails Bx^2=(2,-2). Even p4, which satisfies the first boundary layer, has B(p4'')=(24,-24). No highest-derivative integrability statement alone removes these endpoint conditions. Proofs 01-02 retain them explicitly.

A potentially reusable proof pattern is to write lower derivatives as anchored integrals and prove the integral map bounded in the actual target weights, tracking every integration constant. In this project's s=3 cutoff, all three anchoring constants are zero and the local L^2 mass tends to zero; this is the concrete mechanism in proof 03. Similar vocabulary does not identify the models or confer Legendre's domain collapse on the Krein operator.

No additional Legendre fractional-domain or Krein higher-power theorem is proposed by this note. L06 remains an extension-reading entry with source-version cautions.
