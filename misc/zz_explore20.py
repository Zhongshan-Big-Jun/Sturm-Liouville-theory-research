import pickle, sympy as sp
import mpmath as mp
mp.mp.dps = 30
with open('misc/t3_symbols5.pkl','rb') as fh:
    d = pickle.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
subs = {k: d[k] for k in ['G','Gc','Gx','u','P']}
fG = sp.lambdify((A,t,sg,cg,st,ct), sp.cancel(d['G']), 'mpmath')
fGc = sp.lambdify((A,t,sg,cg,st,ct), sp.cancel(d['Gc']), 'mpmath')
fGx = sp.lambdify((A,t,sg,cg,st,ct), sp.cancel(d['Gx']), 'mpmath')
fu = sp.lambdify((A,t,sg,cg,st,ct), sp.cancel(d['u']), 'mpmath')
def E(g,q,fn):
    A_ = mp.pi-g; t_ = mp.atan(q*mp.tan(g))
    return fn(A_, t_, mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_))
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
N = 250
res = {}
for name, fn in [('G',fG),('Gc',fGc),('Gx',fGx),('u',fu)]:
    mn = (mp.mpf('1e30'), None); mx = (mp.mpf('-1e30'), None)
    for i in range(N+1):
        g = glo + mp.mpf(i)*(ghi-glo)/N
        for j in range(N+1):
            q = 1 + mp.mpf(j)/N
            v = E(g,q,fn)
            if v < mn[0]: mn = (v, (float(g),float(q)))
            if v > mx[0]: mx = (v, (float(g),float(q)))
    res[name] = (mn, mx)
    print('%s: [%.4f, %.4f]  min at %s  max at %s' % (name, mn[0], mx[0], mn[1], mx[1]))
# uGx
mn = (mp.mpf('1e30'), None); mx = (mp.mpf('-1e30'), None)
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        v = E(g,q,fu)*E(g,q,fGx)
        if v < mn[0]: mn = (v, (float(g),float(q)))
        if v > mx[0]: mx = (v, (float(g),float(q)))
print('uGx: [%.4f, %.4f]  min at %s  max at %s' % (mn[0], mx[0], mn[1], mx[1]))
# G^2+Gc
mn = (mp.mpf('1e30'), None); mx = (mp.mpf('-1e30'), None)
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        v = E(g,q,fG)**2 + E(g,q,fGc)
        if v < mn[0]: mn = (v, (float(g),float(q)))
        if v > mx[0]: mx = (v, (float(g),float(q)))
print('G^2+Gc: [%.4f, %.4f]  min at %s  max at %s' % (mn[0], mx[0], mn[1], mx[1]))
