import math
from collections import Counter

import numpy as np
from scipy.optimize import least_squares


SEED = 20260901
ALPHA_MIN = 0.02
ALPHA_MAX = math.pi - 0.02
BETA_MIN = 0.02
BETA_MAX = 1.5 * math.pi - 0.02
THETA_MIN = 0.02
THETA_MAX = math.pi / 2.0 - 0.02
C_MIN = 0.10
C_MAX = 0.99
M_MIN = 1.01
M_MAX = 40.0


def phase_data(m, c, alpha, beta, theta):
	M = m * m
	C = math.cos(theta)
	S = math.sin(theta)
	s = math.sin(c * theta)
	Cc = math.cos(c * theta)
	X = C * math.cos(beta) - m * S * math.sin(beta)
	Z = S * math.cos(beta) + C * math.sin(beta) / m
	Y = s * math.cos(c * beta) + m * Cc * math.sin(c * beta)
	T = Cc * math.cos(c * beta) - s * math.sin(c * beta) / m
	F3 = X * math.cos(alpha) - Z * math.sin(alpha)
	F2 = Y * math.cos(c * alpha) + T * math.sin(c * alpha)
	Fband = Y + s * X / C
	u = math.tan(theta)
	v = math.tan(c * theta)
	x = 1.0 / math.tan(alpha)
	y = 1.0 / math.tan(c * alpha)
	rho = (1.0 + M * x * x) / (1.0 + M * y * y)
	H0 = u * v * (1.0 + v * v) * (1.0 + M * u * u)
	H0 += c * (1.0 + u * u) * (M + v * v)
	E = M * c * u * (M - 1.0) * (u * u * v * v - 1.0) ** 2
	E /= (M + v * v) * H0
	q = x - c * rho * y
	Lalpha = 1.0 / math.sin(c * alpha) ** 2
	Lalpha -= c * c / math.sin(alpha) ** 2
	A = s * s * X * X * Lalpha
	B = s * s * X * X
	B *= m * Lalpha - (m - 1.0 / m) * (1.0 - c * c)
	H = C * C - c * c * s * s
	Js = lambda z: z / 2.0 - math.sin(2.0 * z) / 4.0
	Jc = lambda z: z / 2.0 + math.sin(2.0 * z) / 4.0
	J = lambda a, b, z: a * a * Jc(z) + b * b * Js(z) + a * b * math.sin(z) ** 2
	I3 = M * X * X * Js(alpha) / math.sin(alpha) ** 2
	I3 += m * J(C, -m * S, beta) + M * Jc(theta)
	I2 = M * Y * Y * Js(c * alpha) / math.sin(c * alpha) ** 2
	I2 += m * J(s, m * Cc, c * beta) + M * Js(c * theta)
	MassResidual = C * C * I2 - c ** 3 * s * s * I3
	delta3 = math.atan(C / (m * S))
	delta2 = math.pi - math.atan(s / (m * Cc))
	Modal = delta3 < beta < delta3 + math.pi and 0.0 < c * beta < delta2
	p = 2.0 * (alpha + m * beta + theta)
	a = alpha / p
	b = (alpha + m * beta) / p
	Reconstruction = 0.0 < a < b < 0.5
	Orientation = X < 0.0 and Y > 0.0
	return {
		"spectral_residuals": np.array([F3, F2, Fband]),
		"mass_residual": MassResidual,
		"mass_scale": max(1.0, I2 + I3),
		"q_minus_E": q - E,
		"A": A,
		"B": B,
		"H": H,
		"modal": Modal,
		"reconstruction": Reconstruction,
		"orientation": Orientation,
	}


def sign_code(value, tolerance=1.0e-8):
	if value > tolerance:
		return "+"
	if value < -tolerance:
		return "-"
	return "0"


def valid_phase(data):
	return data["modal"] and data["reconstruction"] and data["orientation"]


def scan_spectral_band(rng):
	Solutions = []
	MGrid = np.unique(np.append(np.geomspace(M_MIN, M_MAX, 12), [1.4, 2.2, 5.0, 10.0]))
	CGrid = np.unique(np.append(np.linspace(C_MIN, C_MAX, 12), [0.66, 0.67, 0.68, 0.80]))
	Lower = np.array([ALPHA_MIN, BETA_MIN, THETA_MIN])
	Upper = np.array([ALPHA_MAX, BETA_MAX, THETA_MAX])
	for m in MGrid:
		for c in CGrid:
			Initials = [
				np.array([math.pi - 0.05, 0.05, math.pi / 2.0 - 0.05]),
			]
			Initials.extend(Lower + (Upper - Lower) * rng.random(3) for _ in range(3))
			for Initial in Initials:
				Result = least_squares(
					lambda z: phase_data(m, c, *z)["spectral_residuals"],
					Initial,
					bounds=(Lower, Upper),
					max_nfev=350,
					xtol=1.0e-11,
					ftol=1.0e-11,
					gtol=1.0e-11,
				)
				Data = phase_data(m, c, *Result.x)
				if np.linalg.norm(Result.fun, ord=np.inf) < 1.0e-8 and valid_phase(Data):
					Solutions.append((m, c, *Result.x, Data))
	return Solutions


