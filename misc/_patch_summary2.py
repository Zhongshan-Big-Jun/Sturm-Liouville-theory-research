p = r"F:\LaTeX\BVE research\docs\SL_gap_n1_research_summary.tex"
s = open(p, encoding="utf-8").read()

# split equation (6) into two display equations
old_eq = "\tM(\\alpha;c) := \\frac{q(q^2-1)\\,\\alpha^2\\sin^2\\alpha}{q + c\\,\\Phi(\\alpha)},\n" \
         "\t\\qquad \\Phi(\\alpha) := \\cos^2\\alpha + q^2\\sin^2\\alpha,\n" \
         "\t\\qquad M_k(c) := M(\\alpha_k(c);c),\n" \
         "\t\\qquad F(c) := M_1 - M_2,\n" \
         "\\end{equation}"
new_eq = "\tM(\\alpha;c) := \\frac{q(q^2-1)\\,\\alpha^2\\sin^2\\alpha}{q + c\\,\\Phi(\\alpha)},\n" \
         "\t\\qquad \\Phi(\\alpha) := \\cos^2\\alpha + q^2\\sin^2\\alpha,\n" \
         "\\end{equation}\n" \
         "\\begin{equation}\n" \
         "\tM_k(c) := M(\\alpha_k(c);c), \\qquad F(c) := M_1 - M_2,\n" \
         "\\end{equation}"
assert old_eq in s, "eq6 not found"
s = s.replace(old_eq, new_eq)

# fix stale literal cross-reference in O1 proof item 7
old_ref = "由 (5), $\\{f>0\\}$ 为单区间"
new_ref = "由第 5 步, $\\{f>0\\}$ 为单区间"
assert old_ref in s, "ref not found"
s = s.replace(old_ref, new_ref)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched2 OK")