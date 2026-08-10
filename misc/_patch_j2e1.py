# -*- coding: utf-8 -*-
# Part 2: R8-R13 (file unchanged so far; R1-R7 were in-memory only). Re-run all.
import io

PATH = 'docs/SL_gap_n1_O3a_phase_rigidity_proof.tex'
s = open(PATH, encoding='utf-8').read()

def rep(old, new, tag):
    global s
    assert old in s, 'ANCHOR NOT FOUND: ' + tag
    s = s.replace(old, new, 1)
    print('ok:', tag)

# ---- R1-R7 (same as part 1) ----
rep('\\usepackage{booktabs}\n', '\\usepackage{booktabs}\n\\usepackage{longtable}\n', 'R1 longtable')

old = """\\ref{thm:LOG} 纯解析证明。全文只使用\\emph{严格解析证明} (E1) 与\\emph{单变量事实验证器} (E2) 两类结论,
与\\emph{普通数值扫描} (E3, 仅交叉检验) 明确区分并逐一标注; 早期版本中的四族
叶盒证书 (J1 16 叶盒、J2 67 叶盒、C4 200 叶盒与 $(LOG)$ 128 叶盒) 已全部
解析化移除, 历史与复现合同见第 \\ref{sec:certs} 节。"""
new = """\\ref{thm:LOG} 纯解析证明。全文只使用\\emph{严格解析证明} (E1), 与\\emph{普通数值扫描}
(E3, 仅交叉检验) 明确区分并逐一标注; 早期版本中的四族叶盒证书 (J1 16 叶盒、J2 67 叶盒、
C4 200 叶盒与 $(LOG)$ 128 叶盒) 与单变量事实验证器均已解析化移除: $J_2^{(2)}$ 证明所需的
55 项单变量事实由注 \\ref{rem:env} 的有理包络方法逐项给出 E1 证明, 证书总表见附录
\\ref{app:cert}; 历史与复现合同见第 \\ref{sec:certs} 节。"""
rep(old, new, 'R2 abstract')

old = """\\begin{remark}[三类证据的标注约定]\\label{rem:evidence}
全文证据分三类, 按下述约定标注与使用。
\\begin{enumerate}
	\\item[(E1)] \\emph{严格解析证明}: 由闭式恒等式、初等不等式、单调性与精确
	有理常数界组成, 构成定理成立性的依据;
	\\item[(E2)] \\emph{单变量事实验证器}: 对有限个单变量符号事实 (端点有理
	界、导数符号与区间正值, 注 \\ref{rem:riv} 与表 \\ref{tab:facts}) 由十进制
	定向舍入区间运算给出严格包含真值的界。验证器不是形式化证明助手内验证
	过的内核, 其输出如实描述为``验证器认证的严格解析事实''; 本文不再使用
	任何二维叶盒证书, 早期四族证书已全部解析化 (第 \\ref{sec:certs} 节)。
	\\item[(E3)] \\emph{普通数值扫描}: 高精度浮点采样, 只用于交叉检验与探索,
	不作为任何定理的结论依据。
\\end{enumerate}
结论陈述本身只依赖 (E1) 与 (E2)。
\\end{remark}"""
new = """\\begin{remark}[证据标注约定]\\label{rem:evidence}
全文证据分两类, 按下述约定标注与使用。
\\begin{enumerate}
	\\item[(E1)] \\emph{严格解析证明}: 由闭式恒等式、初等不等式、单调性与精确
	有理常数界组成, 构成定理成立性的依据。单变量事实的 E1 证明由第
	\\ref{ss:j2e1} 子节注 \\ref{rem:env} 的\\emph{有理包络方法}给出, 证书总表见
	附录 \\ref{app:cert} (表 \\ref{tab:envprims}--\\ref{tab:envderiv});
	\\item[(E3)] \\emph{普通数值扫描}: 高精度浮点采样, 只用于交叉检验与探索,
	不作为任何定理的结论依据。
\\end{enumerate}
结论陈述本身只依赖 (E1)。
\\end{remark}"""
rep(old, new, 'R3 evidence')

