# -*- coding: utf-8 -*-
"""cert_ce1.py: rigorous interval-arithmetic certificate for CE-1.
Claims proved (with outward-directed interval arithmetic, mpmath.iv):
  At R = 1500, a* = 0.57364 (inside the common range [a0, b0]):
    (i)  the good branch-1 point b1(a*) and branch-2 point b2(a*) exist
         (enclosed by interval IVT bisection; unique in their brackets);
    (ii) the branch slopes satisfy g1'(a*) - g2'(a*) < 0, i.e. Lemma A
         (g1' > g2' pointwise on the common range) is FALSE.
Same certificate repeated at R = 1e4 (larger margin) for robustness.
Method: forward-mode interval automatic differentiation for the partials,
interval bisection with sign-definite interval evaluations for the roots,
and inclusion-monotonic interval evaluation of the implicit-function
closed forms over verified enclosures.
"""
import sys
import numpy as np
from mpmath import iv, mp, mpf

mp.dps = 60
iv.prec = 220

sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at, R1_R2  # float bracketing only

# ---------------- interval functions (y'(0) = 1 normalization) ----------------
def isec(s, a, b, R):
    m = iv.sqrt(R)
    alpha = s * a; beta = s * (1 - b); theta = s * m * (b - a)
    ca, sa = iv.cos(alpha), iv.sin(alpha)
    cb, sb = iv.cos(beta), iv.sin(beta)
    ct, st = iv.cos(theta), iv.sin(theta)
    return cb * ct * sa - m * sb * st * sa + (cb * st / m) * ca + sb * ct * ca

def inorm(s, a, b, R):
    m = iv.sqrt(R)
    L = b - a; beta = 1 - b
    alpha = s * a; theta = s * m * L
    I1 = a / 2 - iv.sin(2 * alpha) / (4 * s)
    Icc = L / 2 + iv.sin(2 * theta) / (4 * s * m)
    Iss = L / 2 - iv.sin(2 * theta) / (4 * s * m)
    Ics = iv.sin(theta) ** 2 / (2 * s * m)
    sa = iv.sin(alpha); ca = iv.cos(alpha)
    I2 = sa * sa * Icc + (ca / m) ** 2 * Iss + 2 * sa * (ca / m) * Ics
    yb_scaled = sa * iv.cos(theta) + (ca / m) * iv.sin(theta)
    ypb = -m * iv.sin(theta) * iv.sin(alpha) + iv.cos(theta) * iv.cos(alpha)
    Icc3 = beta / 2 + iv.sin(2 * s * beta) / (4 * s)
    Iss3 = beta / 2 - iv.sin(2 * s * beta) / (4 * s)
    Ics3 = iv.sin(s * beta) ** 2 / (2 * s)
    I3 = (yb_scaled ** 2 * Icc3 + ypb ** 2 * Iss3 + 2 * yb_scaled * ypb * Ics3) / s ** 2
    return (I1 + R * I2) / s ** 2 + I3

def iy1a(s, a, b, R):
    return iv.sin(s * a) / s

def iy_b(s, a, b, R):
    m = iv.sqrt(R)
    alpha = s * a; theta = s * m * (b - a)
    sa = iv.sin(alpha); ca = iv.cos(alpha)
    return (sa * iv.cos(theta) + (ca / m) * iv.sin(theta)) / s

def ir1(a, b, R, s1, s2):
    n1 = inorm(s1, a, b, R); n2 = inorm(s2, a, b, R)
    return iv.sin(s1 * a) ** 2 / n1 - iv.sin(s2 * a) ** 2 / n2

def ir2(a, b, R, s1, s2):
    n1 = inorm(s1, a, b, R); n2 = inorm(s2, a, b, R)
    return (s1 * iy_b(s1, a, b, R)) ** 2 / n1 - (s2 * iy_b(s2, a, b, R)) ** 2 / n2

def iv_ratio(a, b, R, s1, s2):
    return (iy1a(s2, a, b, R) / iy1a(s1, a, b, R), iy_b(s2, a, b, R) / iy_b(s1, a, b, R))

# ---------------- helpers ----------------
def sign_definite(x):
    if x.b < 0: return -1
    if x.a > 0: return +1
    return 0

