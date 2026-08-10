# -*- coding: utf-8 -*-
# Master verification for symmetric-line well family (gap a).
# STRICT/EVIDENCE discipline: this file only PRODUCES numeric checks (EVIDENCE).
import mpmath as mp
mp.mp.dps = 50
pi = mp.pi

def even_sec(A, c, q):
    # tan(A)*tan(cA) = 1/q,  q = qtilde = 1/m in (0,1); A in (0,pi/2), cA in (0,pi/2)
    return mp.tan(A)*mp.tan(c*A) - 1/q

def odd_sec(A, c, q):
    # q*tan(A2) + tan(c*A2) = 0, A2 in (0,pi); c*A2 in (0,pi)
    return q*mp.tan(A) + mp.tan(c*A)

def Efun(x, q):
    return mp.atan(1/(q*mp.tan(x)))   # x in (0,pi/2)

def Ofun(x, q):
    # continuous branch, x in (0,pi)
    if x < pi/2:
        return pi - mp.atan(q*mp.tan(x))
    elif x == pi/2:
        return pi/2
    else:
        return mp.atan(-q*mp.tan(x))

def alpha1(c, q):
    # E(alpha1) = c*alpha1, alpha1 in (0,pi/2); E decreasing -> unique
    f = lambda A: Efun(A, q) - c*A
    lo, hi = mp.mpf('1e-30'), pi/2 - mp.mpf('1e-30')
    # bracket: E(0+)=pi/2>0? E->pi/2 as x->0+; c*A->0 so f(0+)=pi/2>0; f(pi/2-)=0-c*pi/2<0
    return mp.findroot(f, (lo, hi))

def alpha2(c, q):
    # O(alpha2) = c*alpha2, alpha2 in (0,pi); O decreasing from pi to 0
    f = lambda A: Ofun(A, q) - c*A
    return mp.findroot(f, (mp.mpf('1e-30'), pi - mp.mpf('1e-30')))

def Phi(x, q):
    return mp.cos(x)**2 + q**2*mp.sin(x)**2

def Mf(x, c, q):
    return x**2*mp.sin(x)**2/(q + c*Phi(x, q))

def Fe(c, q):
    a1 = alpha1(c, q); a2 = alpha2(c, q)
    return Mf(a1, c, q) - Mf(a2, c, q)

# ---------------- direct eigenvalue computation for symmetric well ----------------
def eigs_sym_well(v, R):
    # solve secular directly with transfer matrix; return s1, s2 (and check even/odd)
    m = mp.sqrt(R)
    # even mode: y'(1/2)=0.  phases A=msv, th=s(1/2-v).  tan A tan th = m.
    fe = lambda s: mp.tan(m*s*v)*mp.tan(s*(mp.mpf(1)/2-v)) - m
    # find first positive root of fe (s in (0, pi/(m*v))... careful; s1 in (0, pi/m/(2v)? )
    # bracket manually: scan
    roots = []
    s = mp.mpf('1e-9'); prev = None
    # fe has poles; scan with small steps and check sign changes of tan-product? Better: solve E-branch.
    # Use phase branch: A in (0,pi/2), c = (1-2v)/(2mv), alpha1 = A solves E(alpha1)=c*alpha1 with q=1/m
    q = 1/m; c = (mp.mpf(1)-2*v)/(2*m*v)
    a1 = alpha1(c, q); a2 = alpha2(c, q)
    s1 = 2*(c+q)*a1   # s_k = 2(c+q)*alpha_k
    s2 = 2*(c+q)*a2
    return s1, s2, a1, a2, c, q

