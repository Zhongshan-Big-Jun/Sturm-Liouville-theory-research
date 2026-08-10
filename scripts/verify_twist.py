# -*- coding: utf-8 -*-
"""High-precision check of the twist identity dx+/db = -dx-/da, dx+/da = dx-/db (evidence)."""
import mpmath as mp
mp.mp.dps = 40

def sec(s, a, b, R):
    m = mp.sqrt(R); alpha = s*a; beta = s*(1-b); theta = s*m*(b-a)
    ca, sa = mp.cos(alpha), mp.sin(alpha)
    cb, sb = mp.cos(beta), mp.sin(beta)
    ct, st = mp.cos(theta), mp.sin(theta)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca

def roots2(a, b, R):
    out = []
    # scan coarsely with mpmath over [0, 4*pi]
    N = 4000
    lo = mp.mpf(0); hi = 4*mp.pi
    s_prev = lo; v_prev = sec(lo, a, b, R)
    for j in range(1, N+1):
        s = lo + (hi-lo)*mp.mpf(j)/N
        v = sec(s, a, b, R)
        if v*v_prev < 0:
            # bisection
            lo2, hi2 = s_prev, s
            f_lo = v_prev
            for _ in range(120):
                mid = (lo2+hi2)/2
                if sec(mid, a, b, R)*f_lo < 0: hi2 = mid
                else: lo2 = mid
            out.append((lo2+hi2)/2)
            if len(out) == 2: break
        s_prev, v_prev = s, v
    if len(out) < 2:
        raise RuntimeError("roots2 failed")
    return out

def yv(s, a, b, R, x):
    m = mp.sqrt(R); alpha = s*a
    if x <= a:
        return mp.sin(s*x)/s
    elif x <= b:
        u = x - a
        return (mp.sin(alpha)*mp.cos(s*m*u) + (mp.cos(alpha)/m)*mp.sin(s*m*u))/s
    else:
        v = x - b; theta = s*m*(b-a)
        yb = (mp.sin(alpha)*mp.cos(theta) + (mp.cos(alpha)/m)*mp.sin(theta))/s
        ypb = -m*mp.sin(theta)*mp.sin(alpha) + mp.cos(theta)*mp.cos(alpha)
        return mp.cos(s*v)*yb + mp.sin(s*v)*ypb/s

def norm_n(s, a, b, R):
    m = mp.sqrt(R); L = b-a; beta = 1-b
    alpha = s*a; theta = s*m*L
    I1 = a/2 - mp.sin(2*alpha)/(4*s)
    Icc = L/2 + mp.sin(2*theta)/(4*s*m)
    Iss = L/2 - mp.sin(2*theta)/(4*s*m)
    Ics = mp.sin(theta)**2/(2*s*m)
    sa = mp.sin(alpha); ca = mp.cos(alpha)
    I2 = sa*sa*Icc + (ca/m)**2*Iss + 2*sa*(ca/m)*Ics
    yb_scaled = sa*mp.cos(theta) + (ca/m)*mp.sin(theta)
    ypb = -m*mp.sin(theta)*mp.sin(alpha) + mp.cos(theta)*mp.cos(alpha)
    Icc3 = beta/2 + mp.sin(2*s*beta)/(4*s)
    Iss3 = beta/2 - mp.sin(2*s*beta)/(4*s)
    Ics3 = mp.sin(s*beta)**2/(2*s)
    I3 = (yb_scaled**2*Icc3 + ypb**2*Iss3 + 2*yb_scaled*ypb*Ics3)/s**2
    return (I1 + R*I2)/s**2 + I3

def band(a, b, R, npts=20000):
    s1, s2 = roots2(a, b, R)
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    q = (s1/s2)*mp.sqrt(n2/n1)
    # find v-level crossings by sampling on a fine grid then bisection
    xs = [a*mp.mpf(j)/npts for j in range(1, npts)]
    # v(x) = y2/y1 strictly decreasing
    def v_of(x):
        y1 = yv(s1, a, b, R, x); y2 = yv(s2, a, b, R, x)
        return y2/y1
    v0 = v_of(mp.mpf('1e-12'))
    # locate v=q (x_minus) and v=-q (x_plus) via bisection on monotone v
    # x_minus: v decreases from ~1 to q
    lo, hi = mp.mpf('1e-12'), a*mp.mpf('0.99999')
    # make sure v(lo) > q > v(hi); walk hi until v < q
    for _ in range(200):
        if v_of(hi) < q: break
        hi = (lo+hi)/2 if False else hi*mp.mpf('0.999')
    # bisection for v = q
    for _ in range(200):
        mid = (lo+hi)/2
        if v_of(mid) > q: lo = mid
        else: hi = mid
    xm = (lo+hi)/2
    # x_plus: v = -q
    lo, hi = mp.mpf('1e-12'), mp.mpf('1')-mp.mpf('1e-12')
    # walk lo until v < -q... v decreasing, need v(lo) > -q, v(hi) < -q
    for _ in range(300):
        if v_of(lo) > -q: break
        lo = lo*mp.mpf('1.0001')
    for _ in range(200):
        mid = (lo+hi)/2
        if v_of(mid) > -q: lo = mid
        else: hi = mid
    xp = (lo+hi)/2
    return xm, xp

def partials(a, b, R):
    h = mp.mpf('1e-6')
    xm00, xp00 = band(a, b, R)
    xm_a, xp_a = band(a+h, b, R)
    xm_b, xp_b = band(a, b+h, R)
    dxm_da = (xm_a - xm00)/h
    dxm_db = (xm_b - xm00)/h
    dxp_da = (xp_a - xp00)/h
    dxp_db = (xp_b - xp00)/h
    return dxm_da, dxm_db, dxp_da, dxp_db

for (a,b,R) in [(mp.mpf('0.45'), mp.mpf('0.55'), mp.mpf('4')), (mp.mpf('0.48'), mp.mpf('0.58'), mp.mpf('4')), (mp.mpf('0.42'), mp.mpf('0.60'), mp.mpf('10')), (mp.mpf('0.49'), mp.mpf('0.52'), mp.mpf('100'))]:
    dxm_da, dxm_db, dxp_da, dxp_db = partials(a, b, R)
    e1 = dxp_db + dxm_da   # should be 0 if dxp/db = -dxm/da
    e2 = dxp_da - dxm_db   # should be 0 if dxp/da = dxm/db
    print(f"(a,b,R)=({mp.nstr(a,4)},{mp.nstr(b,4)},{mp.nstr(R,4)}):")
    print(f"  dx-/da={mp.nstr(dxm_da,8)} dx-/db={mp.nstr(dxm_db,8)} dx+/da={mp.nstr(dxp_da,8)} dx+/db={mp.nstr(dxp_db,8)}")
    print(f"  E1=dx+/db+dx-/da={mp.nstr(e1,8)}   E2=dx+/da-dx-/db={mp.nstr(e2,8)}")