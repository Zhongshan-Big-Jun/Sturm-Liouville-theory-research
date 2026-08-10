p = r"F:\LaTeX\BVE research\docs\SL_gap_n1_research_summary.tex"
s = open(p, encoding="utf-8").read()

# failed routes: correct the "对 c 单调路线" item
old_r = "	\item[对 $c$ 单调路线] $G_2-G_1$ 对 $c$ 非单调 (见 4.3),\n		改为 $(A-C),(B-D)$ 对 $q$ 的逐项单调性."
new_r = "	\item[对 $c$ 单调路线] $G_2-G_1$ 对 $c$ 非单调 (见 4.3).\n	\item[逐项 $q$-单调路线 (B-D) 失败] $A-C$ 对 $q$ 单调递增 (细网格验证),\n		但 $B-D$ 不单调: $c=0.01$, $q\\colon5000\\to20000$ 时 $B-D\\colon199.79\\to193.99$.\n		交接稿中``$d(B-D)/dq\\ge0$''陈述不成立, 该闭环方案作废 (见 4.3 更正);\n		和的整体下界 $G_2-G_1\\ge2.4184$ 数值稳健但证明仍开放."
assert old_r in s, "route item not found"
s = s.replace(old_r, new_r)

# next directions item 1
old_d = "	\item \\textbf{KEY LEMMA}: 证 $d(A-C)/dq \\ge 0$, $d(B-D)/dq \\ge 0$\n		(数值下界 $A-C \\ge 2.8$, $B-D \\ge -0.4$ 且逐项单调).\n		当前最高杠杆缺口; 建议符号计算 (sympy) 或解析单调性."
new_d = "	\item \\textbf{KEY LEMMA}: 逐项 $q$-单调闭环已否证 ($B-D$ 非单调),\n		新方向: (a) 证明 $A-C$ 的 $q$-单调性 (数值全通过);\n		(b) 在 $B-D$ 递减区域 ($c\\le0.1$) 利用 $B-D$ 的大正性与 $A-C$ 增量互补,\n		或直接对和 $G_2-G_1$ 建立解析下界; (c) 角点极限已精确化 ($q\\to1^+$,\n		$c\\to1/2^-$ 处 $G_2-G_1\\to4\\pi/(3\\sqrt3)$), 可作展开基点.\n		当前最高杠杆缺口; 建议符号计算 (sympy) 或解析单调性."
assert old_d in s, "next item not found"
s = s.replace(old_d, new_d)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched5 OK")