import json, sympy as sp
import mpmath as mp
mp.mp.dps = 30
with open('misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
q = sp.symbols('q')
Phi = cg**2 + q**2*sg**2
K = 3
R = 0
for (mon, coeff) in sp.Poly(NJ2, A, t, sg, cg, st, ct).terms():
    eA, et, e2, e3, e4, e5 = mon
    k = (e4 + e5)//2
    R += coeff * A**eA * t**et * sg**e2 * cg**e3 * (q*sg)**e4 * cg**e5 * Phi**(K - k)
R = sp.expand(R)
fR = sp.factor(R)
print('R factor: 32*A^2*cg^4*sg^2 * H')
# extract H
H = sp.expand(R / (32*A**2*cg**4*sg**2))
print('H degree in q:', sp.Poly(H, q).degree())
Hq = sp.Poly(H, q)
# ranges of each q-coefficient on box
def Hcoef_ranges():
    glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
    N = 120
    res = {k: [mp.mpf('1e30'), mp.mpf('-1e30')] for k in range(7)}
    for i in range(N+1):
        g = glo + mp.mpf(i)*(ghi-glo)/N
        A_ = mp.pi-g; sg_, cg_ = mp.sin(g), mp.cos(g)
        for j in range(N+1):
            q_ = 1 + mp.mpf(j)/N
            t_ = mp.atan(q_*mp.tan(g))
            subs = {A: A_, t: t_, sg: sg_, cg: cg_, q: q_}
            for k in range(7):
                c = sp.expand(Hq.coeff_monomial(q**k))
                v = float(c.evalf(subs=subs))
                if v < res[k][0]: res[k][0] = v
                if v > res[k][1]: res[k][1] = v
    return res
res = Hcoef_ranges()
for k in range(7):
    print('q^%d coeff range: [%.6f, %.6f]' % (k, res[k][0], res[k][1]))
