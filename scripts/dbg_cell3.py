# -*- coding: utf-8 -*-
import numpy as np
def rho_at(rhos, xs, t):
    j = 0
    while j < len(xs) and t > xs[j]: j += 1
    return rhos[j]
def build_phi_n(rhos0, xs0, n):
    cell = 1.0/n
    xs_n = []; rhos_n = []
    for j in range(n):
        xa_c = -0.5 + j*cell
        brk = []
        for x0 in xs0:
            if -0.5 < x0 < 0.5:
                brk.append(xa_c + (x0+0.5)/n)
        brk = sorted(brk)
        pts = [xa_c] + brk + [xa_c+cell]
        for i in range(len(pts)-1):
            midx = 0.5*(pts[i]+pts[i+1])
            t = n*(midx - xa_c) - 0.5
            r = rho_at(rhos0, xs0, t)
            if pts[i] > xa_c+1e-12:
                xs_n.append(pts[i])
            rhos_n.append(r)
    return xs_n, rhos_n

# simple test
xs0 = [0.0]; rhos0 = [1.0, 2.0]
print(build_phi_n(rhos0, xs0, 2))
# random test: verify phi_n(x) == phi_0(n(x+1/2)-1/2 mod period) at many points
rng = np.random.default_rng(7)
for trial in range(5):
    ncell = int(rng.integers(2, 5))
    xs0 = np.sort(rng.uniform(-0.4, 0.4, ncell))
    rhos0 = rng.uniform(1.0, 4.0, ncell+1)
    for n in (2,3):
        xs_n, rhos_n = build_phi_n(rhos0, xs0, n)
        # verify at sample points
        err = 0.0
        for x in np.linspace(-0.5, 0.5, 2001):
            # phi_n(x): cell j = floor((x+0.5)*n)
            j = int(np.floor((x+0.5)*n))
            if j >= n: j = n-1
            xa_c = -0.5 + j/n
            t = n*(x - xa_c) - 0.5
            rn = rho_at(rhos0, xs0, t)
            r0 = rho_at(rhos0, xs0, x)
            # phi_n should equal phi_0 at the cell-mapped argument, NOT at x
            # verify via build: find rho_n(x)
            rn2 = rho_at(rhos_n, xs_n, x)
            err = max(err, abs(rn - rn2))
        print(f"trial{trial} n={n}: max build error vs formula = {err:.2e}")
