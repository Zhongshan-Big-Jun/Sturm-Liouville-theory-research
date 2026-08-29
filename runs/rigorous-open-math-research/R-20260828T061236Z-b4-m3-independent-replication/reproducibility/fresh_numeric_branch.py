"""Independent high-precision root search for the exact four-equation branch."""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".deps"))

import mpmath as mp


mp.mp.dps = 55


def mass(k, p1, p2, p3, eps, mode):
	base = eps * mp.cos(p2) * mp.sin(p1) / k + mp.sin(p2) * mp.cos(p1) / k
	if mode == "D":
		bc = -base / mp.sin(p3)
		m3 = bc**2 * (p3 - mp.sin(2 * p3) / 2) / (2 * k * eps)
	else:
		bc = base / mp.cos(p3)
		m3 = bc**2 * (p3 + mp.sin(2 * p3) / 2) / (2 * k * eps)
	m1 = (p1 - mp.sin(2 * p1) / 2) * eps / (2 * k**3)
	a = eps * mp.sin(p1) / k
	b = mp.cos(p1) / k
	ml = ((a*a + b*b) * p2 / (2*k)
		+ (a*a - b*b) * mp.sin(2*p2) / (4*k)
		+ a*b * (1 - mp.cos(2*p2)) / (2*k))
	return m1 + m3 + ml


def equations(u, kval, aval, bval, cval):
	eps = u**3
	kd = kval * u
	kn = kval * u + cval * u**5
	p1d = mp.pi / 2 + aval * u**2
	p3d = mp.pi / 4 + bval * u**2
	ratio = kn / kd
	p1n = ratio * p1d
	p3n = ratio * p3d
	p2d = kd / 2 - eps * (p1d + p3d)
	p2n = kn / 2 - eps * ratio * (p1d + p3d)
	e1 = (mp.cos(p2d) * mp.sin(p1d + p3d)
		+ mp.sin(p2d) * mp.cos(p3d) * mp.cos(p1d) / eps
		- eps * mp.sin(p3d) * mp.sin(p2d) * mp.sin(p1d))
	e2 = (mp.cos(p2n) * mp.cos(p1n) * mp.cos(p3n)
		- mp.sin(p3n) * mp.sin(p2n) * mp.cos(p1n) / eps
		- mp.sin(p3n) * mp.cos(p2n) * mp.sin(p1n)
		- eps * mp.cos(p3n) * mp.sin(p2n) * mp.sin(p1n))
	id_ = mass(kd, p1d, p2d, p3d, eps, "D")
	in_ = mass(kn, p1n, p2n, p3n, eps, "N")
	e5 = id_ * mp.sin(p1n)**2 - in_ * mp.sin(p1d)**2
	e6 = (mp.sin(p1d) * (eps * mp.cos(p2n) + mp.sin(p2n) * mp.cos(p1n) / mp.sin(p1n))
		+ eps * mp.cos(p2d) * mp.sin(p1d) + mp.sin(p2d) * mp.cos(p1d))
	return e1, e2, e5 / u**4, e6 / u**3


def conditioned_equations(u, kval, aval, bval, cval):
	e1, e2, e5_u4, e6_u3 = equations(u, kval, aval, bval, cval)
	return (
		e1 - e2,
		(e1 + e2) / u**2,
		e5_u4 / u**2,
		(e6_u3 - 2*mp.sqrt(2)*e1) / u**2,
	)


def derived(u, root):
	kval, aval, bval, cval = root
	eps = u**3
	kd = kval*u
	kn = kval*u + cval*u**5
	p1 = mp.pi/2 + aval*u**2
	p3 = mp.pi/4 + bval*u**2
	x1 = eps*p1/kd
	x2 = mp.mpf("0.5") - eps*p3/kd
	return {
		"K": kval,
		"A": aval,
		"B": bval,
		"C": cval,
		"k2": kd,
		"k3": kn,
		"x1": x1,
		"x2": x2,
		"gap_times_R": (kn**2-kd**2)/u**6,
		"residual": max(abs(v) for v in equations(u, *root)),
	}


def find_roots(u):
	roots = []
	for kg, bg, cg in itertools.product(
		(mp.mpf("2.4"), mp.mpf("3.0"), mp.mpf("3.6"), mp.mpf("4.5"), mp.mpf("5.5")),
		(mp.mpf("-2.0"), mp.mpf("-1.0"), mp.mpf("0.0"), mp.mpf("0.5"), mp.mpf("1.5")),
		(mp.mpf("0.5"), mp.mpf("1.5"), mp.mpf("2.5"))):
		ag = 2/kg
		try:
			root = mp.findroot(lambda kk, aa, bb, cc: equations(u, kk, aa, bb, cc),
				(kg, ag, bg, cg), tol=mp.mpf("1e-50"), maxsteps=80)
		except (ValueError, ZeroDivisionError):
			continue
		root = tuple(mp.mpf(v) for v in root)
		if not all(mp.isfinite(v) for v in root):
			continue
		data = derived(u, root)
		if not (root[0] > 0 and root[3] > 0 and 0 < data["x1"] < data["x2"] < mp.mpf("0.5")):
			continue
		if data["residual"] > mp.mpf("1e-30"):
			continue
		if any(max(abs(root[i]-old[i]) for i in range(4)) < mp.mpf("1e-25") for old in roots):
			continue
		roots.append(root)
	return roots


def serializable(value):
	if isinstance(value, dict):
		return {key: serializable(val) for key, val in value.items()}
	if isinstance(value, list):
		return [serializable(val) for val in value]
	if isinstance(value, mp.mpf):
		return mp.nstr(value, 50)
	return value


def main():
	u = mp.mpf(sys.argv[1]) if len(sys.argv) > 1 else mp.mpf("0.25")
	if len(sys.argv) == 6:
		seed = tuple(mp.mpf(v) for v in sys.argv[2:6])
		root = tuple(mp.findroot(lambda kk, aa, bb, cc: conditioned_equations(u, kk, aa, bb, cc),
			seed, tol=mp.mpf("1e-40"), maxsteps=100))
		print(json.dumps(serializable({"u": u, "seed": list(seed), "root": derived(u, root)}), indent=2))
		return
	roots = find_roots(u)
	print(json.dumps(serializable({"u": u, "roots": [derived(u, r) for r in roots]}), indent=2))


if __name__ == "__main__":
	main()
