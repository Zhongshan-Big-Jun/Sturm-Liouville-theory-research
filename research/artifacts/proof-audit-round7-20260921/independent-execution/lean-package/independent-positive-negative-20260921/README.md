# 独立执行摘要：INCOMPLETE

完整新运行目录：`/mnt/f/tools/math-audit-round7-20260921/independent-execution/lean-package/independent-positive-negative-20260921`

本报告记录隔离执行及证据核对，不给出最终数学语义 review verdict。

## 两个实际阻断

1. 原 Lean replay 返回 **1**。第 2 步 exact target 与第 3 步直接正对照成功；第 4 步生成的 `replay/Inspection.lean:75:8` 使用 `let Type`，编译器报 `unsupported pattern in syntax match`。原 replay 只执行了 4/7 步，其 `public-declarations.json` 未生成，后续负对照未由原 replay 执行。
2. 原数值 runner 返回 **1**。`numerical/inputs/manifest.json` 缺失，且不在 PACKET 数值输入清单中。normal 与补跑的 `-O` 都是 **24 PASS + 1 FAIL / 25 组**；汇总构造又因同一缺失输入失败，未产生原定结果 JSON。没有补造 manifest 或替换输入。

## 实际完成的补充核查

| 项目 | 本次实际结果 |
|---|---|
| 冻结身份 | 27 项 SHA256 前后匹配；PACKET 本身也未变 |
| 候选源码重新编译 | 2 次，有独立进程与新产物生成观察 |
| 正 exact target | `local_algebra_root`，`closed`，expected_type matched；直接正对照通过 |
| 实际 import | 独立 Lean import/findOLean 与补跑 `--deps` 都指向本次新 `.olean` |
| 全量声明导出 | 27 个源声明＝20 定理＋7 定义；环境共 32 项（额外 5 个自动生成项）；类型、传递公理及 7 个定义体实际导出 |
| 传递公理 | 仅 `propext`、`Classical.choice`、`Quot.sound` |
| 错误 target | 补跑原 wrong-target contract：verifier 返回 1，`target_mismatch`；原生 Lean 也报告实际结论 `W₂(1/2)=−4π` 与要求 `W₂(1/2)=−6π` 的类型不匹配 |
| 错误镜像因子 | 原 `WrongMirrorFactor.lean` 返回 1；Type mismatch 明确为系数 2 对系数 1 |
| 数值 normal / -O | 各 24/25；额外观察运行在原异常抛出后读取 traceback 中 Results，24 组已完成详情完全一致，两个观察运行仍返回 1 |
| 旧 FH 公式负对照 | 两种模式均返回 1；原因均为公式误差约 26.9404860801203，而非缺文件或导入失败 |
| 依赖身份 | 预哈希 32891 个现有 runtime 产物；实际载入的 13089 个外部产物完成运行后 SHA256 复核 |

独立导出与补跑结果没有覆盖或消除原 runner 的失败。其用途是保留已实际观察到的执行事实。没有用 `author_machine_checks_passed` 标签作为独立性证明；原 runner 实际上未执行到该状态。

## 执行数量与检索

- Lean/Lake 可执行进程共 **24** 个（含版本/依赖查询），候选源码编译 2 次，验证器检查模块编译 2 次。
- `checks.py` 共执行 **6 次**：原 runner normal 1 次，直接 `-O` 1 次，旧 FH 负对照 2 次，保留异常的结果观察 2 次。
- 直接 normal/-O 合计 50 组调用：48 通过、2 失败；观察运行另有相同 50 组调用。负对照走独立分支，不计入 25 组。
- 独立证据一致性核查：**109/109**。该计数表示预期成功/失败与证据相符，不表示原任务整体通过。
- 可检索关键词：`LEAN_RUNNER_INSPECTION_SYNTAX`、`NUMERICAL_MISSING_MANIFEST`、`target_mismatch`、`all-module-declarations`、`old-fh`。

关键数值（有限计算观察）：Wronskian 样例为 `-4*pi`、旧式 `-6*pi`；正确镜像 FH 值约 `53.88097216024057`、旧式约 `26.94048608012029`；n=2 归一化行列式为 `7030400000*pi^4/4782969`。详情与范围标签见数值证据，不将其提升为无限维证明。

## 信任边界

依赖现有 Lean 4.31.0 编译器/内核、mathlib 编译产物、Python/SymPy/mpmath 及 OS/WSL/硬件；未使用第二内核，未全面重编译 mathlib。运行后逐字节复核覆盖实际载入的外部 Lean 产物；其余预哈希产物仅核对最终元数据。不是整个系统的文件写入审计。

exact target 仅指包中 expected_type 在记录环境中匹配。FH 单界面公式仍是显式标量前提，不代表谱可微性或一般 FH 定理已形式化。Volterra 无限维估计、统一 Taylor 余项、min-max 与一般谱极限未获本次 Lean 认证。数值结果含符号运算和有限高精度运算，不是区间证明。

没有读取旧作者输出/README、项目 AGENTS、记忆、其它任务历史或解析新稿。列明的外部审计报告仅做字节哈希。所有主动写入均位于 `independent-execution`；输入脚本、原项目和外部 runtime 未修改，未 commit。最终语义审查留待独立 reviewer。

