"""Author-only exact algebra and manuscript structure checks; no repository import."""
from pathlib import Path
import datetime
import hashlib
import json
import platform
import re
import sympy as sp

Root = Path(__file__).resolve().parent
Results = []


def check(Name, Condition):
	if not bool(Condition):
		raise RuntimeError(Name)
	Results.append({"name": Name, "result": "satisfied"})


def zero_matrix(Matrix):
	return all(sp.cancel(Item) == 0 for Item in Matrix)


def mirror_basis(N):
	Unit = sp.eye(2 * N)
	Be = sp.Matrix.hstack(*[(Unit[:, J] + Unit[:, 2 * N - 1 - J]) / sp.sqrt(2) for J in range(N)])
	Bo = sp.Matrix.hstack(*[(Unit[:, J] - Unit[:, 2 * N - 1 - J]) / sp.sqrt(2) for J in range(N)])
	S = sp.diag(*[(-1) ** J for J in range(2 * N)])
	E = sp.diag(*[(-1) ** J for J in range(N)])
	P = sp.zeros(2 * N)
	for J in range(2 * N):
		P[J, 2 * N - 1 - J] = 1
	return Be, Bo, S, E, P


def symmetric_two(Prefix):
	A, B, C = sp.symbols(Prefix + "11 " + Prefix + "12 " + Prefix + "22")
	return sp.Matrix([[A, B], [B, C]])


for N in range(1, 5):
	Be, Bo, S, E, P = mirror_basis(N)
	K = sp.Matrix(2 * N, 2 * N, sp.symbols("k0:" + str(4 * N * N)))
	check("arbitrary_matrix_odd_swap_n" + str(N), zero_matrix(Bo.T * S * K * S * Bo - E * Be.T * K * Be * E))
	check("arbitrary_matrix_even_swap_n" + str(N), zero_matrix(Be.T * S * K * S * Be - E * Bo.T * K * Bo * E))
	Witness = sp.zeros(2 * N)
	Witness[0, 0] = 1
	check("noncommuting_matrix_witness_n" + str(N), not zero_matrix(Witness * P - P * Witness))

Be, Bo, S, E, P = mirror_basis(2)
a, b, eta = sp.symbols("a b eta", positive=True)
u1, u2, d1, d2 = sp.symbols("u1 u2 d1 d2", real=True)
Delta = b - a
UVector = sp.Matrix([u1, u2, -u2, -u1])
U4 = sp.diag(*UVector)
U = sp.diag(u1, u2)
Q = UVector.applyfunc(lambda Value: Value ** 2)
q = sp.Matrix([u1 ** 2, u2 ** 2])
D4 = sp.diag(d1, d2, d2, d1)
D2 = sp.diag(d1, d2)
GN, GD = symmetric_two("N"), symmetric_two("D")
GtD, GtN = symmetric_two("tD"), symmetric_two("tN")
Gamma2 = Be * GN * Be.T + Bo * GtD * Bo.T
Gamma3 = Be * GtN * Be.T + Bo * GD * Bo.T
Tau = 2 * a * Delta / b ** 2
K = D4 + Tau * S * Q * Q.T * S + 2 * a * U4 * (Gamma3 - a / b * S * Gamma2 * S) * U4
Kp = D4 + Tau * Q * Q.T + 2 * a * U4 * (S * Gamma3 * S - a / b * Gamma2) * U4
M = 2 * a * Delta / b * Q * Q.T - 2 * a ** 2 * U4 * Gamma2 * U4 + 2 * a * b * S * U4 * Gamma3 * U4 * S
check("FH_M_to_raw_K", zero_matrix(D4 + S * M * S / b - K))
check("Kp_conjugation", zero_matrix(Kp - S * K * S))
check("raw_K_mirror_commutation", zero_matrix(P * K - K * P))
check("cross_Green_KpOdd", zero_matrix(Bo.T * Kp * Bo - (D2 + 2 * a * U * (E * GD * E - a / b * GN) * U)))
check("reduced_Green_rawKo", zero_matrix(Bo.T * K * Bo - (D2 + 4 * a * Delta / b ** 2 * E * q * q.T * E + 2 * a * U * (GtN - a / b * E * GtD * E) * U)))
check("normalization_rank_not_zero_rawKo", zero_matrix(Bo.T * S * Q - sp.sqrt(2) * E * q) and not zero_matrix(E * q))
check("normalization_rank_zero_KpOdd", zero_matrix(Bo.T * Q))
check("half_kernel_sqrt2_projection", zero_matrix(Be.T * (Be * sp.Matrix([u1, u2])) - sp.Matrix([u1, u2])))
check("half_normalized_rank_coefficient", zero_matrix(4 * a * Delta / b ** 2 * E * q * q.T * E - a * Delta / b ** 2 * E * (2 * q) * (2 * q).T * E))
for SigmaSign in (1, -1):
	Sigma = SigmaSign * eta * S
	Fprime = b * Sigma * D4
	J = (Fprime + M * Sigma) / b
	H = -Sigma * Fprime - Sigma * M * Sigma
	check("Hessian_sign_" + str(SigmaSign), zero_matrix(H + b * eta ** 2 * K))
	check("jump_symmetrization_" + str(SigmaSign), zero_matrix(Sigma.inv() * J - K))
