"""Independent high-precision Laurent expansion of the two sector determinants.

This file deliberately rebuilds the full five-block transfer problem.  It does
not import any previous M3 asymptotic code or coefficient table.  The branch
coefficients inserted below were derived in the fresh seed/cascade scripts in
this directory.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".deps"))

import mpmath as mp


mp.mp.dps = 140
MIN_ORDER = -24
MAX_ORDER = 46
DROP = mp.mpf("1e-105")
VISIBLE = mp.mpf("1e-75")


@dataclass(frozen=True)
class MPS:
	c: dict[int, mp.mpf]

	def __post_init__(self) -> None:
		clean: dict[int, mp.mpf] = {}
		for power, value in self.c.items():
			power = int(power)
			value = mp.mpf(value)
			if MIN_ORDER <= power <= MAX_ORDER and abs(value) > DROP:
				clean[power] = value
		object.__setattr__(self, "c", clean)

	@staticmethod
	def scalar(value: object) -> "MPS":
		return MPS({0: mp.mpf(value)})

	@staticmethod
	def monomial(power: int, value: object = 1) -> "MPS":
		return MPS({power: mp.mpf(value)})

	def __add__(self, other: "MPS | object") -> "MPS":
		o = other if isinstance(other, MPS) else MPS.scalar(other)
		powers = set(self.c) | set(o.c)
		return MPS({p: self.c.get(p, mp.mpf(0)) + o.c.get(p, mp.mpf(0))
			for p in powers})

	__radd__ = __add__

	def __neg__(self) -> "MPS":
		return MPS({p: -v for p, v in self.c.items()})

	def __sub__(self, other: "MPS | object") -> "MPS":
		return self + (-other if isinstance(other, MPS) else -mp.mpf(other))

	def __rsub__(self, other: object) -> "MPS":
		return MPS.scalar(other) - self

	def __mul__(self, other: "MPS | object") -> "MPS":
		o = other if isinstance(other, MPS) else MPS.scalar(other)
		out: dict[int, mp.mpf] = {}
		for p, a in self.c.items():
			for q, b in o.c.items():
				r = p + q
				if MIN_ORDER <= r <= MAX_ORDER:
					out[r] = out.get(r, mp.mpf(0)) + a*b
		return MPS(out)

	__rmul__ = __mul__

	def __pow__(self, power: int) -> "MPS":
		if power < 0:
			return self.inv() ** (-power)
		out = MPS.scalar(1)
		base = self
		n = power
		while n:
			if n & 1:
				out = out*base
			base = base*base
			n //= 2
		return out

	def inv(self) -> "MPS":
		if not self.c:
			raise ZeroDivisionError("zero Laurent series")
		lead = min(self.c)
		lead_coef = self.c[lead]
		q = MPS({p-lead: value/lead_coef
			for p, value in self.c.items() if p != lead})
		term = MPS.scalar(1)
		geom = MPS.scalar(1)
		for _ in range(MAX_ORDER-MIN_ORDER+6):
			term = -term*q
			if not term.c:
				break
			geom = geom + term
		return MPS.monomial(-lead, 1/lead_coef)*geom

	def __truediv__(self, other: "MPS | object") -> "MPS":
		o = other if isinstance(other, MPS) else MPS.scalar(other)
		return self*o.inv()

	def __rtruediv__(self, other: object) -> "MPS":
		return MPS.scalar(other)/self

	def coefficient(self, power: int) -> mp.mpf:
		return self.c.get(power, mp.mpf(0))


def sin_s(x: MPS) -> MPS:
	constant = x.c.get(0, mp.mpf(0))
	h = MPS({p: value for p, value in x.c.items() if p != 0})
	sinh = MPS.scalar(0)
	cosh = MPS.scalar(1)
	power = MPS.scalar(1)
	for n in range(1, MAX_ORDER-MIN_ORDER+8):
		power = power*h
		if not power.c:
			break
		if n % 2:
			sinh = sinh + ((-1)**((n-1)//2))/mp.factorial(n)*power
		else:
			cosh = cosh + ((-1)**(n//2))/mp.factorial(n)*power
	return mp.sin(constant)*cosh + mp.cos(constant)*sinh


def cos_s(x: MPS) -> MPS:
	constant = x.c.get(0, mp.mpf(0))
	h = MPS({p: value for p, value in x.c.items() if p != 0})
	sinh = MPS.scalar(0)
	cosh = MPS.scalar(1)
	power = MPS.scalar(1)
	for n in range(1, MAX_ORDER-MIN_ORDER+8):
		power = power*h
		if not power.c:
			break
		if n % 2:
			sinh = sinh + ((-1)**((n-1)//2))/mp.factorial(n)*power
		else:
			cosh = cosh + ((-1)**(n//2))/mp.factorial(n)*power
	return mp.cos(constant)*cosh - mp.sin(constant)*sinh


@dataclass(frozen=True)
class DL:
	v: MPS
	d: MPS

	@staticmethod
	def lift(value: "MPS | object") -> "DL":
		return DL(value if isinstance(value, MPS) else MPS.scalar(value),
			MPS.scalar(0))

	def __add__(self, other: "DL | MPS | object") -> "DL":
		o = other if isinstance(other, DL) else DL.lift(other)
		return DL(self.v+o.v, self.d+o.d)

	__radd__ = __add__

	def __neg__(self) -> "DL":
		return DL(-self.v, -self.d)

	def __sub__(self, other: "DL | MPS | object") -> "DL":
		return self + (-other if isinstance(other, DL) else -DL.lift(other))

	def __rsub__(self, other: "MPS | object") -> "DL":
		return DL.lift(other)-self

	def __mul__(self, other: "DL | MPS | object") -> "DL":
		o = other if isinstance(other, DL) else DL.lift(other)
		return DL(self.v*o.v, self.d*o.v+self.v*o.d)

	__rmul__ = __mul__

	def inv(self) -> "DL":
		iv = self.v.inv()
		return DL(iv, -self.d*iv*iv)

	def __truediv__(self, other: "DL | MPS | object") -> "DL":
		o = other if isinstance(other, DL) else DL.lift(other)
		return self*o.inv()

	def __rtruediv__(self, other: "MPS | object") -> "DL":
		return DL.lift(other)/self

	def __pow__(self, power: int) -> "DL":
		if power == 0:
			return DL.lift(1)
		if power < 0:
			return self.inv()**(-power)
		return DL(self.v**power, power*(self.v**(power-1))*self.d)


def sin_d(x: DL) -> DL:
	return DL(sin_s(x.v), cos_s(x.v)*x.d)


def cos_d(x: DL) -> DL:
	return DL(cos_s(x.v), -sin_s(x.v)*x.d)


def advance(k: DL, sqrt_rho: MPS, length: DL,
		state: tuple[DL, DL]) -> tuple[DL, DL]:
	q = k*sqrt_rho
	phase = q*length
	c = cos_d(phase)
	s = sin_d(phase)
	y, yp = state
	return y*c+yp*s/q, -y*q*s+yp*c


def block_norm(k: DL, rho: MPS, sqrt_rho: MPS, length: DL,
		state: tuple[DL, DL]) -> DL:
	q = k*sqrt_rho
	y, yp = state
	b = yp/q
	icc = length/2 + sin_d(2*q*length)/(4*q)
	iss = length/2 - sin_d(2*q*length)/(4*q)
	ics = (1-cos_d(2*q*length))/(4*q)
	return (y*y*icc+2*y*b*ics+b*b*iss)*rho


def spectral_data(k: DL, edges: list[DL]) -> tuple[DL, list[DL], DL]:
	zero = DL.lift(0)
	one = DL.lift(1)
	points = [zero, *edges, one]
	rvalue = MPS.monomial(-6)
	sqrtr = MPS.monomial(-3)
	rhos = [rvalue, MPS.scalar(1), rvalue, MPS.scalar(1), rvalue]
	sqrts = [sqrtr, MPS.scalar(1), sqrtr, MPS.scalar(1), sqrtr]
	state = (zero, one)
	values: list[DL] = []
	norm = zero
	for index in range(5):
		length = points[index+1]-points[index]
		norm = norm+block_norm(k, rhos[index], sqrts[index], length, state)
		state = advance(k, sqrts[index], length, state)
		if index < 4:
			values.append(state[0])
	return state[0], values, norm


def branch_coefficients(k2: mp.mpf = mp.mpf(0),
		k4: mp.mpf = mp.mpf(0)) -> dict[str, mp.mpf]:
	pi = mp.pi
	k0 = mp.root(18*pi-48/pi, 3)
	a0 = 2/k0
	b0 = 1/k0
	c0 = 16/(pi*k0)
	a2 = -(k0**4+12*k0*k2-18*pi*k0+24*k0)/(6*k0**3)
	c2 = -8*(2*pi*k2-9*pi**2+24)/(pi**2*k0**2)
	a4 = -(60*pi**2*k0*k4-60*pi**2*k2**2-240*pi**2*k2
		-240*pi*k2+270*pi**3*k2-243*pi**4-480*pi-64*pi**2
		+192+540*pi**3)/(180*pi*(-8+3*pi**2))
	return {"k0": k0, "k2": k2, "k4": k4, "a0": a0, "a2": a2,
		"a4": a4, "b0": b0, "c0": c0, "c2": c2}


def base_branch(k2: mp.mpf = mp.mpf(0),
		k4: mp.mpf = mp.mpf(0)) -> tuple[MPS, MPS, list[MPS]]:
	bc = branch_coefficients(k2, k4)
	u = MPS.monomial(1)
	eps = MPS.monomial(3)
	kfun = MPS.scalar(bc["k0"])+MPS.monomial(2, bc["k2"])+MPS.monomial(4, bc["k4"])
	afun = MPS.scalar(bc["a0"])+MPS.monomial(2, bc["a2"])+MPS.monomial(4, bc["a4"])
	bfun = MPS.scalar(bc["b0"])
	cfun = MPS.scalar(bc["c0"])+MPS.monomial(2, bc["c2"])
	kd = u*kfun
	kn = kd+MPS.monomial(5)*cfun
	p1 = MPS.scalar(mp.pi/2)+MPS.monomial(2)*afun
	p3 = MPS.scalar(mp.pi/4)+MPS.monomial(2)*bfun
	x1 = eps*p1/kd
	x2 = MPS.scalar(mp.mpf("0.5"))-eps*p3/kd
	edges = [x1, x2, 1-x2, 1-x1]
	return kd, kn, edges


def directional_f_derivative(direction: list[mp.mpf], k2: mp.mpf) -> list[MPS]:
	kd, kn, edge_values = base_branch(k2)
	edges_x = [DL(value, MPS.scalar(direction[i])) for i, value in enumerate(edge_values)]
	edges_0 = [DL(value, MPS.scalar(0)) for value in edge_values]
	sec_dx_d, _, _ = spectral_data(DL(kd, MPS.scalar(0)), edges_x)
	sec_dk_d, _, _ = spectral_data(DL(kd, MPS.scalar(1)), edges_0)
	sec_dx_n, _, _ = spectral_data(DL(kn, MPS.scalar(0)), edges_x)
	sec_dk_n, _, _ = spectral_data(DL(kn, MPS.scalar(1)), edges_0)
	dkd = -sec_dx_d.d/sec_dk_d.d
	dkn = -sec_dx_n.d/sec_dk_n.d
	_, yd, nd = spectral_data(DL(kd, dkd), edges_x)
	_, yn, nn = spectral_data(DL(kn, dkn), edges_x)
	lamd = DL(kd, dkd)**2
	lamn = DL(kn, dkn)**2
	out: list[MPS] = []
	for row in range(4):
		frow = (lamd*yd[row]**2/nd-lamn*yn[row]**2/nn)/lamn
		out.append(frow.d)
	return out


def full_normalized_jacobian(k2: mp.mpf) -> list[list[MPS]]:
	rvalue = MPS.monomial(-6)
	jumps = [1-rvalue, rvalue-1, 1-rvalue, rvalue-1]
	columns: list[list[MPS]] = []
	for col in range(4):
		direction = [mp.mpf(1) if i == col else mp.mpf(0) for i in range(4)]
		df = directional_f_derivative(direction, k2)
		columns.append([df[row]/jumps[row] for row in range(4)])
	return [[columns[col][row] for col in range(4)] for row in range(4)]


def project(matrix: list[list[MPS]], basis: list[list[mp.mpf]]) -> list[list[MPS]]:
	# basis contains two four-component column vectors.
	out = [[MPS.scalar(0), MPS.scalar(0)], [MPS.scalar(0), MPS.scalar(0)]]
	for i in range(2):
		for j in range(2):
			value = MPS.scalar(0)
			for row in range(4):
				for col in range(4):
					value = value+basis[i][row]*matrix[row][col]*basis[j][col]
			out[i][j] = value
	return out


def leading(series: MPS) -> tuple[int, mp.mpf]:
	for power in range(MIN_ORDER, MAX_ORDER+1):
		coefficient = series.coefficient(power)
		if abs(coefficient) > VISIBLE:
			return power, coefficient
	raise ValueError("series vanishes through the retained order")


def determinant(matrix: list[list[MPS]]) -> MPS:
	return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]


def significant_odd_max(series: MPS, through: int) -> mp.mpf:
	return max((abs(series.coefficient(power)) for power in range(MIN_ORDER, through+1)
		if power % 2), default=mp.mpf(0))


def summarize(matrix: list[list[MPS]], expected_power: int,
		expected_coefficient: mp.mpf) -> dict[str, object]:
	det = determinant(matrix)
	power, coefficient = leading(det)
	entry_windows = []
	for i in range(2):
		row = []
		for j in range(2):
			entry_power, _ = leading(matrix[i][j])
			row.append({str(p): mp.nstr(matrix[i][j].coefficient(p), 55)
				for p in range(entry_power, entry_power+5)})
		entry_windows.append(row)
	return {
		"entry_leads": [[{"power": leading(matrix[i][j])[0],
			"coefficient": mp.nstr(leading(matrix[i][j])[1], 60)}
			for j in range(2)] for i in range(2)],
		"entry_windows": entry_windows,
		"determinant": {
			"power": power,
			"coefficient": mp.nstr(coefficient, 80),
			"expected_power": expected_power,
			"expected_coefficient": mp.nstr(expected_coefficient, 80),
			"coefficient_ratio": mp.nstr(coefficient/expected_coefficient, 80),
			"largest_odd_coefficient_through_lead": mp.nstr(
				significant_odd_max(det, max(power, expected_power)), 12),
			"window": {str(p): mp.nstr(det.coefficient(p), 55)
				for p in range(expected_power-4, expected_power+3)},
		},
	}


def compute(k2: mp.mpf) -> dict[str, object]:
	bc = branch_coefficients(k2)
	k0 = bc["k0"]
	sq2 = mp.sqrt(2)
	bo = [[1/sq2, 0, 0, -1/sq2], [0, 1/sq2, -1/sq2, 0]]
	qp = [[1/sq2, 0, 0, 1/sq2], [0, -1/sq2, -1/sq2, 0]]
	jac = full_normalized_jacobian(k2)
	kp = project(jac, qp)
	ko = project(jac, bo)
	return {
		"branch": {name: mp.nstr(value, 70) for name, value in bc.items()},
		"Kp_odd": summarize(kp, 20, 128*k0**2/mp.pi**2),
		"Ko": summarize(ko, 26, 2048*k0**2/mp.pi**4),
	}


def main() -> None:
	# A second arbitrary value tests that the leading determinants do not depend
	# on the free even coefficient k2 left by the lower-order cascade.
	results = {
		"k2_zero": compute(mp.mpf(0)),
		"k2_one_third": compute(mp.mpf(1)/3),
	}
	print(json.dumps(results, indent=2))


if __name__ == "__main__":
	main()
