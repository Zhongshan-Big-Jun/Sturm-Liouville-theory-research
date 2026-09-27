---
title: 十进制定向舍入区间引擎 (interval-dec-directed-rounding)
tags: [mathtool, self-developed]
source: 自研 (O3a I3 去证书化, 会话 40 续, 2026-08-09)
status: E1 有限区间实现 (证书重放器, 非形式化验证内核); 4800 次随机包含性自检零违反; 55 项单变量事实全部认证通过 (ledger 内容哈希 L9)
created: 2026-08-09
---

# 十进制定向舍入区间引擎 (interval-dec-directed-rounding)

## 解析
本项目 E1 去证书化路线需要把单变量符号事实逐项严格化, 为此自建
十进制定向舍入区间运算引擎 `misc/rigid_dec.py`:

1. **区间类型**: 每个量表示为 `[lo, hi]` 的 Decimal 区间, 所有基本运算
   (加减乘除, 幂, 开方) 分别以 ROUND_FLOOR (lo) 与 ROUND_CEILING (hi)
   向外舍入, 保证真值始终被包含.
2. **超越函数**: `pi` 由 Machin 公式 `16 arctan(1/5) - 4 arctan(1/239)`
   构造, 两个反正切项分别按区间处理; `sin/cos` 用带显式交错级数余项界的
   Taylor 展开; `arctan` 用交错级数 (`x <= 1`) 或 `pi/2 - arctan(1/x)`
   (`x > 1`). 余项界保证区间端点严格包含真值.
3. **对偶数 D1**: 每个表达式可带导数通道 `(v, dv/dx)`, 区间传播导数,
   用于导数符号判定.
4. **验证原语**:
   - `der_sign(fn, a, b, want_pos)`: 自适应细分, 证明 fn 的导数在 `[a,b]`
     上恒正/恒负 (区间导数不含零);
   - `range_pos(fn, a, b)`: 自适应细分, 证明 fn 在 `[a,b]` 上取值恒正;
   - `val_at(fn, x)`: 单点区间求值, 与精确有理数端点比较 (as_integer_ratio).
5. **使用范例** (J2 侧 E1, 定理 thm:j2e1): 55 项单变量事实包括
   `B1` 递减与 `gamma0 in (0.85,0.86)`; `B2<0, M<0, B4>0, G5>0, Q_+<0`;
   `Q_-` 递增与两个端点界; `F` 递增与端点界; `h(t) = (t/2) sin 2t >= m`
   于 `t in [0.655,13/10]` (33 盒) 与 `h(gamma), h(tau) >= m`; `tau(1.0472)
   < 13/10` 点界; `T_A,B2 / T_A,M` 各段单调与端点界; `T_B` 递减; `T_C`
   递增/递减与端点界. 细分盒数与逐项结果见 `misc/e1_facts_ledger.json`.

## 适用范围
- 适用: 定义在闭区间上的单变量实函数符号/单调性/端点界的严格判定,
  其中函数由初等运算与 sin/cos/arctan 组合而成; 与 W-分解链
  (J2_2d = N/(16 Delta^4), W = T1+...+T8) 配合可把二维盒目标完全解析化.
- 边界情形: 安全裕量极小的断言 (如 h(0.655) - 0.3164 ~ 2.6e-5) 仍可
  认证, 但需足够细分 (默认 min_w = span/2^24); 区间宽度不够时可提高
  Decimal 精度 (默认 prec = 70).
- 不适用: 多变量相关性问题 (直接二维区间盒依赖过宽, 旧尝试需 11553 盒);
  形式化证明意义上的内核可信度 (本引擎是独立审计的证书重放器, 不是
  kernel-checked proof, 见证明文档 rem:trust 的 caveat).

## 验证与备注
- 引擎与 80 位 mpmath 做过 4800 次随机包含性检查, 零违反
  (`misc/_test_dec.py`).
- 55 项事实全部 PASS (`misc/zz_verify_e1_dec.py`, ~4 s),
  台账 `misc/e1_facts_ledger.json`.
- 内容哈希: L7 引擎 `dd81278e...`; L8 验证脚本 `cad6c5ef...`;
  L9 台账 `cc74fc50...` (2026-08-09 版本).
- 关键使用教训: D1 导数通道必须用完整的表达式自动微分 (含三角项),
  早期 `_test_dec.py` 曾冻结三角项导致 TA_B2 导数误报; 正确实现后
  单调性事实全部通过.
- 相关: [[true-curve-region-decomposition]], [[phase-param-2d-certificate]],
  [[interval-ad-certificate]], [[cot-series-certificate]].