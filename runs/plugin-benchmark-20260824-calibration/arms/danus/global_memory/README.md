# global_memory

## Findings
- The core simplification is M_n = (E S)^n E, with A=E S. This leads to a clean Chebyshev polynomial Q_n=U_n(P)+s^{-1}U_{n-1}(P).
- For s>1, alpha=s+2+1/s>4, P(x)=1-alpha/2+alpha x^2/2 maps (0,1) to (1-alpha/2,1). Only the elliptic region |x|>delta carries roots; the hyperbolic region has a strict positive/negative sign due to sinh monotonicity.
- The trigonometric root count is driven by the strictly increasing argument Phi=n theta+arg(e^{i theta}+r), going from 0 to (n+1)pi.

## Dead ends / not used
- Direct expansion of C_s^n before simplifying to A^n E is messy and unnecessary.
- A pure Sturm-Liouville oscillation theorem was not needed; the proof is self-contained matrix/Chebyshev.
- Pairing roots by interval without the monotone argument does not prove count; the monotone Phi argument is essential.
- Numerical scans only used for sanity checks (not as proof): n<=5, s in {1.1,2,10} all gave 2n real roots with n positive.
- During verification, an error at P=-1 (using U_k(-1)=(-1)^k instead of (-1)^k(k+1)) was caught and corrected; the corrected no-root statement is F7.

## First unresolved obligation
- None. The main theorem is proven STRICT for all n>=1, R>1. (If an external reviewer requires a proof of the hyperbolic Chebyshev formula, it is standard and can be supplied.)
