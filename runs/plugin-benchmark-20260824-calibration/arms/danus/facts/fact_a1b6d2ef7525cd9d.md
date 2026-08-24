# F3: Power formula for A by Chebyshev polynomials

## STATEMENT
Let A be a real 2x2 matrix with det A=1 and trace 2P. For n>=0,
A^n = U_{n-1}(P) A - U_{n-2}(P) I,
where U_{-1}=0, U_0=1, U_1(t)=2t, and U_k satisfies U_{k+1}(t)=2t U_k(t)-U_{k-1}(t).

## PROOF / JUSTIFICATION
Cayley-Hamilton gives A^2 - 2P A + I = 0. Define B_n = U_{n-1}(P)A - U_{n-2}(P)I for n>=0. Then B_0=0, B_1=A, and B_{n+1}=U_n(P)A - U_{n-1}(P)I = 2P(U_{n-1}(P)A - U_{n-2}(P)I) - (U_{n-2}(P)A - U_{n-3}(P)I) = 2P B_n - B_{n-1}; hence B_n=A^n by the same recurrence and initial values. This is standard Chebyshev polynomial power formula.

## TAGS
STRICT linear algebra; Cayley-Hamilton; Chebyshev recurrence
