# -*- coding: utf-8 -*-
"""Test single-box interval evaluation of J on B1 and B2 with mpmath.iv."""
import mpmath as mp
iv = mp.iv
iv.dps = 50

def Phi_iv(x, q): return iv.cos(x)**2 + q*q*iv.sin(x)**2

def G_iv(x, c, q):
    Ph = Phi_iv(x, q)
    D = q + c*Ph
    W = 3 + 2*x/iv.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*iv.sin(x)*iv.cos(x)/(D*D)

def Gc_iv(x, c, q):
    Ph = Phi_iv(x, q)
    D = q + c*Ph
    W = 3 + 2*x/iv.tan(x)
    sc = iv.sin(x)*iv.cos(x)
    dg1c = Ph*W*Ph/(D*D)
    dg2c = 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return dg1c + dg2c

def Gx_iv(x, c, q):
    # use interval derivative formula for d/dx tan? easier: finite diff on iv is wrong.
    # Instead compute Gx via explicit formula: use derivative of W etc.
    Ph = Phi_iv(x, q)
    D = q + c*Ph
    W = 3 + 2*x/iv.tan(x)
    sx = iv.sin(x); cx = iv.cos(x)
    sc = sx*cx
    dPh = 2*sc*(q*q-1)
    dW = 2/iv.tan(x) - 2*x/(sx**2)
    dD = c*dPh
    dsc = cx**2 - sx**2
    term1 = -Ph*W/D
    term2 = 2*c*x*Ph*(q*q-1)*sc/(D*D)
    dt1 = -(dPh*W + Ph*dW)/D + Ph*W*dD/(D**2)
    A = 2*c*(q*q-1)
    num2 = A*(x*dPh*sc + Ph*dsc + Ph*sc)
    dt2 = num2/(D**2) - 2*c*x*Ph*(q*q-1)*sc*2*dD/(D**3)
    return dt1 + dt2

def J_iv(x, c, q):
    Ph = Phi_iv(x, c, q) if False else Phi_iv(x, q)
    D = q + c*Ph
    xp = -x*Ph/D
    Gv = G_iv(x, c, q)
    Gpv = Gx_iv(x, c, q)*xp + Gc_iv(x, c, q)
    return Gv*Gv + Gpv

boxes = {
  "B1": (iv.mpf([mp.mpf('0.8411'), mp.mpf('1.1220')]), iv.mpf([mp.mpf(1), mp.mpf(2)]), iv.mpf([mp.mpf('0.4'), mp.mpf('0.5')])),
  "B2": (iv.mpf([mp.mpf('2.0944'), mp.mpf('2.4859')]), iv.mpf([mp.mpf(1), mp.mpf(2)]), iv.mpf([mp.mpf('0.4'), mp.mpf('0.5')])),
}
for name,(x,c,q) in boxes.items():
    r = J_iv(x,c,q)
    print("%s J box: [%.6f, %.6f]" % (name, r.a, r.b))
    g = G_iv(x,c,q)
    print("%s G box: [%.6f, %.6f]" % (name, g.a, g.b))
