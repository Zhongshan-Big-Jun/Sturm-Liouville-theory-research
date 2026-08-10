p = r"F:\LaTeX\BVE research\docs\SL_gap_n1_research_summary.tex"
s = open(p, encoding="utf-8").read()
old_sub = "\\subsection{已证定理 (Agent B, 恒等式 T3 独立复核 $2.7\\times10^{-6}$)}"
new_sub = "\\subsection{已证定理 (Agent B, 恒等式 T3 独立复核 \\texorpdfstring{$2.7\\times10^{-6}$}{2.7e-6})}"
assert old_sub in s, "sub heading not found"
s = s.replace(old_sub, new_sub)
old_188 = "$u^*$, 符号由 $-$ 变 $+$, $D_{\\rm sym}$ 先增后减, $u^*$ 为对称族唯一极大点."
new_188 = "$u^*$, 符号由 $-$ 变 $+$, $D_{\\rm sym}$ 先增后减, $u^*$ 为对称族\n唯一极大点."
assert old_188 in s, "line188 not found"
s = s.replace(old_188, new_188)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched OK")