# -*- coding: utf-8 -*-
"""trace_hp.py: high-precision continuation of the fp-branch (mpmath 40 dps).
Outputs (a, b, G, u, G(u), Phi, h, hp) along the branch for several R.
"""
import mpmath as mp
mp.mp.dps = 40

def sec_mp(sv, aa, bb, RR):
    mm = mp.sqrt(RR)
    return (mp.cos(sv*(1-bb))*mp.cos(sv*mm*(bb-aa))*mp.sin(sv*aa)
            - mm*mp.sin(sv*(1-bb))*mp.sin(sv*mm*(bb-aa))*mp.sin(sv*aa)
            + (mp.cos(sv*(1-bb))*mp.sin(sv*mm*(bb-aa))/mm)*mp.cos(sv*aa)
            + mp.sin(sv*(1-bb))*mp.cos(sv*mm*(bb-aa))*mp.cos(sv*aa))

def roots2_mp(aa, bb, RR, caps=(2*mp.pi+0.7,)):
    for cap in caps:
        ns = 8000
        xs = [mp.mpf(k)*cap/ns for k in range(ns+1)]
        vals = [sec_mp(x, aa, bb, RR) for x in xs]
        out = []
        for i in range(ns):
            if vals[i]*vals[i+1] < 0:
                lo, hi = xs[i], xs[i+1]; flo = vals[i]
                for _ in range(90):
                    md = (lo+hi)/2
                    if sec_mp(md, aa, bb, RR)*flo > 0: lo = md
                    else: hi = md
                out.append((lo+hi)/2)
                if len(out) == 2:
                    return out
    raise RuntimeError("roots2 fail")

def n_mp(sv, aa, bb, RR):
    mm = mp.sqrt(RR); LL = bb-aa; be = 1-bb
    al = sv*aa; th = sv*mm*LL
    I1 = aa/2 - mp.sin(2*al)/(4*sv)
    Icc = LL/2 + mp.sin(2*th)/(4*sv*mm)
    Iss = LL/2 - mp.sin(2*th)/(4*sv*mm)
    Ics = mp.sin(th)**2/(2*sv*mm)
    sa, ca = mp.sin(al), mp.cos(al)
    I2 = sa*sa*Icc + (ca/mm)**2*Iss + 2*sa*(ca/mm)*Ics
    yb = sa*mp.cos(th) + (ca/mm)*mp.sin(th)
    ypb = -mm*mp.sin(th)*mp.sin(al) + mp.cos(th)*mp.cos(al)
    Icc3 = be/2 + mp.sin(2*sv*be)/(4*sv)
    Iss3 = be/2 - mp.sin(2*sv*be)/(4*sv)
    Ics3 = mp.sin(sv*be)**2/(2*sv)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/sv**2
    return (I1 + RR*I2)/sv**2 + I3

def yat_mp(sv, aa, bb, RR, x):
    mm = mp.sqrt(RR)
    if x <= aa:
        return mp.sin(sv*x)/sv
    if x <= bb:
        u = x - aa
        return (mp.sin(sv*aa)*mp.cos(sv*mm*u) + (mp.cos(sv*aa)/mm)*mp.sin(sv*mm*u))/sv
    v = x - bb
    th = sv*mm*(bb-aa)
    yb = (mp.sin(sv*aa)*mp.cos(th) + (mp.cos(sv*aa)/mm)*mp.sin(th))/sv
    ypb = -mm*mp.sin(th)*mp.sin(sv*aa) + mp.cos(th)*mp.cos(sv*aa)
    return mp.cos(sv*v)*yb + mp.sin(sv*v)*ypb/sv

def cfg_mp(aa, bb, RR):
    s1, s2 = roots2_mp(aa, bb, RR)
    return s1, s2, n_mp(s1, aa, bb, RR), n_mp(s2, aa, bb, RR)