old = """不等式由定理 \\ref{thm:j2e1} 完全解析证明 (E1), 其单变量事实由注 \\ref{rem:riv}
的严格区间验证器认证; 注 \\ref{rem:explore} 的范围数据是 E3 扫描, 仅作侦察与"""
new = """不等式由定理 \\ref{thm:j2e1} 完全解析证明 (E1), 其单变量事实由注 \\ref{rem:env}
的有理包络方法给出 (证书总表见附录 \\ref{app:cert}); 注 \\ref{rem:explore} 的范围数据
是 E3 扫描, 仅作侦察与"""
rep(old, new, 'R4 line 1298')

old = """又由注 \\ref{rem:riv} 的点界
$\\tau\\le\\tau(1.0472)<13/10$ (表 \\ref{tab:facts}), 故 $[\\gamma,\\tau]\\subset[0.655,13/10]$,
$h$ 在 $[\\gamma,\\tau]$ 上的最小值在端点取得; 注 \\ref{rem:riv} 的 range\\_pos 认证
$h(\\gamma)\\ge m$ 与 $h(\\tau)\\ge m$ (表 \\ref{tab:facts}) 得 (iv); 也可直接由同一认证
事实 $h(t)\\ge m$ 于 $t\\in[0.655,13/10]$ (表 \\ref{tab:facts}) 得出。"""
new = """又 $\\tau(0.655)>\\pi/4>0.655$ (因 $2\\tan(0.655)>2\\cdot0.655>1$) 且
$\\tau(1.0472)<13/10$ (表 \\ref{tab:envpoints}), 故
$[\\gamma,\\tau]\\subset[0.655,13/10]$。凹函数在区间上的最小值在端点取得, 而
$h(0.655)\\ge m$ 与 $h(13/10)\\ge m$ (表 \\ref{tab:envpoints}), 故 $h(t)\\ge m$ 于
$[0.655,13/10]$, 特别地 $h(\\gamma)\\ge m$ 与 $h(\\tau)\\ge m$, 得 (iv)。"""
rep(old, new, 'R5 track(iv)')

