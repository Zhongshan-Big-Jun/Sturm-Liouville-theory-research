# -*- coding: utf-8 -*-
"""09_deep_sliver_cert.py  (REWRITE v2, replaces the broken original)
Certified verification of the deep-sliver lemma on the bounded region
    R in [1500, RTAIL], 0 < u <= 2/sqrt(R):  G(R,u) = mu2-mu1 >= 25,
plus the analytic tail claim stated for the proof (R >= RTAIL handled there).

Proven facts used:
  P1. mu_k strictly increasing in R, strictly decreasing in u (Feynman-Hellmann).
  P2. H = mu2*y2(u)^2 - mu1*y1(u)^2 > 0 (certified on cells) => dG/du < 0.
Scheme: (A) certified corner values; (B) curve w=2 corner scheme;
        (C) H > 0 on cells via interval enclosure over the box.
ASCII punctuation. Run: python 09_deep_sliver_cert.py
"""
import mpmath as mp
from mpmath import iv
iv.dps = 40
mp.mp.dps = 60

RMIN = mp.mpf('1500')
RTAIL = mp.mpf('1e4')
TARGET = mp.mpf('25')

# ---------------- float seeds ----------------
def sec_f(mu, R, u):
    kR = mp.sqrt(mu); k1 = mp.sqrt(mu/R)
    cR, sR = mp.cos(kR*u), mp.sin(kR*u)
    c1, s1 = mp.cos(k1*(1-2*u)), mp.sin(k1*(1-2*u))
    a,b = cR, sR/kR; c,d = -kR*sR, cR
    e,f = c1, s1/k1; g,h = -k1*s1, c1
    a2 = a*e + b*g; b2 = a*f + b*h
    return a2*b + b2*d

def seed_mu(R, u, k):
    """Asymptotic seed: mu ~ R*nu0 + delta_k*sqrt(R), valid for w=u*sqrt(R) in (1/2,2];
    for w <= 1/2 use pi^2 R and 4 pi^2 R."""

    w = u*mp.sqrt(R)
    nu0 = mp.pi**2/(4*w*w)
    if w > mp.mpf('0.5'):
        if k == 1:
            d = -(mp.pi/w**2)*mp.tan(mp.pi/(4*w))
        else:
            d = (mp.pi/w**2)*mp.cot(mp.pi/(4*w))
        return R*nu0 + d*mp.sqrt(R)
    else:
        if k == 1:
            return mp.pi**2*R
        else:
            return max(mp.pi**2/(4*w*w), 4*mp.pi**2)*R*mp.mpf('0.9999')

def root_float(R, u, k):
    s = seed_mu(R, u, k)
    try:
        r = mp.findroot(lambda m: sec_f(m, R, u), s, tol=mp.mpf('1e-25'), maxsteps=60)
        return r
    except Exception:
        return None

# ---------------- interval certification ----------------
def y1_iv(mu_iv, R, u):
    kh = iv.sqrt(mu_iv); kl = iv.sqrt(mu_iv/R)
    c1 = iv.cos(kh*u); s1 = iv.sin(kh*u)
    c2 = iv.cos(kl*(1-2*u)); s2 = iv.sin(kl*(1-2*u))
    a00 = c1*c2 - s1*s2*kl/kh
    a01 = c1*s2/kl + s1*c2/kh
    return a00*(s1/kh) + a01*c1

def certified_mu(R, u, k, seed):
    rel = mp.mpf('1e-7')
    a, b = seed*(1-rel), seed*(1+rel)
    fa = y1_iv(iv.mpf([a, a]), R, u)
    fb = y1_iv(iv.mpf([b, b]), R, u)
    if not (fa.b < 0 and fb.a > 0) and not (fa.a > 0 and fb.b < 0):
        for rel2 in [mp.mpf('1e-5'), mp.mpf('1e-3'), mp.mpf('1e-2'), mp.mpf('1e-1')]:
            a, b = seed*(1-rel2), seed*(1+rel2)
            fa = y1_iv(iv.mpf([a, a]), R, u)
            fb = y1_iv(iv.mpf([b, b]), R, u)
            if (fa.b < 0 and fb.a > 0) or (fa.a > 0 and fb.b < 0):
                break
        else:
            raise RuntimeError("cannot bracket at R=%s u=%s seed=%s" % (R, u, seed))
    for _ in range(70):
        mid = (a+b)/2
        fm = y1_iv(iv.mpf([mid, mid]), R, u)
        if fm.b < 0 and fa.b < 0:
            a = mid; fa = fm
        elif fm.a > 0 and fb.a > 0:
            b = mid; fb = fm
        else:
            return iv.mpf([a, b])
    return iv.mpf([a, b])

def certified_point(R, u):
    e1 = certified_mu(R, u, 1, root_float(R, u, 1))
    e2 = certified_mu(R, u, 2, root_float(R, u, 2))
    return e1, e2

