import io, os
base = r"F:\LaTeX\BVE research\tools"

# --- README.md ---
p = os.path.join(base, "README.md")
s = io.open(p, encoding="utf-8").read()
lines = s.split("\n")
out = []
changed_row = False
for ln in lines:
    if "[[gap-n1-reduction]]" in ln and "REPAIRABLE_GAP" in ln:
        ln = "| [[gap-n1-reduction]] | 自研 (O1, 2026-08-05) | CANDIDATE_COMPLETE_PROOF (2026-08-06 修复: S_rho 自伴 + 跳点符号 + 平滑论证; 自审 O1a-O1f 全过, 独立复审待办) | 自研 |"
        changed_row = True
    out.append(ln)
if not changed_row:
    print("WARNING: speed-table row not found")
s = "\n".join(out)
s = s.rstrip("\n") + "\n\n- 2026-08-06: [[gap-n1-reduction]] 修复并自审 (run R-20260806T140000Z-o1revise-2ED02A): 状态 REPAIRABLE_GAP -> CANDIDATE_COMPLETE_PROOF. 修复 R1 (S_rho = M_sqrt(rho) T_0 M_sqrt(rho) 对称核, 自伴 HS, Weyl 可用), R2/R4 (跳点 FH 经平滑逼近, 符号 dD/de = -(c_+ - c_-) f(x_j), 双侧导数处处存在), R3 (u_2 符号约定). 自审发现并修复 F-001 (HS 常数推导一行算术错, 最终界不变); 数值组全部通过且两脚本复跑逐位一致; 独立复审 Lemma 1/3 为关闭义务 O1 的前置步骤.\n"
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README.md updated, row found:", changed_row)

# --- gap-n1-reduction.md ---
p2 = os.path.join(base, "gap-n1-reduction.md")
s2 = io.open(p2, encoding="utf-8").read()
# frontmatter status line
s2 = s2.replace(
    "status: 审计后 REPAIRABLE_GAP: 定理为真, 需两处修正 (O1a 算子自伴修正, O1b 符号修正); 见 R-20260806T011500Z-o1audit-422A69",
    "status: CANDIDATE_COMPLETE_PROOF (2026-08-06 修复并自审, run R-20260806T140000Z-o1revise-2ED02A; 独立复审 Lemma 1/3 为关闭前置步骤); 前审计: R-20260806T011500Z-o1audit-422A69"
)
# step 1 (L1 continuity) fix
s2 = s2.replace(
    "1. **L1 连续性**: 对 Green 算子 $T_\\rho f=\\int_0^1 G(x,t)\\rho(t)f(t)\\,dt$ ($G=\\min(x,t)(1-\\max(x,t))$),\n   $\\lambda_k(\\rho)^{-1}=\\mu_k(T_\\rho)$ 为紧自伴算子特征值; 由 $\\|T_\\rho-T_\\sigma\\|\\le\\|G\\|_\\infty\\|\\rho-\\sigma\\|_2$\n   与 $\\|\\rho-\\sigma\\|_2^2\\le 2R\\|\\rho-\\sigma\\|_1$, 及 min-max 原理, $\\lambda_k$ 在 $L^1$ 拓扑连续.",
    "1. **L1 连续性** (2026-08-06 修复, R1): $T_\\rho=T_0M_\\rho$ 在 $L^2$ 上非自伴, 不能直接套 Weyl; 改用对称 Hilbert-Schmidt 算子\n   $S_\\rho=M_{\\sqrt{\\rho}}T_0M_{\\sqrt{\\rho}}$ (核 $\\sqrt{\\rho(x)}G(x,t)\\sqrt{\\rho(t)}$, $G=\\min(x,t)(1-\\max(x,t))$),\n   $S_\\rho$ 与 $T_\\rho$ 相似 (共轭 $M_{\\sqrt{\\rho}}$), $\\mu_k(S_\\rho)=1/\\lambda_k(\\rho)$; 由\n   $\\|S_\\rho-S_\\sigma\\|_{HS}\\le (R/4)\\|\\rho-\\sigma\\|_1^{1/2}$ (核展开 + $G\\le 1/4$ + $\\|\\rho-\\sigma\\|_2^2\\le R\\|\\rho-\\sigma\\|_1$) 与 Weyl,\n   $\\lambda_k$ 在 $L^1$ 拓扑连续 (模 $|\\lambda_k(\\rho)-\\lambda_k(\\sigma)|\\le (R/4)(k\\pi)^4\\|\\rho-\\sigma\\|_1^{1/2}$)."
)
# step 3 add repair note
s2 = s2.replace(
    "   更正记录: 2026-08-06 审计 (R-20260806T011500Z-o1audit-422A69) 发现草稿符号相反; 零条件 $f(x_j)=0$ 不受影响.",
    "   更正记录: 2026-08-06 审计 (R-20260806T011500Z-o1audit-422A69) 发现草稿符号相反; 零条件 $f(x_j)=0$ 不受影响.\n   修复 R2/R4 (run R-20260806T140000Z-o1revise-2ED02A): 公式经平滑逼近 (AEH Lemma 2.1 + Dirac 族极限) 严格证明,\n   $\\varepsilon\\mapsto D(\\rho_\\varepsilon)$ 的双侧导数在每个跳点存在 (审计括号 \"仅当 f=0 时存在\" 不精确); 向右/向左距离导数异号除非 $f(x_j)=0$."
)
# verification section append
s2 = s2.rstrip("\n") + "\n- 修复与自审 (2026-08-06, run R-20260806T140000Z-o1revise-2ED02A): 重导全部七步; 自审发现并修复 F-001 (第 1 步 HS 常数推导一行算术错, 正确链为 (R/32)(||A||_2^2+||A||_1^2) <= (R^2/16)||A||_1, 最终界 (R/4)||A||_1^{1/2} 不变); 数值组 verify_*.py 全过, bangbang 与 smoothing 复跑逐位一致; 审计报告见该 run 的 audit_report.md, 状态 CANDIDATE_COMPLETE_PROOF (独立复审 Lemma 1/3 为关闭义务 O1 的前置步骤).\n"
io.open(p2, "w", encoding="utf-8", newline="\n").write(s2)
print("gap-n1-reduction.md updated")
