import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def facts(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    return A, sg, cg, B1, M, B2, B4, B5, B7, G5
def c12(g):
    A, sg, cg, B1, M, B2, B4, B5, B7, G5 = facts(g)
    return cg*abs(B2) if B1 >= 0 else cg*abs(M)
def Q(g, q):
    A, sg, cg, B1, M, B2, B4, B5, B7, G5 = facts(g)
    t = mp.atan(q*mp.tan(g)); ct = mp.cos(t)
    z = ct*ct
    return 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
def P2v(g, q):
    A, sg, cg, B1, M, B2, B4, B5, B7, G5 = facts(g)
    t = mp.atan(q*mp.tan(g)); ct = mp.cos(t)
    return t*t*cg*sg*sg*Q(g,q)
def LB(g, q):
    A, sg, cg, B1, M, B2, B4, B5, B7, G5 = facts(g)
    t = mp.atan(q*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
    return c12(g)*A*A*cg*st*st*ct*ct + 2*A**3*sg*sg*t*ct**5 + 3.8*A*sg*t*st*ct*cg*cg
def F(g, q): return LB(g,q) - P2v(g,q)
h = mp.mpf('1e-7')
N = 120
dqmn = mp.mpf('1e30'); dqmx = mp.mpf('-1e30'); dgmn = mp.mpf('1e30'); dgmx = mp.mpf('-1e30')
loc_q = None; loc_g = None
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        dq = (F(g,q+h)-F(g,q-h))/(2*h)
        dg = (F(g+h,q)-F(g-h,q))/(2*h)
        if dq < dqmn: dqmn, loc_q = dq, (float(g), float(q))
        if dq > dqmx: dqmx = dq
        if dg < dgmn: dgmn, loc_g = dg, (float(g), float(q))
        if dg > dgmx: dgmx = dg
print('dF/dq in [%.4f, %.4f], min at %s' % (dqmn, dqmx, loc_q))
print('dF/dg in [%.4f, %.4f], min at %s' % (dgmn, dgmx, loc_g))
# min of F
mn = (mp.mpf('1e30'), None)
for i in range(400+1):
    g = glo + mp.mpf(i)*(ghi-glo)/400
    for j in range(400+1):
        q = 1 + mp.mpf(j)/400
        v = F(g,q)
        if v < mn[0]: mn = (v, (float(g), float(q)))
print('F min = %.5f at %s' % (mn[0], mn[1]))
