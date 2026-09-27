# -*- coding: utf-8 -*-
"""Verify the analytic Jacobian structure of the band self-consistency system.

Round13: all three Jacobian entrypoints use the general quotient derivative.
The stationary identities below are preserved at F=0. Finite Green sums are
numerical evidence, not certified tail bounds.

Claims (all to be verified numerically, EVIDENCE):
  (A1) At a band-consistent point x (F_j = f(x_j)/lambda_{n+1} = 0):
       J = D_xF = (D~ + M~)/lambda_{n+1},  D~ = diag(f'(x_j)),
       M~_{ji} = s_i * { +2 w_i w_j D/(lambda_n lambda_{n+1})
                         - 2 lambda_n^2 u_n(x_i) u_n(x_j) G~_n(x_i,x_j)
                         + 2 lambda_{n+1}^2 u_{n+1}(x_i) u_{n+1}(x_j) G~_{n+1}(x_i,x_j) },
       w_j = lambda_n u_n(x_j)^2 = lambda_{n+1} u_{n+1}(x_j)^2,
       s_i = rho_{i+1} - rho_i = +-(R-1) (alternating),
       G~_k(x,y) = regularized resolvent kernel at lambda_k (pole removed),
       derived from first-order perturbation theory of the weighted string.
  Derivation (signs CORRECTED 2026-08-12, all verified against clean FD at
  non-critical AND critical points; replaces the earlier flipped-convention draft):
  moving switch i RIGHT by dx_i converts pat[i+1] -> pat[i] on [x_i, x_i+dx_i), so
  delta rho = (pat[i] - pat[i+1]) delta(x-x_i) dx_i = -s_i delta(x-x_i) dx_i.
  First-order perturbation (L^2(rho) normalization, A = -(1/rho) d^2/dx^2,
  delta A = (delta rho/rho^2) d^2/dx^2, weighted inner product <f,g> = int rho f g):
    delta lambda_k/dx_i = +lambda_k s_i u_k(x_i)^2,
    delta u_k(x)/dx_i = +(s_i u_k(x_i)^2/2) u_k(x) - lambda_k s_i u_k(x_i) G~_k(x,x_i),
  G~_k(x,y) = sum_{l != k} u_l(x) u_l(y)/(lambda_l - lambda_k).
  Combining the two modes at a band-consistent point (w_i = lambda_n u_n(x_i)^2
  = lambda_{n+1} u_{n+1}(x_i)^2, u_{n+1}^2 - u_n^2 = w D/(lambda_n lambda_{n+1})*sign,
  w = lambda_n u_n^2) gives
  M~_{ji} = s_i * { +2 w_i w_j D/(lambda_n lambda_{n+1})
                         - 2 lambda_n^2 u_n(x_i) u_n(x_j) G~_n(x_i,x_j)
                         + 2 lambda_{n+1}^2 u_{n+1}(x_i) u_{n+1}(x_j) G~_{n+1}(x_i,x_j) }.
  (A2) f'(x_j) = -2 lambda_{n+1} eps_j c W(x_j),  eps_j = u_{n+1}(x_j)/u_n(x_j)/c,
       c = sqrt(lambda_n/lambda_{n+1}), W = u_{n+1}' u_n - u_{n+1} u_n' < 0.
  (A3) Hess(D_n) restricted to the family = -diag(s_i) * lambda_{n+1} * J at any
       critical point F=0 (historically verified 2026-08-12 vs FD Hessian, h=1e-4, err 4.6e-3 on
       entries O(1e3); dD/dx_i = -s_i f(x_i) also verified at non-critical points).
       Hence with K := diag(1/s) J (symmetric, since all |s_i| = R-1):
       Hess = -lambda_{n+1} (R-1)^2 K, det J = prod(s_i) det K, prod(s_i) = (R-1)^(2n) (-1)^n,
       so (G1') [sgn det J = (-1)^n] <=> det K > 0 at every critical point.

Usage: python _gapn2_jacobian_analytic.py [n] [Rs] [mode]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import (Recon, roots_of, eigfun, eigenfunction_states,
	solution_states, real_green_matrix, _real_parameter, _transfer_matrix, positive_blocks)
from _gapn2_jacobian_probe import jac_fd, sym_antisym_decomp, symmetric_root


def prop_matrix(blocks, s):
	"""Physical transfer for frequency s, including the linear limit s=0."""
	Frequency = _real_parameter(s, 'frequency')
	Blocks = positive_blocks(blocks)
	M = np.eye(2)
	with np.errstate(over='raise', invalid='raise', divide='raise', under='ignore'):
		Mu = np.float64(Frequency)**2
		for Length, Density in Blocks:
			M = _transfer_matrix(Mu, Length, Density) @ M
	if not np.all(np.isfinite(M)):
		raise ArithmeticError('transfer matrix is not finite')
	return M


def uv_at(blocks, s, pts, left=True):
	"""Physical states at arbitrary points, with endpoint data (0,1)/(0,-1).

	The compatibility parameter s is frequency; use solution_states for a
	real spectral parameter mu (including mu<0).
	"""
	Frequency = _real_parameter(s, 'frequency')
	with np.errstate(over='raise', invalid='raise'):
		Mu = np.float64(Frequency)**2
	return solution_states(blocks, Mu, pts, right_boundary=None if left else 'D')


def green_kernel(blocks, mu, pts):
	"""DD Green matrix for real resolvent mu, in the supplied coordinate order."""
	return real_green_matrix(blocks, mu, pts)


def regularized_green(blocks, lam, pts, u_k=None, delta=1e-9):
    """G~_k(x,y) = lim_{mu->lam_k} [G_mu(x,y) - u_k(x)u_k(y)/(lam_k-mu)].

    The spectral residue u_k(x)u_k(y) is mu-independent (u_k = normalized
    eigenfunction at lambda_k), so the direct subtraction converges with error
    O(delta); delta relative to lam, e.g. 1e-9 gives ~1e-12 accuracy on the
    smooth part (G_mu ~ 1/delta -> cancellation error ~ 1e-16/delta*lam ~ 1e-6
    relative to the pole, i.e. ~1e-12 absolute for values O(0.01)).

    WARNING (2026-08-12 audit): the claimed accuracy is FALSE at delta=1e-9 in
    practice.  G_mu ~ 4.7e7 near the pole; transfer-matrix relative error
    ~2.7e-8 leaves an absolute error ~1.27 in G~ (verified against the spectral
    sum).  Do NOT use this routine for Jacobian work; use gtilde_spectral from
    _gapn2_jacobian_spectral (finite spectral sum; no certified tail bound).  Kept only for
    green-kernel cross-checks at low accuracy."""
    mu = lam * (1.0 - delta)
    G = green_kernel(blocks, mu, pts)
    if u_k is None:
        # caller must pass the normalized eigenfunction values at pts
        raise ValueError('u_k (normalized eigenfunction values at pts) required')
    return G - np.outer(u_k, u_k) / (lam - mu)


def eigen_data(rc, z):
	"""Adjacent eigenvalues and mass-normalized physical states at switches.

	eps is sign(u_n)*sign(u_{n+1}); its band sign interpretation and the
	Wronskian f' identity require stationarity and nonzero interface values.
	"""
	Blocks = rc.blocks_from_z(z)
	Frequencies = roots_of(Blocks, rc.n + 1)
	A, B = Frequencies[rc.n - 1]**2, Frequencies[rc.n]**2
	Edges = np.cumsum(rc.z_to_widths(z))[:-1]
	U = eigenfunction_states(Blocks, Frequencies[rc.n - 1], Edges)
	V = eigenfunction_states(Blocks, Frequencies[rc.n], Edges)
	return dict(lam_n=A, lam_np1=B, edges=Edges, u_n=U[:, 0], u_np1=V[:, 0],
		up_n=U[:, 1], up_np1=V[:, 1], c=np.sqrt(A / B),
		eps=np.sign(U[:, 0]) * np.sign(V[:, 0]), W=V[:, 1] * U[:, 0] - V[:, 0] * U[:, 1])


def jacobian_terms(Data, Jumps, Gn, Gnp1):
	"""Unscaled terms of d(f/b)/dx at any feasible configuration.

	A=lambda_n, B=lambda_{n+1}, f=A*u^2-B*v^2. Moving switch i gives
	d_i B=B*s_i*v_i^2, so the quotient contributes -s_i*f_j*v_i^2.
	M1 includes that term. At f=0 it reduces to the stationary rank-one
	term 2*s_i*w_i*w_j*(B-A)/(A*B). Green sums remain finite evidence.
	"""
	A, B = Data['lam_n'], Data['lam_np1']
	U, V = Data['u_n'], Data['u_np1']
	F = A * U**2 - B * V**2
	M1 = (2*A*np.outer(U**2, U**2) - 2*B*np.outer(V**2, V**2) - np.outer(F, V**2)) * Jumps[None, :]
	M2 = -2*A**2 * np.outer(U, U) * Gn * Jumps[None, :]
	M3 = 2*B**2 * np.outer(V, V) * Gnp1 * Jumps[None, :]
	Fprime = 2*A*U*Data['up_n'] - 2*B*V*Data['up_np1']
	Stationary = 2*A*(B-A)/B * np.outer(U**2, U**2) * Jumps[None, :]
	return dict(fprime=Fprime, M1=M1, M2=M2, M3=M3, s=Jumps, wj=A*U**2, D=B-A,
		M1_stationary=Stationary, correction=M1-Stationary, eigen_data=Data)


def term_breakdown(rc, z, N=2000):
	"""General Jacobian terms; J=(diag(fprime)+M1+M2+M3)/lambda_{n+1}.

	M1 is the full normalization/quotient term. M1_stationary and correction
	separate its old stationary specialization from the nonstationary part.
	"""
	Data = eigen_data(rc, z)
	from _gapn2_jacobian_spectral import gtilde_spectral
	Gn = gtilde_spectral(rc, z, Data['lam_n'], rc.n - 1, Data['edges'], N=N)
	Gnp1 = gtilde_spectral(rc, z, Data['lam_np1'], rc.n, Data['edges'], N=N)
	return jacobian_terms(Data, np.diff(rc.pat), Gn, Gnp1)


def analytic_jacobian(rc, z, N=2000):
	"""General physical-interface Jacobian with finite spectral Green sums.

	The returned fprime_id is a stationary Wronskian diagnostic only; it is
	not used to assemble J. N controls the numerical spectral truncation.
	"""
	Terms = term_breakdown(rc, z, N=N)
	Data = Terms['eigen_data']
	B = Data['lam_np1']
	J = (np.diag(Terms['fprime']) + Terms['M1'] + Terms['M2'] + Terms['M3']) / B
	FprimeId = -2*B*Data['eps']*Data['c']*Data['W']
	return J, Terms['fprime'], FprimeId, Terms['wj'], B*Data['u_np1']**2


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    Rs = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1.05, 2.0, 4.0, 10.0]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'both'
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    for m in (['sup', 'inf'] if mode == 'both' else [mode]):
        rc0 = Recon(n, R=4.0, mode=m)
        key = f"n{n}_{m.upper()}"
        e0 = np.array(tab[key]['edges'])
        w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
        z0 = rc0.widths_to_z(w0)
        prev = None
        print(f"=== n={n} mode={m} ===")
        for R in Rs:
            rcR = Recon(n, R, m)
            z = z0 if prev is None else prev
            zs = symmetric_root(rcR, z)
            if zs is None:
                print(f"R={R}: no symmetric root found (residual too large)"); continue
            prev = zs
            Jfd = jac_fd(rcR, zs)
            J, fprime, fprime_id, wj, wj2 = analytic_jacobian(rcR, zs)
            err = np.max(np.abs(J - Jfd))
            rel = err / np.max(np.abs(Jfd))
            # residual check: f ~ 0 at switches
            res = np.max(np.abs(rcR.residual(zs)))
            # w consistency
            wrel = np.max(np.abs(wj - wj2) / np.max(np.abs(wj)))
            # f' identity
            fprime_rel = np.max(np.abs(fprime - fprime_id)) / np.max(np.abs(fprime))
            # Stationary F=0 only: Hess = -lambda_{n+1} * diag(s) @ J.
            pat = rcR.pat
            s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
            lam_np1 = eigen_data(rcR, zs)['lam_np1']
            H = (-lam_np1 * np.diag(s)) @ Jfd
            ev = np.linalg.eigvalsh(H)
            print(f"R={R:8.4g} |Jfd|max={np.max(np.abs(Jfd)):10.3e} "
                  f"err={err:10.3e} rel={rel:10.3e} res={res:10.3e} "
                  f"wrel={wrel:10.3e} fprimrel={fprime_rel:10.3e}")
            print(f"         Hess eig (SUP=neg def?, INF=pos def?): {np.round(ev, 4)}")


if __name__ == '__main__':
    main()
