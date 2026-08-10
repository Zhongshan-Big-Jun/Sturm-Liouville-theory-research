# -*- coding: utf-8 -*-
"""t3_num2: extract numerators, factor, summarize."""
import sympy as sp
import pickle, time

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
P = 2*(A*st*ct + t*sg*cg)
p = A*st*ct + t*sg*cg   # P/2
q2m1 = (cg**2-ct**2)/(sg**2*ct**2)
Phi  = cg**2/ct**2
Phi_x= -2*q2m1*sg*cg
W    = 3 - 2*A*cg/sg
W_x  = -2*cg/sg - 2*A/sg**2
sc_  = -sg*cg
cos2x= cg**2 - sg**2
c    = t/A
K    = cg/(2*A*sg*ct**2)
D, D2, D3 = P*K, (P*K)**2, (P*K)**3
G  = (4*A**2*cg**2 - 6*A*sg*cg)/P - 8*A**2*t*sg*cg*(cg**2-ct**2)/P**2
Gc = (12*A**2*sg**2*cg**2 - 8*A**3*sg*cg*(2*cg**2-ct**2))/P**2 + 32*A**3*t*sg**2*cg**2*(cg**2-ct**2)/P**3
u  = 2*A**2*sg*cg/P
t1 = -(Phi_x*W + Phi*W_x)/D
t2 = Phi*W*c*Phi_x/D2
t3 = 2*c*(Phi*q2m1*sc_ + A*Phi_x*q2m1*sc_ + A*Phi*q2m1*cos2x)/D2
t4 = -4*c**2*A*Phi*Phi_x*q2m1*sc_/D3
den_extra = cg**3*sg**3*ct**6
GxP3c = sum(sp.expand(tt*P**3*den_extra) for tt in [t1,t2,t3,t4])
Gx = GxP3c/(P**3*den_extra)

def d_dt(f): return sp.diff(f, t) + ct*sp.diff(f, st) - st*sp.diff(f, ct)
def d_dg(f): return -sp.diff(f, A) + cg*sp.diff(f, sg) - sg*sp.diff(f, cg)
dG_dt = d_dt(G); dG_dg = d_dg(G); dGc_dt = d_dt(Gc); dGc_dg = d_dg(Gc); dGx_dt = d_dt(Gx); dGx_dg = d_dg(Gx)
comp = {
 'dG_dq': (dG_dt, 'p3'),
 'dG_dg': (dG_dg + dG_dt*st*ct/(sg*cg), 'sg*p3'),
 'dGc_dq': (dGc_dt, 'p4'),
 'dGc_dg': (dGc_dg + dGc_dt*st*ct/(sg*cg), 'p4'),
 'dGx_dq': (dGx_dt, 'ct*sg*p4'),
 'dGx_dg': (dGx_dg + dGx_dt*st*ct/(sg*cg), 'cg*sg2*p4'),
}
res = {}
for k,(v,dstr) in comp.items():
    n = sp.expand(v)
    # clear denominators manually: denominators are powers of sg,ct,cg,p
    # multiply by sg^a ct^b cg^c p^d until polynomial
    for mult in [p**3, p**4]:
        pass
    # use fraction with expansion
    n, d = sp.fraction(sp.together(v))
    n = sp.expand(n); d = sp.expand(d)
    # find minimal clearing: repeatedly multiply by p, sg, ct, cg and test polynomial
    extra = sp.Integer(1)
    cur = v
    for name, sym in [('p',p),('sg',sg),('ct',ct),('cg',cg)]:
        for _ in range(8):
            nn, dd = sp.fraction(sp.together(cur))
            if dd == 1:
                break
            cur = sp.expand(cur*sym)
            extra = extra*sym
    nn = sp.expand(sp.fraction(sp.together(cur))[0])
    res[k] = (nn, extra, dstr)
    print('%-8s: clearing=%s  num terms=%d  total deg=%d' % (k, extra, len(sp.Add.make_args(nn)), sp.Poly(nn, A,t,sg,cg,st,ct).total_degree()))
    t0 = time.time()
    try:
        f = sp.factor(nn)
        print('        factor: %s' % (str(f)[:200]))
    except Exception as e:
        print('        factor failed:', e)
    print('        time %.1fs' % (time.time()-t0))

with open('misc/t3_num2.pkl','wb') as fh: pickle.dump({'res': res}, fh)
print('saved misc/t3_num2.pkl')
