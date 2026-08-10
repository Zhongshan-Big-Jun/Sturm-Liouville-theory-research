# verify_o1_audit.py  (version 2, vectorized)
# Independent numeric audit of O1_reduction_draft.md obligations O1a-O1f.
# Exact (vectorized) transfer-matrix solver for piecewise-constant densities.
# All output is EVIDENCE ONLY.
import numpy as np, json, math

def sec_vec(blocks, lam):
    lam = np.asarray(lam, dtype=float)
    M = np.zeros((len(lam), 2, 2))
    M[:, 0, 0] = 1.0
    M[:, 1, 1] = 1.0
    for L, c in blocks:
        om = np.sqrt(lam * c)
        cos = np.cos(om * L)
        sin = np.sin(om * L)
        P = np.empty((len(lam), 2, 2))
        P[:, 0, 0] = cos
        P[:, 0, 1] = sin / om
        P[:, 1, 0] = -om * sin
        P[:, 1, 1] = cos
        M = np.einsum('nij,njk->nik', P, M)
    return M[:, 0, 1]

def eigpair(blocks, R, ncoarse=2500, tol=1e-13):
    lo = 0.5 * math.pi**2 / R
    hi = 9 * math.pi**2
    xs = np.linspace(lo, hi, ncoarse + 1)
    vals = sec_vec(blocks, xs)
    roots = []
    for i in range(ncoarse):
        if vals[i] * vals[i + 1] < 0 or abs(vals[i]) < 1e-12:
            a, b = float(xs[i]), float(xs[i + 1])
            fa = sec_vec(blocks, np.array([a]))[0]
            for _ in range(300):
                m = 0.5 * (a + b)
                fm = sec_vec(blocks, np.array([m]))[0]
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
                if b - a < tol * (1 + abs(m)):
                    break
            roots.append(0.5 * (a + b))
            if len(roots) >= 2:
                break
    if len(roots) < 2:
        raise RuntimeError('fewer than 2 roots found')
    return roots[0], roots[1]

def propagate(blocks, lam):
    M = np.eye(2)
    info = []
    x = 0.0
    for L, c in blocks:
        om = math.sqrt(lam * c)
        cos, sin = math.cos(om * L), math.sin(om * L)
        P = np.array([[cos, sin / om], [-om * sin, cos]])
        s0 = M @ np.array([0.0, 1.0])
        info.append((x, L, c, om, s0))
        M = P @ M
        x += L
    return M[0, 1], info

def eigenfunction(blocks, lam):
    _, info = propagate(blocks, lam)
    N = 0.0
    for x0, L, c, om, s0 in info:
        u0, up0 = s0
        A, B = u0, up0 / om
        I = (A*A)*(L/2 + math.sin(2*om*L)/(4*om)) + (B*B)*(L/2 - math.sin(2*om*L)/(4*om)) + (A*B)*(1 - math.cos(2*om*L))/(2*om)
        N += c * I
    nrm = math.sqrt(N)
    def ev(x):
        for x0, L, c, om, s0 in info:
            if x0 - 1e-14 <= x <= x0 + L + 1e-14:
                t = x - x0
                u0, up0 = s0
                u = u0 * math.cos(om * t) + (up0 / om) * math.sin(om * t)
                up = -u0 * om * math.sin(om * t) + up0 * math.cos(om * t)
                return u / nrm, up / nrm
        raise ValueError(x)
    return ev, nrm

def D_of(blocks, R):
    l1, l2 = eigpair(blocks, R)
    return l2 - l1, l1, l2

