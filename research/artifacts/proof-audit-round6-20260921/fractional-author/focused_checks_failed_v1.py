"""Author checks for R6-C01. Exact identities are not an infinite-dimensional proof."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import re
import sys

import sympy as sp

Root = Path("/mnt/f/LaTeX/BVE research")
Out = Path("/mnt/f/tools/math-audit-round6-20260921/fractional-author")
Checks = []
x, c, a, mu = sp.symbols("x c a mu", real=True, positive=True)
m = sp.symbols("m", integer=True, positive=True)
h = sp.symbols("h", integer=True, nonnegative=True)


def check_equal(Name, Actual, Expected, Scope):
	if(isinstance(Actual, sp.MatrixBase)):
		Ok = (Actual - Expected).applyfunc(sp.simplify) == sp.zeros(*Actual.shape)
	else:
		Ok = sp.simplify(Actual - Expected) == 0
	Checks.append({"name": Name, "scope": Scope, "passed": bool(Ok), "actual": str(Actual), "expected": str(Expected)})
	if(not Ok):
		raise RuntimeError("Failed exact check: " + Name)


def check_true(Name, Ok, Scope):
	Checks.append({"name": Name, "scope": Scope, "passed": bool(Ok)})
	if(not Ok):
		raise RuntimeError("Failed check: " + Name)


def boundary(Poly):
	Delta = Poly.subs(x, 1) - Poly.subs(x, -1)
	First = sp.diff(Poly, x)
	return sp.Matrix([First.subs(x, 1) - Delta / 2, First.subs(x, -1) - Delta / 2]).applyfunc(sp.simplify)


def four_trace(Poly):
	return boundary(Poly).col_join(boundary(sp.diff(Poly, x, 2)))


def integral_cos(Poly):
	return sp.integrate(Poly * sp.cos(a*x), (x, -1, 1))


def integral_sin(Poly):
	return sp.integrate(Poly * sp.sin(mu*x), (x, -1, 1))


def krein_reduction(Expr):
	return sp.simplify(sp.expand_trig(Expr).subs(sp.cos(mu), sp.sin(mu)/mu))


def run_checks():
	AllM = "symbolic identity for every integer m >= 2; not a finite sample"
	Finite = "exact finite polynomial check; not an infinite-dimensional proof"
	Static = "static source/integrity check; not TeX compilation or mathematical certification"
	Even = x**(2*m) - m/(m-1)*x**(2*m-2)
	Odd = x**(2*m+1) - m/(m-1)*x**(2*m-1)
	check_equal("all-m even first boundary", boundary(Even), sp.zeros(2, 1), AllM)
	check_equal("all-m odd first boundary", boundary(Odd), sp.zeros(2, 1), AllM)
	EvenLead = 4*m*(4*m-5)
	OddLead = 4*m*(4*m-3)
	check_equal("all-m even third derivative", sp.diff(Even, x, 3).subs(x, 1), EvenLead, AllM)
	check_equal("all-m odd third-minus-second derivative", (sp.diff(Odd, x, 3)-sp.diff(Odd, x, 2)).subs(x, 1), OddLead, AllM)
	check_true("even leading constant positive for m=h+2", sp.expand(EvenLead.subs(m,h+2)).is_positive, AllM)
	check_true("odd leading constant positive for m=h+2", sp.expand(OddLead.subs(m,h+2)).is_positive, AllM)
	check_equal("all-m even second-layer traces", boundary(sp.diff(Even,x,2)), sp.Matrix([EvenLead,-EvenLead]), AllM)
	check_equal("all-m odd second-layer traces", boundary(sp.diff(Odd,x,2)), sp.Matrix([OddLead,OddLead]), AllM)
	check_equal("all-m actual even K image boundary", boundary(c*Even-sp.diff(Even,x,2)), sp.Matrix([-EvenLead,EvenLead]), AllM)
	check_equal("all-m actual odd K image boundary", boundary(c*Odd-sp.diff(Odd,x,2)), sp.Matrix([-OddLead,-OddLead]), AllM)

	Matrix = sp.Matrix.hstack(*(four_trace(x**Degree) for Degree in range(2,6)))
	Expected = sp.Matrix([[2,2,4,4],[-2,2,-4,4],[0,0,24,40],[0,0,-24,40]])
	check_equal("four-trace matrix from actual differentiations", Matrix, Expected, Finite)
	check_equal("four-trace determinant", Matrix.det(), sp.Integer(15360), Finite)
	check_equal("four-trace inverse", Matrix*Matrix.inv(), sp.eye(4), Finite)
	z = sp.Matrix(sp.symbols("z0:4"))
	RPoly = (sp.Matrix([[x**2,x**3,x**4,x**5]]) * Matrix.inv() * z)[0]
	check_equal("polynomial right inverse TR=I for general trace vector", four_trace(RPoly), z, "symbolic identity for an arbitrary four-component trace vector")

	P4, P5, P6 = Even.subs(m,2), Odd.subs(m,2), Even.subs(m,3)
	Q = sp.expand(P6-sp.Rational(7,2)*P4)
	check_equal("cancelling combination exact polynomial", Q, x**6-5*x**4+7*x**2, Finite)
	check_equal("cancelling combination four traces", four_trace(Q), sp.zeros(4,1), Finite)
	check_equal("cancelling combination K image boundary", boundary(c*Q-sp.diff(Q,x,2)), sp.zeros(2,1), Finite)
	check_true("p4 and p6 individually fail four traces", four_trace(P4)!=sp.zeros(4,1) and four_trace(P6)!=sp.zeros(4,1), Finite)
	LQ = c*Q-sp.diff(Q,x,2)
	check_equal("squared operator expression on verified compatible Q", c*LQ-sp.diff(LQ,x,2), sp.diff(Q,x,4)-2*c*sp.diff(Q,x,2)+c**2*Q, Finite)

	k = sp.symbols("k", integer=True, positive=True)
	Sign = sp.symbols("epsilon", real=True)
	CosP4 = sp.expand_trig(integral_cos(P4)).subs({sp.sin(a):0, sp.cos(a):Sign})
	CosX2 = sp.expand_trig(integral_cos(x**2)).subs({sp.sin(a):0, sp.cos(a):Sign})
	check_equal("p4 exact cosine coefficient", CosP4, -48*Sign/a**4, Finite)
	check_equal("x2 exact cosine coefficient", CosX2, 4*Sign/a**2, Finite)
	check_equal("p5 exact Krein sine coefficient", krein_reduction(integral_sin(P5)), -80*sp.sin(mu)/mu**4, Finite)
	check_equal("x odd-mode orthogonality", krein_reduction(integral_sin(x)), sp.Integer(0), Finite)
	check_equal("p4 constant-mode coefficient", sp.integrate(P4,(x,-1,1)), -sp.Rational(14,15), Finite)
	check_equal("x2 constant-mode coefficient", sp.integrate(x**2,(x,-1,1)), sp.Rational(2,3), Finite)
	check_equal("p4 normalized constant contribution", sp.integrate(P4,(x,-1,1))**2/2, sp.Rational(98,225), Finite)
	check_equal("x2 normalized constant contribution", sp.integrate(x**2,(x,-1,1))**2/2, sp.Rational(2,9), Finite)

	NormRaw = sp.integrate(sp.sin(mu*x)**2,(x,-1,1))
	NormRoot = krein_reduction(NormRaw).subs(sp.sin(mu)**2,mu**2/(1+mu**2))
	check_equal("Krein sine norm with root relations", NormRoot, mu**2/(1+mu**2), "exact symbolic integral subject to mu*cos(mu)=sin(mu) and sin(mu)^2+cos(mu)^2=1")
	check_equal("signed endpoint after sine normalization", ((-1)**k*mu/sp.sqrt(1+mu**2))/(mu/sp.sqrt(1+mu**2)), (-1)**k, "exact symbolic identity; branch sign justified analytically in TeX")

	G = x**7+2*x**6-3*x**3+sp.Rational(5,7)*x**2+x+4
	GPrime = sp.diff(G,x)
	CosDirect = integral_cos(G).subs({sp.sin(a):0,sp.cos(a):Sign})
	CosFormula = (Sign*(GPrime.subs(x,1)-GPrime.subs(x,-1))-integral_cos(sp.diff(G,x,2)).subs({sp.sin(a):0,sp.cos(a):Sign}))/a**2
	check_equal("cosine integration-by-parts sign on mixed polynomial", CosDirect, CosFormula, Finite)
	SinBoundary = GPrime.subs(x,1)+GPrime.subs(x,-1)-G.subs(x,1)+G.subs(x,-1)
	check_equal("Krein sine integration-by-parts sign on mixed polynomial", krein_reduction(integral_sin(G)), krein_reduction((sp.sin(mu)*SinBoundary-integral_sin(sp.diff(G,x,2)))/mu**2), Finite)

	t = sp.symbols("t",real=True)
	for Order in range(4):
		Power = 3-Order
		KernelNormSquared = sp.integrate(sp.integrate((x-t)**(2*Power)/sp.factorial(Power)**2,(t,-1,x)),(x,-1,1))
		ExpectedNormSquared = sp.Rational(2**(8-2*Order),sp.factorial(3-Order)**2*(7-2*Order)*(8-2*Order))
		check_equal("H4 integration-kernel constant order "+str(Order), KernelNormSquared, ExpectedNormSquared, Finite)

	Hyperbolic = sp.Matrix.hstack(boundary(sp.cosh(a*x)),boundary(sp.sinh(a*x)))
	check_equal("surjectivity correction determinant", Hyperbolic.det(), 2*a*sp.sinh(a)*(a*sp.cosh(a)-sp.sinh(a)), "symbolic identity for a>0; sign shown by differentiation in TeX")
	check_equal("hyperbolic determinant positive factor derivative", sp.diff(a*sp.cosh(a)-sp.sinh(a),a), a*sp.sinh(a), "symbolic identity for a>0")
	check_equal("formal inverse of x2 fails boundary", boundary(x**2/c+2/c**2), sp.Matrix([2/c,-2/c]), "symbolic identity for c>0")
	check_equal("threshold exponent at s=7/2", 2*sp.Rational(7,2)-8, -1, "exact arithmetic only; divergence proof in TeX")

	Source = Root/"docs/SL_fractional_left_definite.tex"
	Text = Source.read_text(encoding="utf-8-sig")
	Old = (Root/"research/artifacts/proof-audit-round6-20260921/before/docs/SL_fractional_left_definite.tex").read_text(encoding="utf-8-sig")
	Labels = re.findall(r"\\label\{([^}]+)\}",Text)
	Refs = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}",Text)
	Bibs = re.findall(r"\\bibitem\{([^}]+)\}",Text)
	Cites = []
	for Group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}",Text):
		Cites.extend(Group.split(","))
	check_true("labels unique and references resolved statically",len(Labels)==len(set(Labels)) and set(Refs)<=set(Labels),Static)
	check_true("bibliography keys unique and citations resolved statically",len(Bibs)==len(set(Bibs)) and set(Cites)<=set(Bibs),Static)
	Stack = []
	for Match in re.finditer(r"\\(begin|end)\{([^}]+)\}",Text):
		Kind,Env = Match.groups()
		if(Kind=="begin"):
			Stack.append(Env)
		else:
			if(not Stack or Stack.pop()!=Env):
				raise RuntimeError("Unbalanced TeX environments")
	check_true("TeX environments balanced statically",not Stack,Static)
	BraceDepth = 0
	for Line in Text.splitlines():
		Line = re.split(r"(?<!\\)%",Line)[0]
		for Match in re.finditer(r"(?<!\\)[{}]",Line):
			BraceDepth += 1 if Match.group()=="{" else -1
			if(BraceDepth<0):
				raise RuntimeError("Unbalanced TeX braces")
	check_true("TeX braces balanced statically",BraceDepth==0,Static)
	GrowthStart = r"\begin{lemma}[有显式系数条件的钉住解]"
	GrowthEnd = r"\end{proof}"
	OldGrowth = Old[Old.index(GrowthStart):Old.index(GrowthEnd,Old.index(GrowthStart))+len(GrowthEnd)]
	check_true("conditional growth lemma and proof text preserved",OldGrowth in Text,Static)
	DiagStart = r"\begin{proposition}[精确成员阈值]"
	OldDiag = Old[Old.index(DiagStart):Old.index(GrowthEnd,Old.index(DiagStart))+len(GrowthEnd)]
	check_true("p4/x2 exact diagnostic proof text preserved",OldDiag in Text,Static)
	NumericStart = r"\section{数值工具的含义与限制}"
	OldNumeric = Old[Old.index(NumericStart):Old.index(r"\begin{thebibliography}")]
	check_true("numerical scope and limitations text preserved",OldNumeric in Text,Static)
	NegStart = "对 $s<0$, 定义"
	NegEnd = "对所有元素都按经典二阶导数作用."
	OldNeg = Old[Old.index(NegStart):Old.index(NegEnd)+len(NegEnd)]
	check_true("negative completion mathematical content preserved",OldNeg in Text,Static)
	check_true("no unreceived approval or unresolved template marker", "APPROVED" not in Text and "@@NEGATIVE@@" not in Text, Static)

	Input = json.loads((Out/"input_identity.json").read_text())
	Protected = [Name for Name in Input["files"] if Name not in ["AGENTS.md","docs/SL_fractional_left_definite.tex"]]
	for Name in Protected:
		Digest = hashlib.sha256((Root/Name).read_bytes()).hexdigest()
		check_true("protected input unchanged: "+Name,Digest==Input["files"][Name]["sha256"],Static)
	return {
		"status":"AUTHOR_CHECKS_PASSED",
		"count":len(Checks),
		"python":sys.version,
		"sympy":sp.__version__,
		"optimization":sys.flags.optimize,
		"source_sha256":hashlib.sha256(Source.read_bytes()).hexdigest(),
		"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
		"four_trace_inverse":[[str(Value) for Value in Row] for Row in Matrix.inv().tolist()],
		"checks":Checks,
		"limits":[
			"No PDF/TeX compilation, rendered page inspection, Lean check, independent review or global audit.",
			"All-index convergence, compactness, trace continuity, domain identification and density are proved analytically in the TeX, not certified by these checks.",
			"No floating-point asymptotic sample or numerical convergence test was run.",
			"Protected hashes cover the listed input subset only, not every repository file."
		]
	}


if(__name__=="__main__"):
	Parser = argparse.ArgumentParser()
	Parser.add_argument("--output",required=True)
	Args = Parser.parse_args()
	try:
		Result = run_checks()
	except Exception as Error:
		Result = {"status":"AUTHOR_CHECKS_FAILED","python":sys.version,"sympy":sp.__version__,"optimization":sys.flags.optimize,"error":repr(Error),"checks":Checks}
		Result["captured_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
		with Path(Args.output).open("x",encoding="utf-8") as Handle:
			json.dump(Result,Handle,ensure_ascii=False,indent=2)
			Handle.write("\n")
		print(json.dumps({"status":Result["status"],"checks_before_error":len(Checks),"error":repr(Error)},ensure_ascii=False))
		raise
	Result["captured_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
	with Path(Args.output).open("x",encoding="utf-8") as Handle:
		json.dump(Result,Handle,ensure_ascii=False,indent=2)
		Handle.write("\n")
	print(json.dumps({Key:Result[Key] for Key in ["status","count","optimization","source_sha256"]},ensure_ascii=False))
