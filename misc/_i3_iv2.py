# -*- coding: utf-8 -*-
"""Single-box interval bounds for G, Gc, Gx on B1 and B2 (mpmath.iv)."""
import mpmath as mp
iv = mp.iv
iv.dps = 50

def Phi_iv(x, q): return iv.cos(x)**2 + q*q*iv.sin(x)**2

def parts(x, c, q):
    Ph = Phi_iv(x, q)
    D = q + c*Ph
    W = 3 + 2*x/iv.tan(x)
    sx = iv.sin(x); cx = iv.cos(x)
    sc = sx*cx
    G1 = -Ph*W/D
    G2 = 2*c*x*Ph*(q*q-1)*sc/(D*D)
    G = G1 + G2
    # Gc
    dg1c = Ph*W*Ph/(D*D)
    dg2c = 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    Gc = dg1c + dg2c
    # Gx
    dPh = 2*sc*(q*q-1)
    dW = 2/iv.tan(x) - 2*x/(sx**2)
    dD = c*dPh
    dsc = cx**2 - sx**2
    dt1 = -(dPh*W + Ph*dW)/D + Ph*W*dD/(D**2)
    A = 2*c*(q*q-1)
    num2 = A*(x*dPh*sc + Ph*dsc + Ph*sc)
    dt2 = num2/(D**2) - 2*c*x*Ph*(q*q-1)*sc*2*dD/(D**3)
    Gx = dt1 + dt2
    return G, Gc, Gx, Ph, D

boxes = {
  "B1": (iv.mpf([mp.mpf('0.8411'), mp.mpf('1.1220')]), iv.mpf([mp.mpf(1), mp.mpf(2)]), iv.mpf([mp.mpf('0.4'), mp.mpf('0.5')])),
  "B2": (iv.mpf([mp.mpf('2.0944'), mp.mpf('2.4859')]), iv.mpf([mp.mpf(1), mp.mpf(2)]), iv.mpf([mp.mpf('0.4'), mp.mpf('0.5')])),
}
for name,(x,c,q) in boxes.items():
    G,Gc,Gx,Ph,D = parts(x,c,q)
    print("%s: G=[%.4f,%.4f] Gc=[%.4f,%.4f] Gx=[%.4f,%.4f] Ph=[%.4f,%.4f] D=[%.4f,%.4f]" % (
        name, G.a,G.b, Gc.a,Gc.b, Gx.a,Gx.b, Ph.a,Ph.b, D.a,D.b))
    # x' = -x*Ph/D
    xp = -x*Ph/D
    print("   xp=[%.4f,%.4f]" % (xp.a,xp.b))
