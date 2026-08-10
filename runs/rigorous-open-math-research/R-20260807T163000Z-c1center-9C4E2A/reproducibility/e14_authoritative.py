# -*- coding: utf-8 -*-
"""e14_authoritative.py v6 - optimized: coarse walk + full profile."""
import numpy as np, json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n
from c1trace_lib import R1R2, a_fp, A0, B0, partials
from scipy.optimize import least_squares

def b_roots(a, R, nb=240, ns=701, refine=True, cap=12.0*np.pi):
    b_arr = np.linspace(a+2e-4, 1-2e-4, nb)
    s = np.linspace(1e-9, cap, ns)
    M = sec(s[:,None], a, b_arr[None,:], R)
    pos = M > 0; ch = pos[1:] != pos[:-1]
    nbv = len(b_arr)
    out1 = np.full(nbv, np.nan); out2 = np.full(nbv, np.nan)
    for k in range(2):
        idx = np.zeros(nbv, dtype=int); mask = ch.copy()
        if k == 1:
            first = np.argmax(mask, axis=0)
            for j in range(nbv): mask[first[j], j] = False
        have = mask.any(axis=0); idx[have] = np.argmax(mask[:, have], axis=0)
        lo = s[idx]; hi = s[idx+1]; flo = M[idx, np.arange(nbv)]
        for _ in range(36):
            md = 0.5*(lo+hi); fmd = sec(md, a, b_arr, R)
            upd = (fmd*flo) > 0
            lo = np.where(upd, md, lo); hi = np.where(upd, hi, md)
        val = 0.5*(lo+hi); val = np.where(have, val, np.nan)
        if k == 0: out1 = val
        else: out2 = val
    R1 = np.full(nbv, np.nan)
    for j in range(nbv):
        if np.isnan(out1[j]) or np.isnan(out2[j]): continue
        s1, s2 = out1[j], out2[j]
        n1 = norm_n(s1, a, b_arr[j], R); n2 = norm_n(s2, a, b_arr[j], R)
        R1[j] = (np.sin(s1*a))**2/n1 - (np.sin(s2*a))**2/n2
    roots = []
    for j in range(nbv-1):
        if np.isfinite(R1[j]) and np.isfinite(R1[j+1]) and R1[j]*R1[j+1] < 0:
            if refine:
                lo, hi = b_arr[j], b_arr[j+1]; flo = R1[j]
                for _ in range(55):
                    md = 0.5*(lo+hi)
                    if np.signbit(R1R2(a, float(md), R)[4]) == np.signbit(flo): lo = md
                    else: hi = md
                roots.append(0.5*(lo+hi))
            else:
                roots.append(0.5*(b_arr[j]+b_arr[j+1]))
    return roots

def arm_b(a, R, coarse=False):
    if coarse:
        rs = [r for r in b_roots(a, R, nb=140, ns=501, refine=False) if r - a > 0.002]
    else:
        rs = [r for r in b_roots(a, R) if r - a > 0.002]
    return max(rs) if rs else None

def find_fold(R, seed_ab, cache=None):
    def f(x):
        a, b = x
        R1a, R1b, R2a, R2b = partials(a, b, R, cache=cache)
        return [R1R2(a, b, R, cache)[4], R1b]
    try:
        sol = least_squares(f, seed_ab, xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=300)
        a, b = sol.x
        R1a, R1b, R2a, R2b = partials(a, b, R, cache=cache)
        ok = abs(R1R2(a,b,R,cache)[4]) < 1e-6 and abs(R1b) < 1e-3 and abs(R1a) > 1e-3
        return (float(a), float(b), bool(ok))
    except Exception:
        return (float(seed_ab[0]), float(seed_ab[1]), False)