def R1R2_mp(aa, bb, RR):
    s1, s2, n1, n2 = cfg_mp(aa, bb, RR)
    y1a = mp.sin(s1*aa)/s1; y2a = mp.sin(s2*aa)/s2
    y1b = yat_mp(s1, aa, bb, RR, bb); y2b = yat_mp(s2, aa, bb, RR, bb)
    R1 = s1**2*y1a**2/n1 - s2**2*y2a**2/n2
    R2 = s1**2*y1b**2/n1 - s2**2*y2b**2/n2
    return R1, R2

def partials_mp(aa, bb, RR):
    h = mp.mpf('1e-7')
    s1, s2, n1, n2 = cfg_mp(aa, bb, RR)
    def r1(ss1, ss2, xa, xb):
        nn1 = n_mp(ss1, xa, xb, RR); nn2 = n_mp(ss2, xa, xb, RR)
        return ss1**2*(mp.sin(ss1*xa)/ss1)**2/nn1 - ss2**2*(mp.sin(ss2*xa)/ss2)**2/nn2
    def r2(ss1, ss2, xa, xb):
        nn1 = n_mp(ss1, xa, xb, RR); nn2 = n_mp(ss2, xa, xb, RR)
        return ss1**2*yat_mp(ss1, xa, xb, RR, xb)**2/nn1 - ss2**2*yat_mp(ss2, xa, xb, RR, xb)**2/nn2
    ds1a = -(sec_mp(s1, aa+h, bb, RR)-sec_mp(s1, aa-h, bb, RR))/(2*h) / ((sec_mp(s1+h, aa, bb, RR)-sec_mp(s1-h, aa, bb, RR))/(2*h))
    ds1b = -(sec_mp(s1, aa, bb+h, RR)-sec_mp(s1, aa, bb-h, RR))/(2*h) / ((sec_mp(s1+h, aa, bb, RR)-sec_mp(s1-h, aa, bb, RR))/(2*h))
    ds2a = -(sec_mp(s2, aa+h, bb, RR)-sec_mp(s2, aa-h, bb, RR))/(2*h) / ((sec_mp(s2+h, aa, bb, RR)-sec_mp(s2-h, aa, bb, RR))/(2*h))
    ds2b = -(sec_mp(s2, aa, bb+h, RR)-sec_mp(s2, aa, bb-h, RR))/(2*h) / ((sec_mp(s2+h, aa, bb, RR)-sec_mp(s2-h, aa, bb, RR))/(2*h))
    dr1a = (r1(s1,s2,aa+h,bb)-r1(s1,s2,aa-h,bb))/(2*h) + (r1(s1+h,s2,aa,bb)-r1(s1-h,s2,aa,bb))/(2*h)*ds1a + (r1(s1,s2+h,aa,bb)-r1(s1,s2-h,aa,bb))/(2*h)*ds2a
    dr1b = (r1(s1,s2,aa,bb+h)-r1(s1,s2,aa,bb-h))/(2*h) + (r1(s1+h,s2,aa,bb)-r1(s1-h,s2,aa,bb))/(2*h)*ds1b + (r1(s1,s2+h,aa,bb)-r1(s1,s2-h,aa,bb))/(2*h)*ds2b
    return dr1a, dr1b

def find_fp(RR):
    lo, hi = mp.mpf('0.40'), mp.mpf('0.5')
    for _ in range(70):
        md = (lo+hi)/2
        R1, R2 = R1R2_mp(md, 1-md, RR)
        if R1 < 0: lo = md
        else: hi = md
    return (lo+hi)/2

def branch_step(a_new, b_prev, RR):
    # Newton on R1(a_new, b) = 0 from b_prev
    b = b_prev
    for _ in range(25):
        R1, R2 = R1R2_mp(a_new, b, RR)
        dr1a, dr1b = partials_mp(a_new, b, RR)
        if abs(dr1b) < mp.mpf('1e-30'):
            return None
        db = -R1/dr1b
        b2 = b + db
        if b2 <= 0 or b2 >= 1:
            return None
        b = b2
        if abs(db) < mp.mpf('1e-28'):
            break
    return b

