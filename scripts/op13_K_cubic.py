# -*- coding: utf-8 -*-
"""#13(i): cubic fit of log K(c) for small c."""
import mpmath as mp
mp.mp.dps = 250
# accurate K values
K = {0.001: '0.7499250048211646961', 0.002: '0.74985001928360339163', 0.005: '0.7496251205027366513',
     0.01: '0.74925048187910384734', 0.02: '0.74850192646248586663', 0.05: '0.7462620206698935891',
     0.1: '0.74254795174666372759'}
K = {c: mp.mpf(v) for c, v in K.items()}
import mpmath
cs = sorted(K)
# fit log K = b0 + b1 c + b2 c^2 + b3 c^3 on c<=0.05
sel = [c for c in cs if c <= 0.05]
A = mp.matrix(len(sel), 4); y = mp.matrix(len(sel), 1)
for i, c in enumerate(sel):
    for k in range(4): A[i,k] = c**k
    y[i] = mp.log(K[c])
b = mp.lu_solve(A.T*A, A.T*y)
print("b0 =", mp.nstr(b[0], 20), " (ln(3/4) =", mp.nstr(mp.log(mp.mpf(3)/4), 20), ")")
print("b1 =", mp.nstr(b[1], 20))
print("b2 =", mp.nstr(b[2], 20))
print("b3 =", mp.nstr(b[3], 20))
# candidates for b2
print("1/700 =", mp.nstr(mp.mpf(1)/700, 10), " 1/700.5:", mp.nstr(mp.mpf(1)/700.5, 10))
