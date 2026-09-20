---
title: 有理包络证书 (rational-envelope-certificates)
tags: [mathtool, self-developed]
source: 自研 (O3a I3 去证书化, 会话 44, 2026-08-09)
status: E1 严格解析证书链 (L10 生成器 / L11 台账 / L12 表生成器); 57/57 事实全 PASS; 取代十进制区间引擎 (L7-L9 已退役)
created: 2026-08-09
---

# 有理包络证书 (rational-envelope-certificates)

## 解析
把单变量符号/单调性/端点界事实写成有限精确有理数不等式链的 E1 方法, 取代旧十进制区间引擎
(rigid_dec.py) 成为 55 项单变量事实的唯一权威:

1. **交错级数包络**: 对 sin/cos/arctan 用部分和交替夹逼 (余项显式界), pi 由 Machin 公式
   `pi = 16 arctan(1/5) - 4 arctan(1/239)` 的两个反正切项包络组合得到有理界.
   文档引理 lem:envseries (2026-08-09 F-209 修正后): sin/cos 用 12 项部分和 (m=11),
   在 x <= 3/2 时余项分别 <= (3/2)^25/25! ~ 1.6e-21 与 (3/2)^24/24! ~ 2.7e-20 (均 < 1e-12);
   arctan 用 22 项 (m=21), 但直接级数仅用于参数 v <= 1 (余项 <= v^45/45 <= 1/45);
   pi 由 Machin 公式 (参数 1/5, 1/239, 余项 ~7.8e-34 / ~2.1e-109, pi 宽度 ~2.5e-32);
   最差原语包络宽度为 tau(131/200) 行约 1.8e-10 = 2 v^45/45 (v ~ 0.651), 其余 <= 1e-23;
   全部宽度远小于最小裕量 ~2.6e-5, 不影响任何符号判定.
   每项 = 精确有理区间 + 目标界 + 严格正裕量.
5. **证书表**: misc/e1_cert_tables.py -> misc/e1_cert_tables.tex (5 张表: 原语包络,
   点值证书, 区间符号, 区间极值, 导数符号); 显示为向外取整 (显示区间包含认证区间),
   6/12 位小数.

## 适用范围
- 适用: 闭区间上由初等运算与 sin/cos/arctan 组合的单变量实函数; 符号/单调性/端点有理界的
  严格判定; 裕量可小到 ~2.6e-5 (h(0.655) - m) 仍可认证; 与 W-分解链配合可把二维盒目标
  完全解析化 (J2_2d < 0 的 55 项事实全部 E1).
- 边界情形: 端点闭包含入; 宽区间用值泰勒模型分片; h 类事实用凹性归约 (端点值 + 凹性
  覆盖整个区间); 凹性本身由二阶导数包络认证.
- 不适用: 多维盒依赖 (直接二维叶盒, 旧路线需 67 叶盒); 作为 kernel-checked proof 的替代
  (证书是可人工复核的有理不等式链, 不是形式化证明内核; 文档 rem:trust 有 caveat).

## 验证与备注
- 内容哈希: L10 生成器 misc/e1_certgen.py = 375209e2...; L11 台账 misc/e1_cert_ledger.json
  = ec9ce5ff...; L12 表生成器 misc/e1_cert_tables.py = dce5c453... (2026-08-09 版本).
- 内核修复: misc/rigid1d.py 的 I.sqrt 曾写 `F(isqrt(...), den)+1` (宽度恒为 1.0),
  已改为 `F(isqrt(...)+1, den)`, 这是 TB 点事实失败的原因.
- 复现: `py -X utf8 misc\e1_certgen.py` (约 266 秒, 需 sys.set_int_max_str_digits(1000000));
  57/57 PASS.
- E3 交叉检验 (不构成证明): 最紧裕量 h(0.655) >= m 约 2.6e-5; Qlo(1.0014) <= -1/10000
  约 6.3e-5; TA_B2(0.86) >= 47/25 约 2.2e-4; 区间下界 TA_B2 >= 27/10 于 [0.723,0.724]
  约 2.4e-3; TC >= 19/10 于 [0.82,0.83] 约 0.06; 单调性泰勒模型裕量全正 (最小 ~3.9e-2).
- 取代: 旧十进制定向舍入区间引擎 [[interval-dec-directed-rounding]] (L7-L9) 已退役,
  55 项事实不再依赖任何验证器内核; 结论依据只写 E1 的有限有理区间链.
- 相关: [[true-curve-region-decomposition]], [[phase-param-2d-certificate]],
  [[cot-series-certificate]], [[interval-dec-directed-rounding]].

### 2026-08-10 追加: 独立第三方重放引擎 (misc/audit_o3a_cert_replay.py)
- 用 decimal.Decimal 80 位有效数字 + 定向舍入 (ROUND_FLOOR/CEILING) 独立重放 71 项
  (57 台账事实 + 11 原语行 + 3 结构检查), 全部 PASS; 与精确 Fraction 生成器零共享
  算术代码. sin/cos/atan/pi 经交错 Taylor 级数 (sin/cos 60 项, atan 80 项) 与 Machin
  公式, 余项界同样定向舍入. 裕量偏差 <= 2.7e-11 (全局最小裕量 2.56e-5).
- 用途: 对有理包络证书链的独立复核工具; 证明本身仍是台账中的有限精确有理不等式链.
- 重放脚本哈希 3a8672f4..., 结果 json c239092d...; 详见 run 工件 Audit E 段.

- 2026-08-10 修正: 原表述 "arctan 22 项在 x <= 3/2 时余项 < 1e-12" 为 F-209 修复前残留,
  已按修正后的 lem:envseries 更新 (直接级数仅用于 v <= 1, 余项 <= v^45/45; 最差宽度
  tau(131/200) ~ 1.8e-10).