def profile_on_J(R, cache=None, ngrid=180, a_lo=0.002):
    fp = a_fp(R, cache=cache)
    # coarse walk down
    a, b = fp, 1 - fp
    for a_dec in np.linspace(fp, a_lo, 300)[1:]:
        bnew = arm_b(float(a_dec), R, coarse=True)
        if bnew is None or abs(bnew - b) > 0.04:
            break
        a, b = float(a_dec), bnew
    # refine near end with fine arm_b
    for a_dec in np.linspace(a, max(a_lo, a-0.02), 60)[1:]:
        bnew = arm_b(float(a_dec), R)
        if bnew is None or abs(bnew - b) > 0.01:
            break
        a, b = float(a_dec), bnew
    (a_f, b_f, ok_f) = find_fold(R, (a, b), cache=cache)
    # up walk (coarse then fine)
    a2, b2 = fp, 1 - fp
    for a_inc in np.linspace(fp, min(0.999, 1-1e-3), 300)[1:]:
        bnew = arm_b(float(a_inc), R, coarse=True)
        if bnew is None or abs(bnew - b2) > 0.06:
            break
        a2, b2 = float(a_inc), bnew
    a_max1 = a2
    A_left = max(A0, a_f)
    A_right = min(a_max1, B0, 1 - b_f)
    agrid = np.linspace(A_left, A_right, ngrid)
    rows = []; aa_pts = []; bb_pts = []
    for a in agrid:
        rs = [r for r in b_roots(float(a), R) if r - a > 0.002]
        if not rs:
            rows.append([float(a), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')])
            continue
        b = max(rs)
        aa_pts.append(float(a)); bb_pts.append(b)
        R1a, R1b, R2a, R2b = partials(a, b, R, cache=cache)
        g1p = -R1a/R1b
        rows.append([float(a), float(b), float(g1p), float('nan'), float('nan'), float('nan'), float('nan')])
    aa_pts = np.array(aa_pts); bb_pts = np.array(bb_pts)
    for i, r in enumerate(rows):
        a = r[0]
        if not np.isfinite(r[1]): continue
        y = 1 - a
        if y < bb_pts.min() or y > bb_pts.max(): continue
        u = float(np.interp(y, bb_pts, aa_pts))
        for _ in range(20):
            bu = float(np.interp(u, aa_pts, bb_pts))
            R1a2, R1b2, R2a2, R2b2 = partials(u, bu, R, cache=cache)
            g1pu = -R1a2/R1b2
            if abs(g1pu) < 1e-12: break
            du = -(bu - y)/g1pu
            if not (aa_pts.min()-1e-4 < u+du < aa_pts.max()+1e-4): break
            u = u + du
            if abs(du) < 1e-12: break
        bu = float(np.interp(u, aa_pts, bb_pts))
        R1a2, R1b2, R2a2, R2b2 = partials(u, bu, R, cache=cache)
        g1pu = -R1a2/R1b2
        Phi = r[2]*g1pu; h = r[1] - 1 + u; hp = r[2] - 1/g1pu
        r[3] = float(u); r[4] = float(Phi); r[5] = float(h); r[6] = float(hp)
    return dict(R=R, fp=float(fp), a0=A0, b0=B0, A_left=float(A_left), A_right=float(A_right),
                a_max1=float(a_max1), fold=(a_f, b_f), fold_ok=ok_f, rows=rows)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=float, required=True)
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--ngrid", type=int, default=180)
    args = ap.parse_args()
    cache = {}
    out = profile_on_J(args.R, cache=cache, ngrid=args.ngrid)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f)
    valid = [r for r in out['rows'] if np.isfinite(r[5])]
    hL = valid[0][5]; hR = valid[-1][5]; g1p_min = min(r[2] for r in valid)
    print(f"R={args.R}: A=[{out['A_left']:.6f},{out['A_right']:.6f}] fold=({out['fold'][0]:.6f},{out['fold'][1]:.6f}) ok={out['fold_ok']} "
          f"hL={hL:.6f} hR={hR:.6f} g1p_min={g1p_min:.6f} nvalid={len(valid)}")