def norm_closed(s, v, R, which):
    # n_k = y_k'(1) * Y'(s_k) / (2 s_k); y1'(1)=-1, y2'(1)=+1
    # Y'(s) = d/ds y(1;s) where y = slope-normalized solution.
    # Closed form: Y'(s_even) = -P(A,th), Y'(s_odd) = +P(tau A, tau th)
    m = mp.sqrt(R)
    A = m*s*v; th = s*(mp.mpf(1)/2 - v)
    def P(x, y):
        t = mp.tan(x)
        return (x*m*(1+t**2) + y*(m**2 + t**2))/(2*(x + m*y)**2*(1+t**2))
    if which == 1:
        yp1 = mp.mpf(-1)
        return yp1 * (-P(A, th)) / (2*s)
    else:
        # need tau = s2/s1 to get phases for mode 2
        s2 = None
        # compute both s via phase branch
        q = 1/m; c = (mp.mpf(1)-2*v)/(2*m*v)
        a1 = alpha1(c, q); a2 = alpha2(c, q)
        s1 = 2*(c+q)*a1; s2 = 2*(c+q)*a2
        tau = s2/s1
        yp2 = mp.mpf(1)
        return yp2 * P(tau*A, tau*th) / (2*s)

def norm_direct(s, v, R, which):
    # direct integration of rho*y^2 for slope-normalized y, using exact piecewise trig
    m = mp.sqrt(R)
    A = m*s*v; th = s*(mp.mpf(1)/2 - v)
    # y on [0,v]: sin(msx)/(ms); on [v,1/2]: yv*cos(s(x-v)) + ypv*sin(s(x-v))/s
    yv = mp.sin(A)/(m*s); ypv = mp.cos(A)
    def y(x):
        if x <= v:
            return mp.sin(m*s*x)/(m*s)
        else:
            return yv*mp.cos(s*(x-v)) + ypv*mp.sin(s*(x-v))/s
    # integrate rho*y^2 over [0,1]: symmetry, twice [0,1/2]
    # rho = R on [0,v], 1 on [v,1/2]
    def integ(x):
        rho = R if x <= v else 1
        return rho*y(x)**2
    return 2*mp.quad(integ, [0, v, mp.mpf(1)/2])

# ---------------- checks ----------------
print('=== Check 1: phase-branch eigenvalues vs direct secular ===')
for v in ['0.1','0.2','0.3','0.4','0.45','0.49']:
    vv = mp.mpf(v)
    for R in ['1.2','1.5','4.0']:
        RR = mp.mpf(R)
        m = mp.sqrt(RR); c = (1-2*vv)/(2*m*vv); q = 1/m
        a1 = alpha1(c,q); a2 = alpha2(c,q)
        s1 = 2*(c+q)*a1; s2 = 2*(c+q)*a2
        # direct: even sec tan(msv)tan(s(1/2-v)) = m
        fe = lambda s: mp.tan(m*s*vv)*mp.tan(s*(mp.mpf(1)/2-vv)) - m
        # first root of fe on (0, pi/(2m vv))? actually s1 small; use scan-free: root near s1
        s1c = mp.findroot(fe, s1)
        fo = lambda s: mp.tan(m*s*vv) + m*mp.tan(s*(mp.mpf(1)/2-vv))
        s2c = mp.findroot(fo, s2)
        err1 = abs(s1c-s1)/s1; err2 = abs(s2c-s2)/s2
        print('  v=%s R=%s: s1 err=%s, s2 err=%s' % (v,R,mp.nstr(err1,4),mp.nstr(err2,4)))

print('=== Check 2: norm closed form vs direct integration ===')
for v in ['0.1','0.3','0.4','0.45']:
    vv = mp.mpf(v)
    for R in ['1.2','1.5','4.0']:
        RR = mp.mpf(R)
        m = mp.sqrt(RR); c = (1-2*vv)/(2*m*vv); q = 1/m
        a1 = alpha1(c,q); a2 = alpha2(c,q)
        s1 = 2*(c+q)*a1; s2 = 2*(c+q)*a2
        for k in [1,2]:
            nc = norm_closed(s1 if k==1 else s2, vv, RR, k)
            nd = norm_direct(s1 if k==1 else s2, vv, RR, k)
            print('  v=%s R=%s mode=%d: closed/direct rel err=%s' % (v,R,k,mp.nstr(abs(nc-nd)/abs(nd),4)))
