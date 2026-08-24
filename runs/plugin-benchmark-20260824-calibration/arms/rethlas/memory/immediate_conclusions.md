# Immediate Conclusions

- The normalized transfer matrix entry G_{n,s}(y) satisfies
  G_{n,s}(y) = sin(y) * [ U_n(z) + s^{-1} U_{n-1}(z) ],
  where z = (A cos^2(y) - B)/2, A = (s+1)^2/s, B = s + 1/s.
- Equivalently Q_{n,s}(x) = U_n(z(x)) + s^{-1} U_{n-1}(z(x)), z(x) = (A x^2 - B)/2.
- For s >= 1 the Chebyshev combination U_n(z) + a U_{n-1}(z), a = 1/s <= 1,
  has exactly n simple zeros in (-1,1).
- Consequently, for every R>=1 (in particular R>1) and n>=1, G_{n,s} has exactly
  2n simple zeros in (0,pi).  The claim is TRUE.
