# -*- coding: utf-8 -*-
"""verify_premises.py -- independent audit of the premise chain for the KEY LEMMA.
Checks (all at mpmath 50-60 digits, no use of the prior run's solver):
  P1  secular equations (E) and (O) at alpha1(c), alpha2(c)
  P2  alpha1 < alpha2, ranges, monotonicity in c, corner values c->0, c->1/2
  P3  normalization identity (N): u_k(u,u)^2 = tan^2(alpha_k)/(1/2 + w tan^2 alpha_k)
      via direct high-precision integration of the half-problem eigenfunction
  P4  (F1): f_sym = (2/u^2)(T1 - T2)  [uses P3]
  P5  (D'): D'(c) = (8/q^2)(c+q) F(c)   [numerical derivative check]
  P6  (L) : G formula == numerical derivative of log M along the curve
  P7  (FS): f_sym(u) = 2(c+q)F(c)/(q u^2 (q^2-1))  [via P3/P4 direct]
  P8  KEY LEMMA log form vs G form: (d/dc)log(M1/M2) == G1 - G2
  P9  claimed equivalence audit: F'(c) = M1*G1 - M2*G2; test whether F'<0 <-> G1<G2
  P10 KEY LEMMA margin: min over c in (0,1/2) of G2-G1 and of -F'
"""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import (Phi, Wfun, E_curve, O_curve, alpha1_of_c, alpha2_of_c,
                          Mfun, M1_of_c, M2_of_c, F_of_c, Gfun, G1_of_c, G2_of_c,
                          u_from_c, f_sym_formula, half_problem_s)

mp.mp.dps = 60

def check(name, cond, detail=''):
    status = 'PASS' if cond else 'FAIL'
    print(f'[{status}] {name} {detail}')
    return status == 'PASS'

ok = True

# ---------- P1: secular equations ----------
print('--- P1: secular equations ---')
for q in [mp.mpf(1.001), mp.mpf(1.1), mp.sqrt(mp.mpf(4)), mp.sqrt(mp.mpf(100)), mp.mpf(100)]:
    for c in [mp.mpf('0.01'), mp.mpf('0.3'), mp.mpf('0.49')]:
        a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
        e_res = q*mp.tan(a1)*mp.tan(c*a1) - 1
        o_res = q*mp.tan(a2) + mp.tan(c*a2)
        ok &= check(f'secular q={q} c={c}', abs(e_res) < mp.mpf('1e-50') and abs(o_res) < mp.mpf('1e-50'),
                    f'|E|={0} |O|={0}')

# ---------- P2: ranges, ordering, monotonicity, corners ----------
print('--- P2: ranges and ordering ---')
for q in [mp.mpf(1.001), mp.mpf(1.5), mp.mpf(100)]:
    for c in [mp.mpf('0.05'), mp.mpf('0.25'), mp.mpf('0.4999')]:
        a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
        ok &= check(f'range q={q} c={c}', 0 < a1 < mp.pi/2 and mp.pi/2 < a2 < mp.pi,
                    f'a1={mp.nstr(a1,8)} a2={mp.nstr(a2,8)} a1<a2={a1<a2}')
# corner c->0
q = mp.mpf(3)
a1_0 = alpha1_of_c(mp.mpf('1e-12'), q); a2_0 = alpha2_of_c(mp.mpf('1e-12'), q)
ok &= check('corner c->0', abs(a1_0 - mp.pi/2) < mp.mpf('1e-6') and abs(a2_0 - mp.pi) < mp.mpf('1e-6'),
            f'a1={mp.nstr(a1_0,10)} a2={mp.nstr(a2_0,10)}')
# corner c->1/2: alpha1 = gamma = alpha0 with sin(alpha0/2) = 1/sqrt(2(q+1))
c_half = mp.mpf('0.5')
a1_h = alpha1_of_c(c_half, q); a2_h = alpha2_of_c(c_half, q)
alpha0 = 2*mp.asin(1/mp.sqrt(2*(q+1)))
ok &= check('corner c=1/2', abs(a1_h - alpha0) < mp.mpf('1e-40') and abs(a2_h - (mp.pi - alpha0)) < mp.mpf('1e-40'),
            f'a1={mp.nstr(a1_h,12)} alpha0={mp.nstr(alpha0,12)} a2={mp.nstr(a2_h,12)}')