def check_O1c(blocks, R, npts=20001):
    l1, l2 = eigpair(blocks, R)
    ev1, _ = eigenfunction(blocks, l1)
    ev2, _ = eigenfunction(blocks, l2)
    xi = np.linspace(0.0, 1.0, npts)[1:-1]
    us1 = np.array([ev1(x)[0] for x in xi])
    us2 = np.array([ev2(x)[0] for x in xi])
    ups1 = np.array([ev1(x)[1] for x in xi])
    ups2 = np.array([ev2(x)[1] for x in xi])
    W = us1 * ups2 - us2 * ups1
    v = us2 / us1
    f = l1 * us1**2 - l2 * us2**2
    c = math.sqrt(l1 / l2)
    sgn = np.sign(us2)
    zidx = np.where(np.diff(sgn) != 0)[0]
    z0 = float(xi[zidx[0]])
    nz2 = int(len(zidx))
    g = np.abs(v) - c
    gz = np.where(np.sign(g[:-1]) != np.sign(g[1:]))[0]
    neg = g < 0
    comps = []
    start = None
    for i, val in enumerate(neg):
        if val and start is None:
            start = i
        if not val and start is not None:
            comps.append((float(xi[start]), float(xi[i - 1])))
            start = None
    if start is not None:
        comps.append((float(xi[start]), float(xi[-1])))
    contains = any(a <= z0 <= b for a, b in comps)
    return dict(R=R, l1=l1, l2=l2, z0=z0, nzeros_u2=nz2, nzeros_f=len(gz),
                npos_intervals=len(comps), pos_contains_z0=contains,
                W_max_interior=float(np.max(W)), dv_max=float(np.max(np.diff(v))),
                W_negative=bool(np.all(W < 0)), v_strictly_decreasing=bool(np.all(np.diff(v) < 0)),
                f_at_z0=float(l1 * ev1(z0)[0]**2 - l2 * ev2(z0)[0]**2))

def jump_derivative(blocks, R, j, eps=1e-6):
    L0 = [b[0] for b in blocks]
    C = [b[1] for b in blocks]
    def shifted(delta):
        newL = list(L0)
        newL[j] += delta
        newL[j + 1] -= delta
        out = []
        for Lc, cc in zip(newL, C):
            if Lc > 1e-14:
                out.append((Lc, cc))
        return out
    D0, _, _ = D_of(blocks, R)
    Dr, _, _ = D_of(shifted(eps), R)
    Dl, _, _ = D_of(shifted(-eps), R)
    return D0, (Dr - D0) / eps, (D0 - Dl) / eps

def f_at_jump(blocks, R, j):
    l1, l2 = eigpair(blocks, R)
    ev1, _ = eigenfunction(blocks, l1)
    ev2, _ = eigenfunction(blocks, l2)
    xj = sum(b[0] for b in blocks[:j + 1])
    return l1 * ev1(xj)[0]**2 - l2 * ev2(xj)[0]**2, xj

def sym_barrier(u, R):
    return [(u, 1.0), (1 - 2 * u, R), (u, 1.0)]

