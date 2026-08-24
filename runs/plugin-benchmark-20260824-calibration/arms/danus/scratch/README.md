# scratch (evidence only, not proof)

SymPy checks performed in this arm:
- C_s = S E; det S = det E = det C_s = 1.
- A=E S entries and det/trace.
- For n=1..6 and symbolic s, identity
  Q_n = (alpha x^2 - s) U_{n-1}(P) - U_{n-2}(P) = U_n(P) + (1/s) U_{n-1}(P)
  simplified to 0.
- Numeric root scans for n=1..5, s=1.1,2,10: all roots of Q_n are real, inside (-1,1), exactly 2n, n positive.
- Boundary R=1 gives Q_n=U_{2n}(x) and G=sin((2n+1)y).
- Correction: U_k(-1)=(-1)^k(k+1), not (-1)^k. This was caught in the verifier pass and F7 was regenerated.
