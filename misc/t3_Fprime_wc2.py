# -*- coding: utf-8 -*-
"""t3_Fprime_wc2.py: rational worst-case F' <= A + (22/7)B + (223/100)C on [1/2,2/3]."""
from mpmath import mp, mpf
mp.dps = 40
def A(b): return mpf('147')/10*b**6 + mpf('189')/5*b**5 + mpf('21')/2*b**4 - 42*b**3 - mpf('63')/2*b**2 + mpf('21')/5*b + mpf('63')/10
def B(b): return 8*b**5 + mpf('10')/3*b**4 - mpf('32')/3*b**3 + mpf('16')/3*b - mpf('2')/3
def C(b): return mpf('35')/3*b**4 + mpf('44')/3*b**3 - 6*b**2 - mpf('28')/3*b - mpf('1')/3
def W(b): return A(b) + mpf('22')/7*B(b) + mpf('223')/100*C(b)
lo, hi, arglo, arghi = mpf(1e30), mpf(-1e30), None, None
for i in range(4001):
    b = mpf('0.5') + mpf(i)*mpf('1')/6000
    if b > mpf('2')/3: break
    v = W(b)
    if v < lo: lo = v; arglo = (b, i)
    if v > hi: hi = v; arghi = (b, i)
print('W on [1/2,2/3]: [%.6f, %.6f], max at b=%.4f' % (lo, hi, arghi[0]))
# exact rational W: multiply by lcm(10,5,2,3,7,100)=2100: coefficients?
import sympy as sp
bb = sp.symbols('bb')
Wr = sp.Rational(147,10)*bb**6 + sp.Rational(189,5)*bb**5 + sp.Rational(21,2)*bb**4 - 42*bb**3 - sp.Rational(63,2)*bb**2 + sp.Rational(21,5)*bb + sp.Rational(63,10) \
   + sp.Rational(22,7)*(8*bb**5 + sp.Rational(10,3)*bb**4 - sp.Rational(32,3)*bb**3 + sp.Rational(16,3)*bb - sp.Rational(2,3)) \
   + sp.Rational(223,100)*(sp.Rational(35,3)*bb**4 + sp.Rational(44,3)*bb**3 - 6*bb**2 - sp.Rational(28,3)*bb - sp.Rational(1,3))
print('W rational polynomial:')
print(sp.expand(Wr))
# W' and W'' for monotonicity analysis
Wp = sp.diff(Wr, bb); Wpp = sp.diff(Wp, bb)
print('Wp =', sp.expand(Wp))
print('Wpp =', sp.expand(Wpp))
print('W(1/2) =', sp.nsimplify(Wr.subs(bb, sp.Rational(1,2))))
print('W(2/3) =', sp.nsimplify(Wr.subs(bb, sp.Rational(2,3))))
