# -*- coding: utf-8 -*-
# Verify relations: f(v) <-> F~_e(c), N1 sign, D'(v) formulas. EVIDENCE only.
import mpmath as mp
mp.mp.dps = 50
pi = mp.pi

def alpha1(c,q):
    return mp.findroot(lambda A: mp.atan(1/(q*mp.tan(A))) - c*A, (mp.mpf('1e-30'), pi/2-mp.mpf('1e-30')))
def alpha2(c,q):
    def O(x):
        if x < pi/2: return pi - mp.atan(q*mp.tan(x))
        elif x == pi/2: return pi/2
        else: return mp.atan(-q*mp.tan(x))
    return mp.findroot(lambda A: O(A) - c*A, (mp.mpf('1e-30'), pi-mp.mpf('1e-30')))
def Phi(x,q): return mp.cos(x)**2 + q**2*mp.sin(x)**2
def Mf(x,c,q): return x**2*mp.sin(x)**2/(q + c*Phi(x,q))
def Fe(c,q): return Mf(alpha1(c,q),c,q) - Mf(alpha2(c,q),c,q)

def y_slope(x, s, v, R):
    # slope-normalized solution at x, exact piecewise
    m = mp.sqrt(R)
    A = m*s*v
    if x <= v:
        return mp.sin(m*s*x)/(m*s)
    yv = mp.sin(A)/(m*s); ypv = mp.cos(A)
    if x <= 1-v:
        return yv*mp.cos(s*(x-v)) + ypv*mp.sin(s*(x-v))/s
    # right block: continue to 1
    y1v = yv*mp.cos(s*(1-2*v)) + ypv*mp.sin(s*(1-2*v))/s
    yp1v = -yv*s*mp.sin(s*(1-2*v)) + ypv*mp.cos(s*(1-2*v))
    dx = x-(1-v)
    return y1v*mp.cos(m*s*dx) + yp1v*mp.sin(m*s*dx)/(m*s)

def norm_direct(s, v, R):
    m = mp.sqrt(R)
    def integ(x):
        rho = R if (x <= v or x >= 1-v) else 1
        return rho*y_slope(x,s,v,R)**2
    return mp.quad(integ, [0, v, 1-v, 1])

def fval_direct(v, R):
    m = mp.sqrt(R); c = (1-2*v)/(2*m*v); q = 1/m
    a1 = alpha1(c,q); a2 = alpha2(c,q)
    s1 = 2*(c+q)*a1; s2 = 2*(c+q)*a2
    n1 = norm_direct(s1,v,R); n2 = norm_direct(s2,v,R)
    y1v = y_slope(v,s1,v,R); y2v = y_slope(v,s2,v,R)
    return s2**2*y2v**2/n2 - s1**2*y1v**2/n1

def N1_direct(v, R):
    m = mp.sqrt(R); c = (1-2*v)/(2*m*v); q = 1/m
    a1 = alpha1(c,q); a2 = alpha2(c,q)
    s1 = 2*(c+q)*a1; s2 = 2*(c+q)*a2
    n1 = norm_direct(s1,v,R); n2 = norm_direct(s2,v,R)
    A = m*s1*v
    return n2/n1 - mp.sin(s2*v*m)**2/mp.sin(A)**2

print('=== f(v) vs F~_e(c) relations (v = 0.1..0.49, R = 1.2,1.5,4) ===')
for vv0 in ['0.1','0.2','0.3','0.4','0.45','0.49']:
    vv = mp.mpf(vv0)
    for RR0 in ['1.2','1.5','4.0']:
        RR = mp.mpf(RR0); m = mp.sqrt(RR); q = 1/m
        c = (1-2*vv)/(2*m*vv)
        fv = fval_direct(vv,RR); F = Fe(c,q)
        myrel = fv / (-2*(c+q)*q**4*F/vv**2)
        handrel = fv / (F/(m**5*vv**3))
        N1 = N1_direct(vv,RR)
        print('  v=%s R=%s: f=%s F~=%s  f/(my Fformula)=%s  f/(handoff Fformula)=%s  signN1=%s signF=%s' % (
            vv0,RR0, mp.nstr(fv,6), mp.nstr(F,6), mp.nstr(myrel,4), mp.nstr(handrel,4), '+' if N1>0 else '-', '+' if F>0 else '-'))
