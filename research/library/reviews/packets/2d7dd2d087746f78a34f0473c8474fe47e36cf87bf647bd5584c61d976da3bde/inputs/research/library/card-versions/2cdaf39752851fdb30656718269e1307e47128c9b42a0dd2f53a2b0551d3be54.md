---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0e2aa-7f3b-7c71-87a6-16e984423a97"], "created": "2026-08-04", "dependencies": [{"location": "tools/helly-compactness.md", "sha256": "d23aa349893b77ba09890d26779f6505fd1d48dbaebbf3446bc4a661a908a9b4"}], "evidence_status": "ROUND13_SCOPED_CORRECTION_REQUIRES_CURRENT_RECEIPT", "source": "最优控制经典原理", "sources": [{"locator": "Measurable-box existence; switching structure separate", "path": "docs/SL_gap_nge2_finite_reduction_proof.tex", "sha256": "ec20fb4a288308d321f75c72184f17a997257afb412e6ba1fd0ab99c4d3b9f4b"}, {"locator": "Corrected hypotheses and nonattainment boundary", "path": "tools/helly-compactness.md", "sha256": "d23aa349893b77ba09890d26779f6505fd1d48dbaebbf3446bc4a661a908a9b4"}], "status": "第十三轮修订；按精确版本回执检索", "summary": "存在性先检验实际闭类和谱连续性；一阶变分符号决定盒端点，零集与有限开关数需另证。Helly 选择不能单独推出存在性。", "tags": ["mathtool", "extremal"], "title": "bang-bang 原理", "tool_id": "bang-bang", "updated": "2026-09-27"}
---
# bang-bang 原理：存在性、变分符号和零集分别检验

先证明实际容许类中的极值存在。Helly 选择只给子列；推出取到极值还需容许类在所用拓扑下闭合，以及目标的相应半连续性，见 [[helly-compactness]]。本项目完整可测盒 0<a<=rho<=A 的固定模态谱目标采用弱星紧性与谱连续性；这不适用于附加连续端值条件而不闭的类。

若盒上极大值 rho* 的一阶变分是 integral Phi(x)*delta_rho(x) dx，且允许盒内的局部方向变分，则 Phi>0 处 rho*=A，Phi<0 处 rho*=a 几乎处处。极小值的符号相反。仅当零集 Phi=0 的测度为零等非退化条件另行得到时，才可断言极值为两值。零泛函就是所有密度都极值的简单边界，不能由“仿射/单调”直接断言每个极值两值。

两值不自动等于有限跳点阶梯；有限开关数还需要 SL 结构/振荡论证。特征值比值并非密度的仿射泛函，其变分公式及开关结构须分别核对 [[keller-variational]] 和具体项目证明。未在本轮重新认证所有 Keller/MW 文献定理或所有极值结构。

本轮仅修正原 Helly 存在性桥与相应使用前提。完整可测盒的依据在 docs/SL_gap_nge2_finite_reduction_proof.tex 的 lem:wscompact、lem:wscont、cor:attain；连续单调端值类不取到下确界的反例保留在 Helly 卡及原审计包中。
