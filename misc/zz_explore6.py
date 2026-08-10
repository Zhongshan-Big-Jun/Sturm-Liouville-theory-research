import json, sympy as sp
import mpmath as mp
mp.mp.dps = 30
with open('misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
dNJdt = sp.diff(NJ2, t)
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')
fd = sp.lambdify((A,t,sg,cg,st,ct), dNJdt, 'mpmath')
def NJ(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    return fN(A_, t_, mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_))
def dNJdq(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    dtdq = mp.tan(g)/(1+q*q*mp.tan(g)**2)
    return fd(A_, t_, mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_))*dtdq
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
N = 200
# map region dNJ/dq < 0: for each gamma, find q-range where negative
for gi in [0, 40, 80, 120, 160, 200]:
    g = glo + mp.mpf(gi)*(ghi-glo)/N
    neg = []
    prev = None
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        s = dNJdq(g, q) < 0
        if s != prev:
            neg.append((j, float(q), s))
            prev = s
    print('g=%.4f: sign changes at q: %s' % (g, [(round(q,3), '+' if s else '-') for _, q, s in neg]))
# bisection for the zero curve: for each gamma, the q where dNJ/dq=0 (if any)
def zero_q(g, qlo, qhi):
    flo, fhi = dNJdq(g, qlo), dNJdq(g, qhi)
    if flo*fhi > 0: return None
    for _ in range(80):
        qm = (qlo+qhi)/2
        if dNJdq(g, qm)*flo <= 0: qhi = qm
        else: qlo = qm
    return (qlo+qhi)/2
print('zero curve of dNJ/dq:')
for i in range(0, 201, 10):
    g = glo + mp.mpf(i)*(ghi-glo)/200
    z = zero_q(g, 1, 2)
    print('  g=%.4f -> q*=%s' % (g, ('none' if z is None else '%.5f' % z)))