old = """\\begin{remark}[严格区间验证器]\\label{rem:riv}
下面引理 \\ref{lem:brackets} 与引理 \\ref{lem:track}(iv) 中的全部单变量符号事实
由一个十进制定向舍入区间运算引擎 (misc/rigid\\_dec.py) 认证, 属于 (E1) 的有限
区间实现: 每个基本算术运算分别以 ROUND\\_FLOOR/ROUND\\_CEILING 向下/向上舍入;
$\\pi$ 由 Machin 公式 ($16\\arctan(1/5)-4\\arctan(1/239)$, 两个反正切项均按区间
处理) 构造; $\\sin,\\cos$ 用带显式交错级数余项界的 Taylor 展开, $\\arctan$ 用
交错级数 ($x\\le1$) 或 $\\pi/2-\\arctan(1/x)$ ($x>1$); 导数符号用对偶数自动微分
(D1) 的区间传播加自适应细分 (der\\_sign), 正值用区间值自适应细分 (range\\_pos)。
端点比较用精确有理分数与区间端点的 as\\_integer\\_ratio 逐项比较。引擎与 80 位
mpmath 做过 4800 次随机包含性检查, 零违反 (自检脚本 misc/\\_test\\_dec.py)。全部 55 项
事实逐项认证通过 (misc/zz\\_verify\\_e1\\_dec.py, misc/e1\\_facts\\_ledger.json),
摘要见表 \\ref{tab:facts}。区间重放器不是形式化证明助手内验证过的内核, 本文
沿用第 \\ref{rem:trust} 节的表述如实标注该 caveat。
\\end{remark}"""
new = """\\begin{remark}[有理包络方法]\\label{rem:env}
下面引理 \\ref{lem:brackets} 与引理 \\ref{lem:track}(iv) 中的全部单变量事实
(共 55 项) 由下列\\emph{有理包络方法}逐项给出 E1 证明, 不再使用任何区间验证器
内核。方法的四个组成部分:
\\begin{enumerate}
	\\item[(a)] \\emph{交错级数包络}: 对有理点 $x\\in(0,3/2)$, $\\sin x$ 与 $\\cos x$
	的 Taylor 部分和交替夹逼真值, 余项被下一项控制 (引理 \\ref{lem:envseries});
	对 $x\\in(0,1)$, $\\arctan x$ 同理; $\\pi$ 用 Machin 公式
	$\\pi=16\\arctan(1/5)-4\\arctan(1/239)$ 的两个反正切项包络组合。本文取 12 项
	级数, 余项 $<10^{-12}$, 故表 \\ref{tab:envprims} 的原语包络宽度 $\\le10^{-12}$。
	\\item[(b)] \\emph{单调包络}: 在 $[0.655,1.0472]$ 上 $\\sin\\gamma$ 增、
	$\\cos\\gamma$ 减、$A=\\pi-\\gamma$ 减、$D=\\sqrt{1+3\\sin^2\\gamma}$ 增、
	$\\tau=\\arctan(2\\tan\\gamma)$ 增 (因 $\\tau'=2/D^2>0$), 故任意小区间
	$[a,b]\\subset[0.655,1.0472]$ 上这些原语的值域由端点处的 (a) 包络夹出。
	\\item[(c)] \\emph{精确有理区间算术}: 四则运算与正整数幂作用于有理端点区间时
	按区间自然定义 (端点组合取 min/max) 计算, 每步都是有限次精确有理数运算; 由
	(a)(b) 的原语包络经此算术得到任何代数组合 ($B_1,\\dots,G_5$, $Q_\\pm$, $F$,
	$T_{A,B_2}$, $T_{A,M}$, $T_B$, $T_C$ 等) 的认证区间。
	\\item[(d)] \\emph{泰勒模型}: 设 $f$ 在 $[a,b]$ 上 $C^2$, $c=(a+b)/2$,
	$w=(b-a)/2$, $M:=\\sup_{[a,b]}|f''|$。由中值定理
	$f'(\\gamma)=f'(c)+f''(\\xi)(\\gamma-c)$ 得
	$f'(\\gamma)\\in f'(c)+[-Mw,Mw]$; 若 $f'(c)$ 的包络 (由 (a)(c)) 与 $M$
	(由 (b)(c) 对 $f''$ 的链式法则表达式求包络) 使 $f'(c)$ 的下界 $-Mw>0$
	(或上界 $+Mw<0$), 则 $f'>0$ (或 $f'<0$) 于 $[a,b]$。值泰勒模型
	$f(\\gamma)\\in f(c)+[-M'w,M'w]$ ($M'=\\sup|f'|$) 同理。判据的完整陈述见
	引理 \\ref{lem:envtaylor}。
\\end{enumerate}
表 \\ref{tab:envprims}--\\ref{tab:envderiv} (附录 \\ref{app:cert}) 逐项列出由此
得到的证书: 每个区间都是一条有限精确有理数不等式链, 可人工复核; 生成脚本
misc/e1\\_certgen.py 与认证台账 misc/e1\\_cert\\_ledger.json 只用于生成与复现,
其正确性不是结论的依据。
\\end{remark}"""
rep(old, new, 'R6 rem:env')

