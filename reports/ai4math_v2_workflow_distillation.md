---
title: AI4Math V2 工作方法蒸馏报告
tags: [ai4math, distillation, workflow, report]
created: 2026-08-12
---

# AI4Math V2 工作方法蒸馏报告

- 日期: 2026-08-12
- 数据来源: AI4Math 会议手册 V2 (2026.07.22-24, 浙大 IASM) OCR 全文 + 演讲者项目 GitHub 仓库 README/文档/prompts (GitHub API, 逐一核实可达) + OpenAlex 元数据 (FormalRx 摘要).
- 检索边界 (如实): arXiv API 多次超时不可用, Semantic Scholar 429 限流, OpenAlex 可用; 梁经纬 Paper2Formalization 与邹扬硕 Fyan 未开源 (无公开仓库, 不猜测); 手册为扫描件, 以 OCR 文本为准 (见 _ai4math_ocr.txt).
- 目标: 优化五个功能面 - 提出问题, 搜索文献, 研究问题, 总结技术, Lean 验证.
- 关联: 演讲者仓库定位清单见 [[ai4math_2026_github_repos]]; 蒸馏出的可复用方法条目在 [[tools/README|工具库]] (类别: 研究工作流方法).

> [!info] 使用说明
> 每节给出一张方法卡: 来源 (附链接), 方法要点, 可蒸馏到本项目技能体系的具体做法, 代价与边界.
> 采纳建议只涉及工作方法, 不改变数学结论的证据分层规则 (严格证明/数值证据/猜想必须显式标注).

## 1. 提出问题 (Problem Posing)