def w11_regression():
	h = math.pi / 5.0
	k = math.cos(2.0 * h)
	m = (1.0 - k) / k
	c = 4.0 * h / math.pi
	Data = phase_data(m, c, math.pi / 4.0, math.pi, math.pi / 4.0)
	Residual = np.linalg.norm(Data["spectral_residuals"], ord=np.inf)
	Chamber = tuple(sign_code(Data[key]) for key in ("A", "B", "H"))
	print(f"w11_regression_residual={Residual:.17g}")
	print(f"w11_regression_q_minus_E={Data['q_minus_E']:.17g}")
	print(f"w11_regression_chamber={Chamber}")
	print(f"w11_regression_mass_residual={Data['mass_residual']:.17g}")


def scan_complete(rng):
	Solutions = []
	MGrid = np.geomspace(M_MIN, M_MAX, 14)
	Lower = np.array([C_MIN, ALPHA_MIN, BETA_MIN, THETA_MIN])
	Upper = np.array([C_MAX, ALPHA_MAX, BETA_MAX, THETA_MAX])
	for m in MGrid:
		for _ in range(12):
			Initial = Lower + (Upper - Lower) * rng.random(4)
			def residual(z):
				Data = phase_data(m, *z)
				return np.append(
					Data["spectral_residuals"],
					Data["mass_residual"] / Data["mass_scale"],
				)
			Result = least_squares(
				residual,
				Initial,
				bounds=(Lower, Upper),
				max_nfev=700,
				xtol=1.0e-11,
				ftol=1.0e-11,
				gtol=1.0e-11,
			)
			Data = phase_data(m, *Result.x)
			if np.linalg.norm(Result.fun, ord=np.inf) < 2.0e-8 and valid_phase(Data):
				Solutions.append((m, *Result.x, Data))
	return Solutions


def summarize(Spectral, Complete):
	SpectralPositive = [row for row in Spectral if row[-1]["q_minus_E"] > 1.0e-7]
	MixedPositive = []
	Chambers = Counter()
	for row in SpectralPositive:
		Data = row[-1]
		Chamber = tuple(sign_code(Data[key]) for key in ("A", "B", "H"))
		Chambers[Chamber] += 1
		if len(set(Chamber)) > 1:
			MixedPositive.append(row)
	CompletePositive = [row for row in Complete if row[-1]["q_minus_E"] > 1.0e-7]
	MixedMargins = [row[-1]["q_minus_E"] for row in Spectral if len({
		sign_code(row[-1]["A"]),
		sign_code(row[-1]["B"]),
		sign_code(row[-1]["H"]),
	}) > 1]
	CompleteMargins = [row[-1]["q_minus_E"] for row in Complete]
	def print_row(Label, Row):
		Data = Row[-1]
		Coordinates = ",".join(f"{value:.12g}" for value in Row[:-1])
		SpectralResidual = np.linalg.norm(Data["spectral_residuals"], ord=np.inf)
		NormalizedMass = Data["mass_residual"] / Data["mass_scale"]
		print(f"{Label}_m_c_alpha_beta_theta={Coordinates}")
		print(f"{Label}_q_minus_E={Data['q_minus_E']:.17g}")
		print(f"{Label}_A_B_H={Data['A']:.12g},{Data['B']:.12g},{Data['H']:.12g}")
		print(f"{Label}_spectral_residual={SpectralResidual:.17g}")
		print(f"{Label}_normalized_mass_residual={NormalizedMass:.17g}")
	print("status=EVIDENCE")
	print(f"seed={SEED}")
	print(f"spectral_band_raw_solutions={len(Spectral)}")
	print(f"spectral_band_q_gt_E={len(SpectralPositive)}")
	print(f"spectral_band_q_gt_E_mixed={len(MixedPositive)}")
	print(f"spectral_band_q_gt_E_chambers={dict(Chambers)}")
	print(f"complete_raw_solutions={len(Complete)}")
	print(f"complete_q_gt_E={len(CompletePositive)}")
	if MixedMargins:
		print(f"max_mixed_q_minus_E={max(MixedMargins):.17g}")
		MixedRows = [row for row in Spectral if len({
			sign_code(row[-1]["A"]),
			sign_code(row[-1]["B"]),
			sign_code(row[-1]["H"]),
		}) > 1]
		print_row("closest_mixed", max(MixedRows, key=lambda row: row[-1]["q_minus_E"]))
	if CompleteMargins:
		print(f"max_complete_q_minus_E={max(CompleteMargins):.17g}")
		print_row("closest_complete", max(Complete, key=lambda row: row[-1]["q_minus_E"]))
	for ChamberName, Chamber in (("positive", ("+", "+", "+")), ("negative", ("-", "-", "-"))):
		Rows = [row for row in SpectralPositive if tuple(
			sign_code(row[-1][key]) for key in ("A", "B", "H")
		) == Chamber]
		if Rows:
			print_row(f"q_gt_E_{ChamberName}", max(Rows, key=lambda row: row[-1]["q_minus_E"]))
	print("proof_claim=false")


def main():
	Rng = np.random.default_rng(SEED)
	w11_regression()
	Spectral = scan_spectral_band(Rng)
	Complete = scan_complete(Rng)
	summarize(Spectral, Complete)


if __name__ == "__main__":
	main()
