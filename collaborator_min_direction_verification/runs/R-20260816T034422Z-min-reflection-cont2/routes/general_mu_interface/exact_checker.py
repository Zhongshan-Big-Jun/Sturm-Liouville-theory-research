#!/usr/bin/env python3
"""Exact identity checker for MIN-REFL-C2-H.

The checker verifies the algebra behind the direct positive decomposition,
the phase-only weak-contrast collar, and the positive-cell response lemma.
Inequality directions and transcendental monotonicity are proved in report.md.
"""

from __future__ import annotations

import hashlib
import json
import platform

import sympy as sp


def zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.cancel(expr)) == 0, sp.factor(sp.cancel(expr))


checks: list[str] = []

# Re-derive the complete two-momentum Cramer system and its normalized split
# bridge.  The half-angle pairs (t,T) and (s,S) are kept algebraically
# independent; the physical common-angle curve is a strict subdomain.
tt, TT, ss, SS, rr, mm = sp.symbols("tt TT ss SS rr mm", positive=True)


def endpoint(t: sp.Expr, T: sp.Expr, z: sp.Expr) -> dict[str, sp.Expr]:
    c = (1 - t**2) / (1 + t**2)
    sn = 2 * t / (1 + t**2)
    C = (1 - T**2) / (1 + T**2)
    high_sn = 2 * T / (1 + T**2)
    return {
        "x": (z - c) / sn,
        "y": (-z - C) / high_sn,
        "xR": (c * z - 1) / (sn * z),
        "yR": (1 + C * z) / (high_sn * z),
    }


Lmatch = SS * tt * (1 + ss**2) * (1 + TT**2) - TT * ss * (
    1 + tt**2
) * (1 + SS**2)
Dmatch = (
    2 * TT * rr * tt * (SS**2 * ss**2 - 1)
    + TT * ss * (tt**2 - 1) * (1 + SS**2)
    + SS * tt * (1 + ss**2) * (TT**2 - 1)
)
Nmatch = (
    rr * TT * ss * (1 + tt**2) * (SS**2 - 1)
    + rr * SS * tt * (ss**2 - 1) * (1 + TT**2)
    + 2 * SS * ss * (TT**2 * tt**2 - 1)
)
aa = sp.factor(Lmatch / Dmatch)
bb = sp.factor(-Nmatch / (rr * Lmatch))
ep_pos = endpoint(tt, TT, aa)
ep_neg = endpoint(ss, SS, bb)
zero(ep_neg["x"] - ep_pos["xR"] / rr)
zero(ep_neg["y"] - ep_pos["yR"] / rr)
checks.append("both_momentum_matches")


def normalized_cell(t: sp.Expr, T: sp.Expr) -> dict[str, sp.Expr]:
    sn = 2 * t / (1 + t**2)
    c = (1 - t**2) / (1 + t**2)
    high_sn = 2 * T / (1 + T**2)
    C = (1 - T**2) / (1 + T**2)
    UU = 1 / sn + mm / high_sn
    VV = c / sn - mm * C / high_sn
    WW = mm / sn + 1 / high_sn
    ZZ = mm * c / sn - C / high_sn
    QQ = sn + mm * high_sn
    xx = VV / UU
    pp = QQ / UU
    return {
        "U": sp.factor(UU),
        "x": sp.factor(xx),
        "rho": sp.factor(WW / UU),
        "p": sp.factor(pp),
        "e": sp.factor((UU * ZZ - WW * VV) / UU**2),
        "kappa": sp.factor(1 - xx**2 - pp),
        "Q": sp.factor(QQ),
    }


nc_p = normalized_cell(tt, TT)
nc_m = normalized_cell(ss, SS)
lam_n = sp.factor(nc_p["U"] / nc_m["U"])
d_n = sp.factor(nc_p["rho"] - nc_m["rho"])
eta_n = -nc_m["e"]
u_n = sp.factor(1 / aa)
w_n = sp.factor(u_n - nc_p["x"])
zero(w_n - (nc_p["e"] - rr * eta_n / lam_n) / d_n)
zero(-bb - (lam_n * w_n / rr - nc_m["x"]))
checks.append("normalized_cramer_coordinates")

