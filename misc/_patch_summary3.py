p = r"F:\LaTeX\BVE research\docs\SL_gap_n1_research_summary.tex"
s = open(p, encoding="utf-8").read()
old = "对 $R\\in\\{1.02,1.05,1.2,1.5,2,3,4,5,10,20,50,100,1000\\}$ 的 126 网格点\n扫描无例外"
new = "对 13 个 $R$ 值 ($1.02$ 至 $1000$) 的 126 网格点扫描无例外"
assert old in s, "para not found"
s = s.replace(old, new)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched3 OK")