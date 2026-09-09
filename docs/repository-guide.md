# 目录, 文档构建与复现

[中文首页](../README.md) | [English overview](../README_EN.md) | [研究导航](research-guide.md)

## 从哪里开始

| 位置 | 内容与用途 |
| --- | --- |
| [docs/](./) | TeX 证明与可读 PDF; 从研究导航按问题进入 |
| [tools/README.md](../tools/README.md) | 文献工具, 自研方法及旧路线的卡片索引 |
| [research_map.md](../research_map.md) | 稳定问题编号和关系图; 某些状态段落早于最新 run |
| [PROJECT_UNDERSTANDING.md](PROJECT_UNDERSTANDING.md) | 人机共同编辑的研究解释, 失败路线再检视与候选动作 |
| [lean-proof/](../lean-proof/) | Lean 源码, 状态表, 审计与脚手架登记 |
| [blueprint/](../blueprint/) | canonical 数学图, inventory, 不可变提交与接收记录 |
| [research/artifacts/](../research/artifacts/), [research/runs/](../research/runs/) | 已保存的证明工件及新布局中的研究 run |
| [runs/](../runs/) | 历史研究, benchmark 与复现包; 路径可能被证据清单绑定 |
| [collaborator_min_direction_verification/](../collaborator_min_direction_verification/) | 合作者研究的核验包 |
| [scripts/](../scripts/README.md), [misc/](../misc/) | 探索程序, 证书程序与历史诊断; 按实际用途判断证据等级 |
| [papers/](../papers/), [literature/](../literature/), [research_cache/](../research_cache/) | 已有文献与读取资料; 遵守各来源的使用许可 |
| [state/](../state/), [index/](../index/), [reports/](../reports/) | 接续入口, 索引, 研究与工程报告 |

[blueprint-project.json](../blueprint-project.json) 是物理布局依据. 既有目录按引用保留; 本轮通过导航组织内容, 没有移动 canonical 或哈希绑定的研究工件.

## 阅读与构建文档

阅读可以直接打开研究导航中的 PDF. 编辑后在 `docs/` 使用已配置中文字体的 XeLaTeX, 将中间文件写入 `build/`. 例如从仓库根运行:

```bash
cd docs
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build SL_ratio_proof.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build SL_ratio_proof.tex
```

核对 PDF 与日志后再选择发布的文档版本. `docs/build/` 中的 PDF 也可能是旧证明清单的证据, 应按原路径保留. 本轮清理没有替换任何 TeX 或 PDF, 也没有重新编译研究文档.

## Lean 的复现范围

工程中的 [lean-toolchain](../lean-proof/lean-toolchain) 与 [lakefile.lean](../lean-proof/lakefile.lean) 当前固定 Lean/mathlib v4.31.0. 安装相应工具链后, 从仓库根检查一个已有文件:

```bash
cd lean-proof
lake env lean SL/MomentGrowth.lean
```

`lake build` 可检查包中的构建目标, 但工程包含有 `sorry` 的研究脚手架, 某些已编译定理也显式假设尚未接入的分析结论. 构建成功不等于整个数学项目已形式化. 发布某个形式化结果时, 对照原陈述核对具体根声明, 其依赖和实际使用的公理, 并引用对应代码版本和日志. 使用插件自己的验证工具, 不把旧全库计数当作当前结论.

## Blueprint 与研究程序

canonical 的读取与校验通过当前安装插件的 `runtime/blueprintctl.py` 完成. 根 [AGENTS.md](../AGENTS.md) 约定先完成一次运行时 `ensure`, 再使用 `query` 或 `validate`; 本仓库的历史本地 Blueprint Python 工具不作为运行入口. 本次整理使用已有的有效运行时绑定, 没有接收新的数学命题.

[脚本导航](../scripts/README.md) 帮助区分数学实现和一次性维护代码. 需要复现证明时, 先读取对应 run 的契约与复现清单, 再确定环境, 输入和精度. 不能仅凭脚本名, 目录名或成功退出判断结果是否严格.

## 清理与历史

本轮的 [清理报告](../reports/repository-cleanup-20260909/REPORT.md) 与 [逐项清单](../reports/repository-cleanup-20260909/cleanup-manifest.json) 记录删除理由, 原始哈希, 引用检查和保留项. [归档规则](archive-policy.md) 要求先检查证据绑定与活跃状态; 文件年代和重复内容本身都不是删除依据.

旧中文与英文首页以原字节保存在 [历史中文](history/README.pre-v2.zh.txt) 和 [历史英文](history/README.pre-v2.en.txt). 根 AGENTS 的长会话记录归入 [state/AGENTS_SESSION_LOG.md](../state/AGENTS_SESSION_LOG.md). 数学状态保持原始证据与显式范围, 文档导航中的当前解释不覆盖历史原件.