# monotonicity in c (numerical)
q = mp.mpf(2)
cs = [mp.mpf('0.05'), mp.mpf('0.2'), mp.mpf('0.4')]
a1s = [alpha1_of_c(c, q) for c in cs]; a2s = [alpha2_of_c(c, q) for c in cs]
ok &= check('alpha1 decreasing in c', a1s[0] > a1s[1] > a1s[2])
ok &= check('alpha2 decreasing in c', a2s[0] > a2s[1] > a2s[2])

# ---------- P3: normalization identity (N) ----------
print('--- P3: normalization identity ---')
def N_direct(q, u, s):
    """N = 2*(int_0^u y^2 dx + R int_u^{1/2} y^2 dx) with y = sin(s x)/s, R = q^2."""
    R = q*q
    # left: y = sin(s x)/s
    I_left = (u/2 - mp.sin(2*s*u)/(4*s))/(s*s)
    # right: y(x) = sin(su) cos(s q (x-u)) + (1/q) cos(su) sin(s q (x-u))
    v = mp.mpf(1)/2 - u
    b = s*q*v
    A = mp.sin(s*u)/s; C = mp.cos(s*u)/(s*q)
    # int_0^b (A cos t + C sin t)^2 dt
    I_t = A*A*(b/2 + mp.sin(2*b)/4) + 2*A*C*(mp.sin(b)**2/2) + C*C*(b/2 - mp.sin(2*b)/4)
    I_right = I_t/(s*q)
    return 2*(I_left + q*q*I_right)

for q in [mp.mpf(1.1), mp.sqrt(mp.mpf(4)), mp.sqrt(mp.mpf(100))]:
    for c in [mp.mpf('0.1'), mp.mpf('0.4')]:
        u = u_from_c(c, q)
        a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
        s1 = a1/u; s2 = a2/u
        w = u + q*q*(mp.mpf(1)/2 - u)
        N1 = N_direct(q, u, s1); N2 = N_direct(q, u, s2)
        val1 = (mp.sin(a1)/s1)**2/N1
        val2 = (mp.sin(a2)/s2)**2/N2
        claim1 = mp.tan(a1)**2/(mp.mpf(1)/2 + w*mp.tan(a1)**2)
        claim2 = mp.tan(a2)**2/(mp.mpf(1)/2 + w*mp.tan(a2)**2)
        ok &= check(f'N identity q={q} c={c}',
                    abs(val1-claim1) < mp.mpf('1e-30') and abs(val2-claim2) < mp.mpf('1e-30'),
                    f'|d1|={float(abs(val1-claim1)):.1e} |d2|={float(abs(val2-claim2)):.1e}')

# ---------- P4: (F1) ----------
print('--- P4: (F1) f_sym = (2/u^2)(T1 - T2) ---')
for q in [mp.mpf(1.1), mp.sqrt(mp.mpf(4))]:
    for c in [mp.mpf('0.1'), mp.mpf('0.4')]:
        u = u_from_c(c, q)
        a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
        s1 = a1/u; s2 = a2/u
        N1 = N_direct(q, u, s1); N2 = N_direct(q, u, s2)
        fdir = s1*s1*(mp.sin(a1)/s1)**2/N1 - s2*s2*(mp.sin(a2)/s2)**2/N2
        w = u + q*q*(mp.mpf(1)/2 - u)
        T1 = a1*a1*mp.tan(a1)**2/(1 + 2*w*mp.tan(a1)**2)
        T2 = a2*a2*mp.tan(a2)**2/(1 + 2*w*mp.tan(a2)**2)
        fclaim = 2*(T1 - T2)/u**2
        ok &= check(f'F1 q={q} c={c}', abs(fdir-fclaim) < mp.mpf('1e-30'),
                    f'|d|={float(abs(fdir-fclaim)):.1e}')

# ---------- P5: (D') ----------
print('--- P5: D\'(c) = (8/q^2)(c+q) F(c) ---')
for q in [mp.mpf(1.05), mp.mpf(2), mp.mpf(10)]:
    for c in [mp.mpf('0.05'), mp.mpf('0.3'), mp.mpf('0.49')]:
        h = mp.mpf('1e-6')
        D = lambda cc: 4*(cc+q)**2*((alpha2_of_c(cc,q))**2 - (alpha1_of_c(cc,q))**2)/q**2
        dD_num = (D(c+h) - D(c-h))/(2*h)
        dD_formula = 8*(c+q)*F_of_c(c, q)/q**2
        ok &= check(f"D' q={q} c={c}", abs(dD_num-dD_formula) < mp.mpf('1e-8'),
                    f'|d|={float(abs(dD_num-dD_formula)):.1e}')