# ---------------- grids ----------------
def build_grids():
    ratio = mp.mpf('1.01')
    Rs = [RMIN]
    while Rs[-1] < RTAIL:
        Rs.append(min(Rs[-1]*ratio, RTAIL))
    nufrac = 24  # u-fractions 1..nufrac (k/nufrac of 2/sqrt(R))
    return Rs, nufrac

def run():
    Rs, nufrac = build_grids()
    print("R-grid: %d nodes in [1500, %.4g]" % (len(Rs), RTAIL))
    # (A) certified corner values on the curve w=2: (R_i, u_i), u_i = 2/sqrt(R_i)
    corners = {}
    for R in Rs:
        u = 2/mp.sqrt(R)
        corners[R] = certified_point(R, u)
    # (B) curve corner scheme
    min_margin = mp.inf
    for i in range(len(Rs)-1):
        R1, R2 = Rs[i], Rs[i+1]
        u1, u2 = 2/mp.sqrt(R1), 2/mp.sqrt(R2)
        lo = corners[R1][1].a - corners[R2][0].b
        min_margin = min(min_margin, lo - TARGET)
        if lo <= TARGET:
            print("FAIL curve cell", R1, R2, lo); return False
    print("curve w=2 on [1500, %.4g]: min(G_lo - 25) = %s" % (RTAIL, mp.nstr(min_margin, 8)))
    assert min_margin > 0
    # (C) H > 0 on cells [R_i,R_{i+1}] x [u_f, u_{f+1}], u_f = (2/sqrt(R_i))*(f/nufrac)
    hmin = mp.inf; hworst = None
    for i in range(len(Rs)-1):
        R1, R2 = Rs[i], Rs[i+1]
        umax = 2/mp.sqrt(R1)
        for f in range(1, nufrac+1):
            ub = umax*(mp.mpf(f)/nufrac)
            ua = umax*(mp.mpf(f-1)/nufrac)
            if ua == 0:
                ua = mp.mpf('1e-9')*ub  # exclude exact 0; limit handled in proof
            # mu enclosure over cell from P1 monotonicity
            p12 = certified_point(R1, ub)   # mu(R1, ub): lower corner for mu_k
            p21 = certified_point(R2, ua)   # mu(R2, ua): upper corner
            mu1 = iv.mpf([p12[0].a, p21[0].b])
            mu2 = iv.mpf([p12[1].a, p21[1].b])
            H = H_iv_box(R1, R2, ua, ub, mu1, mu2)
            if H.a < hmin:
                hmin = H.a; hworst = (R1, R2, ua, ub)
            if not H.a > 0:
                print("H FAIL cell R1=%s R2=%s u=[%s,%s] H.a=%s" % (R1, R2, ua, ub, H.a))
                return False
    print("H>0 on %d cells: min H.a = %s at %s" %
          ((len(Rs)-1)*nufrac, mp.nstr(hmin, 6), hworst))
    # (D) corner value G(1500, 2/sqrt(1500)) directly
    p = corners[Rs[0]]
    Gc = p[1].a - p[0].b
    print("G(1500, 2/sqrt(1500)) >= %s (need >= 25)" % mp.nstr(Gc, 12))
    assert Gc > TARGET
    print("PASS: deep-sliver region [1500, %.4g] x (0, 2/sqrt(R)] certified G >= 25" % RTAIL)
    return True

def H_iv_box(R1, R2, u1, u2, mu1, mu2):
    R = iv.mpf([R1, R2]); u = iv.mpf([u1, u2])
    kh1 = iv.sqrt(mu1); kl1 = iv.sqrt(mu1/R)
    kh2 = iv.sqrt(mu2); kl2 = iv.sqrt(mu2/R)
    th1 = kh1*u; z1 = kl1*(iv.mpf('0.5') - u)
    th2 = kh2*u; z2 = kl2*(iv.mpf('0.5') - u)
    I1 = u*iv.mpf('0.5') - iv.sin(2*th1)/(4*kh1)
    I2 = u*iv.mpf('0.5') - iv.sin(2*th2)/(4*kh2)
    J1 = (iv.mpf('0.5') - u)*iv.mpf('0.5') + iv.sin(2*z1)/(4*kl1)
    J2 = (iv.mpf('0.5') - u)*iv.mpf('0.5') - iv.sin(2*z2)/(4*kl2)
    r1 = iv.sin(th1)/iv.cos(z1)
    r2 = iv.sin(th2)/iv.sin(z2)
    D1 = R*I1 + r1**2*J1
    D2 = R*I2 + r2**2*J2
    y1sq = iv.sin(th1)**2/(2*D1)
    y2sq = iv.sin(th2)**2/(2*D2)
    return mu2*y2sq - mu1*y1sq

if __name__ == '__main__':
    run()