old = """\\begin{lemma}[括号符号与单调性]\\label{lem:brackets}
在 $[0.655,1.0472]$ 上 (全部由注 \\ref{rem:riv} 认证, 见表 \\ref{tab:facts}):
\\begin{enumerate}
	\\item[(i)] $B_1$ 严格递减, $B_1(0.85)\\ge1/200>0$ 且 $B_1(0.86)\\le-1/50<0$;
	故存在唯一 $\\gamma_0\\in(0.85,0.86)$ 使 $B_1(\\gamma_0)=0$;
	\\item[(ii)] $B_2<0$, $M<0$, $B_4>0$, $G_5>0$;
	\\item[(iii)] $Q_+<0$; $Q_-$ 严格递增, $Q_-(1.0014)\\le-1/10000<0<Q_-(1.0472)\\le33/200$;
	\\item[(iv)] $F$ 在 $[1.0014,1.0472]$ 上严格递增, $F(1.0472)\\le63/100$;
	\\item[(v)] $T_{A,B_2}$ 递增于 $[0.655,0.72]$ 与 $[0.72,0.723]$,
	$\\ge27/10$ 于 $[0.723,0.724]$, 递减于 $[0.724,0.73]$, $[0.73,0.85]$ 与 $[0.85,0.86]$;
	$T_{A,M}$ 递减于 $[0.85,0.86]$ 与 $[0.86,1.0472]$;
	\\item[(vi)] $T_B$ 于 $[0.655,1.0472]$ 递减; $T_C$ 递增于 $[0.655,0.82]$,
	$\\ge19/10$ 于 $[0.82,0.83]$, 递减于 $[0.83,1.0472]$。
\\end{enumerate}
\\end{lemma}"""
new = """\\begin{lemma}[括号符号与单调性]\\label{lem:brackets}
在 $[0.655,1.0472]$ 上:
\\begin{enumerate}
	\\item[(i)] $B_1$ 严格递减, $B_1(0.85)\\ge1/200>0$ 且 $B_1(0.86)\\le-1/50<0$;
	故存在唯一 $\\gamma_0\\in(0.85,0.86)$ 使 $B_1(\\gamma_0)=0$;
	\\item[(ii)] $B_2<0$, $M<0$, $B_4>0$, $G_5>0$;
	\\item[(iii)] $Q_+<0$; $Q_-$ 严格递增, $Q_-(1.0014)\\le-1/10000<0<Q_-(1.0472)\\le33/200$;
	\\item[(iv)] $F$ 在 $[1.0014,1.0472]$ 上严格递增, $F(1.0472)\\le63/100$;
	\\item[(v)] $T_{A,B_2}$ 递增于 $[0.655,0.72]$ 与 $[0.72,0.723]$,
	$\\ge27/10$ 于 $[0.723,0.724]$, 递减于 $[0.724,0.73]$, $[0.73,0.85]$ 与 $[0.85,0.86]$;
	$T_{A,M}$ 递减于 $[0.85,0.86]$ 与 $[0.86,1.0472]$;
	\\item[(vi)] $T_B$ 于 $[0.655,1.0472]$ 递减; $T_C$ 递增于 $[0.655,0.82]$,
	$\\ge19/10$ 于 $[0.82,0.83]$, 递减于 $[0.83,1.0472]$。
\\end{enumerate}
\\end{lemma}

\\begin{proof}
$B_1'(\\gamma)=-3\\cos\\gamma-(\\pi-\\gamma)\\sin\\gamma<0$ (因
$\\gamma\\in(0,\\pi/2)$), 得 (i) 的严格递减与唯一 $\\gamma_0$; 两个端点值来自表
\\ref{tab:envpoints}。其余各项由注 \\ref{rem:env} 的有理包络方法逐项认证:
点值 (含 (iii)(iv) 的端点界) 见表 \\ref{tab:envpoints}, 区间符号 (ii) 与
$Q_+<0$ 见表 \\ref{tab:envsigns}, 小区间极值 $T_{A,B_2}\\ge27/10$ 与
$T_C\\ge19/10$ 见表 \\ref{tab:envrange}, 全部单调性 (i)(iii)(iv)(v)(vi) 的导数
符号见表 \\ref{tab:envderiv}。
\\end{proof}"""
rep(old, new, 'R7 brackets+proof')

