---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0e2aa-7f3b-7c71-87a6-16e984423a97"], "created": "2026-08-09", "evidence_status": "ROUND13_SCOPED_CORRECTION_REQUIRES_CURRENT_RECEIPT", "source": "自研 (O3a I3 去证书化, 会话 44, 2026-08-09)", "sources": [{"locator": "Current rational envelope, certificate tables and explicit trust boundary", "path": "docs/SL_gap_n1_O3a_phase_rigidity_proof.tex", "sha256": "1c4dc7ea120a1c4f422fb7d2adc9e1ae002aaef0bace45a125a3c5c56e9f0e22"}, {"locator": "R13-01..06 proof and evidence scope", "path": "research/artifacts/proof-audit-round13-20260927/certificate-repair.md", "sha256": "ff63e541ec21fa4714b6ad61e009894ae81da7598bacc6d08bf372461d847c51"}], "status": "第十三轮修订；按精确版本回执检索", "summary": "57 条完整有理证书；精确端点、正确值域、非零阈值及失败传播。解析包络与接收器均须核对，不是 Lean 证明。", "tags": ["mathtool", "self-developed"], "title": "有理包络证书 (rational-envelope-certificates)", "tool_id": "rational-envelope-certificates", "updated": "2026-09-27"}
---
# 有理包络证书：精确端点与完整命题

当前入口为 misc/e1_certgen.py → misc/e1_cert_ledger.json 及其 .status.json → misc/e1_cert_receive.py / misc/e1_cert_tables.py。本轮重算保留 57 条完整命题，不以函数正性替代非零阈值。TA_B2>=27/10、TC>=19/10 与严格 tau<13/10 都进入实际谓词。

sin/cos 点包络使用有界导数 Taylor 余项；区间使用完整偏移值域，包含内部极值，宽偏移使用 [-1,1]。atan 单调端点算法在跨 1 时也终止。支持域、平方根和导数条件详见本轮解析修订。精确有理端点、Taylor 中心、斜率、M、M*w、最终界和裕量存入台账。下端向下，上端向上；半径向上、裕量向下；不得把窄区间显示成漏真值的单点。

生成器只有全部事实验收才发布 PASS；失败、异常和不可判定均退出非零。接收器核对本次状态、精确台账哈希、当前源文件哈希、完整合同与有理见证。它不构成独立超越函数引擎或 Lean 证明。解析包络论证、有理数运算、浮点交叉检验及形式化认证必须区分。

B1(.85) 的当前显示区间为 [0.009851718322,0.009851718323]，仍大于 1/200。本轮未降低原阈值，也未撤回 O3a 相应命题。全部实际命令与负对照见本轮报告；使用前仍须检查函数域和命题合同。

旧 rigid_dec.py、zz_verify_e1_dec.py、旧 Decimal 重放 audit_o3a_cert_replay.py 及其 PASS 记录只保留历史身份，不提供当前可信入口。随机包含性自检不能排除本轮明确反例。旧卡字节在工具库版本历史中保留。当前依据见 [证书修订](../research/artifacts/proof-audit-round13-20260927/certificate-repair.md) 与活动 O3a 正文附录。
