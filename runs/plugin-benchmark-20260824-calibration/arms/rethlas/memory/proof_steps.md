# Proof Steps

Step 1. Let s=sqrt(R).  Direct determinant calculation:
  det C_s(y) = 1, trace C_s(y) = A cos^2 y - B,
  A = (s+1)^2/s, B = s + 1/s.

Step 2. By Cayley-Hamilton, C_s^n = U_{n-1}(z) C_s - U_{n-2}(z) I,
  z = (A cos^2 y - B)/2, with U_{-1}=0.

Step 3. Compute (E C_s)_{12} = sin y (A cos^2 y - s).
  Since A cos^2 y - s = 2z + 1/s, the identity 2z U_{n-1}(z) - U_{n-2}(z)=U_n(z)
  gives
  G_{n,s}(y) = sin y ( U_n(z) + s^{-1} U_{n-1}(z) ).

Step 4. Put F(z) = U_n(z) + a U_{n-1}(z), a=1/s <=1.
  For z in (-1,1), z=cos(theta), F(cos(theta)) =
  [sin((n+1)theta)+a sin(n theta)]/sin(theta).

Step 5. Alternating signs at theta_k=k*pi/n and near theta=0,pi give at least n
  zeros in (0,pi); F is degree n, so exactly n, all simple.

Step 6. For s>1 and z<-1, write z=-cosh(theta): F(z) has sign (-1)^n and is nonzero.
  Hence no new roots below -1. For s=1 the range starts at -1.

Step 7. Since z(x)=(A x^2-B)/2 maps x in (0,1) bijectively onto (z(0),1) and
  (-1,1) is contained there, the n roots in z give n roots in (0,1); evenness
  gives n roots in (-1,0).  Translate back to y with cos(y)=x.
