# verify_o1_audit2.py - supplementary checks (EVIDENCE ONLY)
# - O1f bang-bang direction: increasing rho on {f>0} increases D, decreasing on {f<0} increases D
# - boundary cases: rho constant (1 and R), 2-block configs, a=b configs
# - O1c structure on 5-block (4-jump) configs
import sys, math, json
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o1audit-422A69\reproducibility')
import numpy as np
from verify_o1_audit import eigpair, D_of, eigenfunction, f_at_jump, check_O1c, sec_vec
R = 4.0
out = {}

# ---- O1f: bang-bang direction
# config: symmetric barrier at u=0.4 ; {f>0} should contain (0.4,0.6)-ish
blocks = [(0.4, 1.0), (0.2, R), (0.4, 1.0)]
D0, l1, l2 = D_of(blocks, R)
ev1, _ = eigenfunction(blocks, l1)
ev2, _ = eigenfunction(blocks, l2)
# locate a point xp where f>0 and xm where f<0
xs = np.linspace(0.001, 0.999, 4001)
f = np.array([l1*ev1(x)[0]**2 - l2*ev2(x)[0]**2 for x in xs])
xp = float(xs[np.argmax(f)])
xm = float(xs[np.argmin(f)])
print('xp (f>0 max)', xp, ' f(xp) =', f[np.argmax(f)], ' xm (f<0 min)', xm, ' f(xm) =', f[np.argmin(f)])
def perturb(x0, delta, w=0.01):
    # increase rho by delta on (x0, x0+w) (density there was 1 or R)
    Ls = [x0, w, 1 - x0 - w]
    Cs = [1.0, 1.0 + delta, 1.0]
    return [(Ls[0], Cs[0]), (Ls[1], Cs[1]), (Ls[2], Cs[2])]
res = {}
for label, x0 in [('increase_on_fpos', xp), ('increase_on_fneg', xm)]:
    dD = []
    for delta in [0.05, 0.1, 0.5]:
        Dp, _, _ = D_of(perturb(x0, delta), R)
        dD.append((Dp - D0) / delta)
    res[label] = dict(x0=x0, dD_per_delta=dD)
out['O1f_bangbang_direction'] = res

# ---- boundary cases
bc = {}
D_const1, l1, l2 = D_of([(1.0, 1.0)], R)
D_constR, _, _ = D_of([(1.0, R)], R)
bc['const_1'] = dict(D=D_const1, expect=3*math.pi**2, match=bool(abs(D_const1-3*math.pi**2)<1e-8))
bc['const_R'] = dict(D=D_constR, expect=3*math.pi**2/R, match=bool(abs(D_constR-3*math.pi**2/R)<1e-8))
# 2-block configs: [1,R] (a=0) and [R,1] (b=1) and [1,R,1] with a=b
for name, blk in [('two_block_1R', [(0.5,1.0),(0.5,R)]),
                  ('two_block_R1', [(0.5,R),(0.5,1.0)]),
                  ('degenerate_a_eq_b', [(0.3,1.0),(0.0,R),(0.7,1.0)])]:
    Dv, l1v, l2v = D_of(blk, R)
    bc[name] = dict(D=Dv, l1=l1v, l2=l2v)
out['boundary_cases'] = bc

# ---- O1c structure on 5-block (4-jump) configs
rng = np.random.default_rng(4242)
o1c5 = []
for trial in range(4):
    m = 4
    cuts = np.sort(rng.uniform(0.02, 0.98, m))
    Ls = np.diff(np.concatenate([[0], cuts, [1]]))
    Cs = rng.choice([1.0, R], size=m+1, replace=True)
    blk = [(float(Ls[i]), float(Cs[i])) for i in range(m+1)]
    o1c5.append(check_O1c(blk, R))
out['O1c_5block'] = o1c5

print(json.dumps(out, indent=1))
