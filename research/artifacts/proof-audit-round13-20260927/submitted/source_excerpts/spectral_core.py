"""Source-function excerpts, not a whole-file copy.
Pinned commit: 4a82d3c2c8c7c3e5f3f027efcf2be3c54a612983.
roots_of/eigfun and selected Recon methods: scripts/_gapn2_symmetry_recon.py.
uv_at/green_kernel/eigen_data: scripts/_gapn2_jacobian_analytic.py.
Imports and this provenance header were added; no mathematical fixes applied.
"""
import numpy as np
from _sl_prufer import indexed_roots


def roots_of(blocks, k, npts=20000, refine=60):
	"""First k Dirichlet frequencies, indexed by lifted phase n*pi.

	Numerical only, not interval-certified. npts remains an unused compatibility
	argument; no frequency scan is performed. Unresolved enumeration raises.
	"""
	return indexed_roots(blocks, k, refine)[0]


def eigfun(blocks, s, pts):
    """Normalized eigenfunction values at pts (L^2(rho) normalization)."""
    xs = [0.0]
    for L, _ in blocks:
        xs.append(xs[-1] + L)
    starts = []
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    starts.append((0.0, M00, M01, M10, M11))
    for L, c in blocks:
        w = s * np.sqrt(c); wL = w * L
        cw = np.cos(wL); sw = L * np.sinc(wL / np.pi); sw2 = -w * np.sin(wL)
        M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, \
                             sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
        starts.append((xs[len(starts)], M00, M01, M10, M11))
    norm = 0.0
    for bi, (L, c) in enumerate(blocks):
        _, M00, M01, M10, M11 = starts[bi]
        w = s * np.sqrt(c)
        A = M01; B = M11 / w
        Icos = 0.5 * (L + np.sin(2 * w * L) / (2 * w))
        Isin = 0.5 * (L - np.sin(2 * w * L) / (2 * w))
        Icross = np.sin(w * L) ** 2 / (2 * w)
        norm += c * (A * A * Icos + B * B * Isin + 2 * A * B * Icross)
    out = np.zeros(len(pts))
    for j, p in enumerate(pts):
        bi = max(i for i in range(len(xs) - 1) if xs[i] <= p)
        _, M00, M01, M10, M11 = starts[bi]
        L, c = blocks[bi]
        w = s * np.sqrt(c); d = p - xs[bi]
        out[j] = M01 * np.cos(w * d) + (M11 / w) * np.sin(w * d)
    return out / np.sqrt(norm)


class Recon:
    def __init__(self, n, R, mode):
        self.n = n
        self.R = R
        self.mode = mode  # 'sup' or 'inf'
        self.start_val = 1.0 if mode == 'sup' else R
        self.alt_val = R if mode == 'sup' else 1.0
        self.nb = 2 * n + 1
        self.pat = [self.start_val if i % 2 == 0 else self.alt_val for i in range(self.nb)]

    def z_to_widths(self, z):
        """softmax parameterization: strictly feasible widths, sum = 1."""
        z = np.asarray(z, dtype=float)
        ez = np.exp(z - np.max(z))
        sm = ez / np.sum(ez)
        return (1.0 - self.nb * 1e-7) * sm + 1e-7

    def widths_to_z(self, widths):
        """inverse softmax (up to shift): z_i = log(width_i - 1e-7)."""
        w = np.asarray(widths, dtype=float)
        w = np.clip(w, 2e-7, 1.0 - 2e-7)
        w = w / np.sum(w)
        return np.log(w - 1e-7)

    def blocks_from_z(self, z):
        w = self.z_to_widths(z)
        return [(float(w[i]), self.pat[i]) for i in range(self.nb)]

    def f_at(self, z, pts):
        """f = lam_n u_n^2 - lam_{n+1} u_{n+1}^2 at pts (normalized)."""
        blocks = self.blocks_from_z(z)
        ss = roots_of(blocks, self.n + 1)
        lam_n = ss[self.n - 1] ** 2
        lam_np1 = ss[self.n] ** 2
        u_n = eigfun(blocks, ss[self.n - 1], pts)
        u_np1 = eigfun(blocks, ss[self.n], pts)
        return lam_n * u_n ** 2 - lam_np1 * u_np1 ** 2, lam_n, lam_np1

    def residual(self, z):
        z = np.asarray(z, dtype=float)
        w = self.z_to_widths(z)
        edges = np.cumsum(w)[:-1]  # 2n interior switch points
        f, lam_n, lam_np1 = self.f_at(z, edges)
        return f / lam_np1

    def full_report(self, z):
        z = np.asarray(z, dtype=float)
        w = self.z_to_widths(z)
        edges = np.cumsum(w)[:-1]
        mids = np.cumsum(w) - 0.5 * w  # block midpoints
        f_e, lam_n, lam_np1 = self.f_at(z, edges)
        f_m, _, _ = self.f_at(z, mids)
        D = lam_np1 - lam_n
        n = self.n
        asym = max(abs(edges[j] + edges[2 * n - 1 - j] - 1.0) for j in range(2 * n))
        # band matching (delta D = int delta-rho f dx, numerically verified):
        #   SUP: f>0 on rho=R blocks, f<0 on rho=1 blocks;
        #   INF: f>0 on rho=1 blocks, f<0 on rho=R blocks
        expect = []
        for i in range(self.nb):
            if self.mode == 'sup':
                expect.append(1.0 if self.pat[i] == self.R else -1.0)
            else:
                expect.append(1.0 if self.pat[i] == 1.0 else -1.0)
        expect = np.array(expect)
        band_min = float(np.min(np.abs(f_m) / lam_np1))
        band_ok = bool(np.all(np.sign(f_m) == expect) and band_min > 1e-6)
        return dict(edges=edges.tolist(), widths=w.tolist(), D=float(D),
                    lam_n=float(lam_n), lam_np1=float(lam_np1),
                    asym=float(asym), band_ok=band_ok,
                    band_min=band_min,
                    res_max=float(np.max(np.abs(f_e) / lam_np1)))