def trace(RR, a_lo, a_hi, nstep=240):
    fp = find_fp(RR)
    pts = []
    # right side
    a, b = fp, 1-fp
    for k in range(nstep+1):
        a_new = fp + (a_hi - fp)*mp.mpf(k)/nstep
        if k == 0:
            b_new = b
        else:
            b_new = branch_step(a_new, b, RR)
            if b_new is None: break
        pts.append((a_new, b_new))
        a, b = a_new, b_new
    left = []
    a, b = fp, 1-fp
    for k in range(1, nstep+1):
        a_new = fp - (fp - a_lo)*mp.mpf(k)/nstep
        b_new = branch_step(a_new, b, RR)
        if b_new is None: break
        left.append((a_new, b_new))
        a, b = a_new, b_new
    return fp, left[::-1] + pts

def analyze(RR, nstep=200):
    A0 = mp.acos(mp.mpf('0.25'))/mp.pi
    B0 = 1 - A0
    fp = find_fp(RR)
    # domain: left end is a0 (for R >= ~888 the arm reaches a0; for smaller R it also does per e15)
    a_lo = A0
    a_hi = B0
    fpv, pts = trace(RR, a_lo, a_hi, nstep=nstep)
    rows = []
    for (aa, bb) in pts:
        R1, R2 = R1R2_mp(aa, bb, RR)
        dr1a, dr1b = partials_mp(aa, bb, RR)
        G = -dr1a/dr1b
        # u = g1^{-1}(1-a): solve g1(u) = 1-a by bisection on stored pts
        y = 1 - aa
        us = [p[0] for p in pts]; bs = [p[1] for p in pts]
        if y < min(bs) or y > max(bs):
            rows.append((aa, bb, G, None, None, None, None, None))
            continue
        lo, hi = us[0], us[-1]
        for _ in range(60):
            md = (lo+hi)/2
            # interpolate b at md
            bmd = None
            for i in range(len(us)-1):
                if us[i] <= md <= us[i+1]:
                    t = (md - us[i])/(us[i+1]-us[i])
                    bmd = bs[i] + t*(bs[i+1]-bs[i])
                    break
            if bmd is None: break
            if bmd < y: lo = md
            else: hi = md
        u = (lo+hi)/2
        # refine u by Newton using branch_step-like: solve g1(u) = 1-a
        for _ in range(12):
            bu = branch_step(u, None if False else _interp(us, bs, u), RR) if False else None
        # fallback: use interpolation directly
        bu = _interp(us, bs, u)
        R1u, R2u = R1R2_mp(u, bu, RR)
        du1a, du1b = partials_mp(u, bu, RR)
        Gu = -du1a/du1b
        Phi = G*Gu
        h = bb - 1 + u
        hp = G - 1/Gu
        rows.append((aa, bb, G, u, Gu, Phi, h, hp))
    return fpv, rows

def _interp(xs, ys, x):
    for i in range(len(xs)-1):
        if xs[i] <= x <= xs[i+1]:
            t = (x - xs[i])/(xs[i+1]-xs[i])
            return ys[i] + t*(ys[i+1]-ys[i])
    return None

if __name__ == "__main__":
    for Rs in ["1.02","1.2","2","4","10","100","1000","1e4","1e6"]:
        RR = mp.mpf(Rs)
        fp, rows = analyze(RR, nstep=160)
        valid = [r for r in rows if r[6] is not None]
        if not valid:
            print(Rs, "no valid rows"); continue
        gmin = min(r[2] for r in valid); gmax = max(r[2] for r in valid)
        # sign pattern of Phi-1
        sgn = [mp.sign(r[5]-1) for r in valid]
        chg = sum(1 for i in range(len(sgn)-1) if sgn[i]*sgn[i+1] < 0)
        h0 = valid[0][6]; h1 = valid[-1][6]
        print("R=%s fp=%s a=[%s,%s] g1p in [%s,%s] Phi-1 chg=%d hL=%s hR=%s" % (
            Rs, mp.nstr(fp,8), mp.nstr(valid[0][0],6), mp.nstr(valid[-1][0],6),
            mp.nstr(gmin,7), mp.nstr(gmax,7), chg, mp.nstr(h0,7), mp.nstr(h1,7)))