def pt(x):
    return iv.mpf([x, x])

def mpf_from_float(v):
    return mpf(repr(float(v)))

def roots2_robust(a, b, R):
    """robust float secular roots (fine grids); returns (s1, s2)."""
    s = np.concatenate([np.linspace(1e-12, 1.2, 12000), np.linspace(1.2, 3*np.pi, 12000)])
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx[:4]:
        lo, hi = s[i], s[i+1]
        flo = sec(lo, a, b, R)
        for _ in range(70):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    roots = sorted(set(np.round(r, 13) for r in roots))
    if len(roots) < 2:
        raise RuntimeError("roots2_robust failed at (a,b,R)=(%s,%s,%s)" % (a, b, R))
    return roots[0], roots[1]

def sec_root_bracket(s_lo, s_hi, a, b, R):
    lo, hi = mpf_from_float(s_lo), mpf_from_float(s_hi)
    flo, fhi = isec(pt(lo), pt(a), pt(b), pt(R)), isec(pt(hi), pt(a), pt(b), pt(R))
    sflo, sfhi = sign_definite(flo), sign_definite(fhi)
    assert sflo != 0 and sfhi != 0 and sflo * sfhi < 0, (sflo, sfhi)
    for _ in range(80):
        md = (lo + hi) / 2
        fm = isec(pt(md), pt(a), pt(b), pt(R))
        sm = sign_definite(fm)
        if sm == 0:
            hi = md
            continue
        if sm == sflo: lo = md
        else: hi = md
    return lo, hi

def r1_root_bracket(b_lo, b_hi, a, R):
    lo, hi = mpf_from_float(b_lo), mpf_from_float(b_hi)
    def R1_iv(bv):
        s1f_, s2f_ = roots2_robust(a, float(bv), R)
        s1l, s1h = sec_root_bracket(s1f_ - 1e-6, s1f_ + 1e-6, a, bv, R)
        s2l, s2h = sec_root_bracket(s2f_ - 1e-6, s2f_ + 1e-6, a, bv, R)
        s1 = iv.mpf([s1l, s1h]); s2 = iv.mpf([s2l, s2h])
        return ir1(pt(a), pt(bv), pt(R), s1, s2)
    flo, fhi = R1_iv(lo), R1_iv(hi)
    sflo, sfhi = sign_definite(flo), sign_definite(fhi)
    assert sflo != 0 and sfhi != 0 and sflo * sfhi < 0, (sflo, sfhi)
    for _ in range(80):
        md = (lo + hi) / 2
        fm = R1_iv(md)
        sm = sign_definite(fm)
        if sm == 0:
            hi = md
            continue
        if sm == sflo: lo = md
        else: hi = md
    return lo, hi, sflo

def r2_root_bracket(b_lo, b_hi, a, R):
    lo, hi = mpf_from_float(b_lo), mpf_from_float(b_hi)
    def R2_iv(bv):
        s1f_, s2f_ = roots2_robust(a, float(bv), R)
        s1l, s1h = sec_root_bracket(s1f_ - 1e-6, s1f_ + 1e-6, a, bv, R)
        s2l, s2h = sec_root_bracket(s2f_ - 1e-6, s2f_ + 1e-6, a, bv, R)
        s1 = iv.mpf([s1l, s1h]); s2 = iv.mpf([s2l, s2h])
        return ir2(pt(a), pt(bv), pt(R), s1, s2)
    flo, fhi = R2_iv(lo), R2_iv(hi)
    sflo, sfhi = sign_definite(flo), sign_definite(fhi)
    assert sflo != 0 and sfhi != 0 and sflo * sfhi < 0, (sflo, sfhi)
    for _ in range(80):
        md = (lo + hi) / 2
        fm = R2_iv(md)
        sm = sign_definite(fm)
        if sm == 0:
            hi = md
            continue
        if sm == sflo: lo = md
        else: hi = md
    return lo, hi, sflo

