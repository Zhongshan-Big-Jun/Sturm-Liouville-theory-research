# F5: Exact polynomial form of Q_n

## STATEMENT
Define Q_{n,s}(x) = G_{n,s}(arccos x)/sqrt(1-x^2) for x in (-1,1). Then, with P=P(x) and r=1/s,
Q_{n,s}(x) = U_n(P(x)) + r U_{n-1}(P(x)).
In particular Q_n is a polynomial (not merely a rational/trigonometric expression).

## PROOF / JUSTIFICATION
M_n = E C^n = (E S)^n E = A^n E. Hence
G_n(y) = (A^n E)_{12} = U_{n-1}(P)(AE)_{12} - U_{n-2}(P) E_{12},
using F3 and linearity. By F4, (AE)_{12}=q(alpha x^2-s), E_{12}=q. Dividing by q=sqrt(1-x^2) (nonzero on (-1,1)) gives
Q_n = (alpha x^2-s)U_{n-1}(P) - U_{n-2}(P).
Using alpha x^2 - s = 2P + r and the Chebyshev recurrence U_n = 2P U_{n-1} - U_{n-2},
Q_n = (2P+r)U_{n-1}(P) - U_{n-2}(P) = U_n(P) + r U_{n-1}(P).
This justifies the polynomial formulation.

## TAGS
STRICT; uses F2-F4; polynomial extension justified
