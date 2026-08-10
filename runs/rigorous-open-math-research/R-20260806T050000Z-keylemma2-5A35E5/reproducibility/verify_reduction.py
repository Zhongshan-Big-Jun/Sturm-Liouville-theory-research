# -*- coding: utf-8 -*-
"""verify_reduction.py -- independent audit of the (q,u) reduction.
Checks: (1) IN = G2 * POS with POS > 0 explicit; (2) dIN/dq formula;
(3) dIN/du formula (hand-derived here); (4) dG2/dc vs dIN/du consistency
at large q (the ledger claims dG2/dc > 0 at q=30..100, c in (0.3,0.45),
while dIN/du < 0 was claimed on D -- these must be consistent via the
G2*dPOS/du term).
"""
import sys, mpmath as mp
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
import kl2_lib as L
mp.mp.dps = 40

def u_of(q, c):
    g = L.gamma_of(q, c)
    return q*mp.tan(g)

def A_of(q, u):
    return mp.pi - mp.atan(u/q)

def IN(q, u):
    A = A_of(q, u); t = mp.atan(u)
    return (q*q+u*u)*A*(2*A*q - 3*u + 2*t) - 3*u*q*(1+u*u)*t

def POS(q, u):
    # IN = G2 * POS; POS = D^2*A*(q^2+u^2)*u/(Ph*q)  [hand-derived]
    A = A_of(q, u); t = mp.atan(u)
    Ph = L.Phi(mp.pi - A, q)  # Phi(alpha2)
    c = t/A
    D = q + c*Ph
    return D*D*A*(q*q+u*u)*u/(Ph*q)

# ---- (1) IN = G2*POS ----
print('=== (1) IN = G2*POS ===')
maxrel = mp.mpf(0)
for qv in ['1.05','1.5','2','10','100']:
    for cv in ['0.001','0.1','0.25','0.4','0.49']:
        q = mp.mpf(qv); c = mp.mpf(cv)
        u = u_of(q, c)
        lhs = IN(q, u)
        rhs = L.G2(c, q)*POS(q, u)
        rel = abs(lhs-rhs)/abs(lhs)
        maxrel = max(maxrel, rel)
        if rel > mp.mpf('1e-25'):
            print('  MISMATCH q=%s c=%s rel=%s' % (qv, cv, mp.nstr(rel,3)))
print('  max rel err =', mp.nstr(maxrel, 3))

# ---- (2) dIN/dq formula ----
print('=== (2) dIN/dq formula (M1) ===')
def M1(q, u):
    A = A_of(q, u); t = mp.atan(u)
    return 6*A*A*q*q + 2*A*A*u*u - 2*A*q*u + 4*A*q*t - 3*u*u - u*(1+3*u*u)*t
maxrel = mp.mpf(0)
for qv in ['1.05','1.5','2','10','100']:
    for cv in ['0.05','0.2','0.4','0.49']:
        q = mp.mpf(qv); c = mp.mpf(cv); u = u_of(q, c)
        h = mp.mpf('1e-7')*q
        fd = (IN(q+h, u) - IN(q-h, u))/(2*h)
        rel = abs(fd - M1(q,u))/abs(fd)
        maxrel = max(maxrel, rel)
        if rel > mp.mpf('1e-15'):
            print('  MISMATCH q=%s c=%s rel=%s' % (qv, cv, mp.nstr(rel,3)))
print('  max rel err =', mp.nstr(maxrel, 3))

# ---- (3) dIN/du formula (hand-derived) ----
print('=== (3) dIN/du formula (M2) ===')
def M2(q, u):
    A = A_of(q, u); t = mp.atan(u)
    return 4*A*A*u*q - 7*A*q*q - 9*A*u*u + 2*A*(q*q+u*u)/(1+u*u) + t*(4*A*u - 5*q - 9*q*u*u)
maxrel = mp.mpf(0)
for qv in ['1.05','1.5','2','10','100']:
    for cv in ['0.05','0.2','0.4','0.49']:
        q = mp.mpf(qv); c = mp.mpf(cv); u = u_of(q, c)
        h = mp.mpf('1e-7')
        fd = (IN(q, u+h) - IN(q, u-h))/(2*h)
        rel = abs(fd - M2(q,u))/abs(fd)
        maxrel = max(maxrel, rel)
        if rel > mp.mpf('1e-15'):
            print('  MISMATCH q=%s c=%s rel=%s' % (qv, cv, mp.nstr(rel,3)))
print('  max rel err =', mp.nstr(maxrel, 3))

# ---- (4) dG2/dc vs dIN/du at large q ----
print('=== (4) dG2/dc and dIN/du at q=30..100, c in (0.3,0.45) ===')
def dG2dc_fd(c, q):
    h = mp.mpf('1e-6')
    return (L.G2(c+h, q) - L.G2(c-h, q))/(2*h)
for qv in ['30','50','100']:
    for cv in ['0.30','0.35','0.40','0.45']:
        q = mp.mpf(qv); c = mp.mpf(cv); u = u_of(q, c)
        dgc = dG2dc_fd(c, q)
        du = M2(q, u)
        print('  q=%s c=%s: dG2/dc=%s  dIN/du=%s' % (qv, cv, mp.nstr(dgc,6), mp.nstr(du,6)))
