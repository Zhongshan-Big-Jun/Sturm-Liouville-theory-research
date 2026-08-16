# wdensity_check.py
# Test whether W_r = K_c^r(Pi ∩ D(K_c^r)) [degrees {0,1} U {>=2r+2}] is dense in L^2.
# Equivalently whether Pi ∩ D(K_c^r) is dense in D(K_c^r) (transfer isometry).
# We test the moment problem: is there nonzero f in L^2 with (f, x^k)=0 for
# k in {0,1} U {6,7,...,N} (missing degrees 2..5 for r=2)?
# Use exact/numerical linear algebra on the monomial Gram matrix restricted.

import numpy as np

# Legendre-ish check: approximate f by a polynomial g (degree 2..5 for r=2)
# and require its moments vanish at k in {0,1,6,7,...}.  We look for a linear
# combination of high-ish monomials in the span that is L^2-near but with the
# constrained moments.  More directly: compute projection of x^2 onto
# span{x^k : k in{0,1,6,7,...}} vs the full span - if the residual is nonzero
# and bounded away from 0, then x^2 (hence degree 2) is NOT in the closure.

def moment(i, j):
    # (x^i, x^j)_{L2} on [-1,1] = 2/(i+j+1) if i+j even else 0
    s = i + j
    if s % 2 == 0:
        return 2.0 / (s + 1)
    return 0.0

def gram(inds):
    n = len(inds)
    G = np.zeros((n, n))
    for a, i in enumerate(inds):
        for b, j in enumerate(inds):
            G[a, b] = moment(i, j)
    return G

# W_r degrees for r=2: {0,1,6,7,8,...} up to 16
inds_r2 = [0, 1] + list(range(6, 17))
G = gram(inds_r2)
# test vector: x^2 in L^2, its Gram products with the W basis functions
b = np.array([moment(2, i) for i in inds_r2])
# least squares: coeffs c minimizing ||G c - b||; if b in range(G), x^2 approx in span
c_hat, res, rank, sv = np.linalg.lstsq(G, b, rcond=None)
print('r=2: rank of Gram(W_r)=%d (dim W_r basis=%d)' % (rank, len(inds_r2)))
print('r=2: best residual ||Gc - b|| = %.3e  (nonzero => x^2 not in closure of W_r)' % np.linalg.norm(G @ c_hat - b))
# orthogonal complement: find null vector of G
eigval, eigvec = np.linalg.eigh(G)
print('r=2: min eigenvalue of Gram = %.3e' % eigval[0])

# r=3: degrees {0,1,8,9,...}
inds_r3 = [0, 1] + list(range(8, 17))
G3 = gram(inds_r3)
b3 = np.array([moment(2, i) for i in inds_r3])
c3, res3, rank3, sv3 = np.linalg.lstsq(G3, b3, rcond=None)
print()
print('r=3: rank=%d (dim=%d)' % (rank3, len(inds_r3)))
print('r=3: residual for x^2 = %.3e' % np.linalg.norm(G3 @ c3 - b3))
eig3, _ = np.linalg.eigh(G3)
print('r=3: min eigenvalue = %.3e' % eig3[0])
