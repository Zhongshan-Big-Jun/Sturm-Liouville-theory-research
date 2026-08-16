import sys, numpy as np
sys.path.insert(0,'scripts')
from _gapn2_symmetry_recon import Recon, roots_of
from scipy.optimize import least_squares

def half_eigs(blocks):
    ss=roots_of(blocks, 10)
    lam=ss**2
    # blocks list (height,width) on full [0,1], but for half want eigenfunctions half.
    # Instead build full symmetric density from half? easier use full and select symmetric modes.
    return lam

# Use full Recon n=2 sup with 5 blocks symmetric. Half widths = w1,w2,(w3/2)
def evals_half(a,b,R=4,L=0.5):
    w1=a; w2=b-a; w3=L-b
    # half density p; eigenvalues on [0,L].
    # transfer matrix secular roots by shooting scanning s, Dirichlet and Neumann.
    heights=[1,R,1]; widths=[w1,w2,w3]
    # generic roots_of expects blocks full [0,1]; scale coordinates to L using squares scaled? For interval length L, eigenvalues = (pi? no). Use generic shooting custom.
    return muD1, muN2

# Use existing Recon for full interval with blocks list; to get half on [0,L], use blocks heights and widths, scale to unit by x'=x/L. Eigenvalue of -u''=mu p u on [0,L] = lam/L^2 for unit problem.
def shoot_roots(heights,widths,L=0.5,N=6):
    # roots of unit problem with given widths sum 1; eigenvalues lam; mu=lam/L^2
    ss=roots_of([(h,w) for h,w in zip(heights,widths)], N+1)
    return ss**2/L**2
# boundary conditions via transfer matrix? roots_of returns Dirichlet roots for unit problem likely. For Neumann use derivative.
# inspect roots_of
print(roots_of.__doc__)