| 来源 | 方法 | 可蒸馏点 |
|---|---|---|
| [EvE (scaling-group/eve)](https://github.com/scaling-group/eve) (杨柳, NUS; arXiv:2605.09018) | 双种群进化: 求解器种群 (repo 内功能组件) 与 agent 种群 (指导与技能) 共进化; 每次变异由测试/评分驱动, 边际收益决定取舍, 无需任务特定工作流 | 把"提出新问题"变成可评分过程: 对开放问题清单按证据状态打分 (已证/部分/数值/开放), 让 agent 以"提高一个问题的证据等级"为目标自动生成下一批候选子问题; 工具库 tools/README 维护日志本身就是可评分的演化记录 |
| [FATE 基准设计 (frenzymath/FATE)](https://github.com/frenzymath/FATE) | 每个问题 = 一条形式化陈述 + 单个 sorry + 自然语言注解; M/H/X 三级难度按来源分层 (教材/期末/资格考) | 本项目提问时固定"问题契约"格式: 主断言 + 显示前置条件 + 目标极性 (存在/唯一/不等式/分类/反例), 与 [[workflow-blueprint-dag-ci|蓝图目标契约]] 一致; 难度分层便于安排研究优先级 |
| 居浩成 (北大) 开放问题自动推理 agents (无公开仓库) | 演讲主题: 面向数学开放问题的 agent 设计 | 只能作为趋势参考, 无法蒸馏具体协议; 不猜测其内部机制 |

## 2. 搜索文献 (Literature Search)

| 来源 | 方法 | 可蒸馏点 |
|---|---|---|
| [MMAT nl-prover searcher prompt](https://github.com/MechMath/MechMath-agent-team/tree/main/nl-prover/prompts) (曹一川/邱瑞晨, 中科院) | 发散角色契约: 搜索要宽, 不做守门人; 只做轻审计 (是什么/谁的/哪来的/是否大致相关); 正确性审计交给独立 verifier; 硬约束是来源诚实 - 每条记录必须可追溯到真实查询结果, 禁止编造 | 直接写入 [[workflow-divergent-search|发散式检索]]: 本项目文献检索子任务把"相关性判断"与"正确性审计"分离; 检索产出必须是 查询 -> 结果 -> 定位器 三要素齐全, 无法追溯的一律不写 (呼应已有规则: 引用必须附链接, 不得编造文献) |
| 同上 (searcher 分层检索流程) | 关键词族 (同义词/符号变体/旧词汇) -> KB 优先 -> 本地 references -> 最近查询索引 -> Matlas/arXiv -> 通用网页 (教材/讲义/MO/MSE/期刊页/GitHub, 非论文来源常含构造与反例) -> 深读命中正文而非停在摘要 | 本项目检索升级为分层流水线: 先查 tools/ 与 research_cache/, 再 arXiv/OpenAlex/zbMATH, 再通用网页; 每层记录贡献; 命中必须深读到"需要的陈述 + 前置条件 + 定位器" |
| [MathWeaver 多通道召回](https://github.com/SJTU-AI4Math/MathWeaver) (许景宣, 上交) | 候选召回不直接全量送 LLM: 稀疏通道 (局部窗口/文内引用/BM25F/符号重合) + 稠密通道 (embedding 相似度, 结果缓存) + 图结构扩展, RRF 合并后送 LLM | 搜索文献的候选合并可复用: 多通道候选 + 排序融合; 本项目体量小, 可先落地"引用图扩展" - 从已确认论文的参考文献出发扩展候选, 再按引用频次/年份融合 |
| [KB-Manager](https://github.com/MechMath/MechMath-agent-team/tree/main/kb-manager) (MMAT) | 原始资料 hash 寻址不可变存储 (raw_sources/<sha256_12>/), 编译后的 wiki 为查询入口; researcher 只从 wiki 回答并区分 直接陈述/逻辑推断/缺口 | 搜索前先查知识库, 搜索后把新资料登记为不可变原始源 + 编译摘要, 避免重复追溯; 对应本项目 research_cache/ 升级为"原始源 + 索引"双层结构 |
| [LeanSearch](https://github.com/frenzymath/LeanSearch) (北大 frenzymath; arXiv:2403.13310) + [Herald](https://arxiv.org/abs/2410.10878v2) | Lean 项目的语义检索; Herald 把形式陈述翻译为自然语言用于检索 | 形式化阶段检索 mathlib 命题可用; 现阶段仅记录为可选工具, 不落地 |

## 3. 研究问题 (Problem Research)

| 来源 | 方法 | 可蒸馏点 |
|---|---|---|
| [MMAT nl-prover 编排](https://github.com/MechMath/MechMath-agent-team/tree/main/nl-prover/prompts/orchestration.md) | hub-and-spoke: orchestrator 只路由不证明; sketcher 分解引理 DAG 并写 target_contract (主断言与显示条件分离, 记录等价方向, 边界约定审计); generator 独立证引理; verifier 以"第一次见到证明"的身份独立审稿; auditor/explorer/ce-hunter/regulator 分工; 失败路由到最小责任角色 | 直接落地 [[workflow-hub-spoke-contract|hub-and-spoke 角色契约]]: 研究任务拆分 草稿者/证明者/验证者 三角色, 验证者必须无记忆独立审查, 并内置自动 FAIL 模式清单 (循环论证/方向错误/漏情形/超假设/依赖误用/未解决的承重义务/凭空定理等 14 条) |
| [LeanMarathon](https://github.com/YuanheZ/LeanMarathon) (刘方辉/张远喆, 上交) | 蓝图 = 形式骨架 + 自然语言证明图 + 系统记录; 四角色 (Blueprinter/Target-Reviewer/Refiner/Worker) 契约限定; 两阶段: 先蓝图 CI 绿, 再 DAG 自叶向上并行证明; 失败由 Refiner 修 | 研究问题先出"蓝图文档"再动手: 目标契约 + 引理依赖图 + 每节点状态 (待证/候选/已证/阻塞), 每次会话先读蓝图; 大型项目可并行但本项目以单 agent 串行为主, 蓝图价值在于状态追踪 |
| [Archon-Horizon](https://github.com/frenzymath/Archon-Horizon) (吴彬/董彬, 北大) | workspace 为工作单元; 新鲜上下文收敛检查: 只读 Ground helper 在任务收尾/长跑中段/策略转向后被调起, 从 ledger 差异/报告/路线图/inbox/图/Lean 状态重建上下文并回答"是否在收敛", 只写 issue 不编辑源码; 团队间通过共享 board/inbox/commit ledger 异步协调 | 研究会话收尾前增加"新鲜上下文检查"步骤: 不读对话历史, 只从文档/工具库/清单重建现状, 判断收敛还是发散; 对应 AGENTS.md 的会话记录维护, 可作为每次变更后的强制复核 |
| [M2F/ReasBook](https://github.com/optsuite/M2F) (文再文, 北大) + [Quokka](https://quokka.reaslab.io/) | 文献级形式化两阶段: 陈述编译 (允许 sorry 保持结构覆盖, 修复命名空间/签名一致性) -> 陈述冻结 -> 证明修复 (验证器反馈迭代) | 研究问题中"证明修复"环节: 先保证结构完整与陈述稳定, 再补细节; 避免每轮重写整个证明 |
| [AIM](https://github.com/TheoryFoundry/AIM) (李鹏, 清华) | 自然语言驱动的数学研究 agent, 以论文/笔记为输入组织研究流程 | 研究问题阶段保留 NL 中间产物 (证明草稿/总结), 与形式化解耦; 本项目已有此实践 (docs/*.tex + lean-proof/), 无需改动 |

## 4. 总结技术 (Technique Summarization)

| 来源 | 方法 | 可蒸馏点 |
|---|---|---|
| [KB-Manager wiki 编译](https://github.com/MechMath/MechMath-agent-team/tree/main/kb-manager) | 原始源 -> wiki 编译为可复用知识; 卡片类型 Analysis_*/PartialProof_*/Obstruction_* 显式区分 完整分析/部分证明/受阻路径; 先前的部分进展与排除路线也是知识库的一部分 | 与 tools/ 工具库同构: 新工具文件统一卡片结构 (解析 + 适用范围 + 验证状态), 排除路线/失败尝试也登记 (项目已有此实践); 建议新增字段 关联问题 与 来源链接, 使工具可追溯 |
| [SNL-Basics](https://github.com/SJTU-AI4Math/SNL-Basics) (刘云天, 上交) | 结构化自然语言: 宏 DSL 解析为语法树, 渲染后端与内容分离 (Typst/LaTeX/Markdown 由消费者决定) | 总结技术文档时先写结构化内容再定渲染; 本项目 tex 文档可保持现状, 但工具库 md 统一 frontmatter 即为此做法 |
| [MathWeaver 知识抽取](https://github.com/SJTU-AI4Math/MathWeaver) (许景宣, 上交) | PDF -> MinerU OCR -> Markdown -> 14 阶段知识抽取 (文本修复分段/知识提取补全/结构化引用校正/关系构建) -> 知识图谱; TeX 输入保留标签与源位置, 确定性解析优先, 残余才进受控 LLM | 总结技术时采用 确定性优先 + LLM 兜底: 能从结构解析的 (定理编号/引用/公式) 不交给 LLM; 需要 LLM 的部分 (语义关系) 保留源锚点; 防止 LLM 改写原文 |
| [LeanExplain](https://github.com/SJTU-AI4Math/LeanExplain) (刘晓洋/董子能, 上交) | Lean 4 Infoview 插件: 把声明与证明翻译为自然语言解释, 按声明类型走专用 prompt | 形式化完成后反向生成 NL 说明作为文档素材; 可选工具 |

## 5. Lean 验证 (Lean Verification)

| 来源 | 方法 | 可蒸馏点 |
|---|---|---|
| [M2F](https://github.com/optsuite/M2F) (文再文, 北大) | 陈述编译时允许 sorry 保持结构覆盖 -> 陈述冻结防漂移 -> 验证器引导迭代补证明; 阶段 2 对匹配陈述 100% PSR (README 声明) | lean-verify 工作流先冻结陈述签名再修证明; 任何对已批准陈述的修改必须重新过审 |
| [MMAT sorrifier](https://github.com/MechMath/MechMath-v1) (曹一川/邱瑞晨, 中科院; repo 描述: Sorrifier-Driven Formal Decomposition Workflow) | 失败证明块替换为 sorry 保留验证骨架 -> 提取干净子问题 -> 递归解决; 避免全量重生成与上下文膨胀 | 直接落地 [[workflow-sorrifier-decomposition|sorrifier 分解]]: 失败时把失败子目标 sorry 化, 验证其余部分仍编译, 再单独攻失败块 |
| [MMAT FL-Prover 四道闸](https://github.com/MechMath/MechMath-agent-team/tree/main/fl-prover) | 任何进入 master 的编辑必须过: 编译检查 / sorry 扫描 / axiom 集检查 / 受保护陈述守护 (guard); 最后由 regulator 做语义复核 (陈述仍忠于源文献) - 最后一道是 LLM 不能替代的意义检查; integrator 是唯一合并路径 | lean-verify 增加四道闸 + 语义复核: 编译 / sorry / axiom / 陈述未变, 加一道"形式化陈述与源命题语义一致"的人工复核 (人做, 不是 LLM 自评) |
| [FormalRx](https://github.com/LARK-AI-Lab/formalrx) (王浩丞, ETH/港科大广州; arXiv:2607.04655) | SCI 错误分类法: 自动形式化错误分 28 类带严格优先级; 四个诊断能力: 判定/分类/定位/修正; 8B 诊断模型, 56,287 NL-FL 对训练 (OpenAlex 摘要) | 错误诊断 checklist: 遇到 Lean 报错先分类再修正 (陈述层 vs 证明层 vs 依赖层); 审计报告按"首错定位"写作 |
| [FaithSieve](https://github.com/TropicalFatFish/anonymous-faithsieve) (匿名投稿, 对应文再文演讲) | proofloc 数据集: 奥林匹克 350 + 大学 200 条 问题-证明对, 每条标注 first_error_step | 审稿与验证报告只定位"第一个错误步骤", 而不是泛泛给意见; 本项目 audit_report 已有类似实践, 可固化为模板字段 |
| [LeanAide](https://github.com/siddhartha-gadgil/LeanAide) (Ajay Kumar Nair, 印度科学院) | Autoformalization + Combinator Code Generation (元编程组合子) | NL 陈述 -> Lean 翻译可尝试; 依赖 GPT-5/OpenAI key 与 embedding, 属可选增强 |
| [reap](https://github.com/frenzymath/reap) (王语同, 至知科技) | 神经 tactic: MCTS 证明搜索 + RL 接口, policy/value/premise-selection 服务 | 重型基础设施 (需训练模型/端点), 现阶段仅记录, 不落地 |
| [jixia](https://github.com/frenzymath/jixia) (北大) | Lean 4 静态分析: 声明/符号/引用图/行级证明状态插件, 非侵入式 | 形式化项目结构审计可选工具; 现阶段不落地 |
| [OptProver](https://github.com/chenyili0818/OptProver) (文再文团队; arXiv:2604.23712) | 专家迭代 + 验证器偏好学习 (区分 已证/无效/停滞 tactic) + perplexity-weighted DPO | 属于模型训练方法, 非工作流方法; 可借鉴其"验证器反馈三分类"思想用于人工复核 (有效/无效/无进展) |

## 6. 交叉方法与总体设计原则

- 角色分离是共同主题: orchestrator 只路由不证明 (MMAT), 验证者与作者分离且"第一次见到" (MMAT verifier), searcher 与 auditor 分离 (发散检索不守门, 审计独立), integrator 唯一合并 (FL-Prover). 对应本项目: 提出/研究/验证/总结 四类任务用独立子代理, 避免同一上下文既当运动员又当裁判.
- 双 harness 同步规范: MMAT 的 Codex + Claude 双 harness 共享同一份 prompts, 只有调度机制不同; 保证规范与实现解耦. 本项目 skill 版本更迭说明只写功能增量 (既有约定).
- 记忆与索引压缩: MMAT 要求"读压缩索引而非全量扫描", 长期负约束记忆是硬前置条件. 对应本项目: 会话开始时先读 tools/README 索引与 AGENTS.md 会话记录, 而不是重读全部文档.
- 失败是知识: KB-Manager 把 PartialProof_/Obstruction_ 卡片当作知识库正式成员; 本项目失败尝试登记 (会话记录 + 总结文档) 已符合此原则, 保持.
- 诚实边界: 检索层禁止编造来源; 验证层禁止把数值证据当结论; 这两条与 AI4Math 各团队的"来源诚实/审计独立"原则一致, 是方法的底线而非限制.

## 7. 采纳路线图 (按三个 skill 映射)

### manage-math-research-program (管理)
- 立即落地: [[workflow-kb-hash-wiki|hash 寻址知识库 + wiki 编译]] (项目库结构), [[workflow-divergent-search|发散式检索契约]] (文献检索子任务规范), [[workflow-first-error-taxonomy|首错定位 + 错误分类]] (审计报告模板), 新鲜上下文收敛检查 (会话收尾复核).
- 后续: [[workflow-eve-coevolution|EvE 双种群进化]] 思想用于工具库演化 (边际收益驱动), 蓝图 + DAG 状态追踪 (多任务并行时启用).

### rigorous-open-math-research (研究)
- 立即落地: [[workflow-hub-spoke-contract|hub-and-spoke 角色契约]] (草稿者/证明者/验证者/审计者), target_contract 目标契约 (主断言/方向/边界约定), verifier 自动 FAIL 清单, regulator 失败分类路由.
- 后续: sorrifier 分解用于长证明卡点, 蓝图文档用于跨会话研究.

### lean-verify (验证)
- 立即落地: [[workflow-statement-freeze|M2F 陈述冻结]] 两阶段, [[workflow-sorrifier-decomposition|sorrifier sorry 化分解]], 四道闸 (编译/sorry/axiom/guard) + 人工语义复核.
- 后续: FormalRx 28 类错误分类作为诊断 checklist, jixia 静态分析, LeanAide 翻译器, reap 战术 (需基础设施).

## 8. 来源清单 (全部附链接, 2026-08-12 核实可达)

- LeanMarathon: https://github.com/YuanheZ/LeanMarathon (paper.pdf 在仓库内)
- M2F: https://github.com/optsuite/M2F ; Quokka: https://quokka.reaslab.io/ ; ReasBook: https://github.com/optpku/ReasBook
- LeanAide: https://github.com/siddhartha-gadgil/LeanAide
- FaithSieve (匿名): https://github.com/TropicalFatFish/anonymous-faithsieve
- OptProver: https://github.com/chenyili0818/OptProver ; arXiv:2604.23712
- EvE: https://github.com/scaling-group/eve ; arXiv:2605.09018
- MechMath-v1 (sorrifier): https://github.com/MechMath/MechMath-v1
- MMAT: https://github.com/MechMath/MechMath-agent-team (nl-prover / fl-prover / kb-manager 子目录)
- Archon: https://github.com/frenzymath/Archon ; Archon-Horizon: https://github.com/frenzymath/Archon-Horizon (docs/architecture)
- reap: https://github.com/frenzymath/reap ; jixia: https://github.com/frenzymath/jixia ; FATE: https://github.com/frenzymath/FATE ; LeanSearch: https://github.com/frenzymath/LeanSearch ; REAL-Prover: https://github.com/frenzymath/REAL-Prover ; arXiv:2505.20613 ; LeanSearch arXiv:2403.13310 ; Herald arXiv:2410.10878v2
- LeanExplain: https://github.com/SJTU-AI4Math/LeanExplain ; SNL-Basics: https://github.com/SJTU-AI4Math/SNL-Basics ; MathWeaver: https://github.com/SJTU-AI4Math/MathWeaver ; Fulcrum-Template: https://github.com/SJTU-AI4Math/Fulcrum-Template
- FormalRx: https://github.com/LARK-AI-Lab/formalrx ; arXiv:2607.04655 (OpenAlex 摘要)
- AIM: https://github.com/TheoryFoundry/AIM ; Numina: https://github.com/project-numina/numina-lean-agent , https://github.com/project-numina/kimina-prover-rl
- QED: https://github.com/proofQED/QED ; arXiv:2605.20623
- ComplexVariables (沈颖祺/Kenneth Shum): https://github.com/fubinyan/ComplexVariables ; arXiv:2606.20358
- 徐启源 (南洋理工): https://github.com/xqyww123 (Isa-Mini, Isa-REPL, MLML, NTP4VC, phi-system)
- 未开源 (如实): Paper2Formalization (梁经纬, 无公开仓库), Fyan (邹扬硕, 未开源), 居浩成与陈小杨演讲无对应公开仓库