def uv_at(blocks, s, pts, left=True):
    """(u, u') at pts for the solution with u(0)=0, u'(0)=1 (left=True) or
    the solution with u(1)=0, u'(1)=-1 propagated backward (left=False)."""
    xs = [0.0]
    for L, _ in blocks:
        xs.append(xs[-1] + L)
    out = np.zeros((len(pts), 2))
    # propagate segment starts
    starts = []
    M = np.eye(2)
    starts.append((0.0, M.copy()))
    for L, c in blocks:
        w = s * np.sqrt(c)
        wL = w * L
        cw, sw = np.cos(wL), np.sin(wL)
        P = np.array([[cw, sw / w], [-w * sw, cw]])
        M = P @ M
        starts.append((xs[len(starts)], M.copy()))
    for j, p in enumerate(pts):
        bi = max(i for i in range(len(xs) - 1) if xs[i] < p)
        base_x, M0 = starts[bi]
        L, c = blocks[bi]
        w = s * np.sqrt(c)
        d = p - base_x
        cw, sw = np.cos(w * d), np.sin(w * d)
        if left:
            v0 = np.array([0.0, 1.0])
        else:
            # backward: u(1)=0, u'(1)=-1 ; propagate through blocks after bi
            v1 = np.array([0.0, -1.0])
            Mback = np.eye(2)
            for Lb, cb in blocks[bi + 1:]:
                wb = s * np.sqrt(cb)
                wLb = wb * Lb
                cbw, sbw = np.cos(wLb), np.sin(wLb)
                Pb = np.array([[cbw, sbw / wb], [-wb * sbw, cbw]])
                Mback = Pb @ Mback
            # state at block start x_bi solves Mback @ v_start = v1 (propagate to x=1)
            v_start = np.linalg.solve(Mback, v1)
        if left:
            # forward from 0: state at block start then within-block propagation
            v_at_start = M0 @ v0
            P = np.array([[cw, sw / w], [-w * sw, cw]])
            out[j] = P @ v_at_start
        else:
            # backward from 1: v_start = state at block RIGHT end xs[bi+1];
            # propagate back to p within block bi: P(-(xs[bi+1]-p))
            db = xs[bi + 1] - p
            cbw, sbw = np.cos(w * db), np.sin(w * db)
            Pb = np.array([[cbw, -sbw / w], [w * sbw, cbw]])  # P(-db)
            out[j] = Pb @ v_start
    return out