# ---------------- forward-mode interval AD ----------------
class IAD(object):
    __slots__ = ('v', 'g')
    def __init__(self, v, g):
        self.v = v; self.g = list(g)
    def __add__(self, o):
        if isinstance(o, IAD):
            return IAD(self.v + o.v, [x + y for x, y in zip(self.g, o.g)])
        return IAD(self.v + o, self.g)
    __radd__ = __add__
    def __sub__(self, o):
        if isinstance(o, IAD):
            return IAD(self.v - o.v, [x - y for x, y in zip(self.g, o.g)])
        return IAD(self.v - o, self.g)
    def __rsub__(self, o):
        return IAD(o - self.v, [-x for x in self.g])
    def __neg__(self):
        return IAD(-self.v, [-x for x in self.g])
    def __mul__(self, o):
        if isinstance(o, IAD):
            return IAD(self.v * o.v, [x * o.v + self.v * y for x, y in zip(self.g, o.g)])
        return IAD(self.v * o, [x * o for x in self.g])
    __rmul__ = __mul__
    def __truediv__(self, o):
        if isinstance(o, IAD):
            return IAD(self.v / o.v, [(x * o.v - self.v * y) / (o.v * o.v) for x, y in zip(self.g, o.g)])
        return IAD(self.v / o, [x / o for x in self.g])
    def __rtruediv__(self, o):
        return IAD(o / self.v, [-o * x / (self.v * self.v) for x in self.g])
    def __pow__(self, n):
        nv = self.v ** n
        return IAD(nv, [n * x * (self.v ** (n - 1)) for x in self.g])
    def sin(self):
        return IAD(iv.sin(self.v), [x * iv.cos(self.v) for x in self.g])
    def cos(self):
        return IAD(iv.cos(self.v), [-x * iv.sin(self.v) for x in self.g])

def ad_sec(s, a, b, Rm):
    # NOTE: keep IAD always on the LEFT of every * and / (iv * IAD raises).
    A = s * a; B = s * (1 - b); T = s * (b - a) * Rm
    ca, sa = A.cos(), A.sin()
    cb, sb = B.cos(), B.sin()
    ct, st = T.cos(), T.sin()
    return cb * ct * sa - sb * st * sa * Rm + (cb * st * ca) / Rm + sb * ct * ca

def _norm_ad(s, a, b, Rm, Rd):
    # Rm = m = sqrt(Rd) (barrier wavenumber); Rd = density R
    L = b - a; beta = 1 - b
    alpha = s * a; theta = s * L * Rm
    I1 = a / 2 - (alpha * 2).sin() / (4 * s)
    Icc = L / 2 + (theta * 2).sin() / (4 * s * Rm)
    Iss = L / 2 - (theta * 2).sin() / (4 * s * Rm)
    Ics = theta.sin() ** 2 / (2 * s * Rm)
    sa = alpha.sin(); ca = alpha.cos()
    I2 = sa * sa * Icc + (ca * ca) / (Rm * Rm) * Iss + 2 * sa * (ca / Rm) * Ics
    yb_scaled = sa * theta.cos() + (ca / Rm) * theta.sin()
    ypb = -(theta.sin() * sa * Rm) + theta.cos() * ca
    Icc3 = beta / 2 + (s * beta * 2).sin() / (4 * s)
    Iss3 = beta / 2 - (s * beta * 2).sin() / (4 * s)
    Ics3 = (s * beta).sin() ** 2 / (2 * s)
    I3 = (yb_scaled ** 2 * Icc3 + ypb ** 2 * Iss3 + 2 * yb_scaled * ypb * Ics3) / s ** 2
    return (I1 + I2 * Rd) / s ** 2 + I3

def ad_r1(a, b, s1, s2, Rm, Rd):
    n1 = _norm_ad(s1, a, b, Rm, Rd); n2 = _norm_ad(s2, a, b, Rm, Rd)
    y1a1 = (s1 * a).sin()
    y1a2 = (s2 * a).sin()
    return y1a1 ** 2 / n1 - y1a2 ** 2 / n2

def ad_r2(a, b, s1, s2, Rm, Rd):
    def yb_scaled_ad(s):
        alpha = s * a; theta = s * (b - a) * Rm
        sa = alpha.sin(); ca = alpha.cos()
        return sa * theta.cos() + (ca / Rm) * theta.sin()
    n1 = _norm_ad(s1, a, b, Rm, Rd); n2 = _norm_ad(s2, a, b, Rm, Rd)
    return yb_scaled_ad(s1) ** 2 / n1 - yb_scaled_ad(s2) ** 2 / n2

