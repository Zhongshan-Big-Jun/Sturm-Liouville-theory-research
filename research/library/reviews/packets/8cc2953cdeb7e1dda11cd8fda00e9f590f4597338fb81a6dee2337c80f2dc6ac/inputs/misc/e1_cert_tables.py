# -*- coding: utf-8 -*-
"""e1_cert_tables.py v3: emit LaTeX certificate tables from misc/e1_cert_ledger.json
-> misc/e1_cert_tables.tex (fragment to be \\input in the main document appendix).

Round13: exact endpoints and fail-closed input replace the old display-only chain.
Historical v3 changes (session 44):
- fmt_name maps >= <= > < to LaTeX \\ge \\le > < and normalizes targets (2/1 -> 2).
- primitives/point displays use certified outward-rounded endpoints (narrow_str);
  wide certified bounds use whole-interval outward rounding (iv_str) at 6 digits;
  cells (exact rationals) display at 6 digits.  Captions state the precision and
  that the displayed interval contains the certified one.
- primitives table uses \\footnotesize and \\tabcolsep 3pt to fit the text width.
"""
import argparse
from pathlib import Path
import os
import tempfile
from e1_certificate_io import display_interval, load_accepted_ledger
from fractions import Fraction as F


REL_MAP = {'>=': '\\ge', '<=': '\\le', '>': '>', '<': '<'}
ND = 6


def _trim(s):
    if '.' in s:
        s = s.rstrip('0')
        if s.endswith('.'):
            s = s[:-1]
    return s


def _qpair(lo, hi, nd):
	return tuple(_trim(Value) for Value in display_interval((F(lo), F(hi)), nd))


def narrow_str(lo, hi, nd=ND):
    """outward-rounded display of a certified narrow interval: single value or a\\dots b."""
    a, b = _qpair(lo, hi, nd)
    if a == b:
        return a
    return '%s\\dots%s' % (a, b)


def iv_str(lo, hi, nd=ND):
    """outward-rounded whole-interval display [a,b]; single value when a == b."""
    a, b = _qpair(lo, hi, nd)
    if a == b:
        return a
    return '[%s,\\,%s]' % (a, b)


def dec_str(x, nd=ND):
	"""Cell coordinates are exact, never enlarged by display rounding."""
	Value=F(x)
	Denominator=Value.denominator
	Powers=[]
	for Prime in (2,5):
		Power=0
		while Denominator % Prime == 0:
			Denominator//=Prime
			Power+=1
		Powers.append(Power)
	if Denominator == 1:
		return _trim(display_interval((Value,Value),max(Powers))[0])
	return r'\frac{%d}{%d}' % (Value.numerator,Value.denominator)


def cell_str(cell):
    return '[%s,\\,%s]' % (dec_str(cell[0]), dec_str(cell[1]))


def tgt_str(s):
    f = F(s)
    if f.denominator == 1:
        return str(f.numerator)
    return str(f)


