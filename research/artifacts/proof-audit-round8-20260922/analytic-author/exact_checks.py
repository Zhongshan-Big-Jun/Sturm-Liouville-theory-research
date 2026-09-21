"""Author-only rational checks for elementary constants; no T3 root isolation."""
from fractions import Fraction as Q
from math import factorial
import json

Checks = []

def check(Name, Passed, Detail):
	Checks.append({'name': Name, 'passed': bool(Passed), 'detail': Detail})
	if not Passed:
		raise ArithmeticError(Name + ': ' + str(Detail))

check('sqrt threshold', 38**2 < 1500, 'epsilon < 1/38')
check('sqrt2 bound', Q(3, 2)**2 > 2, 'tan(pi/8)=sqrt2-1 < 1/2')
check('pi squared from Archimedes', Q(22, 7)**2 < 10, 'uses classical 3<pi<22/7')
Sliver = 1 / (2 * Q(1, 38) * Q(5, 2) * (2 + Q(1, 76)))
check('whole sliver pi squared multiplier', Sliver > Q(15, 4), str(Sliver))
check('sliver exceeds 25', Q(15, 4) * 9 > 25, '135/4 > 25; pi>3')
check('sliver endpoint separation', Q(15, 4) > 3, '15*pi^2/4 > 3*pi^2')
check('even phase lower', Q(3, 2) - Q(1, 76) > Q(7, 5), str(Q(3, 2)-Q(1, 76)))
Ctwo = 1 - 10 * Q(1, 152)**2 / 12
check('arctan factor', Ctwo > Q(99, 100), str(Ctwo))
DefOne = Q(7, 5) * Q(29, 10) * Q(99, 100)
check('first deficit coefficient', DefOne > 4, str(DefOne))
Rem = 1 / (3 * (1 - Q(10, 64) / 6))
check('cot remainder coefficient', Rem < Q(7, 20), str(Rem))
SinUpper = sum(((-1)**J) * Q(2)**(2*J+1)/factorial(2*J+1) for J in range(5))
CosUpper = sum(((-1)**J) * Q(2)**(2*J)/factorial(2*J) for J in range(5))
check('sine Taylor at 2', SinUpper < Q(91, 100), str(SinUpper))
check('cosine Taylor at 2', CosUpper < -Q(2, 5), str(CosUpper))
QUpper = Q(91, 50) + Q(11, 100) * Q(8, 7)
check('concave tangent bound', QUpper < 2, str(QUpper))
check('denominator perturbation', Q(7, 20)/1500 < Q(1, 1000), str(Q(7, 20)/1500))
DefTwo = Q(7, 20) * 8 * Q(1000, 999)
check('second deficit coefficient', DefTwo < 3, str(DefTwo))
check('strict A double prime margin', DefOne - DefTwo > 1, str(DefOne-DefTwo))
print(json.dumps({'kind': 'exact rational arithmetic author check; not independent review', 'checks': Checks, 'passed': len(Checks)}, indent=2))
