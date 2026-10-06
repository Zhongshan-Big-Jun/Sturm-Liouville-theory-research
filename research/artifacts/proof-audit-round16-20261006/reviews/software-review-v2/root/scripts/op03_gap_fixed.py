# -*- coding: utf-8 -*-
"""FIXED: correct propagation order M_new = P(block) * M_old.
Solves y'' + s^2 rho y = 0 with (y,y') propagator P(d)=[[cos wd, sin wd / w],[-w sin wd, cos wd]].
"""
import numpy as np

def lams_precise(blocks, k, tol=1e-15, smax_scale=5.0):
	"""Return the first k DD frequencies omega; eigenvalues are omega**2.

	The legacy name is retained for callers.  ``tol`` requests a bracket
	width at most tol * max(1, omega); unresolved binary64 requests raise
	ArithmeticError.  Indexed phase guards still apply for loose requests.
	``smax_scale`` is deprecated: the shared indexed engine uses comparison
	bounds instead of a scanning range.  Positive nondefault values warn.
	This is a floating point diagnostic, not an interval certificate.
	"""
	import math
	import warnings
	import _sl_prufer as SpectralBackend

	for Value, Name in ((tol, 'tol'), (smax_scale, 'smax_scale')):
		if (isinstance(Value, (bool, np.bool_, complex, np.complexfloating))
			or not isinstance(Value, (int, float, np.integer, np.floating))
			or not math.isfinite(float(Value)) or float(Value) <= 0):
			raise ValueError(Name + ' must be a finite positive real number')
	if float(smax_scale) != 5.0:
		warnings.warn('smax_scale is deprecated; DD frequencies use indexed phase bounds',
			DeprecationWarning, stacklevel=2)
	Values = SpectralBackend.positive_blocks(blocks)
	Densities = Values[:, 1]
	ContrastBits = 0.5 * (math.log2(float(np.max(Densities)))
		- math.log2(float(np.min(Densities))))
	Refine = max(60, math.ceil(math.log2(1.125) + ContrastBits
		- math.log2(float(tol))) + 4)
	Frequencies, Records = SpectralBackend.indexed_roots(Values, k,
		Refine=Refine, RightBoundary='D')
	Widths = np.array([Record['bracket'][1] - Record['bracket'][0] for Record in Records])
	Requested = float(tol) * np.maximum(1.0, Frequencies)
	if np.any(Widths > Requested):
		raise ArithmeticError('requested tol is unresolved in binary64; use higher precision')
	return Frequencies

def prop_to(blocks, s):
    """returns list of (x_start, M00,M01,M10,M11) at each block start (correct order)."""
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    starts = []
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    starts.append((xs[0], M00, M01, M10, M11))
    for bi, (L, c) in enumerate(blocks):
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
        starts.append((xs[bi+1], M00, M01, M10, M11))
    return starts

def eigfuns_precise(blocks, s_vals, x_pts):
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    out = np.zeros((len(s_vals), len(x_pts)))
    for ei, s in enumerate(s_vals):
        starts = prop_to(blocks, s)
        # exact normalization: sum over blocks rho * int (A cos + B sin)^2
        norm = 0.0
        for bi, (L, c) in enumerate(blocks):
            x0, M00, M01, M10, M11 = starts[bi]
            w = s*np.sqrt(c)
            A = M01; B = M11/w
            Icos = 0.5*(L + np.sin(2*w*L)/(2*w))
            Isin = 0.5*(L - np.sin(2*w*L)/(2*w))
            Icross = np.sin(w*L)**2/(2*w)
            norm += c*(A*A*Icos + B*B*Isin + 2*A*B*Icross)
        for j, p in enumerate(x_pts):
            bi = max(i for i in range(len(xs)-1) if xs[i] <= p)
            x0, M00, M01, M10, M11 = starts[bi]
            L, c = blocks[bi]
            w = s*np.sqrt(c); d = p - x0
            cw = np.cos(w*d); sw = np.sin(w*d)/w; sw2 = -w*np.sin(w*d)
            n00, n01, n10, n11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
            out[ei, j] = n01
        out[ei] /= np.sqrt(norm)
    return out

if __name__ == "__main__":
    # verify against IVP
    import numpy as np
    from scipy.integrate import solve_ivp
    R = 4.0; u = 0.30; v0 = 1-2*u
    blocks = [(u,1.0),(v0,R),(u,1.0)]
    def rho_v(x):
        x = np.asarray(x, dtype=float)
        return np.where(x < u, 1.0, np.where(x < 1-u, R, 1.0))
    lam = lams_precise(blocks, 3)**2
    print("lam:", lam)
    s = np.sqrt(lam[0])
    sol = solve_ivp(lambda t,y: [y[1], -s*s*rho_v(t)*y[0]], [0,1], [0.0,1.0],
                    rtol=1e-13, atol=1e-15, dense_output=True, max_step=1e-4)
    xs = np.linspace(0,1,2000001)
    ys = sol.sol(xs)
    I2 = np.trapezoid(ys[1]**2, xs); I0 = np.trapezoid(rho_v(xs)*ys[0]**2, xs)
    print("IVP identity ratio:", I2/(s*s*I0))
    vp = eigfuns_precise(blocks, np.array([s]), np.array([0.1,0.3,0.5,0.7,0.9]))
    raw = np.array([ys[0][int(x*2e6-1)] for x in (0.1,0.3,0.5,0.7,0.9)])  # approx
    # compare normalized: u_true = raw_y/sqrt(I0)
    raw_at = np.array([sol.sol([x])[0][0] for x in (0.1,0.3,0.5,0.7,0.9)])
    u_true = raw_at/np.sqrt(I0)
    print("normalized eigenfunction compare (fixed TM vs IVP):")
    print("  TM :", vp[0])
    print("  IVP:", u_true)
