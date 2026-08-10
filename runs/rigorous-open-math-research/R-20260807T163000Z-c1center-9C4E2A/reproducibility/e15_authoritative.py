# -*- coding: utf-8 -*-
"""e15_authoritative.py v6 - fp-arm profile via max-root fine-b scans (midpoint roots)."""
import numpy as np, json, sys, os, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n
from c1trace_lib import R1R2, a_fp, A0, B0, partials

CAP = 2.0*np.pi + 0.6

def col_s12_window(a, b_arr, R, ns=1501):
    s = np.linspace(1e-9, CAP, ns)
    M = sec(s[:, None], a, b_arr[None, :], R)
    pos = M > 0
    ch = pos[1:] != pos[:-1]
    nbv = len(b_arr)
    out = np.full((2, nbv), np.nan)
    for k in range(2):
        mask = ch.copy()
        if k == 1:
            first = np.argmax(mask, axis=0)
            for j in range(nbv):
                mask[first[j], j] = False
        have = mask.any(axis=0)
        idx = np.zeros(nbv, dtype=int)
        idx[have] = np.argmax(mask[:, have], axis=0)
        lo = s[idx]; hi = s[idx + 1]
        flo = M[idx, np.arange(nbv)]
        for _ in range(50):
            md = 0.5*(lo + hi)
            fmd = sec(md, a, b_arr, R)
            upd = (fmd*flo) > 0
            lo = np.where(upd, md, lo); hi = np.where(upd, hi, md)
        out[k] = np.where(have, 0.5*(lo + hi), np.nan)
    return out

def max_root_col(a, R, b_lo, b_hi, nb=1500):
    """Largest-b root of R1(a,.)=0 in [b_lo,b_hi]; midpoint precision."""
    if b_hi <= b_lo:
        return None
    b_arr = np.linspace(b_lo, b_hi, nb)
    s12 = col_s12_window(a, b_arr, R)
    last = None
    prev = None
    for j in range(nb):
        s1, s2 = s12[0, j], s12[1, j]
        if np.isnan(s1) or np.isnan(s2):
            prev = None
            continue
        n1 = norm_n(s1, a, float(b_arr[j]), R); n2 = norm_n(s2, a, float(b_arr[j]), R)
        R1 = np.sin(s1*a)**2/n1 - np.sin(s2*a)**2/n2
        if prev is not None and prev[1]*R1 < 0:
            last = 0.5*(prev[0] + b_arr[j])
        prev = (b_arr[j], R1)
    return last

def trace_extent(R):
    fp = a_fp(R)
    a, b = fp, 1-fp
    step = 0.002
    a_min = fp
    while a > 0.0 + 1e-9 and step >= 1e-7:
        a_new = max(0.0, a - step)
        b_new = max_root_col(a_new, R, max(0.0, b - 0.06), b + 0.06)
        if b_new is None:
            step *= 0.5
            continue
        if abs(b_new - b) > 0.3:
            step *= 0.5
            continue
        a, b = a_new, b_new
        a_min = a_new
        step = min(0.002, step*1.5)
    a, b = fp, 1-fp
    step = 0.002
    a_max = fp
    while a < 1.0 - 1e-6 and step >= 1e-7:
        a_new = a + step
        b_new = max_root_col(a_new, R, b - 0.06, min(1.0, b + 0.06))
        if b_new is None:
            step *= 0.5
            continue
        if abs(b_new - b) > 0.3:
            step *= 0.5
            continue
        a, b = a_new, b_new
        a_max = a_new
        step = min(0.002, step*1.5)
    return a_min, a_max

