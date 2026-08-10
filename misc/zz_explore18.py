import json, sympy as sp
import mpmath as mp
mp.mp.dps = 30
with open('misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')
def NJ(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    return fN(A_, t_, mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_))
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
h = mp.mpf('1e-6')
# second derivative in q via finite differences
N = 60
worst = (mp.mpf('1e30'), None); best = (mp.mpf('-1e30'), None)
cnt_pos = 0; cnt_neg = 0
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        d2 = (NJ(g,q+h)-2*NJ(g,q)+NJ(g,q-h))/(h*h)
        if d2 < worst[0]: worst = (d2, (float(g), float(q)))
        if d2 > best[0]: best = (d2, (float(g), float(q)))
        if d2 > 0: cnt_pos += 1
        else: cnt_neg += 1
print('d2NJ/dq2: min %.2f max %.2f ; positive %d negative %d' % (worst[0], best[0], cnt_pos, cnt_neg))
# check NJ(g,q) vs linear interp of endpoints at sample
bad = 0
for i in range(40+1):
    g = glo + mp.mpf(i)*(ghi-glo)/40
    for j in range(40+1):
        q = 1 + mp.mpf(j)/40
        lin = NJ(g,1) + (q-1)*(NJ(g,2)-NJ(g,1))
        if NJ(g,q) > lin + mp.mpf('1e-8'): bad += 1
print('points above chord: %d' % bad)
