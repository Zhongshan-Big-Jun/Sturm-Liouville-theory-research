# 最小化方向反射对称性：合作者核验包

冻结日期：2026-08-16

本包用于独立核验 Sturm--Liouville 相邻谱隙最小化方向的反射对称性研究。
建议先阅读：

1. output/min_direction_progress_20260816/min_direction_progress.pdf
2. runs/R-20260816T034422Z-min-reflection-cont2/PAUSED_REPORT.md
3. statistics/blueprint.json

## 可信性标签

- accepted/canonical：已完成不可变提案、独立审查和确定性合并。
- pre-reviewed：证明包已独立预审，但尚未进入 canonical 图。
- finite certified：仅对声明的有限参数域成立的严格计算证书。
- open：尚未闭合的证明义务。

请勿把有限 Arb 覆盖、局部代数反例或条件桥解释为一般参数下的全局定理。

## 建议核验顺序

1. full_relay：全区间 relay 约化。
2. symplectic_nested_reduction 与 physical_realizability_r7。
3. r9_min_complementary 与 r10_min_full_interface：n=2, mu=2 局部 twist 和 539 项 Bernstein 证书。
4. r11_min_mu2_global_order：局部符号到全局反射。
5. r15_min_mu2_general_n_nonexistence：n>=3, mu=2 非存在性。
6. compact_mu2_strip：紧对比度区间上的参数带。
7. 其余目录：一般 mu、一般 n、有限覆盖与严格 no-go 结果。

## 重放环境

- Python 3.12
- SymPy 1.14.0
- python-flint 0.9.0（Arb 证书）

脚本中的旧绝对 Python 路径只记录原始运行环境。合作者可用自己的 Python
解释器，从本包根目录运行相同的相对脚本路径。

PACKAGE_MANIFEST_SHA256.txt 列出包内研究文件的 SHA-256。
