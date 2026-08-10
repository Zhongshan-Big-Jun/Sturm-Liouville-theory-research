# -*- coding: utf-8 -*-
"""Update tools/README.md: classification index + quick-reference table + maintenance log."""
import io
p = r"tools\README.md"
src = io.open(p, encoding="utf-8-sig").read()

# 1) classification index: add to 自研方法与技巧 after phase-ratio-rigidity line
old1 = "- [[phase-ratio-rigidity]] - 相位比刚性: good root 唯一性/对称性 (O3a, 2026-08-09)"
new1 = old1 + "\n- [[well-family-rigidity]] - 阱族相位比刚性: 小 R good root 对称性 (INF 侧, 2026-08-10)"
assert old1 in src
src = src.replace(old1, new1)

# 2) quick-reference table: add row after phase-ratio-rigidity row
old2 = "| [[phase-ratio-rigidity]] | 自研 (O3a, 2026-08-09) | 解析 + 两类证书 (2026-08-09: $\\partial_qM_2<0$ 与 C4 均全解析) | 自研方法 |"
new2 = old2 + "\n| [[well-family-rigidity]] | 自研 (INF 侧, 2026-08-10) | 定理已证 (STRICT, 11 页零警告; sympy 8/8; 数值阈值 R=3/2 为 EVIDENCE) | 自研方法 |"
assert old2 in src
src = src.replace(old2, new2)

# 3) maintenance log: append entry at the end (before final line if any)
log_entry = "\n- 2026-08-10: 新增 [[well-family-rigidity]] (阱族小 R 相位刚性, 会话续作): 定理已证 1<R<=3/2 时阱族任意 sign-consistent good root 必为对称根 a+b=1; 证明链 = 相位范围 + 传输能量守恒 (P(psi) 旋转) + 残差消元 + r~_tau 严格单调 (Psi~'<0 于 (0,pi) 的完全初等证明: 因式分解 W^2 sin^2 x Psi~' = -(q+1)(2N0+qN1)/8, H=4N0+N1>0 引理, tan(u/2) 有理化 N(t)>0 引理); 文档 docs/SL_gap_n1_well_rigidity_R32.pdf (11 页零警告); 缺口 (a) 对称线 1D 分析, (b) R>3/2 阱族刚性, (c) 定理 A 独立复核 均开放/CANDIDATE, 全部 EVIDENCE 登记于 misc/_well_explore_log.md.\n"
src = src.rstrip() + log_entry
io.open(p, "w", encoding="utf-8-sig", newline="\r\n").write(src)
print("README patched")