def green_kernel(blocks, mu, pts):
    """G_mu(x_i, x_j) via phi/psi/W formula; returns (npts x npts) matrix."""
    s = np.sqrt(mu)
    npts = len(pts)
    phi = uv_at(blocks, s, pts, left=True)          # (npts,2): phi, phi'
    psi = uv_at(blocks, s, pts, left=False)         # (npts,2): psi, psi'
    # Wronskian W = phi psi' - phi' psi (constant; evaluate at pts, take median)
    W = phi[:, 0] * psi[:, 1] - phi[:, 1] * psi[:, 0]
    Wv = np.median(W)
    # spectral Green kernel: G_mu(x,y) = -phi(x)psi(y)/W for x<=y
    # (normalization phi(0)=0, phi'(0)=1; psi(1)=0, psi'(1)=-1)
    G = np.zeros((npts, npts))
    for i in range(npts):
        for j in range(npts):
            if i <= j:
                G[i, j] = -phi[i, 0] * psi[j, 0] / Wv
            else:
                G[i, j] = -phi[j, 0] * psi[i, 0] / Wv
    return G


def eigen_data(rc, z):
    """lambda_n, lambda_{n+1}, u_n, u_{n+1}, u'_n, u'_{n+1} at switch points,
    eps_j, c, W(x_j)."""
    blocks = rc.blocks_from_z(z)
    ss = roots_of(blocks, rc.n + 1)
    lam_n, lam_np1 = ss[rc.n - 1] ** 2, ss[rc.n] ** 2
    w = rc.z_to_widths(z)
    edges = np.cumsum(w)[:-1]
    n = rc.n
    sn, snp1 = ss[rc.n - 1], ss[rc.n]
    # normalized eigenfunction values + derivatives at edges
    un = eigfun(blocks, sn, edges)
    unp = eigfun(blocks, snp1, edges)
    # derivatives: use uv_at with scaling.  eigfun normalizes by sqrt(int rho u^2).
    def derivs(s, edges_):
        # unnormalized solution (u0,u0') with u(0)=0,u'(0)=1
        vals = uv_at(blocks, s, edges_, left=True)
        # normalization: u = C * u0 ; C from eigfun value at first point
        u0 = vals[:, 0]
        # norm factor: eigfun already normalized; u0 unnormalized -> C = un/ u0
        C = np.mean(eigfun(blocks, s, edges_) / u0)
        return C * vals[:, 0], C * vals[:, 1]
    d_n, d_np = derivs(sn, edges), derivs(snp1, edges)
    u_n, up_n = d_n
    u_np1, up_np1 = d_np
    c = np.sqrt(lam_n / lam_np1)
    eps = np.sign(u_np1 / u_n)  # +1 left switches (odd j), -1 right (even j)
    W = up_np1 * u_n - u_np1 * up_n
    return dict(lam_n=lam_n, lam_np1=lam_np1, edges=edges, u_n=u_n, u_np1=u_np1,
                up_n=up_n, up_np1=up_np1, c=c, eps=eps, W=W)

# Unmodified functions from scripts/_gapn2_jacobian_spectral.py.
def gtilde_spectral(rc, z, lam, k, edges, N=2000):
    blocks = rc.blocks_from_z(z)
    ss = roots_of(blocks, N + 1)
    G = np.zeros((len(edges), len(edges)))
    for l in range(N + 1):
        if l == k:
            continue
        ul = eigfun(blocks, ss[l], edges)
        G += np.outer(ul, ul) / (ss[l] ** 2 - lam)
    return G


def analytic_jacobian_spectral(rc, z, N=2000):
    """Analytic Jacobian with spectral-sum regularized Green kernels."""
    ed = eigen_data(rc, z)
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    edges = ed['edges']
    u_n, u_np1 = ed['u_n'], ed['u_np1']
    up_n, up_np1 = ed['up_n'], ed['up_np1']
    n = rc.n
    pat = rc.pat
    s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
    D = lam_np1 - lam_n
    wj = lam_n * u_n ** 2
    fprime = 2.0 * lam_n * u_n * up_n - 2.0 * lam_np1 * u_np1 * up_np1
    Gn = gtilde_spectral(rc, z, lam_n, n - 1, edges, N=N)
    Gnp1 = gtilde_spectral(rc, z, lam_np1, n, edges, N=N)
    M = np.zeros((2 * n, 2 * n))
    for j in range(2 * n):
        for i in range(2 * n):
            term = (2.0 * wj[i] * wj[j] * D / (lam_n * lam_np1)
                    - 2.0 * lam_n ** 2 * u_n[i] * u_n[j] * Gn[i, j]
                    + 2.0 * lam_np1 ** 2 * u_np1[i] * u_np1[j] * Gnp1[i, j])
            M[j, i] = s[i] * term
    J = (np.diag(fprime) + M) / lam_np1
    return J