def main():
    R = 4.0
    rng = np.random.default_rng(20260806)
    out = {}

    o1c = []
    for trial in range(10):
        a = float(rng.uniform(0.05, 0.8))
        b = a + float(rng.uniform(0.05, 1 - a))
        if trial % 2 == 0:
            c = [1.0, R, 1.0]
        else:
            c = [float(rng.uniform(1, R)) for _ in range(3)]
        blocks = [(a, c[0]), (b - a, c[1]), (1 - b, c[2])]
        o1c.append(check_O1c(blocks, R))
    out['O1c_structure'] = o1c

    a, b = 0.2, 0.65
    blocks = [(a, 1.0), (b - a, R), (1 - b, 1.0)]
    D0, dr, dl = jump_derivative(blocks, R, 0)
    f0, xj = f_at_jump(blocks, R, 0)
    c1mc0 = R - 1.0
    out['O1b_jump0'] = dict(D0=D0, xj=xj, dr_num=dr, dl_num=dl,
                            pred_right=-c1mc0 * f0, pred_left=+c1mc0 * f0,
                            draft_pred=+c1mc0 * f0,
                            right_match_correct=bool(abs(dr - (-c1mc0 * f0)) < 1e-3),
                            left_match_correct=bool(abs(-dl - (+c1mc0 * f0)) < 1e-3),
                            draft_sign_fails=bool(abs(dr - (+c1mc0 * f0)) > 1e-3))
    D0, dr2, dl2 = jump_derivative(blocks, R, 1)
    f1, xj1 = f_at_jump(blocks, R, 1)
    c2mc1 = 1.0 - R
    out['O1b_jump1'] = dict(D0=D0, xj=xj1, dr_num=dr2, dl_num=dl2,
                            pred_right=-c2mc1 * f1, pred_left=+c2mc1 * f1,
                            draft_pred=+c2mc1 * f1,
                            right_match_correct=bool(abs(dr2 - (-c2mc1 * f1)) < 1e-3),
                            left_match_correct=bool(abs(-dl2 - (+c2mc1 * f1)) < 1e-3),
                            draft_sign_fails=bool(abs(dr2 - (+c2mc1 * f1)) > 1e-3))

    sym = []
    for u in [0.2, 0.3, 0.4, 0.45148546584, 0.49]:
        blocks = sym_barrier(u, R)
        D0, l1, l2 = D_of(blocks, R)
        f_at_u, _ = f_at_jump(blocks, R, 0)
        e = 1e-6
        Dp, _, _ = D_of(sym_barrier(u + e, R), R)
        Dm, _, _ = D_of(sym_barrier(u - e, R), R)
        dnum = (Dp - Dm) / (2 * e)
        pred = -2 * (R - 1) * f_at_u
        sym.append(dict(u=u, D=D0, f_at_u=f_at_u, dD_du_num=dnum, pred=pred,
                        match=bool(abs(dnum - pred) < 1e-3)))
    out['O1b_symmetric_family'] = sym

    lo, hi = 0.05, 0.4999
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        f_at_u, _ = f_at_jump(sym_barrier(mid, R), R, 0)
        if f_at_u < 0:
            lo = mid
        else:
            hi = mid
    ustar = 0.5 * (lo + hi)
    Dstar, l1, l2 = D_of(sym_barrier(ustar, R), R)
    out['sym_u_star'] = dict(u_star=ustar, D_star=Dstar, l1=l1, l2=l2,
                             contract_u=0.45148546584, contract_D=32.6139836177,
                             u_match=bool(abs(ustar - 0.45148546584) < 1e-6),
                             D_match=bool(abs(Dstar - 32.6139836177) < 1e-5))

    best = -1e9
    worst = 1e9
    n = 1200
    found_better = found_worse = False
    for _ in range(n):
        m = int(rng.integers(2, 6))
        cuts = np.sort(rng.uniform(0, 1, m))
        Ls = np.diff(np.concatenate([[0], cuts, [1]]))
        if _ % 2 == 0:
            Cs = rng.choice([1.0, R], size=m + 1, replace=True)
        else:
            Cs = rng.uniform(1, R, m + 1)
        blocks = [(float(Ls[i]), float(Cs[i])) for i in range(m + 1)]
        D, _, _ = D_of(blocks, R)
        if D > best:
            best = D
        if D < worst:
            worst = D
        if D > 32.6139836177 + 1e-6:
            found_better = True
        if D < 6.7844823391 - 1e-6:
            found_worse = True
    out['global_search_evidence'] = dict(n=n, best=best, worst=worst,
                                         sup_contract=32.6139836177,
                                         inf_contract=6.7844823391,
                                         beat_sup=found_better, beat_inf=found_worse)

    cont = []
    l10, l20 = eigpair([(0.3, 1.0), (0.4, 3.2), (0.3, 1.0)], R)
    for eps in [1e-3, 1e-4, 1e-5]:
        l1e, l2e = eigpair([(0.3, 1.0), (0.4 - eps, 3.2), (0.3, 1.0)], R)
        cont.append(dict(eps=eps, dlambda1=abs(l1e - l10), dlambda2=abs(l2e - l20)))
    out['L1_continuity_check'] = cont

    print(json.dumps(out, indent=1))

if __name__ == '__main__':
    main()
