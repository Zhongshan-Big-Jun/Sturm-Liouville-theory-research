import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def Fz(g, z):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    c12 = cg*abs(B2) if B1 >= 0 else cg*abs(M)
    t = mp.acos(mp.sqrt(z)); st = mp.sqrt(1-z)
    LB = c12*A*A*cg*(1-z)*z + 2*A**3*sg*sg*t*z**(mp.mpf(5)/2) + G5*A*sg*t*st*mp.sqrt(z)*cg*cg
    Q = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
    P2 = t*t*cg*sg*sg*Q
    return LB - P2
N = 100
dmin = mp.mpf('1e30'); dmax = mp.mpf('-1e30'); bad = 0
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    z_lo = cg*cg/(cg*cg+4*sg*sg); z_hi = cg*cg
    for j in range(N+1):
        z = z_lo + mp.mpf(j)*(z_hi-z_lo)/N
        # derivative in z (central diff)
        hz = (z_hi-z_lo)/N * mp.mpf('0.05')
        zz = min(max(z, z_lo+hz), z_hi-hz)
        d = (Fz(g, zz+hz)-Fz(g, zz-hz))/(2*hz)
        if d < dmin: dmin = d
        if d > dmax: dmax = d
print('dF/dz range: [%.4f, %.4f]' % (dmin, dmax))