def _margin_tex(Value):
	"""Three significant decimal digits, always downward, no float conversion."""
	Value = F(Value)
	if Value == 0:
		return '0'
	if Value < 0:
		raise ValueError('cannot publish a negative certificate margin')
	Exponent = len(str(Value.numerator)) - len(str(Value.denominator))
	while Value < F(10) ** Exponent:
		Exponent -= 1
	while Value >= F(10) ** (Exponent + 1):
		Exponent += 1
	Scaled = Value / (F(10) ** Exponent) * 100
	Digits = Scaled.numerator // Scaled.denominator
	Mantissa = str(Digits // 100) + '.' + str(Digits % 100).zfill(2)
	return Mantissa + r'\times10^{' + str(Exponent) + '}'


def render_tables(d):
	out = []
	out.append('% ===== auto-generated certificate tables (e1_cert_tables.py) =====')
	
	# ---- primitives ----
	out.append(r"""
	\begin{table}[ht]
	\centering
	\footnotesize
	\setlength{\tabcolsep}{3pt}
	\caption{原语有理包络: 11 个主有理点处的精确分数区间另存于当前台账. 本表显示到 6 位小数, 下端向下且上端向上舍入, 显示区间包含原区间. 非退化区间保留两端. 见注 \ref{rem:env} 与引理 \ref{lem:envseries}.}\label{tab:envprims}
	\begin{tabular}{lccccc}
	\toprule
	$\gamma$ & $\sin\gamma$ & $\cos\gamma$ & $\tau(\gamma)$ & $A$ & $D$\\
	\midrule""")
	for r in d['primitives']:
	    out.append('%-12s & %-26s & %-26s & %-26s & %-26s & %-26s \\\\' % (
	        '$%s$' % r['point'],
	        '$%s$' % narrow_str(r['sg_exact'][0], r['sg_exact'][1]),
	        '$%s$' % narrow_str(r['cg_exact'][0], r['cg_exact'][1]),
	        '$%s$' % narrow_str(r['tau_exact'][0], r['tau_exact'][1]),
	        '$%s$' % narrow_str(r['A_exact'][0], r['A_exact'][1]),
	        '$%s$' % narrow_str(r['D_exact'][0], r['D_exact'][1])))
	out.append(r"""\bottomrule
	\end{tabular}
	\end{table}""")
	
	
	def fmt_name(name):
	    """convert ledger fact names to math-mode LaTeX names."""
	    if name == 'B1(0.85) >= 1/200':
	        return '$B_1(0.85)\\ge1/200$'
	    if name == 'B1(0.86) <= -1/50':
	        return '$B_1(0.86)\\le-1/50$'
	    if name == 'B4(1.0472) >= 9/25':
	        return '$B_4(1.0472)\\ge9/25$'
	    if name.startswith('Qlo('):
	        pt, rest = name[4:].split(') ', 1)
	        rel, tgt = rest.split(' ', 1)
	        return '$Q_-(' + pt + ')' + REL_MAP[rel] + tgt_str(tgt) + '$'
	    if name == 'F(1.0472) <= 63/100':
	        return '$F(1.0472)\\le63/100$'
	    if name == 'tau(1.0472) < 13/10':
	        return '$\\tau(1.0472)<13/10$'
	    if name == 'h(gamma) >= m at 0.655':
	        return '$h(0.655)\\ge m$'
	    if name == 'h(13/10) >= m':
	        return '$h(13/10)\\ge m$'
	    if name.startswith('TA_B2('):
	        pt, rest = name[6:].split(') ', 1)
	        rel, tgt = rest.split(' ', 1)
	        return '$T_{A,B_2}(' + pt + ')' + REL_MAP[rel] + tgt_str(tgt) + '$'
	    if name.startswith('TA_M('):
	        pt, rest = name[5:].split(') ', 1)
	        rel, tgt = rest.split(' ', 1)
	        return '$T_{A,M}(' + pt + ')' + REL_MAP[rel] + tgt_str(tgt) + '$'
	    if name.startswith('TB('):
	        pt, rest = name[3:].split(') ', 1)
	        rel, tgt = rest.split(' ', 1)
	        return '$T_B(' + pt + ')' + REL_MAP[rel] + tgt_str(tgt) + '$'
	    if name.startswith('TC('):
	        pt, rest = name[3:].split(') ', 1)
	        rel, tgt = rest.split(' ', 1)
	        return '$T_C(' + pt + ')' + REL_MAP[rel] + tgt_str(tgt) + '$'
	    if name == 'B2 < 0':
	        return '$B_2<0$'
	    if name == 'M < 0':
	        return '$M<0$'
	    if name == 'B4 > 0':
	        return '$B_4>0$'
	    if name == 'G5 > 0':
	        return '$G_5>0$'
	    if name == 'Qhi < 0':
	        return '$Q_+<0$'
	    if name == 'TA_B2 >= 27/10 on [0.723,0.724]':
	        return '$T_{A,B_2}\\ge27/10$ 于 $[0.723,0.724]$'
	    if name == 'TC >= 19/10 on [0.82,0.83]':
	        return '$T_C\\ge19/10$ 于 $[0.82,0.83]$'
	    if name == 'Qlo increasing':
	        return '$Q_-$ 递增'
	    if name == 'F increasing [1.0014,1.0472]':
	        return '$F$ 递增于 $[1.0014,1.0472]$'
	    if name.startswith('TA_B2 inc'):
	        iv = name[name.index('['):]
	        return '$T_{A,B_2}$ 递增于 $' + iv + '$'
	    if name.startswith('TA_B2 dec'):
	        iv = name[name.index('['):]
	        return '$T_{A,B_2}$ 递减于 $' + iv + '$'
	    if name.startswith('TA_M dec'):
	        iv = name[name.index('['):]
	        return '$T_{A,M}$ 递减于 $' + iv + '$'
	    if name == 'TB decreasing':
	        return '$T_B$ 递减'
	    if name.startswith('TC inc'):
	        iv = name[name.index('['):]
	        return '$T_C$ 递增于 $' + iv + '$'
	    if name.startswith('TC dec'):
	        iv = name[name.index('['):]
	        return '$T_C$ 递减于 $' + iv + '$'
	    return name
	
	
	# ---- point certificates (logical order) ----
	POINT_ORDER = [
	 'B1(0.85) >= 1/200','B1(0.86) <= -1/50','B4(1.0472) >= 9/25','Qlo(1.0014) <= -1/10000',
	 'Qlo(1.0472) <= 33/200','F(1.0472) <= 63/100','tau(1.0472) < 13/10',
	 'TA_B2(0.655) >= 11/5','TA_B2(0.72) >= 13/5','TA_B2(0.73) >= 13/5','TA_B2(0.82) >= 2',
	 'TA_B2(0.83) >= 2','TA_B2(0.85) >= 19/10','TA_B2(0.86) >= 47/25',
	 'TA_M(0.86) >= 9/5','TA_M(1.0014) >= 3/5','TA_M(1.0472) >= 3/8',
	 'TB(0.72) >= 3/10','TB(0.73) >= 3/10','TB(0.82) >= 3/20','TB(0.83) >= 3/20',
	 'TB(0.85) >= 1/10','TB(0.86) >= 1/10','TB(1.0014) >= 1/25','TB(1.0472) >= 1/40',
	 'TC(0.655) >= 57/50','TC(0.72) >= 3/2','TC(0.73) >= 3/2','TC(0.85) >= 19/10',
	 'TC(0.86) >= 19/10','TC(1.0014) >= 4/3','TC(1.0472) >= 11/10',
	 'h(gamma) >= m at 0.655','h(13/10) >= m',
	]
	pts = {f['name']: f['detail'] for f in d['facts'] if f['kind'] == 'point'}
	out.append(r"""
	\begin{table}[ht]
	\centering
	\small
	\caption{点值证书: 区间下端向下且上端向上舍入到 12 位小数; 每行按所列严格或非严格目标验收. 裕量列为精确裕量向下截断至 3 位有效数字的下界.}\label{tab:envpoints}
	\begin{tabular}{lll}
	\toprule
	事实 & 认证值 & 裕量\\
	\midrule""")
	for name in POINT_ORDER:
	    det = pts[name]
	    sign = {'le': r'\le', 'ge': r'\ge', 'lt': '<', 'gt': '>'}[det['cmp']]
	    out.append('%s & $%s\\;%s\\;%s$ & $%s$\\\\' % (
	        fmt_name(name), narrow_str(det['val_exact'][0], det['val_exact'][1], 12), sign,
	        tgt_str(det['target']), _margin_tex(F(det['margin_exact']))))
	out.append(r"""\bottomrule
	\end{tabular}
	\end{table}""")
	
	# ---- interval sign certificates ----
	SIGN_ORDER = ['B2 < 0','M < 0','B4 > 0','G5 > 0','Qhi < 0']
	HARD_ORDER = ['TA_B2 >= 27/10 on [0.723,0.724]','TC >= 19/10 on [0.82,0.83]']
	vt = {f['name']: f['detail']['pieces'] for f in d['facts'] if f['kind'] == 'value-taylor'}
	out.append(r"""
	\begin{table}[ht]
	\centering
	\small
	\caption{区间符号证书: 在小区间上量值的认证区间 (值泰勒模型, 注 \ref{rem:env}); 每个小区间上 $f$ 的认证上界 $<0$ (或下界 $>0$), 裕量为该界到零的距离, 所列为向下截断至 3 位有效数字的下界。数值显示为 6 位小数向外取整 (显示区间包含认证区间)。}\label{tab:envsigns}
	\begin{tabular}{llll}
	\toprule
	事实 & 小区间 & 认证值区间 & 裕量\\
	\midrule""")
	for name in SIGN_ORDER:
	    first = True
	    for p in vt[name]:
	        nm = name if first else ''
	        out.append('%s & $%s$ & $%s$ & $%s$\\\\' % (
	            fmt_name(nm), cell_str(p['cell']), iv_str(p['bound_exact'][0], p['bound_exact'][1]), _margin_tex(F(p['margin_exact']))))
	        first = False
	out.append(r"""\bottomrule
	\end{tabular}
	\end{table}""")
	
	out.append(r"""
	\begin{table}[ht]
	\centering
	\small
	\caption{小区间极值证书: 两个``区间下界''事实, 由值泰勒模型直接给出 (不依赖单调性); 每小区间认证下界与目标界之差 (裕量) 严格为正. 裕量列向下截断至 3 位有效数字.数值显示为 6 位小数向外取整 (显示区间包含认证区间)。}\label{tab:envrange}
	\begin{tabular}{llll}
	\toprule
	事实 & 小区间 & 认证值区间 & 裕量\\
	\midrule""")
	for name in HARD_ORDER:
	    first = True
	    for p in vt[name]:
	        nm = name if first else ''
	        marg = F(p['margin_exact'])
	        out.append('%s & $%s$ & $%s$ & $%s$\\\\' % (
	            fmt_name(nm), cell_str(p['cell']), iv_str(p['bound_exact'][0], p['bound_exact'][1]), _margin_tex(marg)))
	        first = False
	out.append(r"""\bottomrule
	\end{tabular}
	\end{table}""")
	
	# ---- derivative sign certificates ----
	DERIV_ORDER = [
	 'Qlo increasing','F increasing [1.0014,1.0472]',
	 'TA_B2 inc [0.655,0.72]','TA_B2 inc [0.72,0.723]',
	 'TA_B2 dec [0.724,0.73]','TA_B2 dec [0.73,0.85]','TA_B2 dec [0.85,0.86]',
	 'TA_M dec [0.85,0.86]','TA_M dec [0.86,1.0472]','TB decreasing',
	 'TC inc [0.655,0.82]','TC dec [0.83,1.0472]',
	]
	dt = {f['name']: f['detail']['pieces'] for f in d['facts'] if f['kind'] == 'deriv-taylor'}
	out.append(r"""
	{\setlength{\tabcolsep}{3pt}
	\begin{longtable}{llll}
	\caption{导数符号证书: 每个小区间 $[a,b]$ 上 $f'$ 的认证区间 (泰勒模型 $f'(\gamma)\in f'(c)+f''(\cdot)[-w,w]$, $w=(b-a)/2$, 注 \ref{rem:env}) 与裕量下界 (向下截断至 3 位有效数字).所有 $f'$ 认证区间与零严格分离, 故各单调性成立。数值显示为 6 位小数向外取整 (显示区间包含认证区间)。}\label{tab:envderiv}\\
	\toprule
	事实 & 小区间 & $f'$ 认证区间 & 裕量\\
	\midrule
	\endfirsthead
	\toprule
	事实 & 小区间 & $f'$ 认证区间 & 裕量\\
	\midrule
	\endhead
	\bottomrule
	\endlastfoot""")
	for name in DERIV_ORDER:
	    first = True
	    for p in dt[name]:
	        nm = name if first else ''
	        out.append('%s & $%s$ & $%s$ & $%s$\\\\' % (
	            fmt_name(nm), cell_str(p['cell']), iv_str(p['bound_exact'][0], p['bound_exact'][1]), _margin_tex(F(p['margin_exact']))))
	        first = False
	out.append(r"""\end{longtable}}""")
	
	return '\n'.join(out) + '\n'


def main(argv=None):
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument('--ledger', type=Path, default=Path(__file__).resolve().with_name('e1_cert_ledger.json'))
	Parser.add_argument('--output', type=Path, default=Path(__file__).resolve().with_name('e1_cert_tables.tex'))
	Args = Parser.parse_args(argv)
	Ledger = load_accepted_ledger(Args.ledger)
	Text = render_tables(Ledger)
	Args.output.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=Args.output.parent, delete=False) as Stream:
		Temporary = Path(Stream.name)
		Stream.write(Text)
		Stream.flush()
		os.fsync(Stream.fileno())
	os.replace(Temporary, Args.output)
	print('Accepted all57 complete facts; wrote', Args.output)
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
