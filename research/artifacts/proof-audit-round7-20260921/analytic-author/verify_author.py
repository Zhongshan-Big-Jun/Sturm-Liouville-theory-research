"""Local author checks only; not an independent mathematical review."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import re
import sys
import sympy as sp
import mpmath as mp

Root = Path(__file__).resolve().parent
Source = Path('/mnt/f/LaTeX/BVE research/docs/SL_gap_nge2_symmetry_local_proof.tex')
Candidate = Root / Source.name
Rows = []

def record(Name, Condition, Detail, Kind='exact'):
	Passed = bool(Condition)
	Rows.append({'name': Name, 'passed': Passed, 'kind': Kind, 'detail': Detail})
	if not Passed:
		raise RuntimeError(Name)

def zero(Expression):
	return sp.simplify(sp.trigsimp(sp.expand_trig(Expression))) == 0

N = sp.symbols('n', integer=True, positive=True)
A, Theta, X, T, S, Delta = sp.symbols('a theta x t s delta', real=True)
W = 2*((N+1)*sp.sin(A)*sp.cos(A+Theta)-N*sp.sin(A+Theta)*sp.cos(A))
record('wronskian_product_to_sum', zero(W-sp.sin(2*A+Theta)+(2*N+1)*sp.sin(Theta)),
	'Identity with arbitrary phase a=n*theta and symbolic n; missing overall pi is restored in TeX.')
record('finite_sum_telescoping_step',
	zero(sp.sin(A+Theta)-sp.sin(A-Theta)-2*sp.sin(Theta)*sp.cos(A)),
	'Telescope with a=2*j*theta to obtain the stated finite sine-square sum.')
record('n2_midpoint_exact_counterexample',
	sp.pi*(sp.sin(5*sp.pi/2)-5*sp.sin(sp.pi/2)) == -4*sp.pi,
	'Correct W=-4*pi; old -6*pi differs by -2*pi.')
F = 2*sp.pi**2*(N**2*sp.sin(N*sp.pi*X)**2-(N+1)**2*sp.sin((N+1)*sp.pi*X)**2)
Coeff = sp.diff(F, X, 2).subs(X, 0)/2
record('endpoint_pi4_coefficient', sp.simplify(Coeff-2*sp.pi**4*(N**4-(N+1)**4)) == 0,
	'Symbolic n, exact coefficient of x^2.')
P = 144*T*T-88*T+9
Roots = [(11+2*sp.sqrt(10))/36, (11-2*sp.sqrt(10))/36]
record('n2_polynomial_roots_and_derivatives',
	all(sp.simplify(P.subs(T, R)) == 0 for R in Roots)
	and sp.simplify(sp.diff(P, T).subs(T, Roots[0])-16*sp.sqrt(10)) == 0
	and sp.simplify(sp.diff(P, T).subs(T, Roots[1])+16*sp.sqrt(10)) == 0,
	'Both roots exact and P prime equals plus/minus 16*sqrt(10).')
record('n2_root_products',
	sp.simplify(Roots[0]*Roots[1]-sp.Rational(1,16)) == 0
	and sp.simplify((1-Roots[0])*(1-Roots[1])-sp.Rational(65,144)) == 0,
	't_plus*t_minus=1/16; complementary product=65/144.')
Det = Fraction(40960**2, 9**4)*Fraction(1,16)*Fraction(65,144)**3
record('n2_exact_determinant', Det == Fraction(7030400000,4782969),
	'Coefficient of pi^4 is '+str(Det)+'.')
record('volterra_remainder_constants',
	sp.integrate((X-T)*T,(T,0,X)) == X**3/6 and sp.integrate(T,(T,0,X)) == X**2/2,
	'Kernel integrals for |y|<=C*x, independent of density interfaces.')
record('halfwidth_mass_bound_constant',
	sp.integrate(T,(T,S,Delta)) == (Delta**2-S**2)/2,
	'Delta is halfwidth; each half-interval contributes delta^2/2 times its derivative energy.')
for Count in range(1,9):
	C = (0,)+sp.symbols(f'c1:{Count+1}')+(0,)
	Diff = sum((C[J+1]-C[J])**2 for J in range(Count+1))
	Plus = sum((C[J+1]+C[J])**2 for J in range(Count+1))
	if sp.expand(4*sum(V*V for V in C)-Diff-Plus) != 0:
		raise RuntimeError('platform_energy_squares')
record('platform_energy_squares', True,
	'Exact finite algebra for n=1..8 of 4*sum(c^2)-sum(diff^2)=sum(adjacent sums squared); general inequality is proved in TeX.',
	'exact_finite_cases')
record('plateau_constant_and_scale',
	Fraction(2,1)/(1-Fraction(2,12)) == Fraction(12,5) and Fraction(12,5) < 6
	and Fraction(1)-Fraction(2,3) > 0 and Fraction(1)-2*Fraction(2,3) < 0,
	'12/5 is valid for halfwidth<=h/12; R*delta diverges and R*delta^2 vanishes for delta=R^(-2/3).')
record('general_inference_diagnostics',
	sp.diag(1,1,-1,-1).det() == 1
	and sp.sin(X).subs(X,0) == (sp.sin(2*X)/2).subs(X,0)
	and sp.diff(sp.sin(X),X).subs(X,0) == sp.diff(sp.sin(2*X)/2,X).subs(X,0)
	and not zero(sp.sin(X)-sp.sin(2*X)/2),
	'General linear algebra only: positive determinant does not imply definiteness. No realizability claim for this SL K family. Matching data across different ODEs does not imply uniqueness.')
mp.mp.dps = 80
NumRoots = [(11+2*mp.sqrt(10))/36,(11-2*mp.sqrt(10))/36]
Positions = [mp.acos(mp.sqrt(R))/mp.pi for R in NumRoots]
Positions += [1-Positions[1],1-Positions[0]]
Derivatives = [4*mp.pi**3*(8*mp.sin(2*mp.pi*V)*mp.cos(2*mp.pi*V)-27*mp.sin(3*mp.pi*V)*mp.cos(3*mp.pi*V)) for V in Positions]
NumericalDet = mp.fprod(Derivatives)/(9*mp.pi**2)**4
ExpectedDet = mp.mpf(Det.numerator)/Det.denominator*mp.pi**4
record('n2_high_precision_crosscheck', abs(NumericalDet/ExpectedDet-1)<mp.mpf('1e-70'),
	{'positions':[mp.nstr(V,24) for V in Positions], 'determinant':mp.nstr(NumericalDet,30),
	 'derivatives':[mp.nstr(V,24) for V in Derivatives]}, 'numerical_crosscheck')
Original = Source.read_bytes()
Current = Candidate.read_bytes()
OriginalText = Original.decode()
CurrentText = Current.decode()
UneditedSections = []
for Start, End in [
	(r'\begin{proposition}[第一阶变分恒等式]', r'\begin{proposition}[(G1'),
	(r'\begin{proposition}[Wronskian 的 $D$ 界]', r'\section{2026-08-12'),
]:
	OldPart = OriginalText[OriginalText.index(Start):OriginalText.index(End,OriginalText.index(Start))]
	NewPart = CurrentText[CurrentText.index(Start):CurrentText.index(End,CurrentText.index(Start))]
	UneditedSections.append(OldPart == NewPart)
record('unedited_tail_sections_byte_identity', all(UneditedSections),
	'First-order variation proposition and Wronskian D bound retained byte-for-byte; this is not their recertification.', 'artifact')
L, C, U, Ud, Vd = sp.symbols('L c u ud vd', real=True)
for Sign in [-1,1]:
	Fp = 2*L*C*C*U*Ud-2*L*Sign*C*U*Vd
	WW = Vd*U-Sign*C*U*Ud
	if sp.expand(Fp+2*L*Sign*C*WW) != 0:
		raise RuntimeError('simple_zero_wronskian_identity')
record('simple_zero_wronskian_identity', True,
	'At v=sign*c*u and lambda_n=lambda_(n+1)*c^2: f prime=-2*lambda_(n+1)*sign*c*W, both signs exact.')
TailText = CurrentText[CurrentText.index(r'\label{sec:aug}'):]
Banned = [
	'所有断言均为 STRICT', '由 Cauchy 数据唯一性', '主元符号恒定等价于',
	'全局分类猜想现仅依赖',
	r'\lambda_{n+1}^*-\lambda_n^*\ge(2n+1)\pi^2/R_1',
	r'\operatorname{Hess}(D_n)$ 处处定号',
]
record('requested_tail_claim_repairs', all(V not in TailText for V in Banned)
	and r"f'(x_j)/s_j=\sigma\cdot 2\lambda_{n+1}c|W(x_j)|/(R-1)" in TailText
	and '历史 (G2) 闭合声明, 未重新认证' in TailText
	and '不相容, 待重新核算' in TailText,
	'Known false assertions removed or qualified at their original locations; historical whole-G2 status explicitly unrecertified.', 'artifact')
record('publication_neutral_version_wording', '第七轮范围修订; 验收见版本绑定报告' in CurrentText
	and '作者候选' not in CurrentText and '未最终审查' not in CurrentText,
	'Date and abstract do not anticipate independent acceptance.', 'artifact')
record('main_source_unchanged', hashlib.sha256(Original).hexdigest() == '151c7ec65a67789a043b01a46f6c87c40e6827e9994be9fb4be88a45da0c0aaa',
	'Original source hash unchanged.', 'artifact')
Labels = re.findall(r'\\label\{([^}]+)\}',CurrentText)
Refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',CurrentText)
OriginalLabels = set(re.findall(r'\\label\{([^}]+)\}',OriginalText))
record('tex_labels_and_references', len(Labels)==len(set(Labels)) and set(Refs)<=set(Labels) and OriginalLabels<=set(Labels),
	{'labels':len(Labels),'references':len(Refs),'all_original_labels_retained':True}, 'artifact')
record('no_internal_tab_corruption', all('\t' not in Line.lstrip('\t ') for Line in CurrentText.splitlines()),
	'No tabs inserted into TeX commands; ordinary indentation retained.', 'artifact')
Output = {
	'scope':'Author algebra and artifact checks; not independent review, all-density executable validation, or formal proof.',
	'python':sys.version.split()[0], 'sympy':sp.__version__, 'mpmath':mp.__version__,
	'source_sha256':hashlib.sha256(Original).hexdigest(),
	'candidate_sha256':hashlib.sha256(Current).hexdigest(),
	'passed':len(Rows), 'checks':Rows,
}
print(json.dumps(Output,ensure_ascii=False,indent=2))
