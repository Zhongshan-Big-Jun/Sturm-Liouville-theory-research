# -*- coding: utf-8 -*-
"""qderiv.py -- decompose dH/dq and dF~'/dq; look for sign structure.
dH/dq = [A(a2)-A(a1)] + [G_a(a2)*a2q - G_a(a1)*a1q]
with A = dG/dq (partial), G_a = dG/dalpha, akq = d alpha_k / d q (implicit).
"""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import Phi, Wfun, alpha1_of_c, alpha2_of_c, Gfun
mp.mp.dps = 30

def dalpha_dq(alpha, q, c):
    # d alpha / d q for either curve (slope -q/Phi): -tan(alpha)*Phi/((1+q^2 tan^2)(q+c Phi))
    Ph = Phi(alpha, q)
    t = mp.tan(alpha)
    return -t*Ph/((1+q*q*t*t)*(q + c*Ph))

def dG_dq(alpha, c, q):
    Ph = Phi(alpha, q); W = Wfun(alpha); s = mp.sin(alpha); co = mp.cos(alpha)
    term1 = Ph*W/(q + c*Ph)**2
    term2 = 4*c*alpha*Ph*s*co*(q*c*Ph + 1)/(q + c*Ph)**3
    return term1 + term2

def dG_da(alpha, c, q):
    Ph = Phi(alpha, q); Php = 2*(q*q-1)*mp.sin(alpha)*mp.cos(alpha)
    W = Wfun(alpha); Wp = 2*(mp.cos(alpha)*mp.sin(alpha) - alpha)/mp.sin(alpha)**2
    s = mp.sin(alpha); co = mp.cos(alpha)
    den = q + c*Ph
    t1 = (-(Php*W + Ph*Wp)*den + Ph*W*c*Php)/den**2
    t2 = 2*c*(q*q-1)*((Ph + alpha*Php)*s*co + alpha*Ph*(co*co - s*s))/den**2 \
         - 2*c*alpha*Ph*(q*q-1)*s*co*2*c*Php/den**3
    return t1 + t2

def Mtil(alpha, c, q):
    return alpha*alpha*mp.sin(alpha)**2/(q + c*Phi(alpha, q))

def dH_dq(c, q):
    a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
    return (dG_dq(a2,c,q) - dG_dq(a1,c,q)) + (dG_da(a2,c,q)*dalpha_dq(a2,q,c) - dG_da(a1,c,q)*dalpha_dq(a1,q,c))

def dFp_dq(c, q):
    # d/dq [M1t G1 - M2t G2] with all quantities depending on q through alpha_k too
    a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
    M1t = Mtil(a1, c, q); M2t = Mtil(a2, c, q)
    G1 = Gfun(a1, c, q); G2 = Gfun(a2, c, q)
    # dM/dq (total, along curve)
    dM1 = dM_dq(a1, c, q, dalpha_dq(a1,q,c))
    dM2 = dM_dq(a2, c, q, dalpha_dq(a2,q,c))
    dG1 = dG_dq(a1,c,q) + dG_da(a1,c,q)*dalpha_dq(a1,q,c)
    dG2 = dG_dq(a2,c,q) + dG_da(a2,c,q)*dalpha_dq(a2,q,c)
    return dM1*G1 + M1t*dG1 - dM2*G2 - M2t*dG2

def dM_dq(alpha, c, q, aq):
    # total d/dq of Mtil(alpha(q),c,q) = partial + partial_alpha * aq
    Ph = Phi(alpha, q); Phq = 2*q*mp.sin(alpha)**2
    Php = 2*(q*q-1)*mp.sin(alpha)*mp.cos(alpha)
    s = mp.sin(alpha)
    # partial q: alpha^2 sin^2 * (-(1 + c Phq))/(q+c Ph)^2  ... d/dq [1/(q+c Ph)] = -(1 + c Phq)/(q+c Ph)^2
    partq = -alpha*alpha*s*s*(1 + c*Phq)/(q + c*Ph)**2
    # partial alpha: [2a s^2 + 2a^2 s cos]/(den) - a^2 s^2 c Php/den^2
    parta = (2*alpha*s*s + 2*alpha*alpha*s*mp.cos(alpha))/(q + c*Ph) - alpha*alpha*s*s*c*Php/(q + c*Ph)**2
    return partq + parta*aq

print('=== dH/dq decomposition at several (q,c) ===')
for q in [mp.mpf('1.05'), mp.mpf('2'), mp.mpf('10')]:
    for c in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.499')]:
        a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
        br1 = dG_dq(a2,c,q) - dG_dq(a1,c,q)
        br2 = dG_da(a2,c,q)*dalpha_dq(a2,q,c) - dG_da(a1,c,q)*dalpha_dq(a1,q,c)
        tot = dH_dq(c,q)
        print(f'  q={mp.nstr(q,4)} c={mp.nstr(c,4)}: [A2-A1]={mp.nstr(br1,7)}  [Ga]={mp.nstr(br2,7)}  total={mp.nstr(tot,7)}  '
              f'Ga1={mp.nstr(dG_da(a1,c,q),6)} Ga2={mp.nstr(dG_da(a2,c,q),6)}')

print()
print('=== dFp/dq sign check ===')
for q in [mp.mpf('1.01'), mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10'), mp.mpf('100')]:
    cs = [mp.mpf('1e-4') + mp.mpf('0.4998')*k/200 for k in range(201)]
    mn = mp.inf; mx = mp.ninf; cmin = None
    for c in cs:
        v = dFp_dq(c, q)
        if v < mn: mn, cmin = v, c
        if v > mx: mx = v
    print(f'  q={mp.nstr(q,4)}: dFp/dq in [{mp.nstr(mn,6)} at c={mp.nstr(cmin,4)}, {mp.nstr(mx,6)}]')
