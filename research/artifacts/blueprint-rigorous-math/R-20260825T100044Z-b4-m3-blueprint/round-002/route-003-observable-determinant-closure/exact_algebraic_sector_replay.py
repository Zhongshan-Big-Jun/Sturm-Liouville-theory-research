"""Coefficient-local exact replay for the two observable determinants.

The coefficient field is

    Q(p)[k,s] / (k**3 - 18*p + 48/p, s**2 - 2),

so every intermediate coefficient is reduced by the frozen seed identities.
No floating-point arithmetic is used.  The script reconstructs the branch,
mass normalizations, Wronskians, dynamic-stiffness Green matrices, and the
reduced-resolvent finite parts directly from the closed residual convention.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.fields import field


HERE = Path(__file__).resolve()
REPO = HERE.parents[6]
CLOSED = REPO / "scripts/_gapn2_largeR_closed.py"
CLOSED_SHA256 = "e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4"
if hashlib.sha256(CLOSED.read_bytes()).hexdigest() != CLOSED_SHA256:
	raise SystemExit("frozen closed-residual hash mismatch")


# ---------------------------------------------------------------------------
# Exact coefficient field.  Cubic elements are x0+x1*k+x2*k^2 over Q(p).
# Quadratic elements are a+b*s with s^2=2.  The cubic inverse is the adjugate
# formula for k^3=alpha; hence there is no unproved symbolic simplification.
# ---------------------------------------------------------------------------

PF, p0 = field("p", QQ)
alpha = 18*p0 - 48/p0


class Cubic:
	__slots__ = ("x",)

	def __init__(self, x0=0, x1=0, x2=0):
		self.x = (PF(x0), PF(x1), PF(x2))

	@staticmethod
	def coerce(value):
		return value if isinstance(value, Cubic) else Cubic(value)

	def __bool__(self):
		return any(self.x)

	def __eq__(self, other):
		other = Cubic.coerce(other)
		return self.x == other.x

	def __hash__(self):
		return hash(self.x)

	def __neg__(self):
		return Cubic(*(-z for z in self.x))

	def __add__(self, other):
		other = Cubic.coerce(other)
		return Cubic(*(a+b for a, b in zip(self.x, other.x)))

	__radd__ = __add__

	def __sub__(self, other):
		return self + (-Cubic.coerce(other))

	def __rsub__(self, other):
		return Cubic.coerce(other) - self

	def __mul__(self, other):
		other = Cubic.coerce(other)
		a0, a1, a2 = self.x
		b0, b1, b2 = other.x
		return Cubic(
			a0*b0 + alpha*(a1*b2+a2*b1),
			a0*b1+a1*b0+alpha*a2*b2,
			a0*b2+a1*b1+a2*b0,
		)

	__rmul__ = __mul__

	def inv(self):
		x0, x1, x2 = self.x
		det = x0**3 + alpha*x1**3 + alpha**2*x2**3 - 3*alpha*x0*x1*x2
		if not det:
			raise ZeroDivisionError("zero cubic element")
		return Cubic(
			(x0**2-alpha*x1*x2)/det,
			(alpha*x2**2-x0*x1)/det,
			(x1**2-x0*x2)/det,
		)

	def __truediv__(self, other):
		return self*Cubic.coerce(other).inv()

	def __rtruediv__(self, other):
		return Cubic.coerce(other)/self

	def __pow__(self, power):
		power = int(power)
		if power < 0:
			return self.inv()**(-power)
		out, base = Cubic(1), self
		while power:
			if power & 1:
				out = out*base
			base = base*base
			power //= 2
		return out

	def as_expr(self):
		p, k = sp.symbols("p k")
		return sum(z.as_expr()*k**j for j, z in enumerate(self.x))


class Alg:
	"""a+b*s over the cubic field, with s^2=2."""

	__slots__ = ("a", "b")

	def __init__(self, a=0, b=0):
		self.a, self.b = Cubic.coerce(a), Cubic.coerce(b)

	@staticmethod
	def coerce(value):
		return value if isinstance(value, Alg) else Alg(value)

	def __bool__(self):
		return bool(self.a) or bool(self.b)

	def __eq__(self, other):
		other = Alg.coerce(other)
		return self.a == other.a and self.b == other.b

	def __hash__(self):
		return hash((self.a, self.b))

	def __neg__(self):
		return Alg(-self.a, -self.b)

	def __add__(self, other):
		if other.__class__.__name__ == "Series":
			return NotImplemented
		other = Alg.coerce(other)
		return Alg(self.a+other.a, self.b+other.b)

	__radd__ = __add__

	def __sub__(self, other):
		if other.__class__.__name__ == "Series":
			return NotImplemented
		return self + (-Alg.coerce(other))

	def __rsub__(self, other):
		return Alg.coerce(other) - self

	def __mul__(self, other):
		if other.__class__.__name__ == "Series":
			return NotImplemented
		other = Alg.coerce(other)
		return Alg(self.a*other.a+2*self.b*other.b, self.a*other.b+self.b*other.a)

	__rmul__ = __mul__

	def inv(self):
		den = (self.a*self.a-2*self.b*self.b).inv()
		return Alg(self.a*den, -self.b*den)

	def __truediv__(self, other):
		if other.__class__.__name__ == "Series":
			return NotImplemented
		return self*Alg.coerce(other).inv()

	def __rtruediv__(self, other):
		return Alg.coerce(other)/self

	def __pow__(self, power):
		power = int(power)
		if power < 0:
			return self.inv()**(-power)
		out, base = Alg(1), self
		while power:
			if power & 1:
				out = out*base
			base = base*base
			power //= 2
		return out

	def as_expr(self):
		s = sp.Symbol("s")
		return self.a.as_expr()+self.b.as_expr()*s


p = Alg(p0)
k = Alg(Cubic(0, 1, 0))
s = Alg(0, 1)


# Exact unit checks for the quotient-field implementation.
assert k**3 == 18*p-48/p
assert s**2 == 2
field_probe = 3+p+k+s+p*k+k*s+p*s
assert field_probe/field_probe == 1


# Four guard orders beyond the largest certified u^28 remainder threshold.
# This also permits an independent truncation-stability rerun by increasing
# the value without changing any mathematical formula.
ORDER = 34


class Series:
	"""Truncated exact Laurent series in u; powers >= ORDER are discarded."""

	__slots__ = ("c",)

	def __init__(self, coefficients=None):
		self.c = {}
		for power, value in (coefficients or {}).items():
			if power >= ORDER:
				continue
			value = Alg.coerce(value)
			if value:
				self.c[int(power)] = value

	@staticmethod
	def scalar(value):
		return Series({0: value})

	@staticmethod
	def coerce(value):
		return value if isinstance(value, Series) else Series.scalar(value)

	def coeff(self, power):
		return self.c.get(power, Alg())

	def lead_power(self):
		if not self.c:
			raise ZeroDivisionError("zero series")
		return min(self.c)

	def shift(self, power):
		return Series({j+power: z for j, z in self.c.items()})

	def __neg__(self):
		return Series({j: -z for j, z in self.c.items()})

	def __add__(self, other):
		other = Series.coerce(other)
		return Series({j: self.coeff(j)+other.coeff(j) for j in set(self.c)|set(other.c)})

	__radd__ = __add__

	def __sub__(self, other):
		return self + (-Series.coerce(other))

	def __rsub__(self, other):
		return Series.coerce(other)-self

	def __mul__(self, other):
		other = Series.coerce(other)
		out = {}
		for i, a in self.c.items():
			for j, b in other.c.items():
				if i+j < ORDER:
					out[i+j] = out.get(i+j, Alg())+a*b
		return Series(out)

	__rmul__ = __mul__

	def inv(self):
		m = self.lead_power()
		a0 = self.coeff(m)
		out = {0: 1/a0}
		for n in range(1, max(0, ORDER+m)):
			total = Alg()
			for j in range(1, n+1):
				total += self.coeff(m+j)*out.get(n-j, Alg())
			out[n] = -total/a0
		return Series({n-m: z for n, z in out.items()})

	def __truediv__(self, other):
		return self*Series.coerce(other).inv()

	def __rtruediv__(self, other):
		return Series.coerce(other)/self

	def __pow__(self, power):
		power = int(power)
		if power < 0:
			return self.inv()**(-power)
		out, base = Series.scalar(1), self
		while power:
			if power & 1:
				out = out*base
			base = base*base
			power //= 2
		return out


u = Series({1: 1})


def sin_cos(argument):
	constant = argument.coeff(0)
	delta = argument-constant
	centers = {
		Alg(0): (Alg(0), Alg(1)),
		p/4: (s/2, s/2),
		p/2: (Alg(1), Alg(0)),
		3*p/4: (s/2, -s/2),
		p: (Alg(0), Alg(-1)),
	}
	if constant not in centers:
		raise ValueError(f"unsupported trigonometric center {constant.as_expr()}")
	s0, c0 = centers[constant]
	if not delta.c:
		return Series.scalar(s0), Series.scalar(c0)
	valuation = delta.lead_power()
	sd, cd, power, factorial = Series.scalar(0), Series.scalar(1), Series.scalar(1), 1
	for n in range(1, ORDER//valuation+2):
		power *= delta
		factorial *= n
		term = power/factorial
		if n % 4 == 1:
			sd += term
		elif n % 4 == 3:
			sd -= term
		elif n % 4 == 2:
			cd -= term
		else:
			cd += term
	return s0*cd+c0*sd, c0*cd-s0*sd


def det2(matrix):
	return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]


def inv2(matrix):
	det = det2(matrix)
	return [[matrix[1][1]/det, -matrix[0][1]/det], [-matrix[1][0]/det, matrix[0][0]/det]]


def build():
	# Exact implicit-branch coefficients through v=u^2.  Their independent
	# residual check is printed below.
	K2 = (-272*p**2+576+81*p**4)/(30*p*(3*p**2-8))
	B2 = -(-272*p**2-480*p+576+180*p**3+81*p**4)/(30*p*k**2*(3*p**2-8))
	X0 = -(k**6-90*p*k**3+120*k**3-1620*p**2-3360+4320*p)/(360*k**2)
	X2 = (-306180*p**7-2462336*p**4-3465216-16896*p**2+3870720*p+698880*p**3+816480*p**5+413424*p**6+59049*p**8)/(37800*p**2*(3*p**2-8)**2)
	Y0 = 4*(p*k**3-96+36*p**2)/(3*p**2*k**2)
	Y2 = 2*(-792*p**2-160*p+1536+81*p**4)/(15*p**2*(3*p**2-8))

	K = k+K2*u**2
	B = 1/k+B2*u**2
	X = X0+X2*u**2
	Y = Y0+Y2*u**2
	q0 = (18*p-24-K**3)/(6*K)
	q = q0+X*u**2
	C = 16/(p*K)+Y*u**2
	eps = u**3
	k2 = K*u
	k3 = K*u+C*u**5
	ratio = k3/k2
	A = (2+q*u**2)/K
	p1 = p/2+A*u**2
	p3 = p/4+B*u**2
	p2 = k2/2-eps*(p1+p3)
	p1t, p2t, p3t = ratio*p1, ratio*p2, ratio*p3

	def mass_parts(wave, ph1, ph2, ph3, boundary):
		s1, c1 = sin_cos(ph1)
		s2, c2 = sin_cos(ph2)
		s3, c3 = sin_cos(ph3)
		sin2p1, _ = sin_cos(2*ph1)
		sin2p2, cos2p2 = sin_cos(2*ph2)
		sin2p3, _ = sin_cos(2*ph3)
		if boundary == "D":
			bc = -(eps*c2*s1/wave+s2*c1/wave)/s3
			m3 = bc**2*(ph3-sin2p3/2)/(2*wave*eps)
		else:
			bc = (eps*c2*s1/wave+s2*c1/wave)/c3
			m3 = bc**2*(ph3+sin2p3/2)/(2*wave*eps)
		m1 = (ph1-sin2p1/2)*eps/(2*wave**3)
		aa, bb = eps*s1/wave, c1/wave
		middle = (aa**2+bb**2)*ph2/(2*wave)+(aa**2-bb**2)*sin2p2/(4*wave)+aa*bb*(1-cos2p2)/(2*wave)
		return m1, m3, middle

	print("STAGE=masses", flush=True)
	m1d, m3d, mld = mass_parts(k2, p1, p2, p3, "D")
	m1n, m3n, mln = mass_parts(k3, p1t, p2t, p3t, "N")
	ID, IN = m1d+m3d+mld, m1n+m3n+mln

	# Frozen closed residuals, scaled exactly as in _gapn2_largeR_closed.py.
	s1, c1 = sin_cos(p1); s2, c2 = sin_cos(p2); s3, c3 = sin_cos(p3)
	s1t, c1t = sin_cos(p1t); s2t, c2t = sin_cos(p2t); s3t, c3t = sin_cos(p3t)
	s13, _ = sin_cos(p1+p3)
	E1 = c2*s13+s2*c3*c1/eps-eps*s3*s2*s1
	E2 = c2t*c1t*c3t-s3t*s2t*c1t/eps-s3t*c2t*s1t-eps*c3t*s2t*s1t
	E5 = ID*s1t**2-IN*s1**2
	E6 = s1*(eps*c2t+s2t*c1t/s1t)+eps*c2*s1+s2*c1
	residual = [E1.shift(-4), E2.shift(-4), E5.shift(-6), E6.shift(-7)]

	def left_values(wave):
		scale = wave/k2
		ph1, ph2 = scale*p1, scale*p2
		sa, ca = sin_cos(ph1); sb, cb = sin_cos(ph2)
		qh, ql = wave/eps, wave
		y1, dy1 = sa/qh, ca
		y2 = y1*cb+dy1*sb/ql
		dy2 = -ql*y1*sb+dy1*cb
		return [y1, y2], [dy1, dy2]

	def stiffness(wave, boundary):
		scale = wave/k2
		ph1, ph2, ph3 = scale*p1, scale*p2, scale*p3
		s1x, c1x = sin_cos(ph1); s2x, c2x = sin_cos(ph2); s3x, c3x = sin_cos(ph3)
		qh, ql = wave/eps, wave
		a11 = qh*c1x/s1x+ql*c2x/s2x
		a12 = -ql/s2x
		a22 = ql*c2x/s2x+(qh*c3x/s3x if boundary == "D" else -qh*s3x/c3x)
		return [[a11, a12], [a12, a22]]

	# The coefficient jets are in delta=spectral_wave/eigen_wave-1.
	def stiffness_jet(wave, phases, boundary):
		ph1, ph2, ph3 = phases
		qh, ql = wave/eps, wave

		def cot_jet(qv, ph):
			si, co = sin_cos(ph); cot, csc = co/si, 1/si
			return qv*cot, qv*(cot-ph*csc**2), qv*(-ph*csc**2+ph**2*csc**2*cot)

		def csc_jet(qv, ph):
			si, co = sin_cos(ph); csc, cot = 1/si, co/si
			return qv*csc, qv*(csc-ph*csc*cot), qv*(-ph*csc*cot+ph**2*csc*(cot**2+csc**2)/2)

		def tan_jet(qv, ph):
			si, co = sin_cos(ph); tan, sec = si/co, 1/co
			return qv*tan, qv*(tan+ph*sec**2), qv*(ph*sec**2+ph**2*sec**2*tan)

		h1, l2, x2 = cot_jet(qh, ph1), cot_jet(ql, ph2), csc_jet(ql, ph2)
		h3 = cot_jet(qh, ph3) if boundary == "D" else tan_jet(qh, ph3)
		out = []
		for j in range(3):
			out.append([[h1[j]+l2[j], -x2[j]], [-x2[j], l2[j]+h3[j] if boundary == "D" else l2[j]-h3[j]]])
		return out

	def reduced_green(wave, phases, boundary):
		a0, a1, a2 = stiffness_jet(wave, phases, boundary)
		d1 = a1[0][0]*a0[1][1]+a0[0][0]*a1[1][1]-2*a0[0][1]*a1[0][1]
		d2 = a2[0][0]*a0[1][1]+a1[0][0]*a1[1][1]+a0[0][0]*a2[1][1]-a1[0][1]**2-2*a0[0][1]*a2[0][1]
		n0 = [[a0[1][1], -a0[0][1]], [-a0[1][0], a0[0][0]]]
		n1 = [[a1[1][1], -a1[0][1]], [-a1[1][0], a1[0][0]]]
		# A(delta)^-1=L_-1/delta+L_0+O(delta), whereas
		# (wave^2-spectral_wave^2)^-1=-1/(2 wave^2 delta)+1/(4 wave^2)+...
		# Therefore the eigenprojection-subtracted finite part is L_0+L_-1/2.
		return [[n1[i][j]/d1-n0[i][j]*d2/d1**2+n0[i][j]/(2*d1) for j in range(2)] for i in range(2)]

	print("STAGE=ordinary_Green", flush=True)
	yd, dyd = left_values(k2); yn, dyn = left_values(k3)
	W = [yd[j]*dyn[j]-yn[j]*dyd[j] for j in range(2)]
	GD, GN = inv2(stiffness(k3, "D")), inv2(stiffness(k2, "N"))
	c = k2/k3
	d = [c*w*s1/s1t*u**6/(1-u**6)/ID for w in W]  # W<0, hence -|W|=W.
	Kp = [[Series.scalar(0), Series.scalar(0)] for _ in range(2)]
	for i in range(2):
		for j in range(2):
			e = 1 if i == j else -1
			Kp[i][j] = k2**2/ID*yd[i]*(e*GD[i][j]-c**2*GN[i][j])*yd[j]
			if i == j:
				Kp[i][j] += d[i]

	print("STAGE=reduced_Green", flush=True)
	GtD = reduced_green(k2, (p1, p2, p3), "D")
	GtN = reduced_green(k3, (p1t, p2t, p3t), "N")
	r = 2*k2**2*(k3**2-k2**2)/k3**4
	Ko = [[Series.scalar(0), Series.scalar(0)] for _ in range(2)]
	for i in range(2):
		for j in range(2):
			e = 1 if i == j else -1
			Ko[i][j] = k2**2/ID*yd[i]*(GtN[i][j]-c**2*e*GtD[i][j])*yd[j]
			Ko[i][j] += r/(2*ID**2)*(1 if i == 0 else -1)*(1 if j == 0 else -1)*yd[i]**2*yd[j]**2
			if i == j:
				Ko[i][j] += d[i]

	return {
		"m3_difference": m3d-m3n,
		"W1": W[0], "W2": W[1],
		"residual": residual,
		"Kp11": Kp[0][0], "Kp12": Kp[0][1], "Kp22": Kp[1][1],
		"det_Kp": det2(Kp),
		"Ko11": Ko[0][0], "Ko12": Ko[0][1], "Ko22": Ko[1][1],
		"det_Ko": det2(Ko),
	}


def render(value):
	expr = value.as_expr().subs({sp.Symbol("p"): sp.pi, sp.Symbol("k"): sp.Symbol("kappa"), sp.Symbol("s"): sp.sqrt(2)})
	return sp.factor(expr)


def first(label, series):
	power = series.lead_power()
	print(f"{label}=u^{power}*({render(series.coeff(power))})", flush=True)


if __name__ == "__main__":
	data = build()
	print("STAGE=certificate", flush=True)
	first("M3_DIFFERENCE", data["m3_difference"])
	first("W1", data["W1"]); first("W2", data["W2"])
	for index, residual in enumerate(data["residual"], 1):
		for power in (0, 1, 2, 3):
			assert not residual.coeff(power), f"G{index} residual coefficient u^{power} nonzero"
		first(f"G{index}_TRUNCATION_REMAINDER", residual)
	first("KP11", data["Kp11"]); first("KP12", data["Kp12"]); first("KP22", data["Kp22"])
	first("DET_KP_ODD", data["det_Kp"])
	first("KO11", data["Ko11"]); first("KO12", data["Ko12"]); first("KO22", data["Ko22"])
	first("DET_KO", data["det_Ko"])