check("symmetric_coordinate_factor_two", zero_matrix((sp.sqrt(2) * Bo).T * (-b * eta ** 2 * K) * (sp.sqrt(2) * Bo) + 2 * b * eta ** 2 * (Bo.T * K * Bo)))

lam, si, sj, ui, uj, upi, gij, dij = sp.symbols("lam si sj ui uj upi gij dij", real=True)
LambdaPrimeJ = lam * sj * uj ** 2
UPrimeJAtI = sj * uj ** 2 * ui / 2 - lam * sj * uj * gij
DerivedSecond = LambdaPrimeJ * si * ui ** 2 + lam * si * 2 * ui * (UPrimeJAtI + dij * upi)
ExpectedSecond = 2 * dij * lam * si * ui * upi + 2 * lam * si * sj * ui ** 2 * uj ** 2 - 2 * lam ** 2 * si * sj * ui * uj * gij
check("normalization_half_factor_in_second_variation", sp.expand(DerivedSecond - ExpectedSecond) == 0)
check("band_normalization_positive_coefficient", sp.cancel(2 * a * u1 ** 2 * u2 ** 2 - 2 * b * (a / b) ** 2 * u1 ** 2 * u2 ** 2 - 2 * a * Delta / b * u1 ** 2 * u2 ** 2) == 0)

t, h1, h2 = sp.symbols("t h1 h2", real=True)
AWeight = t * Delta / ((t - b) * (t - a))
BWeight = a / (t - a) + b / (t - b)
check("partial_fraction_A_weight", sp.cancel(b / (t - b) - a / (t - a) - AWeight) == 0)
for ModeParity in (1, -1):
	Mode = sp.Matrix([h1, h2, ModeParity * h2, ModeParity * h1])
	G = Mode * Mode.T
	Gbar = Mode * (P * Mode).T
	Tail = 2 * a * U4 * (S * G * S / (t - b) - a / b * G / (t - a)) * U4
	HOldE, HOldO = sp.zeros(2), sp.zeros(2)
	for I in range(2):
		for J in range(2):
			Factor = 2 * a / b * UVector[I] * UVector[J]
			if (I + J) % 2 == 0:
				HOldE[I, J] = Factor * (AWeight * G[I, J] + BWeight * Gbar[I, J])
				HOldO[I, J] = Factor * (AWeight * G[I, J] - BWeight * Gbar[I, J])
			else:
				HOldE[I, J] = Factor * (-BWeight * G[I, J] - AWeight * Gbar[I, J])
				HOldO[I, J] = Factor * (-BWeight * G[I, J] + AWeight * Gbar[I, J])
	check("oldHe_is_KpHe_mode_parity_" + str(ModeParity), zero_matrix(HOldE - Be.T * Tail * Be))
	check("oldHo_is_KpHo_mode_parity_" + str(ModeParity), zero_matrix(HOldO - Bo.T * Tail * Bo))
	check("rawHe_swaps_mode_parity_" + str(ModeParity), zero_matrix(Be.T * S * Tail * S * Be - E * HOldO * E))
	check("rawHo_swaps_mode_parity_" + str(ModeParity), zero_matrix(Bo.T * S * Tail * S * Bo - E * HOldE * E))
