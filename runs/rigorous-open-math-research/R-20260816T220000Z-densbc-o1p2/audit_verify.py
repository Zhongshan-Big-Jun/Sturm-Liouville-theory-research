import sympy as sp
lam = sp.symbols('lam', real=True)
A = 1 + lam**2

def G(i, k):
    if i == k:
        return A
    if abs(i - k) == 1:
        return lam
    return 0

def coeff(n):
    m = n // 2 if n % 2 == 0 else (n - 1) // 2
    return sp.Rational(m, m - 1)

def inner_v_p(v_deg, n):
    if n < 4:
        return sp.sympify(G(v_deg, n))
    return sp.simplify(G(v_deg, n) - coeff(n) * G(v_deg, n - 2))

print('p coefficients n>=4:', {n: coeff(n) for n in [4, 5, 6, 7, 8]})
print('<v1,p_n>:')
for n in [0, 1, 4, 5, 6, 7, 8, 9, 10, 11]:
    print(' n =', n, ' -> ', sp.simplify(inner_v_p(4, n)))

def Nset(lamval):
    N = []
    for n in [0, 1] + list(range(4, 13)):
        val = sp.simplify(inner_v_p(4, n).subs(lam, lamval))
        if val == 0:
            N.append(n)
    return N
print('N lambda=0:', Nset(0))
print('N lambda=1/2:', Nset(sp.Rational(1, 2)))

# Direct obstruction w = J^{-1} delta_2, exact truncated for k 0..10
def M_delta2(k):
    return 1 if k == 2 else 0
w_expr = [sp.simplify(sum((-lam)**j * M_delta2(k + j) for j in range(0, 20))) for k in range(0, 6)]
print('w:', w_expr)
print('M(w):', [sp.simplify(w_expr[k] + lam * w_expr[k + 1]) for k in range(0, 5)])

# T rows for v1=x^4, finite free bases
for lamval_name, lamval, Bfin in [('lam=0', 0, [2, 4]), ('lam=1/2', sp.Rational(1, 2), [2, 3, 4, 5])]:
    row = []
    for b in Bfin:
        # For this example the finite runs are singletons {b}; only R_4 contains degree 4.
        val = sp.Integer(1) if b == 4 else sp.Integer(0)
        row.append(val)
    print(lamval_name, 'Bfin', Bfin, 'Trow', row)