# Reconstruct the pre-normalized split numerator from the cell factors and
# verify its exact equality with U_+^2*Phi/(lambda*u^3).
dpos = mm * TT**2 * tt + TT * tt**2 + TT + mm * tt
npos = mm * TT**2 * tt - TT * tt**2 + TT - mm * tt
dneg = mm * SS**2 * ss + SS * ss**2 + SS + mm * ss
nneg = mm * SS**2 * ss - SS * ss**2 + SS - mm * ss
gpos = sp.factor((dpos * aa - npos) / (2 * TT * tt))
hpos = sp.factor((dpos - npos * aa) / (2 * TT * tt * aa))
Bamp = -bb
Gneg = sp.factor((nneg + dneg * Bamp) / (2 * SS * ss))
Jneg = sp.factor((dneg + nneg * Bamp) / (2 * SS * ss * Bamp))
delta_n = rr**2 - 1
Dcell = delta_n * aa * nc_p["Q"] + rr * Gneg + aa**2 * gpos
split_raw = sp.together(
    rr**2
    * aa
    * Bamp
    * (Gneg + Jneg)
    * (delta_n * nc_p["Q"] + aa * gpos)
    - delta_n * nc_m["Q"] * Dcell
)
zero(hpos - rr * Gneg)
A_n = sp.factor(1 - nc_p["x"] * u_n)
Phi_n = sp.together(
    (lam_n**2 * w_n**2 + rr**2 * nc_m["kappa"] + nc_m["p"])
    * (A_n + delta_n * nc_p["p"] * u_n**2)
    - delta_n * nc_m["p"] * w_n * u_n**3
)
zero(split_raw - nc_p["U"] ** 2 * Phi_n / (lam_n * u_n**3))
checks.append("full_normalized_split_bridge")

# Time reversal maps every endpoint ratio z to 1/z and interchanges g,h.
# First verify this on the full physical endpoint and cell formulas.
cc_ratio = sp.factor(1 / aa)
bb_right = sp.factor(1 / bb)
Bamp_right = sp.factor(-bb_right)
ep_pos_right = endpoint(tt, TT, cc_ratio)
ep_neg_right = endpoint(ss, SS, bb_right)
zero(ep_pos_right["x"] - rr * ep_neg_right["xR"])
zero(ep_pos_right["y"] - rr * ep_neg_right["yR"])

gpos_right = sp.factor((dpos * cc_ratio - npos) / (2 * TT * tt))
hpos_right = sp.factor(
    (dpos - npos * cc_ratio) / (2 * TT * tt * cc_ratio)
)
Gneg_right = sp.factor((nneg + dneg * Bamp_right) / (2 * SS * ss))
Jneg_right = sp.factor(
    (dneg + nneg * Bamp_right) / (2 * SS * ss * Bamp_right)
)
zero(gpos_right - hpos)
zero(hpos_right - gpos)
zero(Gneg_right - Jneg)
zero(Jneg_right - Gneg)
zero(gpos_right - rr * Jneg_right)

# Now replay both Schur gaps in an exact rational-function ring.  We set the
# middle-cell normalization u_2^2=1; homogeneity makes every displayed sign
# scale independent.  The substitution h_+=rG is precisely the physical
# gamma match already checked above at line 120.
aS, BS, QpS, QmS, gpS, GS, JS, deltaS, rS = sp.symbols(
    "aS BS QpS QmS gpS GS JS deltaS rS", positive=True
)
hS = rS * GS
D1S = deltaS * aS * QpS + rS * GS + aS**2 * gpS
NLS = (
    rS**2
    * aS
    * BS
    * (GS + JS)
    * (deltaS * QpS + aS * gpS)
    - deltaS * QmS * D1S
)
middle_weight_S = QmS / (rS * BS)
xstar_LS = rS * (GS + JS) / middle_weight_S
beta_RS = (
    aS
    * hS
    * (deltaS * QpS + aS * gpS)
    / (deltaS * D1S)
)
ELS = beta_RS * xstar_LS - rS * GS
zero(ELS - rS * GS * NLS / (deltaS * D1S * QmS))
checks.append("left_schur_gap_positive_prefactor")

# In the original right orientation c=1/a and B_R=1/B.  Time reversal
# swaps gp<->hp and G<->J.  This gives N_R=N_L/(a^2 B), a strictly positive
# rescaling, and the exact right Schur prefactor below.
cS = 1 / aS
BRS = 1 / BS
gpRS, hpRS = hS, gpS
GRS, JRS = JS, GS
D3S = deltaS * cS * QpS + hpRS + cS**2 * rS * JRS
NRS = (
    rS**2
    * (GRS + JRS)
    * (deltaS * cS * QpS + hpRS)
    - deltaS * QmS * BRS * D3S
)
zero(D3S - D1S / aS**2)
zero(NRS - NLS / (aS**2 * BS))
middle_weight_RS = QmS / (rS * BRS)
xstar_RS = rS * (GRS + JRS) / middle_weight_RS
beta_LS = (
    gpRS
    * (deltaS * cS * QpS + hpRS)
    / (deltaS * D3S * BRS**2)
)
ERS = beta_LS * xstar_RS - rS * JRS
zero(
    ERS
    - rS * JRS * NRS / (deltaS * D3S * BRS * QmS)
)
checks.append("time_reversed_right_schur_gap_positive_prefactor")