独立汇总曾有一次未完成尝试：重复解析已给出的绝对路径造成大量挂载文件系统元数据访问，执行者以 SIGTERM 停止自己的该进程（退出码 -15），保留原程序、原收据及当时输入核对记录；随后只将该路径处理改为清单绝对路径的直接匹配，重新执行完整且相同的字节哈希及证据检查。详见 `audit-retry-reason.json` 和 `executor-logs/independent-evidence-audit*.json`，没有改动输入程序或 Lean/数值结果。

## SHA256 指针

小型机器报告：`independent-execution.json` — SHA256 `1d3bb0bca349fa954f2e841e5577922fe4693c2b9c59b1962bf6f5f79583d0be`。

全部本次程序、日志、原始 manifest、声明和运行前后清单均列于 `evidence-index.json` 与 `SHA256SUMS`；索引中的每条记录含路径、完整 SHA256、字节数。外部程序和输入的完整 SHA256 在 `preflight.json`，载入依赖在 runtime 清单，Python 观察模块在 `python-loaded-files-*.json`。大型清单保持原始字节，未改写或截短。

- `evidence-index.json` — SHA256 `d25b019d9751fdccc88a38a220aac05df50048ef9b137fd1f1b158755d891ab8`
- `preflight.json` — SHA256 `7856c1f5d9590176403a842aeddd020a654f68f2cc6241254a29cd5c644c35a8`
- `runner-review.json` — SHA256 `7cf9e39d4ada63a061a55a5249beb00ade023a051f6f5b2b7ca7aa78f0d2eae0`
- `runtime-before.json` — SHA256 `566bb7a5f2939c3e1829270ea9d0fc6b79157855e2ae6a4c1ef1cee21fc1502c`
- `runtime-after-imports.json` — SHA256 `219aed51e52ff6897cb1037d8c0cd91aab5660b74282b1a9b4b720d61e5b63bf`
- `final-input-identity.json` — SHA256 `100748494927e971404586d8878e23c034329617c304d9aa929e38c3a652bf68`
- `executor-logs/lean-replay.json` — SHA256 `f70d9161448cb0cfb2db2b74ed4940775f79924bbf8c525959f17c195eadb8fc`
- `replay/Inspection.lean` — SHA256 `22577b45942dc986e8a3b19abed5473c1eacdfca5aba5139e542b1489c5113f7`
- `replay/positive/run-manifest.json` — SHA256 `a74f8c85a0c623301f1e31c28a0555ceea81295a6acf48dc9e74baaff6ac0409`
- `supplemental-negative/run-manifest.json` — SHA256 `11d405fede70c31acbd62699dc545986424a9ceb169238e0b687618a3ce96773`
- `all-module-declarations.json` — SHA256 `d801b93963c2d100fe4008fcd646b8ebb74f8191b28cb62b723c47b4de35305a`
- `independent-root-artifact.json` — SHA256 `9f13680056ddfbf842868a49a61d566765d3bf6a3b773d3a78985670de0e870d`
- `numerical-crosscheck.json` — SHA256 `5b652d83fc263c390c07495341daafd0df92a1492bb09da8f8eb3f2519109721`
- `command-inventory.json` — SHA256 `b7580970f447d3348bfe1453ef5dc5c3d67ff91a7a901b6b11e86a7cf2e7a6c6`
- `independent-checks.json` — SHA256 `6d8febdfc85b31db3140948bce4acbfec63dcb7257eefc1d4287efb26ca9a4be`

执行者新增程序（输入程序另见 preflight）：

- `assemble_report.py` — SHA256 `64e84849500976e88df1cede2b817d83eb7074446f1956985119734dd8732381`
- `audit_results.py` — SHA256 `1cf719c344cf1d02319246b8efe2e6654a31fe1592f5658b2e569ab6988047ee`
- `audit_results_fast.py` — SHA256 `8d1bb96f275c6e572e1631e24f7d2255dec29b323efaef1e3fdb3e8b30180aea`
- `check_import_resolution.py` — SHA256 `49f18aead20692a5729b25b3c6f158b09b408239f9b4b8d740551bdb54d70f45`
- `executor.py` — SHA256 `bf07e2cc10eee130c979b5d073fc97cced9e8fa878e3bcf5f7629b481541bbd4`
- `observe_numerical.py` — SHA256 `aeda607d59494aa46343bd1186af60b317100d4b4dcab8ca624f8a2f8e0b2a65`
- `observe_replay.py` — SHA256 `1328ac897b0c1701c9f42bfd6bf08035a0d92a05296294f9a47f92b34438ec16`
- `preserve_inputs.py` — SHA256 `8e229d6f50e73f95e0c48c0ef5c0e1830d2f0f8f07bfabc30c31e1f560ea47fb`
- `probe_environment.py` — SHA256 `9c8e381cbb3d4f472ac8c5741d64a10ad9cc2c7f0dd10e2410a3f55973d0961d`
- `seal_delivery.py` — SHA256 `f3f43ad559f73356abd065779f0f826bffccc6dd3e74c63c6370d122079b879e`
- `supplemental_controls.py` — SHA256 `113b2d79fe928c10216142108cf9ae69c399e0395b16277727192afceb590424`