# ---------------- the certificate ----------------
def branch_slopes(a, b_lo, b_hi, R):
    Rm = pt(iv.sqrt(pt(R)))  # m = sqrt(R), the barrier wavenumber factor
    A = pt(a)
    B = iv.mpf([b_lo, b_hi])
    # secular-root enclosures over the whole b-bracket via IVT with b as interval
    def sec_over_b(sv):
        return isec(pt(sv), A, B, pt(R))
    bm = (b_lo + b_hi) / 2
    s1m, s2m = roots2_robust(float(a), float(bm), float(R))
    def root_range(sm):
        sl = sm - 0.05; sh = sm + 0.05
        while True:
            fs_l = sec_over_b(sl); fs_h = sec_over_b(sh)
            sl_s, sh_s = sign_definite(fs_l), sign_definite(fs_h)
            if sl_s != 0 and sh_s != 0 and sl_s * sh_s < 0:
                break
            sl -= 0.05; sh += 0.05
        lo, hi = mpf_from_float(sl), mpf_from_float(sh)
        ref = sign_definite(sec_over_b(lo))
        for _ in range(60):
            md = (lo + hi) / 2
            fm = sec_over_b(md)
            smv = sign_definite(fm)
            if smv == 0:
                hi = md; continue
            if smv == ref: lo = md
            else: hi = md
        return lo, hi, ref
    S1lo, S1hi, ref1 = root_range(s1m)
    S2lo, S2hi, ref2 = root_range(s2m)
    S1 = iv.mpf([S1lo, S1hi]); S2 = iv.mpf([S2lo, S2hi])
    # uniqueness of sec roots over the rectangle: dsec/ds sign-definite
    a3 = IAD(A, [iv.mpf(1), iv.mpf(0), iv.mpf(0)])
    b3 = IAD(B, [iv.mpf(0), iv.mpf(1), iv.mpf(0)])
    s13 = IAD(S1, [iv.mpf(0), iv.mpf(0), iv.mpf(1)])
    s23 = IAD(S2, [iv.mpf(0), iv.mpf(0), iv.mpf(1)])
    sec1 = ad_sec(s13, a3, b3, Rm)
    sec2 = ad_sec(s23, a3, b3, Rm)
    sec_a1, sec_b1, sec_s1 = sec1.g
    sec_a2, sec_b2, sec_s2 = sec2.g
    # 4-var AD for r1, r2 partials
    a4 = IAD(A, [iv.mpf(1), iv.mpf(0), iv.mpf(0), iv.mpf(0)])
    b4 = IAD(B, [iv.mpf(0), iv.mpf(1), iv.mpf(0), iv.mpf(0)])
    s14 = IAD(S1, [iv.mpf(0), iv.mpf(0), iv.mpf(1), iv.mpf(0)])
    s24 = IAD(S2, [iv.mpf(0), iv.mpf(0), iv.mpf(0), iv.mpf(1)])
    r1 = ad_r1(a4, b4, s14, s24, Rm, pt(R))
    r2 = ad_r2(a4, b4, s14, s24, Rm, pt(R))
    r1_a, r1_b, r1_s1, r1_s2 = r1.g
    r2_a, r2_b, r2_s1, r2_s2 = r2.g
    num1 = -r1_a + r1_s1 * sec_a1 / sec_s1 + r1_s2 * sec_a2 / sec_s2
    den1 = r1_b - r1_s1 * sec_b1 / sec_s1 - r1_s2 * sec_b2 / sec_s2
    num2 = -r2_a + r2_s1 * sec_a1 / sec_s1 + r2_s2 * sec_a2 / sec_s2
    den2 = r2_b - r2_s1 * sec_b1 / sec_s1 - r2_s2 * sec_b2 / sec_s2
    g1p = num1 / den1
    g2p = num2 / den2
    dR1db = r1_b + r1_s1 * (-sec_b1 / sec_s1) + r1_s2 * (-sec_b2 / sec_s2)
    dR2db = r2_b + r2_s1 * (-sec_b1 / sec_s1) + r2_s2 * (-sec_b2 / sec_s2)
    return dict(g1p=g1p, g2p=g2p, dR1db=dR1db, dR2db=dR2db,
                S1=S1, S2=S2, sec_s1=sec_s1, sec_s2=sec_s2, den1=den1, den2=den2)

