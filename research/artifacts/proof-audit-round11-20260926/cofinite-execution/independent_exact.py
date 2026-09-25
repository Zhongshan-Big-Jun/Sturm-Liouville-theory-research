"""Independent rational coefficient checks; no numerical/analytic certification."""
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial
import json


class P:
    """Polynomials over Q in five formal indeterminates."""
    def __init__(self, value=0):
        terms = value if isinstance(value, dict) else {(0,) * 5: F(value)}
        self.terms = {m: F(c) for m, c in terms.items() if c}

    @staticmethod
    def cast(v):
        return v if isinstance(v, P) else P(v)

    def __add__(self, other):
        terms = dict(self.terms)
        for m, c in P.cast(other).terms.items():
            terms[m] = terms.get(m, F(0)) + c
        return P(terms)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-P.cast(other))

    def __rsub__(self, other):
        return P.cast(other) - self

    def __mul__(self, other):
        terms = {}
        for m, c in self.terms.items():
            for n, d in P.cast(other).terms.items():
                e = tuple(a + b for a, b in zip(m, n))
                terms[e] = terms.get(e, F(0)) + c * d
        return P(terms)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        out = P(1)
        for _ in range(exponent):
            out = out * self
        return out


def variable(index):
    powers = [0] * 5
    powers[index] = 1
    return P({tuple(powers): 1})


records = []


def equal(label, left, right=0):
    difference = P.cast(left) - right
    assert not difference.terms, (label, difference.terms)
    records.append({"name": label, "passed": True})


def determinant(matrix):
    result = P(0)
    for perm in permutations(range(len(matrix))):
        inversions = sum(perm[i] > perm[j]
                         for i in range(len(perm)) for j in range(i + 1, len(perm)))
        term = P((-1) ** inversions)
        for row, column in enumerate(perm):
            term = term * matrix[row][column]
        result = result + term
    return result


def actual_endpoint_residuals(q, parity):
    """For x^q, using endpoint falling factorials and (-1)^q=parity."""
    second = q * (q - 1)
    third = second * (q - 2)
    delta_half = F(1 - parity, 2)
    return [q - delta_half, -parity * q - delta_half,
            third - delta_half * second, -parity * third - delta_half * second]


z, xr, xi, br, bi = [variable(i) for i in range(5)]
columns = [actual_endpoint_residuals(z + j, (-1) ** j) for j in range(4)]
matrix = [[columns[j][i] for j in range(4)] for i in range(4)]
equal("All-even-L full boundary determinant from actual endpoint formulas",
      determinant(matrix), 16 * z**2 * (z + 2)**2 * (4 * z**2 - 1))

even = [[(matrix[i][j] - matrix[i + 1][j]) * F(1, 2)
         for j in [0, 2]] for i in [0, 2]]
odd = [[(matrix[i][j] + matrix[i + 1][j]) * F(1, 2)
        for j in [1, 3]] for i in [0, 2]]
equal("Even boundary block determinant", determinant(even), 2 * z * (z + 2) * (2 * z - 1))
equal("Odd boundary block determinant", determinant(odd), 2 * z * (z + 2) * (2 * z + 1))
equal("Terminal two-monomial residual determinant",
      determinant([row[:2] for row in matrix[:2]]), 2 * z**2)

# Here the same indeterminate z represents m. Clearing m-1 is valid for m>=2.
for odd_flag in [0, 1]:
    parity = (-1) ** odd_flag
    upper = actual_endpoint_residuals(2 * z + odd_flag, parity)
    lower = actual_endpoint_residuals(2 * z + odd_flag - 2, parity)
    numerator = [(z - 1) * a - z * b for a, b in zip(upper, lower)]
    for endpoint in [0, 1]:
        equal(f"All-m member first residual parity={odd_flag} endpoint={endpoint}",
              numerator[endpoint])
    leading = 4 * z * (4 * z - 5 + 2 * odd_flag)
    equal(f"All-m member second plus residual parity={odd_flag}", numerator[2], (z - 1) * leading)
    equal(f"All-m member second minus residual parity={odd_flag}", numerator[3], -parity * (z - 1) * leading)

# Complex-coordinate completion of squares, where z=t^2*w>0.
objective = (xr - br)**2 + (xi - bi)**2 + z * (br**2 + bi**2)
equal("Complex K-functional exact completion of squares",
      (1 + z) * objective,
      z * (xr**2 + xi**2) + ((1 + z) * br - xr)**2 + ((1 + z) * bi - xi)**2)
# z/(1+z)^2 <= 1/4 follows from the following nonnegative square.
equal("Admissibility bound numerator", (1 + z)**2 - 4 * z, (z - 1)**2)

# Independently integrate the squared Volterra kernel on 0<t<x<1.
for derivative_order in range(4):
    power = 6 - 2 * derivative_order
    integral = sum((F((-1)**j * comb(power, j), (j + 1) * (power + 2))
                    for j in range(power + 1)), F(0)) / factorial(3 - derivative_order)**2
    claimed = F(1, factorial(3 - derivative_order)**2 *
                (7 - 2 * derivative_order) * (8 - 2 * derivative_order))
    equal(f"Cutoff squared-kernel coefficient j={derivative_order}", integral, claimed)

print(json.dumps({
    "status": "PASSED",
    "arithmetic": "Exact rational polynomial coefficients; no floating point",
    "total_checks": len(records),
    "checks": records,
    "scope": [
        "Boundary identities in an unrestricted formal parameter, with endpoint parity requiring even L",
        "Member identities after clearing m-1, applicable to every integer m>=2",
        "Complex scalar minimization identity and admissibility inequality numerator",
        "Exact cutoff integral coefficients for the four derivative orders used"
    ],
    "limitations": "These coefficient checks do not establish infinite summation, operator domains, density, trace continuity or any analytic closure theorem."
}, indent=2))
