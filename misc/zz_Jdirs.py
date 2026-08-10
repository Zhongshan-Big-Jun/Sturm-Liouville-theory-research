# -*- coding: utf-8 -*-
"""dJ/dg|q and dJ/dq|g on T2 with CORRECT J."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 50

def comps(x, th):
    q = -tan(th)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Phi = b*b/(C*C)
    c = th/x
    den = q + c*Phi
    u = x*Phi/den
    A0 = mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*(-b)/den
    V = H - A0
    Phix = 2*s*b*(1-q*q)
    denx = c*Phix
    ux = (Phi + x*Phix)/den - x*Phi*denx/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = 2*c*(q*q-1)*((b*b - s*s)*den - s*(-b)*denx)/(den*den)
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*b*q/(den*den))
    J = G*G + Gc - u*Gx
    return J

def J_gq(g, q):
    A = mppi - g
    t = atan(q*tan(g))
    return comps(A, t)

gstar = mpf('0.65564932893873566325493245529469')
glo, ghi = gstar, mppi/3
h = mpf('1e-7')
def qlo(g): return max(mpf(1), tan(mpf('0.4')*(mppi-g))/tan(g))
def qhi(g): return min(mpf(2), tan(mpf('0.5')*(mppi-g))/tan(g))
N = 120
mn = {'dg': (mpf('1e30'), None), 'dq': (mpf('1e30'), None)}
mx = {'dg': (mpf('-1e30'), None), 'dq': (mpf('-1e30'), None)}
for i in range(N+1):
    g = glo + mpf(i)*(ghi-glo)/N
    ql, qh = qlo(g), qhi(g)
    if qh <= ql: continue
    for j in range(N+1):
        q = ql + mpf(j)*(qh-ql)/N
        if q <= ql or q >= qh: continue
        J0 = J_gq(g, q)
        dg = (J_gq(g+h, q)-J0)/h; dq = (J_gq(g, q+h)-J0)/h
        for k, v in [('dg', dg), ('dq', dq)]:
            if v < mn[k][0]: mn[k] = (v, (float(g), float(q)))
            if v > mx[k][0]: mx[k] = (v, (float(g), float(q)))
print('dJ/dg|q: [%.4f, %.4f] ; dJ/dq|g: [%.4f, %.4f]' % (mn['dg'][0], mx['dg'][0], mn['dq'][0], mx['dq'][0]))
# J along q=1 (should be <0, from doc) and c=1/2, c=2/5 curves
print()
for (nm, qf) in [('q=1', lambda g: mpf(1)), ('c=1/2', lambda g: tan(g/2)*0+1), ]:
    pass
print('J on q=1 line:')
for g in [mppi/3, mpf('1.0'), mpf('0.95'), mpf('0.9'), 2*mppi/7]:
    print('  g=%.4f: J=%.6f' % (g, J_gq(g, 1)))
print('J on c=1/2 curve (q = tan(g/2... solve atan(q tan g)=(pi-g)/2 => q = tan((pi-g)/2)/tan g):')
for g in [mppi/3, mpf('1.05'), mpf('1.1'), mpf('1.15'), mpf('1.2')]:
    qq = tan((mppi-g)/2)/tan(g)
    print('  g=%.4f q=%.4f: J=%.6f' % (g, qq, J_gq(g, qq)))