# The scale-independent three-cell gamma-jump gluing is a separate exact
# identity.  Its sign input is gamma_2<0<gamma_3 and |K_2|>0.
beta_L, beta_R, Kabs, Gmid, Jmid, rmid = sp.symbols(
    "beta_L beta_R Kabs Gmid Jmid rmid", positive=True
)
gamma2 = -rmid * Gmid
gamma3 = rmid * Jmid
xstar = (gamma3 - gamma2) / Kabs
Hscalar = beta_L + beta_R - Kabs
E_L = beta_R * xstar + gamma2
E_R = beta_L * xstar - gamma3
zero(Hscalar * xstar - (E_L + E_R))
checks.append("three_cell_gamma_jump_schur_gluing")

# Exact split decomposition.  P denotes p_+, p denotes p_-, K denotes
# kappa_-, and L2 denotes lambda^2.  The physical identity r^2=1+delta is
# built in before comparison.
L2, w, delta, K, p, P, u, A0 = sp.symbols(
    "L2 w delta K p P u A0", positive=True
)
Phi = (L2 * w**2 + (1 + delta) * K + p) * (
    A0 + delta * P * u**2
) - delta * p * w * u**3
decomposition = (
    p * (A0 - delta * w * u**3)
    + (L2 * w**2 + (1 + delta) * K) * A0
    + delta * P * u**2 * (L2 * w**2 + (1 + delta) * K + p)
)
zero(Phi - decomposition)
checks.append("three_positive_blocks_decomposition")

# A second, often larger, collar follows by completing the square in the
# three terms lambda^2*A0*w^2 + delta*p_+*p_-*u^2
# - delta*p_-*w*u^3.
square_core = L2 * A0 * w**2 + delta * P * p * u**2 - delta * p * w * u**3
square_form = (
    L2 * A0 * (w - delta * p * u**3 / (2 * L2 * A0)) ** 2
    + delta * P * p * u**2
    - delta**2 * p**2 * u**6 / (4 * L2 * A0)
)
zero(square_core - square_form)
checks.append("amgm_square_completion")

# Affine contrast evolution and the fixed phase-only collar data.
r, c0, w0, x = sp.symbols("r c0 w0 x", positive=True)
w_r = w0 - c0 * (r - 1)
u_r = x + w_r
u0 = x + w0
A_r = 1 - x * u_r
A00 = 1 - x * u0
zero(w0 - w_r - c0 * (r - 1))
zero(u0 - u_r - c0 * (r - 1))
zero(A_r - A00 - x * c0 * (r - 1))
checks.append("affine_contrast_monotonicity")

# Positive-cell response lemma algebra in half-sum variables.  The analytic
# sign uses 0<B<A<pi/2 and tan(t)/t strictly increasing.
mu = sp.symbols("mu", positive=True)
s, S, cc, C = sp.symbols("s S cc C", real=True)
D = S + mu * s
Q = s + mu * S
N = S * cc - mu * s * C
rho = Q / D
pplus = Q * s * S / D
xplus = N / D
eplus = (mu**2 - 1) * s * S * (cc + C) / D**2
response = sp.factor(pplus * (rho - 1) - xplus * eplus)
expected_response = (
    (mu - 1)
    * s
    * S
    * (Q * D * (S - s) - (mu + 1) * N * (cc + C))
    / D**3
)
zero(response - expected_response)
checks.append("positive_cell_response_factor")

# Verify the exact A,B reduction of the brace, modulo the two circle
# identities.  Here q=(mu-1)/(mu+1).
A, B, q = sp.symbols("A B q", positive=True)
sa, ca, sb, cb = sp.symbols("sa ca sb cb", real=True)
mu_q = (1 + q) / (1 - q)
s_ab = sa * cb - ca * sb
S_ab = sa * cb + ca * sb
c_ab = ca * cb + sa * sb
C_ab = ca * cb - sa * sb
D_ab = S_ab + mu_q * s_ab
Q_ab = s_ab + mu_q * S_ab
N_ab = S_ab * c_ab - mu_q * s_ab * C_ab
brace = sp.together(
    Q_ab * D_ab * (S_ab - s_ab)
    - (mu_q + 1) * N_ab * (c_ab + C_ab)
)
target = (
    2
    * (mu_q + 1) ** 2
    * ca**3
    * cb
    * (q * sa / ca - (sb / cb) * (cb**2 + q**2 * sb**2))
)
num = sp.together(brace - target).as_numer_denom()[0]
# Polynomial reduction by sin^2+cos^2=1 for A and B.
gb = sp.groebner(
    [sa**2 + ca**2 - 1, sb**2 + cb**2 - 1],
    sa,
    ca,
    sb,
    cb,
    order="lex",
    domain=sp.QQ.frac_field(q),
)
rem = gb.reduce(sp.Poly(sp.expand(num), sa, ca, sb, cb).as_expr())[1]
zero(rem)
checks.append("positive_cell_half_sum_reduction")


