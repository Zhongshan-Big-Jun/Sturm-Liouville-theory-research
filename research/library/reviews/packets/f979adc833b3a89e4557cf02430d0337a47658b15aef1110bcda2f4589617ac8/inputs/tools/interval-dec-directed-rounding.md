---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0e2aa-7f3b-7c71-87a6-16e984423a97"], "created": "2026-08-09", "evidence_status": "WITHDRAWN_RETIRED_ENGINE", "source": "自研 (O3a I3 去证书化, 会话 40 续, 2026-08-09)", "sources": [{"locator": "R13-03/05/06", "path": "research/artifacts/proof-audit-round13-20260927/submitted/REPORT.md", "sha256": "bd54f71accd5fe0d4d2940e198102a638bee5a2c142e1206abe23ffb702c58b8"}], "status": "已退役；默认可信复用撤回", "summary": "WITHDRAWN：旧 Decimal 的 sqrt、负号、三角内部极值漏包及失败退出码反例已确认，仅供历史复现；当前入口是有理包络证书。", "tags": ["mathtool", "self-developed"], "title": "十进制定向舍入区间引擎 (interval-dec-directed-rounding)", "tool_id": "interval-dec-directed-rounding", "updated": "2026-09-27"}
---
# 旧 Decimal 区间引擎：退役与复用阻断

本卡是失效提示，不是可靠引擎推荐。原 misc/rigid_dec.py 的 sqrt、取负和三角内部极值存在明确漏包反例；旧 zz_verify_e1_dec.py 的失败事实仍可能成功退出。本轮保留原代码、原台账、4800 次随机自检记录及原卡版本，不能将它们重写成新的通过记录。

默认可信复用已撤回。需要历史复现时必须显式标注旧版本、不可信包络与失败退出码缺陷；若以后确需 Decimal 路线，应建立新版本并独立验证，不能凭提高精度或追加随机样本恢复信任。当前主证明已退役此引擎；这里的错误不直接反证当前主定理。

当前替代入口是 [[rational-envelope-certificates]] 的精确 Fraction 包络与完整接收合同。反例和原始证据见 [第十三轮原包](../research/artifacts/proof-audit-round13-20260927/submitted/REPORT.md) R13-03/05/06。旧独立 Decimal 重放脚本也只作历史材料，不作为当前证书接收器。
