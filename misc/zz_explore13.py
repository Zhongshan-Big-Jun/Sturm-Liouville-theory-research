import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
N = 120
rng = {k: [mp.mpf('1e30'), mp.mpf('-1e30')] for k in ['K0b','K1b','K2b','K0','K1','K2']}
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        t = mp.atan(q*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
        K0b = 4*A*A*cg**3 - 2*A*A*cg*ct*ct - A*A*cg - 12*A*cg*cg*sg + 4*A*ct*ct*sg + 6*cg*sg*sg
        K1b = (A*A*cg**4 - 7*A*A*cg*cg*ct*ct - A*A*cg*cg*sg*sg + 2*A*A*cg*cg + 2*A*A*ct**4 + A*A*ct*ct*sg*sg + 12*A*cg**3*sg + 4*A*cg*ct*ct*sg - 12*cg*cg*sg*sg)
        K2b = (A*A*cg**4 - 3*A*A*cg*cg*ct*ct + A*A*cg*cg*sg*sg - A*A*cg*cg + 4*A*A*ct**4 - A*A*ct*ct*sg*sg - 8*A*cg*ct*ct*sg + 6*cg*cg*sg*sg)
        K0 = 32*A**4*cg*ct*ct*st*st*K0b
        K1 = -32*A**3*cg*ct*sg*st*K1b
        K2 = 32*A*A*cg*cg*sg*sg*K2b
        for k, v in [('K0b',K0b),('K1b',K1b),('K2b',K2b),('K0',K0),('K1',K1),('K2',K2)]:
            if v < rng[k][0]: rng[k][0] = v
            if v > rng[k][1]: rng[k][1] = v
for k in ['K0b','K1b','K2b','K0','K1','K2']:
    print('%s: [%.6f, %.6f]' % (k, rng[k][0], rng[k][1]))
