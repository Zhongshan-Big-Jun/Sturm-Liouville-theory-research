# 第六轮 Lean 独立执行核验

判定: **PASS**. 25/25 项执行及结构一致性检查通过. 本报告不构成最终语义批准.

原生会话: `01a0c2fb-374c-7671-bdfb-cbacb59b1d9d`. 身份直接读取本会话环境变量 `CODEX_THREAD_ID`; 不伪造 fork 元数据. 本人不是作者, 未读取或采用作者 REPORT/RESULTS、其他审稿会话或研究工具库的结论.

## 实际运行及检查

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B /mnt/f/tools/math-audit-round6-20260921/lean-author/replay.py /mnt/f/tools/math-audit-round6-20260921/independent-execution/replay --skip-negative-control
```

上述命令只执行一次, 输出目录原先不存在. 退出码 0, 耗时 867.90 秒. 原始命令、PID、stdout、stderr、退出码和流哈希保存在 `replay-command.json`、`replay.stdout.txt`、`replay.stderr.txt`. 其内五个阶段与维护版 verifier 的各编译子命令均保留原始回执.

| 检查 | 结果与证据 |
| --- | --- |
| 冻结输入和源身份 | 执行前后各 33 项身份检查; freeze 自身哈希及 snapshot 文件集合保持一致. 见 preflight.json、postflight.json. |
| 实际运行时 | Windows PE Lean 4.31.0, x86_64-w64-windows-gnu, 从 WSL 调用. 运行时与维护版工具均按冻结哈希核对. |
| 新对象构建 | AuditRound5、AuditRound6 均从与原项目一致的冻结源实际编译, 只生成在本次独立新目录. 见 local-build-checks.json. |
| 精确根及类型 | SL.AuditRound6.local_algebra_root; Lean 实际 isDefEq、宇宙参数、绑定参数检查均匹配. 正确期望类型的独立 example 编译通过. |
| 导入身份 | 4587 个已加载模块, 13753 个导入工件文件. 实际路径和哈希受回执绑定; 当前全部模块解析再核对通过. 旧项目 SL 对象未被采用. |
| 根和公共闭包 | 根 20642 节点; 共享公共图 20644 节点. 独立重算闭包及公理集合, 无 sorryAx、额外 axiom、unsafe 或缺失节点. |
| 全部显式公共导出 | 36 项, 包括 21 个定理和 15 个定义. 每项核对类型 AST、类型/证明依赖边、宇宙参数、绑定参数以及重算的传递公理. 编译器生成的辅助声明随闭包检查. 见 public-declaration-checks.json. |
| 可达本地定义 | 逐项核对类型和定义体 AST 的依赖边, 在根提取提供对应 AST 时交叉比对. 见 local-definition-checks.json 的逐项比较范围. |
| 回执一致性 | 只消费本会话新生成的回执, 核对原始日志、源、工具、运行时、工件及实时 import resolution. 无第二次证明重放. 见 receipt.stdout.txt. |

逐项机器判定和具体证据见 [CHECKS.json](CHECKS.json). 根及全部公共声明的传递公理均不超出 `propext`, `Classical.choice`, `Quot.sound`. 检查器为比较期望类型而生成的 `LeanVerifyV2.expected_statement` 合成声明不在根或期望类型的证明依赖闭包内; 正对照直接使用实际根证明项.

## 身份绑定

- freeze.json SHA-256: `fec3e38c904e0052e5bdd1da9cbc6080beb697cea480dd9c84590e5d2cd0117d`.
- AuditRound5.lean SHA-256: `035043c154c215e995a210b798f80cf131414eee5529ad54396a5af3d669ae45`.
- AuditRound6.lean SHA-256: `f765205b55ee454261a1a365e157ffa4f4f0202662c450b8a9c92328820a7c3e`.
- 实际新 AuditRound6.olean SHA-256: `25a6b7cbec3320accd6e9215ccdf7f0e338e1056e971a65de18a132ef84f91be`.
- 维护版 verifier run_id: `9f81447f8d0a4fb8bbfb0bcf4da92a5b`.

## 明确边界

- **错误期望类型负对照未独立运行**, 状态为 NOT_RUN_BY_REQUEST; wrong-expected-contract.json 仅作为冻结输入核对. 作者的负对照证据须由另行语义审查核实, 本报告不作其通过或失败结论.
- replay/REPLAY_RESULT.json 的 `role=author_execution_not_independent_review` 和 `independent_review=not_performed` 是冻结通用脚本的原文字段, 保持不变. 本目录的实际执行来自上列真实原生会话; 本人另写的 CHECKS.json、native-session.json 和本报告说明独立执行核验身份.
- 本次检查精确的局部实代数 Lean 目标. 没有批准解析 Sobolev、分数幂、谱阈值、拓扑密度或完整解析证明已经 Lean 化, 也未作最终陈述保真审查.
- 依赖库使用已有固定运行时和包对象; 未全量重建 Mathlib, 未运行全 Lake 工程或旧项目工具, 未使用第二个独立内核. 编译器与被哈希绑定的依赖工件是本轮执行的信任边界.
- 不修改作者包、项目源、插件、canonical 或 Git. Python 文件运行均使用 -B 和 PYTHONDONTWRITEBYTECODE=1. 本目录及 snapshot 内无新增 Python 字节码缓存.

## 全部新增文件

输出父目录原先不存在, 本次全部文件均为此目录下新增. 完整逐文件相对路径、大小和 SHA-256 见 [FILES.json](FILES.json), 包括嵌套 replay 的源、对象、JSON 和原始日志. 清单自身列为索引文件并明确排除自哈希, 不作循环哈希声明.
