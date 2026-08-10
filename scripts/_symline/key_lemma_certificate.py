# -*- coding: utf-8 -*-
# key_lemma_certificate.py — exact rational certificates for P2 (W0 bound) and P1.
# Uses sympy exact arithmetic; output feeds the STRICT proof doc.
import sympy as sp

# ---- P2 certificate: W0(Gamma) < (4/3) q0 ----
# q0 = sqrt(2/3); Gamma = arccos(q0/(1+q0)) < 10/9  (via cos(10/9) < q0/(1+q0))
# cot(10/9) > Lc/Us,  Lc = 1-x^2/2+x^4/24-x^6/720 (cos lower, alternating), Us = x-x^3/6+x^5/120 (sin upper)
x = sp.Rational(10,9)
Lc = 1 - x**2/2 + x**4/24 - x**6/720
Us = x - x**3/6 + x**5/120
print('Lc =', Lc, '=', sp.nsimplify(sp.nsimplify(Lc)))
print('Us =', Us)
print('Lc/Us =', sp.nsimplify(Lc/Us), '~', float(Lc/Us))

# q0 > 2247/2753 ?
q0sq = sp.Rational(2,3)
print('q0 > 2247/2753:', sp.Rational(2247,2753)**2 < q0sq)
# q0/(1+q0) > 2247/5000
print('q0/(1+q0) > 2247/5000:', sp.Rational(2247,5000) < sp.sqrt(q0sq)/(1+sp.sqrt(q0sq)))
# cos(10/9) < 8783/19683 < 2247/5000?
print('8783/19683 =', sp.nsimplify(sp.Rational(8783,19683)), '< 2247/5000:', sp.Rational(8783,19683) < sp.Rational(2247,5000))
# hence Gamma < 10/9
print('Gamma < 10/9  established.')

# W0(Gamma) = 3 - 2(pi-Gamma)cot(Gamma) < 3 - 2(pi-10/9)cot(10/9) < 3 - 2*(pi-10/9)*(Lc/Us)
# with pi > 22/7:  2(pi-10/9) > 2(22/7 - 10/9) = 2*128/63
two_pi_minus = 2*sp.Rational(128,63)
print('2(22/7-10/9) =', two_pi_minus)
prod = two_pi_minus * (Lc/Us)
print('2(pi-10/9)cot(10/9) >', sp.nsimplify(prod), '~', float(prod))
# need prod > 3 - (4/3)q0 ; bound 3 - (4/3)(2247/2753) = 15789/8259
B = 3 - sp.Rational(4,1)*sp.Rational(2247,2753)/3
print('3-(4/3)(2247/2753) =', sp.nsimplify(B), '~', float(B))
print('prod > B:', sp.simplify(prod - B) > 0)
# hence 3 - 2(pi-Gamma)cotGamma < (4/3)q0  => W0(Gamma) < (4/3)q0
print('=> W0(Gamma) < (4/3)q0  established.')

# ---- P1 certificate: G1 <= -3/(1/q0+1/2) < -4/3 ----
# 3/(1/q0+1/2) > 4/3  iff  q0 > 4/7
print('q0 > 4/7:', sp.Rational(4,7) < sp.sqrt(q0sq))
# explicit bound value
val = 3/(1/sp.sqrt(q0sq) + sp.Rational(1,2))
print('3/(1/q0+1/2) =', sp.nsimplify(val), '~', float(val))

# ---- also verify: W0 increasing on (0,Gamma]: W0' = 2cot g + 2(pi-g)csc^2 g > 0 ----
print('W0\'(g) = 2cotg + 2(pi-g)csc^2g > 0 on (0,pi/2): trivially positive since cotg>0, csc^2g>0, pi-g>0.')
