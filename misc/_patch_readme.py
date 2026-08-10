p = r"F:\LaTeX\BVE research\tools\README.md"
s = open(p, encoding="utf-8").read()

anchor = "- [[gap-band-extremals]] - 带状自洽极值判据: 相邻间距驻点条件与 FH 对称加倍 (会话 13)"
assert anchor in s, "index anchor missing"
add_idx = anchor + "\n" + \
"- [[gap-n1-reduction]] - 两块族归约定理 (O1, 2026-08-05)\n" + \
"- [[two-block-gap-bounds]] - 两块相位间距界 3pi^2/R < D < 3pi^2 (O3b, 2026-08-05)\n" + \
"- [[key-lemma-decomposition]] - KEY LEMMA 分解 + 逐项 q-单调性否证 (O2, 2026-08-05)"
s = s.replace(anchor, add_idx)

trow = "| [[residual-exactness]] | 自研 (O3a, 2026-08-05) | 定理已证 + 数值验证 (~1e-7) | 自研 |"
assert trow in s, "table row missing"
add_row = trow + "\n" + \
"| [[gap-n1-reduction]] | 自研 (O1, 2026-08-05) | 定理证明草稿 PROVED (审计待补) | 自研 |\n" + \
"| [[two-block-gap-bounds]] | 自研 (O3b, 2026-08-05) | 定理已证 + 4000 点零违例 | 自研 |\n" + \
"| [[key-lemma-decomposition]] | 自研 (O2, 2026-08-05) | 分解已证 + 否证反例已复现 | 自研 |"
s = s.replace(trow, add_row)

log = "- 2026-08-05: 新增 [[residual-exactness]] (O3a: 残差闭合恒等式 dR1/db = -dR2/da, 由 FH 公式 + Schwarz 定理证明; 残差 Jacobian 结构与临界点斜率分裂; 分支交点唯一性归约)."
assert log in s, "log anchor missing"
add_log = log + "\n" + \
"- 2026-08-05: 新增 [[gap-n1-reduction]] (O1: 两块族归约, Green 算子 L1 连续 + Wronskian 单区间 + bang-bang 七步), [[two-block-gap-bounds]] (O3b: 两块相位间距界, 三区上界 + mpmath 60 位), [[key-lemma-decomposition]] (O2: G2-G1 分解 + 精确角点极限 4pi/(3 sqrt3) + 否证 B-D 的 q-单调性; 交接稿逐项 q-单调闭环作废, 以本条目为准)."
s = s.replace(log, add_log)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README updated, len", len(s))