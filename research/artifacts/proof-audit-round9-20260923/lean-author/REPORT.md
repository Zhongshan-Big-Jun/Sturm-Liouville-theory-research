# 第九轮 Lean 作者交付

作者原生 session_meta.id / 当前 task ID: `01a0cbe7-a5ba-7be1-9170-4484e929436b`. 继承环境 CODEX_SESSION_ID 为 `01a06f46-dd03-7c83-9267-32048412c359`; 它与父会话一致, 不是本作者独立 task 的 ID. 原生证据见 identity.json.

## 当前结果

候选 `project/AuditRound9.lean` 的 `AuditRound9.local_root` 实际编译及原插件精确检查通过: machine_verification_passed=true, exact_root_passed=true, root_closure=closed. 15 项合取包含欧氏投影的零法向量分支与幂等性, 线性归一化核修正与核方程保持, 真实 2x2 归一化矩阵的 J 共轭及任意 n 乘积 (0,1) 反射不变, 状态相似变换乘积桥接, omega=y/(s*t) 对应物理 F 的 y/(pi-y) 因子与内部零点反射.

源码有 25 个具名定理和 13 个定义/缩写. 实际导出含 59 个声明, 包括 Lean 自动生成的等式和辅助声明. 未选择可选的宽度加权投影.

运行时: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`. 原仓库 pin 为 leanprover/lean4:v4.31.0; Mathlib 当前 HEAD 和 manifest rev 均为 `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`. 只导入 5 个具体模块, 没有 import Mathlib, 没有全 lake build 或下载缓存. 外部包只读; 每个精确检查都在自身 evidence 输出目录新编译目标, premise 对照还新编译本地依赖 AuditRound9.

根的实际传递公理为 `propext, Classical.choice, Quot.sound`. unexpected/unknown/unsafe dependencies 均为空. 传递依赖 16629 个声明, 完整加载环境 4162 个模块, 绑定 12480 个外部 olean/server/private 工件. 完整类型, 依赖 AST/边, 定义, 公理, 工件身份, 命令与 stdout/stderr 在原插件 manifest 及其不可变 per-run 目录内. 插件的 expected_statement 合成公理仅用于类型比较, 不属于候选或根闭包.

## 原插件实跑

| case | run_id | machine | exact root | expected result |
| --- | --- | --- | --- | --- |
| positive-02 | 53ffa853f2384b1abdef141a33bb058e | True | True | closed |
| negative-wrong-type-01 | 0e13a66d31274fb5bbbee3505aa314a0 | True | False | target_mismatch |
| negative-missing-01 | 9de1d709c8a74da08c412b6d2d85021f | False | False | incomplete |
| negative-premise-02 | b1fee0d282294a4fbd39e61fc9a7c6e8 | True | False | target_mismatch |

错误类型对照把归一化目标的 -a/2 改成 +a/2; 原始证明编译完成, 精确比较拒收. 缺目标对照实际报 `Exact root declaration not found: AuditRound9.missing_root`. 未证前提对照的真实类型以 `∀ (H : Prop) (_pending : H), ...` 开头; 虽然命题后的合取由已证根提供, 额外前提仍使它不能匹配无该前提的合同. 三者均不是靠异常退出泛称成功, finalize.py 分别检查了具体拒收原因. 候选和控制源码无 sorry、新 axiom 或 True 占位目标.

开发第一次编译因矩阵条目化简和归纳重写失败; development-02 已编译成功. 清理提示时产生“无剩余目标”的战术错误, positive-01 因而失败; 已保留完整失败原文、输入快照与回执, 随后修正并重新跑 positive-02. 未证前提对照 negative-premise-01 在最终回执之前外层返回 143, 记录的 Python PID 消失, 原因未确认; 未伪造其退出码或闭合结果. 已保留原提取和 interruption.json, 另用原工作流 research_state.py 的 detached local job 完成 negative-premise-02. 本地任务因预期的 strict-exit=1 记为 FAILED, 具体类型拒收才是该负对照的成功标准. 不将先前轮次结果当成本轮证据.

## 交付入口

- `project/AuditRound9.lean`: 唯一候选源.
- `positive-contract.json`: 全部精确 expected type; `HUMAN-CONTRACT.md`: 数学定义、假设、应用边界和逐项合同.
- `evidence/positive-02/run-manifest.json`: 当前作者机器通过回执; 下属 lean-verification-runs 保存不可变报告、提取和完整日志.
- `controls/` 与 `project/ConditionalRound9.lean`: 三类负对照的精确输入.
- `formal-only/packet.json`: 给新盲读 agent 的单独输入清单. 同目录只有形式源码、机器导出的声明/定义、完整 explicit 类型、依赖闭包、环境与哈希. 不含本报告、人类合同或意图注释. 含 generated 声明的全量文件为 declarations-all.json, 对外声明清单为 declarations.json.
- `commands/*/command.json` 与 stdout/stderr: 真实 argv、显式 cwd、环境、PID、退出码、时间、源码快照及哈希. `author-result.json`: 简洁机器交付.
- `identity.json`, `candidate-freeze.json`, `readonly-{baseline,postcheck}.json`, `handoff-manifest.json`: 身份、冻结及边界证据.

如需全新重放, 在本目录显式设置 workdir 后运行 `python3 -B launch_replay.py fresh-prefix`; 前缀必须未使用. 启动器用原工作流 research_state.py 持久化本地任务, 状态和完整监督日志在 .research-state/jobs. 任务依次调用当前未修改插件进行一正三负检查, 将日志和结果写在本目录的新 evidence/commands 子目录. 它使用现有固定依赖, 不触发 lake build. 不重复使用已有目录覆盖旧证据.

## 必须保留的范围

作者自检已完成, 插件 semantic.status=not_reviewed. 本作者未执行或声称独立 blind readback/最终语义审查; 协调器需分别安排新会话. 归一化修正是线性代数接口, 不等于无限维谱展开证明. 积分法向量的解析识别、约化逆构造、谱级数收敛、本征函数可微性、完整二阶变分/Green 核结论、ODE 转移矩阵来源、2n 根计数与单根输运、平衡候选极限和全局极值均未在本文件形式化. 实际矩阵形式及从归一化矩阵到物理函数的代数桥接则已经证明.

全部作者写入位于本目录. 原仓库 Lean 源、已有本地 Lean 工件和插件脚本按已记录基线复核不变; 这不声称协调器在其它文稿中的并行工作没有变化. 无仓库/plugin/global config 修改, 无 commit/push.
