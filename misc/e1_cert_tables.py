# -*- coding: utf-8 -*-
"""e1_cert_tables.py v3: emit LaTeX certificate tables from misc/e1_cert_ledger.json
-> misc/e1_cert_tables.tex (fragment to be \\input in the main document appendix).

v3 changes (session 44):
- fmt_name maps >= <= > < to LaTeX \\ge \\le > < and normalizes targets (2/1 -> 2).
- primitives/point displays use outward-rounded single-or-dots (narrow_str);
  wide certified bounds use whole-interval outward rounding (iv_str) at 6 digits;
  cells (exact rationals) display at 6 digits.  Captions state the precision and
  that the displayed interval contains the certified one.
- primitives table uses \\footnotesize and \\tabcolsep 3pt to fit the text width.
"""
import json
from fractions import Fraction as F

d = json.load(open('misc/e1_cert_ledger.json', encoding='utf-8'))
facts = {f['name']: f for f in d['facts']}

REL_MAP = {'>=': '\\ge', '<=': '\\le', '>': '>', '<': '<'}
ND = 6


def _trim(s):
    if '.' in s:
        s = s.rstrip('0')
        if s.endswith('.'):
            s = s[:-1]
    return s


def _qpair(lo, hi, nd):
    from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING
    q = Decimal(1).scaleb(-nd)
    a = _trim(str(Decimal(str(lo)).quantize(q, rounding=ROUND_FLOOR)))
    b = _trim(str(Decimal(str(hi)).quantize(q, rounding=ROUND_CEILING)))
    return a, b


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
    """outward-rounded display of an exact rational (cell endpoint)."""
    from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING
    v = Decimal(F(x).numerator) / Decimal(F(x).denominator)
    q = Decimal(1).scaleb(-nd)
    a = _trim(str(v.quantize(q, rounding=ROUND_FLOOR)))
    b = _trim(str(v.quantize(q, rounding=ROUND_CEILING)))
    if a == b:
        return a
    return '%s\\dots%s' % (a, b)


def cell_str(cell):
    return '[%s,\\,%s]' % (dec_str(cell[0]), dec_str(cell[1]))


def tgt_str(s):
    f = F(s)
    if f.denominator == 1:
        return str(f.numerator)
    return str(f)


out = []
out.append('% ===== auto-generated certificate tables (e1_cert_tables.py) =====')

# ---- primitives ----
out.append(r"""
\begin{table}[ht]
\centering
\footnotesize
\setlength{\tabcolsep}{3pt}
\caption{原语有理包络 (输入层): $\sin\gamma$, $\cos\gamma$, $\tau(\gamma)$, $A=\pi-\gamma$, $D=\sqrt{1+3\sin^2\gamma}$ 在 11 个主有理点处的认证区间。显示为 6 位小数向外取整 (显示区间包含认证区间); 认证宽度最坏为 $\tau(131/200)$ 行约 $1.8\times10^{-10}$ (22 项 $\arctan$ 级数在参数 $v=1/(2\tan\gamma)\approx0.651$ 处余项的二倍), 其余行宽度均 $\le10^{-23}$, 故多数行显示为单点。由注 \ref{rem:env} 与引理 \ref{lem:envseries} 计算。}\label{tab:envprims}
\begin{tabular}{lccccc}
\toprule
$\gamma$ & $\sin\gamma$ & $\cos\gamma$ & $\tau(\gamma)$ & $A$ & $D$\\
\midrule""")
for r in d['primitives']:
    out.append('%-12s & %-26s & %-26s & %-26s & %-26s & %-26s \\\\' % (
        '$%s$' % r['point'],
        '$%s$' % narrow_str(r['sg'][0], r['sg'][1]),
        '$%s$' % narrow_str(r['cg'][0], r['cg'][1]),
        '$%s$' % narrow_str(r['tau'][0], r['tau'][1]),
        '$%s$' % narrow_str(r['A'][0], r['A'][1]),
        '$%s$' % narrow_str(r['D'][0], r['D'][1])))
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
\caption{点值证书 (输出层): 每个事实的认证区间 (12 位小数向外取整, 区间宽度 $\le10^{-12}$ 故通常显示为单点) 与所需有理界; 裕量 = 认证界到目标界的距离, 严格为正。}\label{tab:envpoints}
\begin{tabular}{lll}
\toprule
事实 & 认证值 & 裕量\\
\midrule""")
for name in POINT_ORDER:
    det = pts[name]
    sign = '\\le' if det['cmp'] == 'le' else '\\ge'
    out.append('%s & $%s\\;%s\\;%s$ & $%.1e$\\\\' % (
        fmt_name(name), narrow_str(det['val'][0], det['val'][1], 12), sign,
        tgt_str(det['target']), float(det['margin'])))
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
\caption{区间符号证书: 在小区间上量值的认证区间 (值泰勒模型, 注 \ref{rem:env}); 每个小区间上 $f$ 的认证上界 $<0$ (或下界 $>0$), 裕量为该界到零的距离。数值显示为 6 位小数向外取整 (显示区间包含认证区间)。}\label{tab:envsigns}
\begin{tabular}{llll}
\toprule
事实 & 小区间 & 认证值区间 & 裕量\\
\midrule""")
for name in SIGN_ORDER:
    first = True
    for p in vt[name]:
        nm = name if first else ''
        out.append('%s & $%s$ & $%s$ & $%.2e$\\\\' % (
            fmt_name(nm), cell_str(p['cell']), iv_str(p['bound'][0], p['bound'][1]), float(p['margin'])))
        first = False
out.append(r"""\bottomrule
\end{tabular}
\end{table}""")

out.append(r"""
\begin{table}[ht]
\centering
\small
\caption{小区间极值证书: 两个``区间下界''事实, 由值泰勒模型直接给出 (不依赖单调性); 每小区间认证下界与目标界之差 (裕量) 严格为正。数值显示为 6 位小数向外取整 (显示区间包含认证区间)。}\label{tab:envrange}
\begin{tabular}{llll}
\toprule
事实 & 小区间 & 认证值区间 & 裕量\\
\midrule""")
HARD_TARGET = {'TA_B2 >= 27/10 on [0.723,0.724]': 27.0/10, 'TC >= 19/10 on [0.82,0.83]': 19.0/10}
for name in HARD_ORDER:
    first = True
    tgt = HARD_TARGET[name]
    for p in vt[name]:
        nm = name if first else ''
        marg = float(p['bound'][0]) - tgt
        out.append('%s & $%s$ & $%s$ & $%.2e$\\\\' % (
            fmt_name(nm), cell_str(p['cell']), iv_str(p['bound'][0], p['bound'][1]), marg))
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
\caption{导数符号证书: 每个小区间 $[a,b]$ 上 $f'$ 的认证区间 (泰勒模型 $f'(\gamma)\in f'(c)+f''(\cdot)[-w,w]$, $w=(b-a)/2$, 注 \ref{rem:env}) 与裕量。所有 $f'$ 认证区间与零严格分离, 故各单调性成立。数值显示为 6 位小数向外取整 (显示区间包含认证区间)。}\label{tab:envderiv}\\
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
        out.append('%s & $%s$ & $%s$ & $%.2e$\\\\' % (
            fmt_name(nm), cell_str(p['cell']), iv_str(p['bound'][0], p['bound'][1]), float(p['margin'])))
        first = False
out.append(r"""\end{longtable}}""")

open('misc/e1_cert_tables.tex', 'w', encoding='utf-8').write('\n'.join(out))
print('written misc/e1_cert_tables.tex, %d lines' % len(out))