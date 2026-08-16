# boundary_facts.py
# Exact (sympy rational) verification of the operator-domain boundary structure
# for the Krein Laplacian K_c = -d^2/dx^2 + c on L^2(-1,1),
# D(K_c) = { f in AC, f'' in L^2 : f'(1) = f'(-1) = (f(1)-f(-1))/2 }.
#
# Run: R-20260816T200000Z-hs-operator-domain
# Purpose: EVIDENCE (exact arithmetic) for STRICT claims in candidate_proof.md.
# In particular:
#   (A) for which n is the formal polynomial Q_n^{(2)} := K_c^{-1} P_n in D(K_c)?
#   (B) for which n is Q_n^{(2r)} := K_c^{-r} P_n in D(K_c^r) (r = 1,2,3)?
#   (C) exact description of D(K_c^r) ∩ (polynomials).
# Output: exact Krein-boundary deficits, all rational in c.

import sympy as sp

x, c = sp.symbols('x c', positive=True)

def K_poly(p):
    # K_c p = c p - p''
    return sp.expand(c * p - sp.diff(p, x, 2))

def K_inv_poly(p):
    # formal inverse: K_c^{-1} p = c^{-1} * sum_{j>=0} c^{-j} p^{(2j)}  (terminates)
    out = 0
    pj = p
    j = 0
    # iterate until derivative vanishes
    while True:
        out += c**(-1) * c**(-j) * pj
        pj = sp.expand(sp.diff(pj, x, 2))
        if pj == 0:
            break
        j += 1
        if j > 200:
            raise RuntimeError('nontermination')
    return sp.expand(out)

def K_inv_r_poly(p, r):
    q = p
    for _ in range(r):
        q = K_inv_poly(q)
    return sp.expand(q)

def krein_deficit_even(f):
    # for even f: Krein BC reduces to f'(1) = 0  (f'(1)=f'(-1)=0)
    return sp.expand(sp.diff(f, x, 1).subs(x, 1))

def krein_deficit_odd(f):
    # for odd f: Krein BC reduces to f'(1) = f(1)
    return sp.expand(sp.diff(f, x, 1).subs(x, 1) - f.subs(x, 1))

def in_DKc(f):
    # general Krein check: f'(1)==f'(-1)==(f(1)-f(-1))/2
    d1 = sp.expand(sp.diff(f, x, 1).subs(x, 1))
    dm1 = sp.expand(sp.diff(f, x, 1).subs(x, -1))
    avg = sp.expand((f.subs(x, 1) - f.subs(x, -1)) / 2)
    return (d1 - avg == 0) and (dm1 - avg == 0)

def legendre(n):
    # P_n standard Legendre polynomial
    return sp.legendre(n, x)

print('=== (A) Q_n^{(2)} = K_c^{-1}P_n in D(K_c)? ===')
for n in range(0, 10):
    fn = legendre(n)
    q = K_inv_poly(fn)
    print('n=%d inD(Kc)=%s  parity=%s' % (n, in_DKc(q), 'even' if n % 2 == 0 else 'odd'))

print()
print('=== (B.1) Q_n^{(4)} = K_c^{-2}P_n in D(K_c^2)? ===')
for n in range(0, 9):
    q2 = K_inv_r_poly(legendre(n), 2)
    # D(K_c^2): q2 in D(K_c) and K_c q2 in D(K_c)
    kq = K_poly(q2)
    print('n=%d q2 in DKc=%s, Kc q2 in DKc=%s  => in D(Kc^2)=%s' % (
        n, in_DKc(q2), in_DKc(kq), in_DKc(q2) and in_DKc(kq)))

print()
print('=== (B.2) Q_n^{(6)} = K_c^{-3}P_n in D(K_c^3)? ===')
for n in range(0, 7):
    q3 = K_inv_r_poly(legendre(n), 3)
    k1 = K_poly(q3)
    k2 = K_poly(k1)
    ok = in_DKc(q3) and in_DKc(k1) and in_DKc(k2)
    print('n=%d in D(Kc^3)=%s' % (n, ok))

print()
print('=== explicit Q_4^{(2)} and its Krein deficit ===')
q = K_inv_poly(legendre(4))
print('Q_4^{(2)} =', sp.factor(q))
print('f prime at 1 =', sp.factor(sp.diff(q, x).subs(x, 1)))
print('even Krein deficit f\'(1)  =', sp.factor(krein_deficit_even(q)))

print()
print('=== (C.1) D(K_c) ∩ polynomials in {1,x,x^2,...,x^8}: which monomials in D(K_c)? ===')
for k in range(0, 9):
    print('x^%d in DKc = %s' % (k, in_DKc(x ** k)))

print()
print('=== (C.2) D(K_c^2) ∩ monomials ===')
for k in range(0, 9):
    m = x ** k
    km = K_poly(m)
    print('x^%d in D(Kc^2) = %s' % (k, in_DKc(m) and in_DKc(km)))
