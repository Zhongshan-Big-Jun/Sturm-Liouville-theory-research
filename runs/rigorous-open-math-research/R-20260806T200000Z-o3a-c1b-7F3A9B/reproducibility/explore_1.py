# -*- coding: utf-8 -*-
"""explore_1.py: independent re-verification of foundations + test of NEW convexity
mechanisms (D_ww < 0 on the axis, D_tt < 0 on the triangle)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c1_lib as L

# ---- adaptive roots2 (fix the 2pi cap bug): retry with larger caps ----
def roots2_adaptive(a, b, R, caps=(6.0*np.pi, 10.0*np.pi, 16.0*np.pi)):
    for cap in caps:
        try:
            s = np.linspace(1e-9, cap, 6001)
            M = L.sec(s, a, b, R)
            ch = np.signbit(M[1:]) != np.signbit(M[:-1])
            idx = np.nonzero(ch)[0]
            out = []
            for i in idx:
                out.append(L._bisect(lambda t: L.sec(t, a, b, R), s[i], s[i+1]))
                if len(out) == 2:
                    return out[0], out[1]
        except Exception:
            pass
    raise RuntimeError(f"roots2_adaptive failed (a,b,R)=({a},{b},{R})")

# ---- high-accuracy config with adaptive roots ----
def cfg2(a, b, R):
    s1, s2 = roots2_adaptive(a, b, R)
    return s1, s2, L.norm_n(s1, a, b, R), L.norm_n(s2, a, b, R)

def R1R2(a, b, R, cfg=None):
    if cfg is None:
        cfg = cfg2(a, b, R)
    s1, s2, n1, n2 = cfg
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = L.y_at(s1, a, b, R, b); y2b = L.y_at(s2, a, b, R, b)
    R1 = s1**2*y1a**2/n1 - s2**2*y2a**2/n2
    R2 = s1**2*y1b**2/n1 - s2**2*y2b**2/n2
    return R1, R2

def Dval(a, b, R):
    s1, s2 = roots2_adaptive(a, b, R)
    return s2**2 - s1**2

def partials2(a, b, R, h=1e-6):
    """A=dR1/da, B=dR2/da, C=dR2/db, Dp=dR1/db via central differences, s_k implicit."""
    def r1(s1,s2,a,b,R):
        n1 = L.norm_n(s1,a,b,R); n2 = L.norm_n(s2,a,b,R)
        return s1**2*(np.sin(s1*a)/s1)**2/n1 - s2**2*(np.sin(s2*a)/s2)**2/n2
    def r2(s1,s2,a,b,R):
        n1 = L.norm_n(s1,a,b,R); n2 = L.norm_n(s2,a,b,R)
        return s1**2*L.y_at(s1,a,b,R,b)**2/n1 - s2**2*L.y_at(s2,a,b,R,b)**2/n2
    def dsec(s, var):
        if var=='s': return (L.sec(s+h,a,b,R)-L.sec(s-h,a,b,R))/(2*h)
        if var=='a': return (L.sec(s,a+h,b,R)-L.sec(s,a-h,b,R))/(2*h)
        return (L.sec(s,a,b+h,R)-L.sec(s,a,b-h,R))/(2*h)
    s1, s2, n1, n2 = cfg2(a,b,R)
    ds1a = -dsec(s1,'a')/dsec(s1,'s'); ds1b = -dsec(s1,'b')/dsec(s1,'s')
    ds2a = -dsec(s2,'a')/dsec(s2,'s'); ds2b = -dsec(s2,'b')/dsec(s2,'s')
    def d(var, f, s1, s2):
        if var=='a': return (f(s1,s2,a+h,b,R)-f(s1,s2,a-h,b,R))/(2*h)
        if var=='b': return (f(s1,s2,a,b+h,R)-f(s1,s2,a,b-h,R))/(2*h)
        if var=='s1': return (f(s1+h,s2,a,b,R)-f(s1-h,s2,a,b,R))/(2*h)
        return (f(s1,s2+h,a,b,R)-f(s1,s2-h,a,b,R))/(2*h)
    A = d('a',r1,s1,s2) + d('s1',r1,s1,s2)*ds1a + d('s2',r1,s1,s2)*ds2a
    Db = d('b',r1,s1,s2) + d('s1',r1,s1,s2)*ds1b + d('s2',r1,s1,s2)*ds2b
    B = d('a',r2,s1,s2) + d('s1',r2,s1,s2)*ds1a + d('s2',r2,s1,s2)*ds2a
    C = d('b',r2,s1,s2) + d('s1',r2,s1,s2)*ds1b + d('s2',r2,s1,s2)*ds2b
    return dict(A=A, B=B, C=C, Db=Db, s1=s1, s2=s2)

def hessian2(a, b, R):
    """D_aa, D_ab, D_bb from FH double derivatives."""
    p = partials2(a, b, R)
    Daa = -(R-1)*p['A']; Dab = (R-1)*p['B']; Dbb = (R-1)*p['C']
    return Daa, Dab, Dbb, p

# ---- P1 verification: FH with eigenvalue factor ----
def check_fh(R=4.0):
    pts = [(0.42,0.56),(0.45,0.55),(0.3,0.7),(0.4196,0.5804)]
    print(f"P1 check (R={R}): dlambda/da = (R-1)*lambda*u(a)^2")
    for (a,b) in pts:
        h = 1e-6
        lam1 = Dval_lam(a,b,R,1); lam2 = Dval_lam(a,b,R,2)
        s1,s2,n1,n2 = cfg2(a,b,R)
        u1a2 = (np.sin(s1*a)/s1)**2/n1
        u2a2 = (np.sin(s2*a)/s2)**2/n2
        fd1 = (Dval_lam(a+h,b,R,1)-Dval_lam(a-h,b,R,1))/(2*h)
        fd2 = (Dval_lam(a+h,b,R,2)-Dval_lam(a-h,b,R,2))/(2*h)
        fh1 = (R-1)*lam1*u1a2; fh2 = (R-1)*lam2*u2a2
        print(f"  ({a},{b}): fd1={fd1:.8f} fh1={fh1:.8f} | fd2={fd2:.8f} fh2={fh2:.8f}")

def Dval_lam(a,b,R,k):
    s1,s2 = roots2_adaptive(a,b,R)
    return (s1**2 if k==1 else s2**2)

if __name__ == "__main__":
    check_fh(4.0)
    # T3 check
    for (a,b,R) in [(0.42,0.56,4.0),(0.45,0.55,10.0),(0.3,0.7,2.0),(0.35,0.65,100.0)]:
        p = partials2(a,b,R)
        print(f"T3 ({a},{b},{R}): dR1/db + dR2/da = {p['Db']+p['B']:.3e}")

