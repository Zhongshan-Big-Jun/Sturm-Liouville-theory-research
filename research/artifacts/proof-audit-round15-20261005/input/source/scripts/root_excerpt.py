# Isolated current symmetric_root body, read in turn391. Not a complete source file.
import numpy as np

def symmetric_root(rc, z_seed, max_nfev=300, *, return_diagnostics=False):
    """solve the symmetric 2-param system: enforce x3=1-x2, x4=1-x1 by symmetry of widths."""
    from scipy.optimize import least_squares
    n = rc.n
    def res_sym(z):
        # project z onto symmetric widths: w_i = w_{nb-1-i}
        w = rc.z_to_widths(z)
        ws = 0.5 * (w + w[::-1])
        zs = rc.widths_to_z(ws)
        return rc.residual(zs)
    try:
        r = least_squares(res_sym, z_seed, xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=max_nfev)
        w = rc.z_to_widths(r.x)
        ws = 0.5 * (w + w[::-1])
        z = rc.widths_to_z(ws)
        Evidence = rc.stationarity_diagnostics(z, solver_success=r.success)
    except (ValueError, ArithmeticError) as Error:
        z = None
        Evidence = dict(accepted=False, status='unresolved', reason=str(Error),
                        evidence='float64 diagnostic, not interval certification')
    Result = z if Evidence['accepted'] else None
    return (Result, Evidence) if return_diagnostics else Result
