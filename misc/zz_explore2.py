import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
N = 200
def terms(g, q):
    A = mp.pi-g; t = mp.atan(q*mp.tan(g))
    sg, cg, st, ct = mp.sin(g), mp.cos(g), mp.sin(t), mp.cos(t)
    B1 = A*cg-2*sg; B2 = 4*A*A*cg*cg-A*A-12*A*cg*sg+6*sg*sg
    B4 = 7*A*cg*cg-A*sg*sg-4*cg*sg; B5 = A*A*cg*cg-A*A*sg*sg+2*A*A+12*A*cg*sg-12*sg*sg
    B7 = 3*A*cg*cg+A*sg*sg+8*cg*sg
    T = [None]
    T.append(-2*A**3*B1*st*st*ct**4); T.append(A*A*cg*B2*st*st*ct*ct)
    T.append(-2*A**3*sg*t*st*ct**5); T.append(A*A*sg*t*B4*st*ct**3)
    T.append(-A*cg*cg*sg*t*B5*st*ct); T.append(4*A*A*cg*sg*sg*t*t*ct**4)
    T.append(-A*cg*sg*sg*t*t*B7*ct*ct); T.append(6*cg**3*sg**4*t*t)
    return T, dict(A=A,t=t,sg=sg,cg=cg,st=st,ct=ct)
groups = {
 'G1=T1+T2': (1,2), 'G2=T3+T6': (3,6), 'G3=T7+T8': (7,8),
 'G4=T1+T2+T3': (1,2,3), 'G5=T4+T5': (4,5), 'G6=T6+T7+T8': (6,7,8),
 'G7=T3+T6+T7+T8': (3,6,7,8), 'G8=T1+T2+T6+T7+T8': (1,2,6,7,8),
 'G9=T1+T2+T3+T6': (1,2,3,6), 'G10=T7+T8': (7,8),
 'G11=T3+T7': (3,7), 'G12=T6+T8': (6,8),
 'G13=T1+T2+T3+T7': (1,2,3,7), 'G14=T6+T8+T4': (4,6,8),
}
R = {k: [mp.mpf('1e30'), mp.mpf('-1e30')] for k in groups}
pos_loc = {}
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        T, _ = terms(g, q)
        for k, idx in groups.items():
            v = sum(T[i] for i in idx)
            if v < R[k][0]: R[k][0] = v
            if v > R[k][1]: R[k][1] = v
for k in groups:
    print('%s: [%.5f, %.5f]' % (k, R[k][0], R[k][1]))
# where is P2=T6+T7+T8 positive?
print()
mx = mp.mpf('-1e30'); loc = None
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        T, v = terms(g, q)
        p2 = T[6]+T[7]+T[8]
        if p2 > mx: mx, loc = p2, (float(g), float(q))
print('P2 max %.5f at (g,q)=(%.4f, %.4f)' % (mx, loc[0], loc[1]))