# ---- R8: delete tab:facts (robust anchors) ----
cap = s.index('\\caption{引理 \\ref{lem:brackets} 与引理 \\ref{lem:track}(iv) 的认证事实摘要')
tbl_start = s.rindex('\\begin{table}[ht]', 0, cap)
tbl_end = s.index('\\end{table}', cap) + len('\\end{table}')
# also swallow the following blank line
tail = s[tbl_end:]
if tail.startswith('\n\n'):
    tbl_end += 2
rep(s[tbl_start:tbl_end], '', 'R8 delete tab:facts')

# ---- R9 ----
old = '端点有理界 (26 项, 全部 ``点界' + chr(39) + chr(39) + ' 认证, 用于表 \\ref{tab:g1}):'
new = '端点有理界 (26 项, 全部由注 \\ref{rem:env} 的点值包络给出, 见表 \\ref{tab:envpoints}; 用于表 \\ref{tab:g1}):'
rep(old, new, 'R9 endpoints intro')

# ---- R10 ----
old = """端点有理界 (\\eqref{eq:endpoints}) 全部由注 \\ref{rem:riv} 认证, 单调性来自引理
\\ref{lem:brackets}; 分段下界见表 \\ref{tab:g1}。表中各行的组合方式如:"""
new = """端点有理界 (\\eqref{eq:endpoints}) 全部由注 \\ref{rem:env} 的点值包络给出
(表 \\ref{tab:envpoints}), 单调性来自引理 \\ref{lem:brackets}; 分段下界见表
\\ref{tab:g1}。表中各行的组合方式如:"""
rep(old, new, 'R10 j2e1 proof')