Nu = -2 * a * (a ** 2 + b ** 2) / (b ** 2 * Delta)
Gamma3Pair = -UVector * UVector.T / Delta
Gamma2Pair = a / b * S * UVector * UVector.T * S / Delta
PairTerm = 2 * a * U4 * (S * Gamma3Pair * S - a / b * Gamma2Pair) * U4
check("two_removed_modes_negative_rank", zero_matrix(PairTerm - Nu * S * Q * Q.T * S))
w = a * q
Ce = 4 * Delta / (a * b ** 2)
Co = -4 * (a ** 2 + b ** 2) / (a * b ** 2 * Delta)
check("KpEe_coefficient", zero_matrix(Be.T * (Tau * Q * Q.T) * Be - Ce * w * w.T))
check("KpEo_coefficient", zero_matrix(Bo.T * PairTerm * Bo - Co * E * w * w.T * E))
check("rawEe_swapped_negative_rank", zero_matrix(E * (Co * E * w * w.T * E) * E - Co * w * w.T))
check("rawEo_swapped_positive_rank", zero_matrix(E * (Ce * w * w.T) * E - Ce * E * w * w.T * E))
Z = sp.Matrix([1, -1]) / sp.sqrt(2)
BadE = -2 * Z * Z.T
BadM = sp.eye(2) + BadE
check("historical_minus_E_bound_counterexample", min((-BadE).eigenvals()) + 1 == 1 and sorted(BadM.eigenvals()) == [-1, 1])

Text = (Root / "analytic-repair.md").read_text()
Data = (Root / "analytic-repair.md").read_bytes()
check("no_C0_or_DEL_controls_except_LF_TAB", not any(Byte < 32 and Byte not in (9, 10) or Byte == 127 for Byte in Data))
check("no_legacy_math_delimiters", not any(Token in Text for Token in (r"\(", r"\)", r"\[", r"\]")))
Display = False
DisplayCount = 0
InlineCount = 0
MathParts = []
OutsideParts = []
Current = []
for Number, Line in enumerate(Text.splitlines(), 1):
	if Line.strip() == "$$":
		if Display:
			MathParts.append("\n".join(Current))
			Current = []
			DisplayCount += 1
		Display = not Display
	elif Display:
		if "$" in Line:
			raise RuntimeError("nested dollar in display line " + str(Number))
		Current.append(Line)
	else:
		Parts = Line.split("$")
		if len(Parts) % 2 == 0:
			raise RuntimeError("unpaired inline math line " + str(Number))
		InlineCount += len(Parts) // 2
		MathParts.extend(Parts[1::2])
		OutsideParts.extend(Parts[0::2])
check("paired_dollar_delimiters", not Display and not Current)
check("no_TeX_commands_outside_math", not any(re.search(r"\\[A-Za-z]+", Part) for Part in OutsideParts))
for Number, Part in enumerate(MathParts):
	if not Part.strip():
		raise RuntimeError("empty math span " + str(Number))
	Clean = re.sub(r"\\[{}]", "", Part)
	Depth = 0
	for Char in Clean:
		if Char == "{":
			Depth += 1
		elif Char == "}":
			Depth -= 1
		if Depth < 0:
			raise RuntimeError("unmatched closing brace")
	if Depth != 0:
		raise RuntimeError("unmatched opening brace")
	Stack = []
	for Token in re.finditer(r"\\(begin|end)\{([^}]+)\}", Part):
		if Token[1] == "begin":
			Stack.append(Token[2])
		elif not Stack or Stack.pop() != Token[2]:
			raise RuntimeError("unmatched TeX environment")
	if Stack:
		raise RuntimeError("unclosed TeX environment")
check("math_braces_and_environments_balanced", True)
Tags = re.findall(r"\\tag\{([0-9.]+)\}", Text)
check("equation_tags_unique", len(Tags) == len(set(Tags)))
Refs = set(re.findall(r"\(([1-9]\.[0-9]+)\)", "\n".join(OutsideParts)))
check("equation_references_exist", not Refs.difference(Tags))

Record = {
	"role": "author_self_check",
	"independent_review": False,
	"scope": "Finite exact symbolic identities and Markdown structure only; no repository execution, no spectral or stationary-point interval certificate",
	"completed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
	"python": platform.python_version(),
	"sympy": sp.__version__,
	"script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
	"manuscript_sha256": hashlib.sha256(Data).hexdigest(),
	"checks": Results,
	"count": len(Results),
	"markdown": {"display_equations": DisplayCount, "inline_math_spans": InlineCount, "equation_tags": len(Tags), "visual_rendering_checked": False},
}
(Root / "author-selfcheck.json").write_text(json.dumps(Record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"author_checks": len(Results), "markdown": Record["markdown"], "independent_review": False}, ensure_ascii=False))
