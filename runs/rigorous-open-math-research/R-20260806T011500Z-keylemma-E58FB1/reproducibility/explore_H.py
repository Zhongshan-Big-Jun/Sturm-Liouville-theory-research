# -*- coding: utf-8 -*-
"""explore_H.py -- structural exploration of the KEY LEMMA surface.
Questions:
  E1  rescaled F~' = F'/(q(q^2-1)) and its min over c in (0,1/2): where attained?
  E2  H = G2-G1 and its min: where attained?  is H(q,c) >= H(1,c) (q-monotone)?
  E3  is -F~' or F~ q-monotone?  is F~ c-monotone (i.e. KEY LEMMA form (i))?
  E4  location of c*(q) (zero of F~); sign structure of G1, G2, F on (0,1/2)
  E5  corner values: exact q=1 limits for F~, F~', G2-G1 (symbolic check)
"""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import (Phi, Wfun, alpha1_of_c, alpha2_of_c, Mfun, Gfun,
                          G1_of_c, G2_of_c, u_from_c)
mp.mp.dps = 40

def Ftil(c, q):
    a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
    M1t = a1*a1*mp.sin(a1)**2/(q + c*Phi(a1, q))
    M2t = a2*a2*mp.sin(a2)**2/(q + c*Phi(a2, q))
    return M1t - M2t

def Ftil_p(c, q):
    # F~' = M1t*G1 - M2t*G2
    a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
    M1t = a1*a1*mp.sin(a1)**2/(q + c*Phi(a1, q))
    M2t = a2*a2*mp.sin(a2)**2/(q + c*Phi(a2, q))
    return M1t*Gfun(a1, c, q) - M2t*Gfun(a2, c, q)

def scan(q, n=400):
    cs = [mp.mpf('1e-5') + mp.mpf('0.49999')*k/(n-1) for k in range(n)]
    out = []
    for c in cs:
        Fp = Ftil_p(c, q)
        H = G2_of_c(c, q) - G1_of_c(c, q)
        Ft = Ftil(c, q)
        G1 = G1_of_c(c, q); G2 = G2_of_c(c, q)
        out.append((c, Ft, Fp, H, G1, G2))
    return out

print('=== E1/E2: margins and argmins ===')
for q in [mp.mpf(1.001), mp.mpf(1.025), mp.mpf(1.05), mp.mpf(1.1), mp.mpf(1.5),
          mp.mpf(2), mp.mpf(4), mp.mpf(10), mp.mpf(100)]:
    out = scan(q)
    mF = min(out, key=lambda t: t[2]); mH = min(out, key=lambda t: t[3])
    # zero of F~ (sign change)
    zc = None
    for i in range(len(out)-1):
        if out[i][1] > 0 and out[i+1][1] < 0:
            zc = (out[i][0], out[i+1][0]); break
    print(f'q={mp.nstr(q,6)}: minFp={mp.nstr(mF[2],7)} at c={mp.nstr(mF[0],5)} | '
          f'minH={mp.nstr(mH[3],7)} at c={mp.nstr(mH[0],5)} | F~(c*)~0 at c~{mp.nstr(zc[0] if zc else 0,4)}')

print()
print('=== E2b: is H(q,c) >= H(1,c)?  sample diff ===')
q1 = mp.mpf(1)
for q in [mp.mpf(1.001), mp.mpf(1.1), mp.mpf(2), mp.mpf(10), mp.mpf(100)]:
    mind = mp.inf; argc = None
    for c in [mp.mpf('1e-4') + mp.mpf('0.4998')*k/200 for k in range(201)]:
        d = (G2_of_c(c,q)-G1_of_c(c,q)) - (G2_of_c(c,q1)-G1_of_c(c,q1))
        if d < mind: mind, argc = d, c
    print(f'  q={mp.nstr(q,6)}: min over c of [H(q,c)-H(1,c)] = {mp.nstr(mind,6)} at c={mp.nstr(argc,5)}')

print()
print('=== E3: is F~ decreasing in c (i.e. F~\'<0)? already shown by minFp>0. Is F~ q-monotone? ===')
# F~(q1,c) vs F~(q2,c): increasing or decreasing in q?
for c in [mp.mpf('0.05'), mp.mpf('0.2'), mp.mpf('0.4')]:
    vals = [(q, Ftil(c, q)) for q in [mp.mpf(1.0), mp.mpf(1.1), mp.mpf(2), mp.mpf(10)]]
    print(f'  c={c}: ' + '  '.join(f'q={mp.nstr(q,4)}:F~={mp.nstr(v,7)}' for q, v in vals))

print()
print('=== E4: signs of G1, G2 at sample points ===')
for q in [mp.mpf(1.1), mp.mpf(2), mp.mpf(10)]:
    for c in [mp.mpf('0.01'), mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.49')]:
        G1 = G1_of_c(c,q); G2 = G2_of_c(c,q); Ft = Ftil(c,q)
        print(f'  q={mp.nstr(q,4)} c={mp.nstr(c,4)}: G1={mp.nstr(G1,7)} G2={mp.nstr(G2,7)} F~={mp.nstr(Ft,7)}')
