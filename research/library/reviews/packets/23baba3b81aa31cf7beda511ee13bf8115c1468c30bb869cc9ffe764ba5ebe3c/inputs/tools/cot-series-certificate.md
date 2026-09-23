---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c4c7-52f9-71e3-bc0b-ef3e30abb78e", "01a0c4c7-595b-7a40-9740-ec99ceb721a6", "01a0c4cc-45bc-77e1-8ce3-f79b2f3d31aa"], "conditions": ["0<z<pi; uniform convergence only on compact subintervals", "Cz bound only for 0<z<=pi/8"], "created": "2026-08-07", "dependencies": [], "evidence_status": "ROUND8_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT", "resources": [{"kind": "exact-computation", "locator": "Fraction/Machin/Taylor scalar certificate, no full spectral formalization", "path": "research/artifacts/proof-audit-round8-20260922/certificate/certificate.py", "sha256": "39cd4b13019fddfc7342e9c2d56131de01686504944b444af0e3bb92301833d6"}, {"kind": "author-execution", "locator": "Exact scalar outputs; independent review receipt required", "path": "research/artifacts/proof-audit-round8-20260922/certificate/results.json", "sha256": "15723e490e332b4b979a1641f86fed216cc4232964fb2e5c0d3c5bd642cb7166"}], "source": "自研 (会话 30)", "sources": [{"locator": "Round8 corrected phases, A doubleprime, continuous sliver, T1/T2/T3 and fixed-u rate", "path": "docs/SL_gap_n1_inf_limit_proof.tex", "sha256": "a41e919dccd9d28f876a6d0cccf65a70a31fe4ba8b906f1ea46935bfc64a6b00"}, {"locator": "Equation4.22.3 actually retrieved formula and pole exclusions", "source_id": "bb729c250eb36b380f0ab4f7be158562340ba3b2bf505887681952e3aab405e6", "url": "https://dlmf.nist.gov/4.22.E3"}], "status": "第八轮范围明确的修订; 检索复用由当前精确版本纠错回执控制", "summary": "0<z<pi 的正确 Laurent 幂次与局部一致收敛; 0<z<=pi/8 时余项<=Cz*z, Cz<0.337; 新精确证书替代旧 libm 区间.", "tags": ["mathtool", "analysis"], "title": "余切余项的部分分式与精确有理常数", "tool_id": "cot-series-certificate", "updated": "2026-09-22"}
---
# 余切余项的部分分式与有理常数

令 r(z)=1/z-cot(z). 对实数 0<z<pi, NIST DLMF4.22.3 给出

    r(z)/z = 2 sum_(j>=1) 1/(j^2*pi^2-z^2).

右侧在 (-pi,pi) 的每个紧子区间上一致收敛. 每个加项在正半轴严格递增, 因而 r(z)/z>0 且严格递增. 不能把局部一致收敛写成在整个 (0,pi) 上一致收敛.

正确的 Laurent 展开为

    cot(z) = 1/z - sum_(k>=1) c_k*z^(2k-1),
    c_k = 2^(2k)*abs(B_(2k))/(2k)! > 0,
    r(z)/z = 1/3 + z^2/45 + 2*z^4/945 + ... .

旧卡的 z^(2k+1) 漏掉了线性项 z/3, 其旧版本作为纠错历史保留.

在 0<z<=pi/8,

    0 < r(z) <= C_z*z,
    C_z = (8/pi-(1+sqrt(2)))/(pi/8) < 337/1000.

定义 r(0)=0 后上界连续延伸到 z=0; r(z)/z 在零点的连续值为 1/3. C_z 的上界由第八轮精确有理包络核对, 使用有理 pi/sqrt(2) 界和精确四则运算, 不沿用普通 libm 加一次 nextafter 的旧区间实现.

这同时给出 cot(z)<=1/z, 以及 epsilon*cot(z)>=epsilon*(1/z-C_z*z) (epsilon>=0). 后者只在上述小相位区间使用. 接近 pi 的奇异区不能使用同一个 C_z; 本卡不为旧 tan 余项数值扫描授予新的证明地位.

实际读过的外部来源是 [NIST DLMF4.22.3](https://dlmf.nist.gov/4.22.E3) 的公式及极点排除条件, 未声称阅读其参考书. 原始 web 工具响应、明确转录的公式和本地 source_id 指针已保存. 从部分分式推导正性、单调性与局部一致收敛的论证见 [当前 INF 极限证明](../docs/SL_gap_n1_inf_limit_proof.tex).

当前纠错与验收范围见 [第八轮报告](../reports/proof-audit-round8-20260922/REPORT.md). 解析推理、精确有理证书与局部 Lean 分别计证据; 检索放行由精确版本复核回执决定.
