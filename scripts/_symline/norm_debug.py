# -*- coding: utf-8 -*-
# Debug norm closed forms: compute Y'(s) = d/ds y(1;s) via transfer matrix + finite diff
import mpmath as mp
mp.mp.dps = 50
pi = mp.pi

def slope_norm_solution_y1(s, v, R):
    # value y(1;s) for slope-normalized solution, via transfer matrix
    m = mp.sqrt(R)
    # [0,v]: y=sin(msx)/(ms), y'=cos(msx)
    A = m*s*v
    yv = mp.sin(A)/(m*s); ypv = mp.cos(A)
    # middle [v,1-v], width 1-2v
    psi = s*(1-2*v)
    y1v = yv*mp.cos(psi) + ypv*mp.sin(psi)/s
    yp1v = -yv*s*mp.sin(psi) + ypv*mp.cos(psi)
    # right block [1-v,1]: solution from (y(1-v), y'(1-v)) with coefficient m^2 rho... equation -y''=s^2 m^2 y
    # y(x) = y1v*cos(m s (x-(1-v))) + yp1v*sin(m s (x-(1-v)))/(m s)
    # at x=1: dx = v
    dx = v
    y1 = y1v*mp.cos(m*s*dx) + yp1v*mp.sin(m*s*dx)/(m*s)
    yp1 = -y1v*m*s*mp.sin(m*s*dx) + yp1v*mp.cos(m*s*dx)
    return y1, yp1

def Yp_num(s, v, R):
    # d/ds y(1;s) by central difference
    h = mp.mpf('1e-25')
    yp, _ = slope_norm_solution_y1(s+h, v, R)
    ym, _ = slope_norm_solution_y1(s-h, v, R)
    return (yp-ym)/(2*h)

def alpha1(c,q):
    return mp.findroot(lambda A: mp.atan(1/(q*mp.tan(A))) - c*A, (mp.mpf('1e-30'), pi/2-mp.mpf('1e-30')))
def alpha2(c,q):
    def O(x):
        if x < pi/2: return pi - mp.atan(q*mp.tan(x))
        elif x == pi/2: return pi/2
        else: return mp.atan(-q*mp.tan(x))
    return mp.findroot(lambda A: O(A) - c*A, (mp.mpf('1e-30'), pi-mp.mpf('1e-30')))

def Pfun(x, y, m):
    t = mp.tan(x)
    return (x*m*(1+t**2) + y*(m**2+t**2))/(2*(x+m*y)**2*(1+t**2))

for v in ['0.1','0.3','0.45']:
    vv = mp.mpf(v)
    for R in ['1.5','4.0']:
        RR = mp.mpf(R); m = mp.sqrt(RR)
        c = (1-2*vv)/(2*m*vv); q = 1/m
        a1 = alpha1(c,q); a2 = alpha2(c,q)
        s1 = 2*(c+q)*a1; s2 = 2*(c+q)*a2
        tau = s2/s1
        A = m*s1*vv; th = s1*(mp.mpf(1)/2-vv)
        Yp1 = Yp_num(s1,vv,RR); Yp2 = Yp_num(s2,vv,RR)
        yp1_1, _ = slope_norm_solution_y1(s1,vv,RR); _, yp1end = slope_norm_solution_y1(s1,vv,RR)
        _, yp2end = slope_norm_solution_y1(s2,vv,RR)
        print('v=%s R=%s: Yp1_num=%s vs -P(A,th)=%s' % (v,R, mp.nstr(Yp1,12), mp.nstr(-Pfun(A,th,m),12)))
        print('        Yp2_num=%s vs +P(tauA,tau th)=%s' % (mp.nstr(Yp2,12), mp.nstr(Pfun(tau*A,tau*th,m),12)))
        print('        y1p(1)=%s  y2p(1)=%s' % (mp.nstr(yp1end,10), mp.nstr(yp2end,10)))
