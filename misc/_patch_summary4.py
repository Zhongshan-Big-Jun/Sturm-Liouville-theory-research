p = r"F:\LaTeX\BVE research\docs\SL_gap_n1_research_summary.tex"
s = open(p, encoding="utf-8").read()

# 1) table values -> exact corner limits
old_tab = "$A-C$ & $2.8086$ & $q\\to1^+$, $c\\to1/2^-$ \\\\\n$B-D$ & $-0.3751$ & $q\\to1^+$, $c\\to1/2^-$ \\\\\n$G_2-G_1 = (A-C)+(B-D)$ & $2.4258$ & $q\\to1^+$, $c\\to1/2^-$ \\\\"
new_tab = "$A-C$ & $2.80613$ & $q\\to1^+$, $c\\to1/2^-$ (精确角点极限) \\\\\n$B-D$ & $-0.38773$ & $q\\to1^+$, $c\\to1/2^-$ (精确角点极限) \\\\\n$G_2-G_1 = (A-C)+(B-D)$ & $2.41840$ & $q\\to1^+$, $c\\to1/2^-$ (即 $q=1$ 基值) \\\\"
assert old_tab in s, "tab not found"
s = s.replace(old_tab, new_tab)

# 2) replace the closure paragraph (itemwise q-monotonicity) with corrected finding
old_closure = "剩余缺口: 若逐项 $q$-单调性 $d(A-C)/dq \\ge 0$ 且 $d(B-D)/dq \\ge 0$ 成立\n(数值全网格验证, 最小正增量 $+9\\times10^{-5}$ at $q=10^6$, $c=0.48$),\n则 KEY LEMMA 闭环:\n\\begin{equation}\n\tG_2-G_1 \\ge 2.806 - 0.388 = 2.418 > 0.\n\\end{equation}"
new_closure = ("角点极限 (精确): 在 $q\\to1^+$, $c\\to1/2^-$ 处 $\\alpha_1\\to\\pi/3$, $\\alpha_2\\to2\\pi/3$,\n"
"$A-C \\to W(\\pi/3)/(3/2) = 2.80613\\ldots$, $B-D \\to -W(2\\pi/3)/(3/2) = -0.38773\\ldots$,\n"
"和 $\\to 4\\pi/(3\\sqrt3) = 2.41840\\ldots$.\n\n"
"\\textbf{重要更正 (独立复核 2026-08-05): 逐项 $q$-单调性路线被否证.} "
"细网格复核显示 $A-C$ 对 $q$ 单调递增 (全采样通过), 但 $B-D$ \textbf{不}对 $q$ 单调:\n"
"反例 $c=0.01$, $q\\colon 5000\\to20000$ 时 $B-D\\colon 199.79\\to193.99$ (递减); "
"$c\\le0.1$ 时均递减, $c\\ge0.3$ 时才递增. "
"因此交接稿中``$d(B-D)/dq\\ge0$ 全网格成立''的陈述不成立, "
"``分解 + 逐项 $q$-单调''的闭环方案作废. "
"但和的整体下界数值稳健: 全网格 $q\\in[1.00025,10^6]$, $c\\in(0,1/2)$ 扫描\n"
"$G_2-G_1 \\ge 2.41840$, 最小值恰在角点 $q\\to1^+$, $c\\to1/2^-$ (即 $q=1$ 基值). "
"KEY LEMMA 仍开放; 新的可能机制: $A-C$ 的 $q$-单调性 (可证方向) 与 $B-D$ 在\n"
"$A-C$ 增量区域的大正互补性, 或 $G_2-G_1$ 整体的解析下界.")

assert old_closure in s, "closure para not found"
s = s.replace(old_closure, new_closure)

# 3) negation list: add item (8)
old_neg = "补充: (7) $G_2-G_1$ 对 $c$ 单调 -- 假\n($R=10^4$ 时 $c\\approx0.44$ 处 $d(G_2-G_1)/dc > 0$),\n故``分解 + 逐项 $q$-单调''路线是当前唯一存活方案."
new_neg = "补充: (7) $G_2-G_1$ 对 $c$ 单调 -- 假\n($R=10^4$ 时 $c\\approx0.44$ 处 $d(G_2-G_1)/dc > 0$);\n(8) 逐项 $q$-单调性 $d(B-D)/dq\\ge0$ -- 假 ($c\\le0.1$ 时 $B-D$ 随 $q$ 递减),\n故``分解 + 逐项 $q$-单调''闭环方案作废 (见 4.3 更正)."
assert old_neg in s, "neg list not found"
s = s.replace(old_neg, new_neg)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched4 OK")