# -*- coding: utf-8 -*-
"""Audit re-derivation (coordinator-conducted; subagent mechanism unavailable):
verify densbc candidate_proof claims with exact sympy arithmetic.

Checks:
(1) Lemma 4.1 odd-run ratio: recursion-derived M_{2m+1} = (m/q) M_{2q+1}
    (odd lowest L = 2q+1) vs the stated ((m+1)/b) formula with idx(2m+1)=m+1.
(2) Counterexample (a): R = {2,3}, w with M_4 = M_5 = 1, even chain
    M_{2m} = (m/2) M_4 (m>=2), odd chain M_{2m+1} = (m/2) M_5 (m>=3):
    (w, p_n) == 0 exactly for every KEPT p_n (supports avoid {2,3}).
(3) Counterexample (b): R = {4}, w = e_2: (w, p_n) == 0 for kept p_n
    (kept even p_{2m} iff {2m,2m-2} cap {4} = empty, i.e. m >= 4; all kept odds
    p_{2m+1} with m >= 2? check supports: p_5 = {5,3}, p_7={7,5}, ... keep all odds).
(4) Norm-threshold: ||w||_beta^2 tail ~ sum m^{2-2 beta} (both counterexamples).
(5) Theorem D recursion: M_{2m} = (m/(m-1)) M_{2m-2} with M_0 = M_2 = 0 forces
    all even moments zero (m >= 2); odd side likewise.
"""
import sympy as sp

# ---- (1) odd chain from the recursion ----
M5 = sp.symbols('M5')
Ms = {5: M5}
for m in range(3, 12):  # p_{2m+1} kept from m=3 onward for R={2,3}
    k = 2 * m + 1
    Ms[k] = sp.Rational(m, m - 1) * Ms[k - 2]
odd_ratio = sp.simplify(Ms[11] / M5)
print('(1) M11/M5 from recursion =', odd_ratio, ' (stated lemma formula (m+1)/3 at m=5 gives 2)')
print('    recursion pattern M_{2m+1} = (m/2) M5: m=3 ->', sp.Rational(3, 2),
      'm=4 ->', sp.Integer(2), 'm=5 ->', sp.Rational(5, 2))

# ---- (2) counterexample (a) exact orthogonality ----
def kept_even(m, R):
    return (2 * m) not in R and (2 * m - 2) not in R

def kept_odd(m, R):
    return (2 * m + 1) not in R and (2 * m - 1) not in R

def inner_even(w, m):
    # (w, p_{2m}) = M_{2m} - (m/(m-1)) M_{2m-2}
    return w[2 * m] - sp.Rational(m, m - 1) * w[2 * m - 2]

def inner_odd(w, m):
    return w[2 * m + 1] - sp.Rational(m, m - 1) * w[2 * m - 1]

R = {2, 3}
M4 = M5 = 1
w = {}
for m in range(2, 40):
    w[2 * m] = sp.Rational(m, 2) * M4          # even top run, lowest 4, idx 2
w[5] = M5                                       # odd base degree 5
for m in range(3, 40):
    w[2 * m + 1] = sp.Rational(m, 2) * M5      # odd top run, lowest 5 (correct chain)
w[2] = 0; w[3] = 0
viol = 0
for m in range(2, 40):
    if kept_even(m, R):
        if sp.simplify(inner_even(w, m)) != 0:
            viol += 1
            print('(2) VIOLATION even m =', m, inner_even(w, m))
for m in range(2, 40):
    if kept_odd(m, R):
        if sp.simplify(inner_odd(w, m)) != 0:
            viol += 1
            print('(2) VIOLATION odd m =', m, inner_odd(w, m))
print('(2) counterexample (a): kept p_n orthogonality violations =', viol)

# wrong-chain check: what does the lemma's stated odd formula give?
w2 = {k: v for k, v in w.items()}
w2[5] = M5
for m in range(3, 40):
    w2[2 * m + 1] = sp.Rational(m + 1, 3) * M5
v2 = 0
for m in range(3, 40):
    if sp.simplify(inner_odd(w2, m)) != 0:
        v2 += 1
print('(2b) lemma-stated odd formula (m+1)/3: violations =', v2, ' (expect >0 => lemma formula incorrect)')

# ---- (3) counterexample (b): R = {4}, w = e_2 ----
R2 = {4}
we = {}
for k in range(0, 60):
    we[k] = sp.Integer(1) if k == 2 else sp.Integer(0)
vb = 0
for m in range(2, 30):
    if kept_even(m, R2):
        if sp.simplify(inner_even(we, m)) != 0:
            vb += 1
            print('(3) VIOLATION even m =', m, inner_even(we, m))
for m in range(2, 30):
    if kept_odd(m, R2):
        if sp.simplify(inner_odd(we, m)) != 0:
            vb += 1
            print('(3) VIOLATION odd m =', m, inner_odd(we, m))
print('(3) counterexample (b) R={4}, w=e_2: violations =', vb)
print('    kept even p_{2m} for m >= 4 (support {2m,2m-2} avoids 4); p_4 itself not kept')

# ---- (4) norm threshold: tail ~ sum m^{2-2 beta} ----
print('(4) even chain norm tail: sum_{m>=2} (m/2)^2 (2m+1)^{-2 beta} ~ (1/4) sum m^{2-2 beta}:'
      ' converges iff 2 - 2 beta < -1 iff beta > 3/2')

# ---- (5) Theorem D recursion ----
M2 = sp.symbols('M2')
Me = {0: sp.Integer(0), 2: M2}
for m in range(2, 10):
    Me[2 * m] = sp.Rational(m, m - 1) * Me[2 * m - 2]
print('(5) Theorem D: M_{2m} = m*M2 for m=2..8:', [sp.simplify(Me[2 * m]) for m in range(2, 9)])
print('    with M2 = 0 all vanish; odd side M_{2m+1} = m*M3 likewise (check)')
M3 = sp.symbols('M3')
Mo = {3: M3, 5: sp.Integer(2) * M3}
for m in range(3, 10):
    Mo[2 * m + 1] = sp.Rational(m, m - 1) * Mo[2 * m - 1]
print('    odd: M_{2m+1} = m*M3 for m=2..8:', [sp.simplify(Mo[2 * m + 1]) for m in range(2, 9)])
