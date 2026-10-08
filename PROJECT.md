# BVE research (MRP-20260731-BVE-SL)

Sturm-Liouville 边值问题的长期研究成果仓库. 两条主线是左定空间/正交系与特征值比值/谱隙极值. 保存文献, 证明, 反例, 失败路线, 数值诊断和部分形式化.

## 文档职责

| 文件 | 职责 |
| --- | --- |
| [README](README.md), [English](README_EN.md) | 首次访问者的项目介绍与代表成果 |
| [research_map](research_map.md) | 人工维护的问题编号, 依赖, 结果范围与剩余缺口 |
| [研究导航](docs/research-guide.md) | 按数学问题选择当前证明, 前置材料和历史替代关系 |
| [项目理解](docs/PROJECT_UNDERSTANDING.md) | 数学理解, 直觉, 失败路线分析和人的批注 |
| [AGENTS](AGENTS.md) | 长期工作规则和简短维护摘要 |
| [RESUME](state/RESUME.md), [current.json](state/current.json) | 人工续接入口与兼容的机器摘要; 历史任务不因旧 active 字段自动重启 |
| [会话日志](state/AGENTS_SESSION_LOG.md), [reports](reports/) | 详细请求, 决定, 实际操作及对应证据; 保留日期语境 |

数学状态由研究地图汇总, 证明由实际来源承载; 本页不另维护逐轮成果清单. 数学证明, 独立审查, 软件测试, 各接收门禁, Lean 与发布分别核对.

## 物理布局与目录职责

[blueprint-project.json](blueprint-project.json) 是现行布局依据. [仓库说明](docs/repository-guide.md) 解释 docs, runs, research, blueprint, index 等目录及源/PDF关系; [归档规则](docs/archive-policy.md) 界定证据保护.

- `docs/` 是活动数学文稿和已有阅读版; `runs/` 与 `research/runs/` 保存各自时期的研究上下文与复现路径.
- `blueprint/` 承载 canonical 图, inventory, submissions 和接收历史. 操作使用已安装插件 gateway.
- `tools/` 保存当前可读工具卡; `index/tools.json` 是派生指针, `research/library/` 保存版本, 批注, 原文及审查/纠错证据. `knowledge/tools/` 是保留的旧管理布局位置, 当前为空. 三者不合并.
- `scripts/` 与 `misc/` 的推荐数值/证书接口见 [脚本导航](scripts/README.md); 历史实现保持原路径. `lean-proof/` 的范围见 [状态表](lean-proof/STATUS.md).

## 接手

先读 [AGENTS](AGENTS.md) 和 [RESUME](state/RESUME.md), 再按问题进入证明与证据. 已有未提交进展, 冻结包和精确版本绑定优先保护. 本次 2026-10-08 先完成本地文档整理与验证, 用户后续“上传”明确授权发布本轮精确范围; 具体授权及实际结果见 [AGENTS](AGENTS.md#2026-10-08-本轮整理发布-用户明确授权).
