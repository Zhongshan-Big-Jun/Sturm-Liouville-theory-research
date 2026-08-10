import mpmath as mp
mp.mp.dps = 40
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def F1(g, use_pw=True):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    c12 = cg*abs(B2) if B1 >= 0 else cg*abs(M)
    g5 = G5 if use_pw else mp.mpf('3.8')
    t = mp.atan(2*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
    D = mp.sqrt(1+3*sg*sg)
    z_lo = cg*cg/(D*D)
    Qlo = 4*A*A*z_lo*z_lo - A*B7*z_lo + 6*cg*cg*sg*sg
    TA = c12*A*A*cg*st*st*ct*ct
    TB = 2*A**3*sg*sg*t*ct**5
    TC = g5*A*sg*t*st*ct*cg*cg
    TD = t*t*cg*sg*sg*Qlo
    return TA+TB+TC-TD
mn = (mp.mpf('1e30'), None)
for i in range(4001):
    g = glo + mp.mpf(i)*(ghi-glo)/4000
    v = F1(g)
    if v < mn[0]: mn = (v, float(g))
print('F1 (pointwise G5, piecewise c12) min = %.6f at g=%.6f' % (mn[0], mn[1]))
# also with constant G5=3.8 and constant c12>=1.41 (crude uniform)
def F1c(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    t = mp.atan(2*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
    D = mp.sqrt(1+3*sg*sg)
    z_lo = cg*cg/(D*D)
    Qlo = 4*A*A*z_lo*z_lo - A*B7*z_lo + 6*cg*cg*sg*sg
    TA = 1.41*A*A*cg*st*st*ct*ct
    TB = 2*A**3*sg*sg*t*ct**5
    TC = 3.8*A*sg*t*st*ct*cg*cg
    TD = t*t*cg*sg*sg*Qlo
    return TA+TB+TC-TD
mn2 = (mp.mpf('1e30'), None)
for i in range(4001):
    g = glo + mp.mpf(i)*(ghi-glo)/4000
    v = F1c(g)
    if v < mn2[0]: mn2 = (v, float(g))
print('F1 (constant 3.8 & 1.41) min = %.6f at g=%.6f' % (mn2[0], mn2[1]))