# ---- R11: sec:certs ----
old_start = s.index('本文当前版本\\emph{不使用任何二维叶盒证书}。')
old_end = s.index('\\end{remark}', s.index('\\begin{remark}[可信度边界]')) + len('\\end{remark}')
old_block = s[old_start:old_end]
new_block = """本文当前版本\\emph{不使用任何二维叶盒证书, 也不使用任何单变量事实验证器}。
早期版本中的四族证书——$J_1^{(2)}$ 的 16 叶盒、$J_2^{(2)}$ 的 67 叶盒、C4 区间段
$K>0$ 的 200 叶盒与伴随命题 $(LOG)$ 的 128 叶盒——已全部被纯解析证明 (E1)
取代并移除: $J_1^{(2)}$ 由定理 \\ref{thm:j1e1}, $J_2^{(2)}$ 由定理 \\ref{thm:j2e1},
$K>0$ 由引理 \\ref{lem:corner} 的 C4 段, $(LOG)$ 由定理 \\ref{thm:LOG}。主定理
\\ref{thm:main} 的证明链只依赖 (E1) 解析证明; 其中 $J_2^{(2)}$ 所需的 55 项单变量
事实由注 \\ref{rem:env} 的有理包络方法逐项给出 E1 证明, 证书总表见附录
\\ref{app:cert}。

\\subsection{历史证书一览 (已退役)}

旧 128 叶盒证书目标为 $(G_2-G_1)'<0$ 于闭盒 $Q$ (旧 $(LOG)$ 路线): 128 叶,
最接近零的认证上界 $-4.841603818885058$, 零失败。该路线已被定理 \\ref{thm:LOG}
取代, 仅作历史记录; 原 16/67/200 叶盒族亦已分别随定理 \\ref{thm:j1e1},
\\ref{thm:j2e1} 与引理 \\ref{lem:corner} 完成解析化而退役。每个叶盒族当时都用
有理端点验证了精确铺砌、无重叠和无遗漏 (叶面积总和等于盒面积), 并在独立重放
与二次引擎复算中全部通过; 这些历史记录不影响本文任何结论。

\\subsection{单变量事实验证器 (历史, 已退役)}

更早版本对上述 55 项单变量事实使用十进制定向舍入区间运算引擎
(\\texttt{misc/rigid\\_dec.py}): $\\pi$ 由 Machin 公式构造, $\\sin,\\cos$ 用带
显式交错级数余项界的 Taylor 展开, $\\arctan$ 用交错级数或
$\\pi/2-\\arctan(1/x)$, 导数符号用对偶数自动微分加自适应细分, 端点比较用精确
有理分数; 引擎与 80 位 mpmath 做过 4800 次随机包含性检查, 零违反
(misc/\\_test\\_dec.py)。该引擎输出是``验证器认证的严格解析事实'', 不是
kernel-checked proof。自本版本起, 该引擎被注 \\ref{rem:env} 的有理包络方法
(E1) 完全取代: 55 项事实全部改写为有限精确有理数不等式链 (附录 \\ref{app:cert}
的证书总表), 不再依赖任何验证器内核。旧引擎三件套 (\\texttt{misc/rigid\\_dec.py},
\\texttt{misc/zz\\_verify\\_e1\\_dec.py}, \\texttt{misc/e1\\_facts\\_ledger.json})
仅作历史复现记录, 不影响本文任何结论。

\\subsection{内容哈希}

\\begin{itemize}
	\\item L5 (旧 $(LOG)$ 证书验证脚本, 已退役, 不再支撑任何结论):\\\\
	\\texttt{\\small 132e998f2a4f4807443c33e669435d6382de646b88be25d42e455251c7447f4a}
	\\item L6 ($J_1^{(2)}$ E1 交叉检验脚本): \\texttt{\\small 64e24ace3117772b6cd2ea2ac53986a75cad6c3fd797b61369472ac87ec6ab04}
	\\item L7--L9 (旧十进制区间验证器三件套 \\texttt{rigid\\_dec.py},
	\\texttt{zz\\_verify\\_e1\\_dec.py}, \\texttt{e1\\_facts\\_ledger.json}, 已退役):\\\\
	\\texttt{\\small dd81278ed7a9e1ccf063cc446456c473546c1dbab73f6db7b60e11ec0d153525}\\\\
	\\texttt{\\small cad6c5ef56b7ccd38c2108def99916779cee77d387d8313c321912fdfed24bc4}\\\\
	\\texttt{\\small cc74fc5026866d33a367aad7dcd5152e6114751c9c2abe6a3b02e06b085cd9ef}
	\\item L10 (E1 有理包络证书生成器 \\texttt{misc/e1\\_certgen.py}):\\\\
	\\texttt{\\small 375209e2574aea15e3966b442316e2326070d75d4b9445d4bdb9ccf74dfec57c}
	\\item L11 (E1 有理包络认证台账 \\texttt{misc/e1\\_cert\\_ledger.json}):\\\\
	\\texttt{\\small ec9ce5ff7af7d9684bdd2097368e789e6f0b1dae798a04e62aef3d073fd68d30}
	\\item L12 (E1 证书表生成器 \\texttt{misc/e1\\_cert\\_tables.py}):\\\\
	\\texttt{\\small 5d97517e9e577d55632264e5a89b64b8f05e486dea9397e51e97ad7c0c588d32}
\\end{itemize}
L10--L12 为当前有理包络证书链的内容哈希; L5--L9 为历史产物, 仅作复现记录。
证书结论本身是附录 \\ref{app:cert} 中的有限有理不等式链, 不依赖上述脚本的正确性。

\\begin{remark}[可信度边界]\\label{rem:trust}
本版本不依赖任何软件验证器内核。主定理 \\ref{thm:main} 的证明链只由 (E1) 解析
证明组成: 闭式恒等式、初等不等式、单调性, 以及注 \\ref{rem:env} 的有理包络方法
(附录 \\ref{app:cert} 的证书总表——每一项都是一条由有限次精确有理数运算构成、
可人工复核的不等式链)。E3 扫描数据 (注 \\ref{rem:explore} 等) 只用于交叉检验,
不构成结论依据。早期叶盒证书与十进制验证器均已退役, 仅作历史记录。
\\end{remark}"""
rep(old_block, new_block, 'R11 sec:certs')

open(PATH, 'w', encoding='utf-8').write(s)
print('part 2 written')
