# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 50

def shoot_half(w, endBC, s, t, R):
    a, b, c2 = s*t, t, s*t/2
    u, up = mp.mpf(0), mp.mpf(1)
    for L, cc in ((a,1.0),(b,R),(c2,1.0)):
        ww = w*mp.sqrt(cc); L = mp.mpf(L); wwL = ww*L
        u, up = u*mp.cos(wwL) + up*mp.sin(wwL)/ww, -u*ww*mp.sin(wwL) + up*mp.cos(wwL)
    return up if endBC=='mixed' else u

for R in (2.0, 4.0, 10.0, 100.0):
    s = mp.sqrt(R); t = 1/(3*s+2)
    # scan for first Dirichlet root
    ws = [mp.mpf(k)*0.05 for k in range(1, 3000)]
    dv = [shoot_half(w,'dir',s,t,R) for w in ws]
    dr = None
    for i in range(len(ws)-1):
        if (dv[i] > 0) != (dv[i+1] > 0):
            dr = mp.findroot(lambda w: shoot_half(w,'dir',s,t,R), (ws[i]+ws[i+1])/2); break
    mv = [shoot_half(w,'mixed',s,t,R) for w in ws]
    mroots = []
    for i in range(len(ws)-1):
        if (mv[i] > 0) != (mv[i+1] > 0):
            mroots.append(mp.findroot(lambda w: shoot_half(w,'mixed',s,t,R), (ws[i]+ws[i+1])/2))
        if len(mroots) >= 3: break
    nu1, mu2 = dr, mroots[1]
    y2 = s*t*nu1; y3 = s*t*mu2
    print(f"R={R}: y2 = {mp.nstr(y2,14)}  y3 = {mp.nstr(y3,14)}  y2+y3 = {mp.nstr(y2+y3,16)}  pi = {mp.nstr(mp.pi,16)}")
    print(f"     ratio (y3/y2)^2 = {mp.nstr((y3/y2)**2, 14)}")