def cell_mu2(t: sp.Rational) -> dict[str, sp.Expr]:
    """Exact same-angle data from t=tan(theta/2), with mu=2."""
    sn = 2 * t / (1 + t**2)
    cs = (1 - t**2) / (1 + t**2)
    high_sn = 2 * sn * cs
    high_cs = cs**2 - sn**2
    FF = high_sn / sn
    UU = 1 / sn + 2 / high_sn
    QQ = sn + 2 * high_sn
    xx = (FF * cs - 2 * high_cs) / (FF + 2)
    rrho = (2 * FF + 1) / (FF + 2)
    pp = QQ / UU
    ee = 3 * FF * (cs + high_cs) / (FF + 2) ** 2
    kk = 1 - xx**2 - pp
    return {
        "F": sp.factor(FF),
        "U": sp.factor(UU),
        "x": sp.factor(xx),
        "rho": sp.factor(rrho),
        "p": sp.factor(pp),
        "e": sp.factor(ee),
        "kappa": sp.factor(kk),
    }


# Exact physical common-angle witness showing that neither sufficient collar
# factor is globally positive.  This is not a counterexample to Phi>0.
t_plus = sp.Rational(1, 100)
t_minus = sp.Rational(3, 5)
plus = cell_mu2(t_plus)
minus = cell_mu2(t_minus)
assert 3 * t_plus**2 < 1
assert 3 * t_minus**2 > 1 and t_minus < 1
lam_w = sp.factor(plus["U"] / minus["U"])
d_w = sp.factor(plus["rho"] - minus["rho"])
eta_w = -minus["e"]
rb_w = sp.factor(lam_w * plus["e"] / (eta_w + d_w * minus["x"]))
r_w = sp.factor((1 + rb_w) / 2)
w_w = sp.factor((plus["e"] - r_w * eta_w / lam_w) / d_w)
u_w = sp.factor(plus["x"] + w_w)
A_w = sp.factor(1 - plus["x"] * u_w)
delta_w = sp.factor(r_w**2 - 1)
B_w = sp.factor(lam_w * w_w / r_w - minus["x"])
Lambda_w = sp.factor(A_w - delta_w * w_w * u_w**3)
Xi_w = sp.factor(
    4 * lam_w**2 * plus["p"] * A_w
    - delta_w * minus["p"] * u_w**4
)
Phi_w = sp.factor(
    (lam_w**2 * w_w**2 + r_w**2 * minus["kappa"] + minus["p"])
    * (A_w + delta_w * plus["p"] * u_w**2)
    - delta_w * minus["p"] * w_w * u_w**3
)
assert rb_w == sp.Rational(4798560, 38791)
assert 1 < r_w < rb_w
assert w_w > 0 and u_w > 0 and A_w > 0 and B_w > 0
assert plus["e"] > 0 and minus["e"] < 0
assert plus["p"] > 0 and minus["p"] > 0
assert plus["kappa"] > 0 and minus["kappa"] > 0
assert Lambda_w < 0 and Xi_w < 0 and Phi_w > 0
checks.append("exact_physical_failure_of_global_collar_factors")

witness_record = {
    "mu": "2",
    "tan_alpha_over_2": str(t_plus),
    "tan_beta_over_2": str(t_minus),
    "rB": str(rb_w),
    "r": str(r_w),
    "Lambda_sign": "negative",
    "Xi_sign": "negative",
    "Phi_sign": "positive",
    "scope_warning": "physical local interface; not a counterexample to Phi positivity",
}

# Hash a stable exact textual form of the main decomposition.
decomposition_text = sp.sstr(sp.factor(decomposition))

print(
    json.dumps(
        {
            "status": "PASS",
            "route": "MIN-REFL-C2-H",
            "checks": checks,
            "exact_factor_no_go_witness": witness_record,
            "main_decomposition_sha256": hashlib.sha256(
                decomposition_text.encode("utf-8")
            ).hexdigest(),
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "limitations": (
                "Identity checker only; sign directions and strict-domain "
                "arguments are in report.md."
            ),
        },
        indent=2,
        sort_keys=True,
    )
)
