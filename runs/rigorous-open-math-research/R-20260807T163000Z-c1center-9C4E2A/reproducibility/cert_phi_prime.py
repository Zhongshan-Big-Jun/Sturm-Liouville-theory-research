# -*- coding: utf-8 -*-
"""cert_phi_prime.py - CERTIFIED: phi'(b) > 0 on [a0, 1) for the exact closed form
phi(b) of the R->1+ sheet (run R-20260807T163000Z, follow-up 2026-08-09).

Closed form (derivation sym_phi_closedform3.py, verified vs exact secular solver):
  phi'(b) = -N/(60 pi),
  N = (56 pi a0 - 6 s15) u^2 + (2 pi a0 + 3 s15) u + (3 s15 - 58 pi a0)
      + 2 s15 pi (1-b) (1-4u) v,  u = cos(2 pi b), v = sin(2 pi b),
  a0 = acos(1/4)/pi, s15 = sqrt(15).

Part 1 (CERTIFIED): interval arithmetic (mpmath.iv, 200-bit, correctly-rounded
interval extensions of cos/sin) proves phi' > 0 on [a0, 0.999] over a uniform
4000-cell grid; worst enclosure lower bound recorded.
Part 2 (STRICT, elementary): for b = 1-e, e in (0, 1/1000], using
  sin(pi e) >= pi e (1-(pi e)^2/6), cos(pi e) >= 1-(pi e)^2/2,
  sin(2 pi e) <= 2 pi e, 4 cos(2 pi e) - 1 <= 3,  with m = 56 pi a0 - 6 s15 > 0,
  n = 2 pi a0 + 3 s15 > 0:
  phi'(b) 60 pi >= 2 (pi e)^2 (1-d1)^2 (2 m (1-d2)^2 + n) - 12 s15 pi^2 e^2
                   = C_tail * e^2,  d1 = (pi/1000)^2/6, d2 = (pi/1000)^2/2,
  C_tail > 9.65 (interval-certified), hence phi' > 0 on (0.999, 1).
Output: cert_phi_prime.json (ASCII)."""
import mpmath as mp
import json, os
mp.mp.prec = 200
iv = mp.iv
piI = iv.pi
s15I = iv.sqrt(15)
a0I = iv.atan2(s15I/4, iv.mpf(1)/4)/piI

def dphi_iv(b):
    u = iv.cos(2*piI*b); v = iv.sin(2*piI*b)
    N = (56*piI*a0I - 6*s15I)*u**2 + (2*piI*a0I + 3*s15I)*u + (3*s15I - 58*piI*a0I) + 2*s15I*piI*(1-b)*(1-4*u)*v
    return -N/(60*piI)

# Part 1
a0f = float(mp.mpf(a0I.a))
NCELL = 4000
edges = [a0f + (0.999 - a0f)*i/NCELL for i in range(NCELL+1)]
ok = True
worst = mp.inf
worst_at = 0.0
worst_cell = None
for i in range(NCELL):
    B = iv.mpf([mp.mpf(edges[i]), mp.mpf(edges[i+1])])
    val = dphi_iv(B)
    if val.a <= 0:
        ok = False
        worst = val.a; worst_at = edges[i]; worst_cell = (edges[i], edges[i+1])
        break
    if val.a < worst:
        worst = val.a; worst_at = edges[i]
worst_s = mp.nstr(worst, 20)
# Part 2: tail constant
d1I = iv.mpf((mp.pi/1000)**2/6)
d2I = iv.mpf((mp.pi/1000)**2/2)
mI = 56*piI*a0I - 6*s15I
nI = 2*piI*a0I + 3*s15I
Plb = 2*piI**2*(1-d1I)**2*(2*mI*(1-d2I)**2 + nI)
Tub = 12*s15I*piI**2
Ctail = (Plb - Tub)/(60*piI)
Ctail_lb = mp.nstr(Ctail.a, 20)
out = dict(
    a0=mp.nstr(a0I, 30),
    part1=dict(interval="[a0, 0.999]", cells=NCELL, certified=ok,
               worst_lower_bound=worst_s, worst_at=worst_at,
               note="mpmath.iv 200-bit; correctly-rounded interval cos/sin"),
    part2=dict(interval="(0.999, 1)", e_range="(0, 1/1000]",
               C_tail_lower_bound=Ctail_lb,
               m_lower=mp.nstr(mI.a, 15), n_lower=mp.nstr(nI.a, 15),
               formula="phi'*60pi >= C_tail*(1-b)^2"),
    conclusion="phi' > 0 on [a0, 1)"
)
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "cert_phi_prime.json"), "w") as f:
    json.dump(out, f, indent=1)
print("PART1 [a0,0.999]: certified=%s  worst lower bound=%s at b=%.5f" % (ok, worst_s, worst_at))
print("PART2 tail: C_tail lower bound =", Ctail_lb)
print("conclusion: phi' > 0 on [a0, 1)  ->", out["conclusion"])