def certify(R, a_str, b1_lo, b1_hi, b2_lo, b2_hi):
    a = mpf(a_str)
    A = pt(a)
    # a0 < a* < b0 via monotonicity of cos on (0, pi):
    # a0 = arccos(1/4)/pi <=> cos(pi*a0) = 1/4; cos decreasing -> a0 < a* iff cos(pi a*) < 1/4
    cA = iv.cos(iv.pi * A)
    in_range = (cA.b < mpf('0.25')) and (cA.a > mpf('-0.25'))
    print(f"R={R:g} a*={a_str}: cos(pi a*) in {cA}; a* in (a0,b0) rigorously: {in_range}")
    lo1, hi1, sgn1 = r1_root_bracket(b1_lo, b1_hi, float(a), R)
    lo2, hi2, sgn2 = r2_root_bracket(b2_lo, b2_hi, float(a), R)
    print(f"  b1* in [{lo1}, {hi1}] width={hi1 - lo1}  (R1 sign pattern {sgn1})")
    print(f"  b2* in [{lo2}, {hi2}] width={hi2 - lo2}  (R2 sign pattern {sgn2})")
    s1 = branch_slopes(a, lo1, hi1, R)
    s2 = branch_slopes(a, lo2, hi2, R)
    g1p, g2p = s1['g1p'], s2['g2p']
    hp = g1p - g2p
    print(f"  g1' = {g1p}")
    print(f"  g2' = {g2p}")
    print(f"  h'  = {hp}  (upper bound {hp.b})")
    checks = {
        'sec_s1 sign-def (b1)': sign_definite(s1['sec_s1']),
        'sec_s2 sign-def (b1)': sign_definite(s1['sec_s2']),
        'den1 sign-def (b1)': sign_definite(s1['den1']),
        'den2 sign-def (b1)': sign_definite(s1['den2']),
        'dR1/db sign-def (b1)': sign_definite(s1['dR1db']),
        'sec_s1 sign-def (b2)': sign_definite(s2['sec_s1']),
        'sec_s2 sign-def (b2)': sign_definite(s2['sec_s2']),
        'den1 sign-def (b2)': sign_definite(s2['den1']),
        'den2 sign-def (b2)': sign_definite(s2['den2']),
        'dR2/db sign-def (b2)': sign_definite(s2['dR2db']),
    }
    for k, v in checks.items():
        print(f"  {k}: {v}")
    for name, (blo, bhi), br, want in [('b1', (lo1, hi1), s1, 'va'), ('b2', (lo2, hi2), s2, 'vb')]:
        B = iv.mpf([blo, bhi])
        va, vb = iv_ratio(A, B, pt(R), br['S1'], br['S2'])
        print(f"  {name}: v(a) in {va} (sign {sign_definite(va)}), v(b) in {vb} (sign {sign_definite(vb)})")
        if want == 'va':
            assert sign_definite(va) > 0, 'branch-1 good-root check v(a)>0 failed'
        else:
            assert sign_definite(vb) < 0, 'branch-2 good-root check v(b)<0 failed'
    ok = (hp.b < 0) and in_range and all(v != 0 for v in checks.values())
    print(f"  CERTIFICATE PASS: h'(a*) < 0 rigorously = {hp.b < 0}; all sign checks nonzero = {all(v != 0 for v in checks.values())}")
    return hp, ok

if __name__ == '__main__':
    hp1, ok1 = certify(1500.0, '0.57364', 0.5830, 0.5836, 0.5758, 0.5762)
    print()
    hp2, ok2 = certify(1e4, '0.57364', 0.5770, 0.5778, 0.5745, 0.5751)
    print()
    print(f"SUMMARY: R=1500 ok={ok1}; R=1e4 ok={ok2}")
