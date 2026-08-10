import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def facts(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    return A, sg, cg, B1, M, B2
def c12(g):
    A, sg, cg, B1, M, B2 = facts(g)
    return cg*abs(B2) if B1 >= 0 else cg*abs(M)
def LB(g, q):
    A, sg, cg, B1, M, B2 = facts(g)
    t = mp.atan(q*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
    return c12(g)*A*A*cg*st*st*ct*ct + 2*A**3*sg*sg*t*ct**5 + 3.8*A*sg*t*st*ct*cg*cg
h = mp.mpf('1e-7')
for gi in [0, 40, 80, 120, 160, 200]:
    g = glo + mp.mpf(gi)*(ghi-glo)/200
    vals = []
    for j in range(0, 201, 25):
        q = 1 + mp.mpf(j)/200
        vals.append((float(q), float(LB(g,q))))
    # derivative sign
    dq1 = (LB(g,1+h)-LB(g,1-h))/(2*h)
    dq2 = (LB(g,2+h)-LB(g,2-h))/(2*h)
    print('g=%.4f: LB(q) %s ; dLB/dq at q=1: %.4f, at q=2: %.4f' % (g, ['%.4f'%v[1] for v in vals], dq1, dq2))
