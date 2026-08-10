import mpmath as mp
mp.mp.dps = 40
pi = mp.pi

def secular(v, R, s):
    m = mp.sqrt(R); A = m*s*v; th = s*(mp.mpf(1)/2 - v)
    y_v = mp.sin(A)/(m*s); yp_v = mp.cos(A)
    psi = s*(1-2*v)
    y_m = y_v*mp.cos(psi) + yp_v*mp.sin(psi)/s
    yp_m = -y_v*s*mp.sin(psi) + yp_v*mp.cos(psi)
    return y_m*mp.cos(A) + yp_m*mp.sin(A)/(m*s)

def eigs_sym(v, R):
    m = mp.sqrt(R)
    f = lambda s: secular(v, R, s)
    xs = [mp.mpf(k)*mp.mpf(0.004) for k in range(1, 5000)]
    roots=[]; prev=None
    for x in xs:
        val=f(x)
        if prev is not None and prev*val<0:
            r=mp.findroot(f,(xs[xs.index(x)-1],x)); roots.append(r)
        prev=val
        if len(roots)>=2: break
    return roots[0], roots[1]

def Fep(q, c):
    m = 1/q; R = m**2
    v = 1/(2*(c*m+1))
    s1,s2 = eigs_sym(v,R)
    th1 = s1*(mp.mpf(1)/2-v); th2 = s2*(mp.mpf(1)/2-v)
    r = 2*m*v/(1-2*v)
    a1 = r*th1; a2 = r*th2
    def Mf(x):
        Phi = mp.cos(x)**2 + q**2*mp.sin(x)**2
        return x**2*mp.sin(x)**2/(q + c*Phi)
    def Gval(x):
        Phi = mp.cos(x)**2 + q**2*mp.sin(x)**2
        D = q + c*Phi
        return -Phi*(3+2*x*mp.cot(x))/D + 2*c*x*Phi*(q**2-1)*mp.sin(x)*mp.cos(x)/D**2
    M1,M2 = Mf(a1), Mf(a2)
    G1,G2 = Gval(a1), Gval(a2)
    return M1*G1 - M2*G2

q0 = 1/mp.sqrt(mp.mpf('1.5'))
print('(b) Fep(q, 1/2):')
for q in [q0, mp.mpf('0.85'), mp.mpf('0.9'), mp.mpf('0.95'), mp.mpf('0.99'), mp.mpf('0.999')]:
    print('  q=%s: Fep(1/2)=%s' % (mp.nstr(q,5), mp.nstr(Fep(q, mp.mpf('0.5')),9)))
print('(a) Fep second-difference on box [q0,1]x[0.42,0.5]:')
h = mp.mpf('1e-4')
for q in [q0, mp.mpf('0.9'), mp.mpf('1.0')]:
    for c in [mp.mpf('0.42'), mp.mpf('0.45'), mp.mpf('0.48')]:
        fpp = (Fep(q,c-h) - 2*Fep(q,c) + Fep(q,c+h))/h**2
        print('  q=%s c=%s: Fep2~%s' % (mp.nstr(q,4), mp.nstr(c,4), mp.nstr(fpp,7)))
