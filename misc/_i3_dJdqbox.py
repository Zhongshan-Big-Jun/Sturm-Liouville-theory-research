# -*- coding: utf-8 -*-
"""dJ/dq along curve, box-relaxed: -sc*Jx/D + Jq on B1 and B2."""
import mpmath as mp
mp.mp.dps = 40

def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def J(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    W = 3 + 2*x/mp.tan(x)
    Gv = G(x, c, q)
    h = mp.mpf('1e-6')
    Gpv = ((G(x+h,c,q)-G(x-h,c,q))/(2*h))*xp
    sc = mp.sin(x)*mp.cos(x)
    Gc_ = Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_
def Jx(x,c,q):
    h=mp.mpf('1e-6'); return (J(x+h,c,q)-J(x-h,c,q))/(2*h)
def Jq(x,c,q):
    h=mp.mpf('1e-6'); return (J(x,c,q+h)-J(x,c,q-h))/(2*h)
def dJdq_box(x,c,q):
    Ph = Phi(x,q); D = q + c*Ph
    sc = mp.sin(x)*mp.cos(x)
    return -sc*Jx(x,c,q)/D + Jq(x,c,q)

def scan3(x0,x1,nx,q0,q1,nq,c0,c1,nc):
    mn=mp.inf; mx=-mp.inf; argmn=None; argmx=None
    for i in range(nx+1):
        x=x0+(x1-x0)*i/nx
        for j in range(nq+1):
            q=q0+(q1-q0)*j/nq
            for k in range(nc+1):
                c=c0+(c1-c0)*k/nc
                v=dJdq_box(x,c,q)
                if v<mn: mn=v; argmn=(x,c,q)
                if v>mx: mx=v; argmx=(x,c,q)
    return mn,mx,argmn,argmx

mn,mx,argmn,argmx = scan3(mp.mpf('0.8411'),mp.mpf('1.1220'),12,mp.mpf(1),mp.mpf(2),12,mp.mpf('0.4'),mp.mpf('0.5'),12)
print("B1 dJdq_box: [%.4f, %.4f], min at %s, max at %s" % (mn,mx,argmn,argmx))
mn,mx,argmn,argmx = scan3(mp.mpf('2.0944'),mp.mpf('2.4859'),12,mp.mpf(1),mp.mpf(2),12,mp.mpf('0.4'),mp.mpf('0.5'),12)
print("B2 dJdq_box: [%.4f, %.4f], min at %s, max at %s" % (mn,mx,argmn,argmx))