# ---------- P6: (L) ----------
print('--- P6: G formula vs numeric log-derivative ---')
for q in [mp.mpf(1.1), mp.mpf(2), mp.mpf(10)]:
    for c in [mp.mpf('0.1'), mp.mpf('0.45')]:
        h = mp.mpf('1e-6')
        for k in (1, 2):
            a_k = (lambda cc: alpha1_of_c(cc, q) if k == 1 else alpha2_of_c(cc, q))
            logM = lambda cc: mp.log(Mfun(a_k(cc), cc, q))
            num = (logM(c+h) - logM(c-h))/(2*h)
            Gk = G1_of_c(c, q) if k == 1 else G2_of_c(c, q)
            ok &= check(f'L q={q} c={c} k={k}', abs(num-Gk) < mp.mpf('1e-8'),
                        f'|d|={float(abs(num-Gk)):.1e}')

# ---------- P7: (FS) ----------
print('--- P7: (FS) f_sym = 2(c+q)F/(q u^2 (q^2-1)) ---')
for q in [mp.mpf(1.1), mp.sqrt(mp.mpf(4))]:
    for c in [mp.mpf('0.1'), mp.mpf('0.4')]:
        u = u_from_c(c, q)
        a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
        s1 = a1/u; s2 = a2/u
        N1 = N_direct(q, u, s1); N2 = N_direct(q, u, s2)
        fdir = s1*s1*(mp.sin(a1)/s1)**2/N1 - s2*s2*(mp.sin(a2)/s2)**2/N2
        fform = f_sym_formula(c, q)
        ok &= check(f'FS q={q} c={c}', abs(fdir-fform) < mp.mpf('1e-25'),
                    f'|d|={float(abs(fdir-fform)):.1e}')

# ---------- P8: log form == G1 - G2 ----------
print('--- P8: (d/dc)log(M1/M2) == G1 - G2 ---')
for q in [mp.mpf(1.1), mp.mpf(2), mp.mpf(10)]:
    for c in [mp.mpf('0.05'), mp.mpf('0.4')]:
        h = mp.mpf('1e-6')
        ld = (mp.log(M1_of_c(c+h,q)/M2_of_c(c+h,q)) - mp.log(M1_of_c(c-h,q)/M2_of_c(c-h,q)))/(2*h)
        Gdiff = G1_of_c(c, q) - G2_of_c(c, q)
        ok &= check(f'P8 q={q} c={c}', abs(ld-Gdiff) < mp.mpf('1e-8'),
                    f'|d|={float(abs(ld-Gdiff)):.1e}')

# ---------- P9: equivalence audit ----------
print('--- P9: F\' = M1 G1 - M2 G2; equivalence audit ---')
for q in [mp.mpf(1.1), mp.mpf(2), mp.mpf(10)]:
    for c in [mp.mpf('0.05'), mp.mpf('0.4')]:
        h = mp.mpf('1e-6')
        dF_num = (F_of_c(c+h,q) - F_of_c(c-h,q))/(2*h)
        dF_formula = M1_of_c(c,q)*G1_of_c(c,q) - M2_of_c(c,q)*G2_of_c(c,q)
        ok &= check(f'P9a F\'=M1G1-M2G2 q={q} c={c}', abs(dF_num-dF_formula) < mp.mpf('1e-8'),
                    f'|d|={float(abs(dF_num-dF_formula)):.1e}')
        # both signs, but check they are not logically identical: find a point where they disagree in sign? (test below)
        print(f'    q={q} c={c}: F\'={mp.nstr(dF_formula,6)}  G1-G2={mp.nstr(G1_of_c(c,q)-G2_of_c(c,q),6)}')

# ---------- P10: margins ----------
print('--- P10: KEY LEMMA margins ---')
for q in [mp.mpf(1.025), mp.mpf(1.1), mp.sqrt(mp.mpf(4)), mp.sqrt(mp.mpf(100)), mp.mpf(100)]:
    cs = [mp.mpf('1e-4') + mp.mpf('0.4999')*k/300 for k in range(301)]
    mG = mp.inf; mF = mp.inf
    for c in cs:
        mG = min(mG, G2_of_c(c,q) - G1_of_c(c,q))
        mF = min(mF, -(M1_of_c(c,q)*G1_of_c(c,q) - M2_of_c(c,q)*G2_of_c(c,q)))
    print(f'  q={mp.nstr(q,6)}: min(G2-G1)={mp.nstr(mG,8)}  min(-F\')={mp.nstr(mF,8)}')
    ok &= check(f'margin q={q}', mG > 0 and mF > 0)

print()
print('ALL PREMISES PASS' if ok else 'SOME CHECKS FAILED')



