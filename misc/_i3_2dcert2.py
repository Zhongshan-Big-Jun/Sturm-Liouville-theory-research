# -*- coding: utf-8 -*-
"""iv evaluators with hand-rolled iv_atan; adaptive subdivision counts."""
import mpmath as mp
iv = mp.iv
iv.dps = 50

def iv_atan(x, nterms=160):
    a, b = x.a, x.b
    if a < 0:
        if a > -mp.mpf('1e-40'):
            a = mp.mpf(0)
        else:
            raise ValueError('atan for x >= 0 only, got %s' % (x,))
    def atan_series(xx, n):
        x2 = xx*xx; xp = xx; acc = iv.mpf(0); sign = 1
        for j in range(n+1):
            d = 2*j+1
            term = xp/iv.mpf(d)
            acc = acc + term if sign > 0 else acc - term
            sign *= -1
            xp = xp*x2
        R = xx.b**(2*n+3)/iv.mpf(2*n+3)
        return iv.mpf([acc.a - R, acc.b + R])
    def atan_endpoint(pt):
        if pt <= 1:
            return atan_series(iv.mpf([pt,pt]), nterms)
        inv = iv.mpf([1,1])/iv.mpf([pt,pt])
        return iv.pi/2 - atan_series(inv, nterms)
    return iv.mpf([atan_endpoint(a).a, atan_endpoint(b).b])

def Ph_iv(x, q): return iv.cos(x)**2 + q*q*iv.sin(x)**2

def G_iv(x, c, q):
    Ph = Ph_iv(x, q); D = q + c*Ph; W = 3 + 2*x/iv.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*iv.sin(x)*iv.cos(x)/(D*D)

def Gc_iv(x, c, q):
    Ph = Ph_iv(x, q); D = q + c*Ph; W = 3 + 2*x/iv.tan(x)
    sc = iv.sin(x)*iv.cos(x)
    return Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)

def Gx_iv(x, c, q):
    Ph = Ph_iv(x, q); D = q + c*Ph; W = 3 + 2*x/iv.tan(x)
    sx = iv.sin(x); cx = iv.cos(x); sc = sx*cx
    dPh = 2*sc*(q*q-1); dW = 2/iv.tan(x) - 2*x/(sx**2); dD = c*dPh; dsc = cx**2 - sx**2
    dt1 = -(dPh*W + Ph*dW)/D + Ph*W*dD/(D**2)
    A = 2*c*(q*q-1)
    num2 = A*(x*dPh*sc + Ph*dsc + Ph*sc)
    dt2 = num2/(D**2) - 2*c*x*Ph*(q*q-1)*sc*2*dD/(D**3)
    return dt1 + dt2

def J_iv(x, c, q):
    Ph = Ph_iv(x, q); D = q + c*Ph
    xp = -x*Ph/D
    Gv = G_iv(x, c, q)
    return Gv*Gv + Gx_iv(x, c, q)*xp + Gc_iv(x, c, q)

def c1_iv(x, q):
    return iv_atan(1.0/(q*iv.tan(x)))/x

def c2_iv(g, q):
    return iv_atan(q*iv.tan(g))/(iv.pi - g)

def J1_2d_iv(x, q):
    return J_iv(x, c1_iv(x, q), q)

def J2_2d_iv(g, q):
    return J_iv(iv.pi - g, c2_iv(g, q), q)

def certify2(f, x0, x1, q0, q1, want_pos, depth=0, maxdepth=12):
    x = iv.mpf([x0, x1]); q = iv.mpf([q0, q1])
    try:
        r = f(x, q)
    except Exception as e:
        return None, 1, 0, str(e)
    if want_pos and r.a > 0: return True, 1, 0, ''
    if (not want_pos) and r.b < 0: return True, 1, 0, ''
    if depth >= maxdepth: return None, 1, 0, 'depth'
    xm = (x0+x1)/2; qm = (q0+q1)/2
    subs = [(x0,xm,q0,qm),(xm,x1,q0,qm),(x0,xm,qm,q1),(xm,x1,qm,q1)]
    ok = True; total = 1; leaves = 0; err = ''
    for (a,b,c,d) in subs:
        st, n, lf, e = certify2(f, a, b, c, d, want_pos, depth+1, maxdepth)
        if st is None: ok = False
        if e and not err: err = e
        total += n; leaves += lf
    return (True if ok else None), total, leaves, err

st, n, lf, e = certify2(J1_2d_iv, mp.mpf('0.8411'), mp.mpf('1.1220'), mp.mpf(1), mp.mpf(2), True, maxdepth=10)
print("J1_2d>0: status=%s boxes=%d leaves=%d err=%s" % (st,n,lf,e[:100]))
st, n, lf, e = certify2(J2_2d_iv, mp.mpf('0.6557'), mp.mpf('1.0472'), mp.mpf(1), mp.mpf(2), False, maxdepth=10)
print("J2_2d<0: status=%s boxes=%d leaves=%d err=%s" % (st,n,lf,e[:100]))