def profile(R, ngrid=200):
    a_min, a_max = trace_extent(R)
    fp = a_fp(R)
    A_left = max(A0, a_min)
    A_right = min(a_max, B0)
    if A_right <= A_left:
        return dict(R=R, error="empty domain", a_min=a_min, a_max=a_max)
    agrid = np.linspace(A_left, A_right, ngrid+1)
    bprev = None
    rows = []
    for a in agrid:
        if bprev is None:
            lo, hi = A_left - 0.02, 1.0
        else:
            lo, hi = max(0.0, bprev - 0.05), min(1.0, bprev + 0.05)
        b = max_root_col(float(a), R, lo, hi)
        if b is None:
            rows.append([float(a), np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
            continue
        bprev = b
        R1a, R1b, R2a, R2b = partials(a, b, R)
        g1p = -R1a/R1b
        rows.append([float(a), float(b), float(g1p), np.nan, np.nan, np.nan, np.nan])
    pts = [(r[0], r[1]) for r in rows if np.isfinite(r[1])]
    if len(pts) < 3:
        return dict(R=R, error="no arm rows", a_min=a_min, a_max=a_max)
    aa = np.array([p[0] for p in pts]); bb = np.array([p[1] for p in pts])
    dbb = np.gradient(bb, aa)
    for r in rows:
        if not np.isfinite(r[1]):
            continue
        a, b, g1p = r[0], r[1], r[2]
        y = 1.0 - a
        if y < bb.min() - 1e-6 or y > bb.max() + 1e-6:
            continue
        u = float(np.interp(y, bb, aa))
        for _ in range(25):
            bu = float(np.interp(u, aa, bb)); sl = float(np.interp(u, aa, dbb))
            if abs(sl) < 1e-12:
                break
            du = (y - bu)/sl
            u = u + du
            if abs(du) < 1e-12:
                break
        if not (aa.min() - 1e-3 <= u <= aa.max() + 1e-3):
            continue
        u = min(max(u, aa.min()), aa.max())
        ok = False
        for _ in range(4):
            bugu = float(np.interp(u, aa, bb))
            bu = max_root_col(float(u), R, max(0.0, bugu - 0.02), min(1.0, bugu + 0.02), nb=400)
            if bu is None:
                break
            R1a2, R1b2, R2a2, R2b2 = partials(u, bu, R)
            g1pu = -R1a2/R1b2
            if abs(g1pu) < 1e-10:
                break
            du = (y - bu)/g1pu
            if not (aa.min()-1e-4 < u+du < aa.max()+1e-4):
                break
            u = u + du
            if abs(du) < 1e-11:
                ok = True
                break
        bugu = float(np.interp(u, aa, bb))
        bu = max_root_col(float(u), R, max(0.0, bugu - 0.02), min(1.0, bugu + 0.02), nb=400)
        if bu is None:
            continue
        R1a2, R1b2, R2a2, R2b2 = partials(u, bu, R)
        g1pu = -R1a2/R1b2
        Phi = g1p*g1pu
        h = b - 1.0 + u
        hp = g1p - 1.0/g1pu
        r[3], r[4], r[5], r[6] = float(u), float(Phi), float(h), float(hp)
    return dict(R=R, fp=float(fp), A0=A0, B0=B0, a_min=a_min, a_max=a_max,
                A_left=float(A_left), A_right=float(A_right), rows=rows)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=float, required=True)
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--ngrid", type=int, default=200)
    args = ap.parse_args()
    out = profile(args.R, ngrid=args.ngrid)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f)
    valid = [r for r in out["rows"] if np.isfinite(r[5])]
    if not valid:
        print("R=%g: NO valid h rows (arm a=[%.5f,%.5f])" % (args.R, out["a_min"], out["a_max"]))
    else:
        hps = [r[6] for r in valid]
        nz = sum(1 for i in range(len(valid)-1) if valid[i][5]*valid[i+1][5] < 0)
        nch = sum(1 for i in range(len(valid)-1) if hps[i]*hps[i+1] < 0)
        print("R=%g: arm a=[%.6f,%.6f] A=[%.6f,%.6f] hL=%.6f hR=%.6f hzeros=%d hp_chg=%d g1p_min=%.6f g1p_max=%.6f nvalid=%d" %
              (args.R, out["a_min"], out["a_max"], out["A_left"], out["A_right"],
               valid[0][5], valid[-1][5], nz, nch, min(r[2] for r in valid), max(r[2] for r in valid), len(valid)))

