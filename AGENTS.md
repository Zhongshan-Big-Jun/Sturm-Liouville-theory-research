# AGENTS.md

## 项目目标
- 寻找, 阅读论文, 研究前沿数学问题 (当前主题: Sturm-Liouville 边值问题).
- 研究数学问题时调用 `rigorous-open-math-research` skill.
- 查找论文时多用 Google, 寻找最前沿结果, 总结证明技术.
- 用户会提供论文链接, 生成 tex 文件解析论文, 并以此为基准寻找相关结果.

## 当前关注问题
1. 多大的空间中 SL 边值问题的解能等价于该空间内的所有正交函数系 (基准论文: Springer 章节 10.1007/978-3-031-90135-5_7).
2. 优化 SL 边值问题相邻特征值间距的界 (联网检索先进结果).

## 工作方法
1. 进入项目先读 AGENTS.md; 若不存在则创建并开始维护.
2. 每次变更后更新 AGENTS.md, 简述工作内容.
3. 研究数学问题严格按 rigorous-open-math-research skill: 精确定义问题, 多路线探索, 对抗性审查, 边界情形检查, 结论可验证.
4. 生成 obsidian 仓库中的 md 文件时调用 obsidian 相关 skill.
5. 任何问题如实回答, 不允许编造答案或想象问题.
6. 只允许使用英文标点符号; 代码使用 tab 缩进.
7. 从论文学到新方法或在研究中发现新工具时, 实时更新 `tools/` 工具库: 新建 `tools/<slug>.md` (含解析与适用范围), 更新 `tools/README.md` 索引, 并在本文件会话记录中登记.
8. **数值检验不得作为结果呈现.** 整理文档 (docs/*.tex, tools/*.md, run 工件) 时, 必须把数值部分与严格证明部分区分开来并显式标注: 严格证明用 ``严格证明``/``定理已证``/``STRICT`` 标签; 数值证据用 ``数值证据``/``数值验证 (精度)``/``EVIDENCE`` 标签且注明不构成证明; 猜想/开放必须标 ``猜想``/``开放``. 未完成严格证明的断言不得称为``已解决``.

## 注意事项 (Notes for future agents)

- **本文件保持精简**: 完整历史会话日志在 `state/AGENTS_SESSION_LOG.md`; 需要归档时用
  `scripts/split_agents_log.py --agents AGENTS.md --archive state/AGENTS_SESSION_LOG.md`.
- **runs/misc 归档**: 使用 `scripts/archive_old_runs.py` (默认 dry-run, `--apply` 才执行);
  策略说明见 `docs/archive-policy.md`.
- **未跟踪临时脚本**: `scripts/_tmp_p1_bounded.py`、`scripts/_tmp_p1_bounded2.py` 等
  `_tmp_*` 文件是临时探索产物, 不属于正式工件; 提交前清理或加入 `.gitignore`, 不要纳入
  正式研究提交.
- **远程推送顺序**: `project.json` 配置 `git_sync.push_order = ["origin", "fork"]`;
  先 push `Zhongshan-Big-Jun/Sturm-Liouville-theory-research`, 再 push
  `xsoc1/Sturm-Liouville-theory-research`.
- **插件仓库注意事项**: 见 `_xsoc1_work/AGENTS.md` (Codex 父仓库) 与
  `C:\Users\HuangZY\.dsh\math-research-dsh\AGENTS.md` (DSH 适配仓库) 的
  "Notes for future agents" 小节.
- **GitHub 网络**: 直连 github.com 失败时, 用本地代理 push:
  `git -c http.proxy=http://127.0.0.1:7897 push origin main` (本机实测可用).
- **外部仓库克隆位置**: 临时调研用的外部仓库统一克隆到 `F:\tools\` 下
  (例如 `F:\tools\rethlas-clone\`), 不要放到 C 盘用户目录; 用完可删除.

## 会话记录

- 完整历史会话日志: `state/AGENTS_SESSION_LOG.md` (由 `scripts/split_agents_log.py` 维护, 本文件只保留指针与近期摘要).
- 每次变更后在本节追加一行近期摘要; 长日志一律写入归档文件.
- 2026-08-16 会话 108: 清查未跟踪文件并交接 (session log 归档, G1' EVIDENCE 脚本, 社区蒸馏缓存, 维护脚本); 同步状态; 尝试闭合 P1/M3 或 DensBC O1.
- 2026-08-16 会话 109 (R-20260816T000000Z-densbc-o1): DensBC O1 求解 run. 新 STRICT 结构定理 (投影稠密性 P_V(Pi)=V, 障碍矩系统, 游程/首个障碍, 对角归约 Theorem E, 有限秩分类); 诚实化约核 O1' (矩可实现/成员步). 独立对抗审计 (fresh subagent) REPAIRABLE_GAP 并已修复. 未 commit/push.
- 2026-08-16 会话 110 (R-20260816T174722Z-min-direction-audit): 审计合作者 min_direction_progress.tex; 独立对抗审计 + 符号/数值验证; 补充核验包 collaborator_min_direction_verification/ 后重放 Bernstein 证书/charge_compensation/det_forest 全部 PASS, 结论升级为 ACCEPT. 已加入 docs/SL_gap_nge2_min_direction_progress.tex/.pdf, README 索引, 审计 run + 核验包入库.
- 2026-08-22: 插件性能实验完成 (A6 root-1 高阶有理积分解排除, Q-20260822-a6-perf-A1B2C3D4). baseline (97ba72f7) 与 reuse-gate (c13dd1f0) 均得 root-1 no-go RIGOROUS_PARTIAL_RESULT; reuse-gate 多耗约 2x input/cache、46% tool calls, 未显著改善数学产出, 但更显式可审计. 独立审计 (b1df4d9e) REPAIRABLE_GAP 2 处已修复; 可用结果已登记 (research_map/tools/Lean scaffold/状态/性能报告 reports/plugin-performance-a6-ab.md).
- 2026-08-22: 第二轮插件性能实验完成 (B3 fixed-n 上确界, 更难更大). baseline (b9543550) 与 reuse-gate (c93ffd79) 均独立得出 2 项 STRICT 结果: 固定 n 比值全局极大子 = bang-bang [1,R,1,...,1] 且恰 2n 开关; 交替平衡世俗多项式 F_n 在 (0,pi) 恰 2n 个简单根 (关闭 O3). reuse-gate 本回合更省 cache/步骤 (但产物文档较少), 另发现非平衡自洽解; O1/O2 仍开放. 独立审计 (cb3b9695) REPAIRABLE_GAP 3 处已修复; 性能报告 reports/plugin-performance-b3-ab.md, scaffold/tools/research_map 已登记.
- 2026-08-22: B3 baseline run R-20260822T220000Z-b3-baseline: 新 STRICT 结果 2 项 — (i) 固定 n 比值全局极大子均为 bang-bang [1,R,1,...,1] 且恰 2n 开关 (比值能量不变量 E=0, q0=1/c, q1=-1/c); (ii) 交替平衡世俗多项式 F_n(y) 在 (0,pi) 恰 2n 个简单根 (转移矩阵递推 + Chebyshev/Jacobi 谱论证). O1 全局极值闭式/O2 交替族单调仍开放. Artifacts 在 run root.
- 2026-08-23: 第三轮插件性能实验完成 (DensBC O1' 一般非对角 H). baseline (40a27890) 与 light-reuse (5fda63a6) 各得互补 STRICT 子类结果: 稳定带 Toeplitz H_shift(m,lambda) 有限秩判据 (baseline) 和加权移位 H_{beta,lambda} 判据 (light-reuse, beta>3/2 门槛). 轻量 reuse 协议比 baseline 少 41% 步骤/53% 工具调用/59% cache, 且维持最低产物集 (94K 未缓存 vs 127K); 独立审计 (b086bc37) baseline 无缺口、light-reuse REPAIRABLE_GAP 已修复; 性能报告 reports/plugin-performance-o1p-ab.md, 两个 scaffold/tools/research_map 已登记.
- 2026-08-23: 第三轮插件性能实验 baseline run R-20260823T000000Z-o1p-baseline 完成: 新 STRICT 有限秩判据 (稳定移位带 Toeplitz 空间 H_shift(m,lambda), 带宽 m>=1, 有限多项式 representer): dense <=> ker(T|B_fin)={0}; 带宽 2 v_1=x^4 非稠密例; 一般 O1' 仍开放. 工具/状态未提交, 工件在 run root.
- 2026-08-23: 启动左定空间稠密性一般判据 O1'LD 研究 (Q-20260823-leftdef-o1pld-D4E5F6A7, run R-20260823T030000Z-leftdef-o1pld). solver c3cdb7b0, 使用 v1.5.0 轻量 reuse 协议, 等待结果后审计并登记.
- 2026-08-23: O1'LD run R-20260823T030000Z-leftdef-o1pld 完成: 新 STRICT 结构定理 (L^2 有限支撑矩刚性 via Müntz-Szász L^p, 无限游程不可实现, cofinite-N 稠密 => H^2 真子空间保留集非余有限, 奇偶分解) + 具体 W=ker μ_4 非稠密例; 一般 O1'LD 仍开放. Artifacts 在 run root; 工具 [[leftdef-o1pld-l2-structural]]/research_map 已登记.
- 2026-08-23: O1'LD run 独立审计 (R-20260823T040000Z-leftdef-o1pld-audit) 判定 REPAIRABLE_GAP; 已修复: Lemma 1 改为 Lebesgue L^2 加权代入, 移除 DensBC O1 两项游程代数, 尾部刚性/cofinite-N 降级 NOT-YET-STRICT, μ_4 奇侧用 SL_h2 奇增长引理, H^1 无限游程降级 EVIDENCE; run/工具/报告已同步.
- 2026-08-23: O1'LD re-audit R-20260823T050000Z (PASS): 修复后的 STRICT 断言 (有限支撑矩刚性/Cauchy-Schwarz/奇偶分解/μ_4 非稠密) 可入库; cofinite-N/H^1 无限游程按 NOT-YET-STRICT/EVIDENCE 登记; 陈旧 MET/SUCCEEDED 标签已清理.
- 2026-08-23: 根据用户 11 页手写 SL 笔记在 F:\LaTeX\SL_Spectral_Theory_Lecture 创建 LaTeX 讲义 (SL_Spectral_Theory_Lecture.tex + Handwritten_Notes_LaTeX.tex + images/), 笔记整理含 Euler-Bernoulli 梁推导、Liouville 标准形、Prüfer 变换、Sturm 比较、正交性与广义 Fourier 级数.
- 2026-08-23: 安装 LaTeX 工具链并接入 VSCode: WSL TinyTeX (~/.local/bin/xelatex, texlive 2026, 已装 ctex/xecjk) + Windows MiKTeX (user PATH 已加入); LaTeX Workshop 扩展已装 Windows 与 WSL Remote; 在 F:\LaTeX\SL_Spectral_Theory_Lecture 创建 .vscode/settings.json (xelatex/latexmk-xelatex) 并成功编译两份 PDF.
- 2026-08-23: 将 SL 谱理论 LaTeX 讲义转为 Obsidian Markdown 并同步: 安装 kepano/obsidian-skills 到 DSH 技能目录 C:\Users\HuangZY\.dsh\skills; 新建 SL谱理论/ 目录 (讲义 7 篇 + 手写图片 11 张 + 入门计划移入); 更新 README/AGENTS; 通过 Windows Git + Clash 代理 push 到 xsoc1/math-notes (55d97cb, 清理后 228a460).
- 2026-08-23: 当前插件 v1.5.0 性能 benchmark 启动 (B3 剩余 O1/O2, run R-20260823T060000Z-b3-current). solver 557e3ac0; 将采集指标并与 round2 B3 baseline 比较, 运行 performance_alert.
- 2026-08-23: 当前插件 v1.5.0 性能 benchmark 完成 (B3 O1/O2, 557e3ac0): 新 STRICT 一般交替 Chebyshev 世俗表示 + 振幅相等推论 + 固定 delta 根定位引理; O1/O2 仍开放. 性能指标 vs round2 baseline: steps -16%, tool calls -30%, uncached -37%, cache -48%, wall -22%; performance_alert INFO. 独立审计 REPAIRABLE_GAP 2 处已修复, re-audit PASS; 报告 reports/plugin-performance-b3-o1o2-current.md, 工具与 scaffold 已登记.
- 2026-08-24: 研究插件更新并优化到 v1.6.0. 父插件 commit 88e1c97, DSH commit 0cc9961. 四个 SKILL.md 静态入口总量减少 21.4%, rigorous 入口减少 43.0%. 修复 Markdown fence 协议缺陷, 加入 Codex 轻量上下文路径和静态门禁. 父仓库 81/81, DSH 51/51, 全部 smoke tests 和本地 doctor 通过. 本轮未重跑端到端数学 A/B, 详见 reports/plugin-performance-v1.6-codex-context.md.
- 2026-08-24: 预注册 B3 O3 三臂 calibration benchmark. 冻结 prompt, source/gold commits, A/B/C 配置, 污染声明, 隔离规则, 指标与独立审计口径已写入 runs/plugin-benchmark-20260824-calibration/. 尚未运行任何 arm.
- 2026-08-24: 五臂 B3 O3 校准 benchmark 启动 (our-plugin 7ee9c2af, blank cb6dbbb0, rethlas 78a98af9, danus fe794a81, mmat 1c14031e). 使用 frozen_task 隔离; 采集指标与独立评审后出表格.
- 2026-08-24: 五臂 B3 O3 校准 benchmark 完成并出结果表 (our-plugin/blank/rethlas/danus/mmat). 五臂均给出同一 STRICT 证明 (Chebyshev 约化); 独立中性评审 A/B/C/D PASS, E (MMAT) 一处非致命 leading-coefficient 笔误 REPAIRABLE_GAP 并已修正. 实际运行模型 deepseek-v4-flash-vision-exp (非预注册 gpt-5.6-sol xhigh); 外部三臂为提示词级模拟, 非完整上游系统. 详细表见 runs/plugin-benchmark-20260824-calibration/RESULTS.md 与 independent_review.md.
- 2026-08-24: Codex/QED 三臂复现实验 Arm A 完成. gpt-5.6-sol xhigh + rigorous-open-math-research v1.6.0 + 子 agent 得到 B3 O3 STRICT 证明, Chebyshev 与 Sturm shooting 两条路线; 插件内审与外部匿名审计均 PASS. 正式 wall 1132.770 s, 77 model responses, 71 tool calls, 222773 uncached input, 3672576 cached input, 73731 output; 周额度剩余 43%. 工件在 runs/plugin-benchmark-20260824-calibration/codex-qed-replication/arms/a-plugin/.
- 2026-08-24: Codex/QED 三臂复现实验 Arm B 空白对照完成. 上下文探针确认 AGENTS/skills/plugins/memory/multi-agent 均为 0; 单次 gpt-5.6-sol xhigh 响应独立给出 STRICT Chebyshev 证明, 外部匿名审计 PASS. 正式 wall 253.951 s, 1 model response, 0 tool calls, 9397 uncached input, 0 cache, 10279 output; 周额度剩余 41%. 工件在 runs/plugin-benchmark-20260824-calibration/codex-qed-replication/arms/b-blank/.
- 2026-08-24: OOD 未污染 benchmark 完成 (指数混合/有界剪切问题, QED problem 3 复现). F 盘部署三个真实系统: Rethlas (verification service + Codex/DeepSeek), Danus codex branch (workers+verify fact graph), MMAT NL-Prover (Codex/DeepSeek). 结果: A 本插件 PASS 自含证明; B 空白 PARTIAL_NOT_COMPLETE; C Rethlas blueprint PASS 但 verify 500 且用了 MCP 网络; D Danus 完整 fact graph 证明 No (3 verified facts), 独立审查把单一 theorem fact 给 REPAIRABLE_GAP 但 fact graph 含全部引理; E MMAT 未产出最终工件 (read-only 误启动/重连). 详细见 runs/plugin-benchmark-20260824-ood-mixing/RESULTS.md.
- 2026-08-24: 完成 B3 O3 实际 Codex/QED 三组校准. A 插件, B 空白 Codex, C 固定 QED 均获匿名审计 PASS, 数学证明全部保留. B 在单题上最省资源; C 走 Easy 短路, 未运行 QED 分解与验证链; A 产出多路线, 内审与最大研究包. 结果与协议限制见 runs/plugin-benchmark-20260824-calibration/codex-qed-replication/RESULTS.md.
- 2026-08-25: 按要求把 DeepSeek 适配版单独拆出并标注，原配置恢复保留. 适配拷贝: F:\tools\rethlas-deepseek, danus-deepseek, mmat-deepseek (每个有 DEEPSEEK-ADAPT.md, 总览 F:\tools\DEEPSEEK-ADAPT-README.md). Rethlas verify 服务修复(HTTP 500 -> correct), MMAT writable/thread 稳定化. 用 QED problem 4 Batchelor-scale liminf 做足够难新测试: 31分钟 cap 内 A 本地插件 RIGOROUS_PARTIAL_RESULT (独立性评审 PARTIAL_NOT_COMPLETE), B 空白 REPAIRABLE_GAP (外部定理引用不精确), C/D/E DeepSeek 适配版未出最终证明 (Rethlas iter0, Danus 无 fact, MMAT sketch phase). 结果见 runs/plugin-benchmark-20260824-ood-batchelor/RESULTS.md.
- 2026-08-25: K(1)=e/4 strict-anchor benchmark (2 hour cap) completed. Run R-20260824T184147Z-k1-e4-ab stores the two isolated solver outputs, metrics, source manifest, blind audit, and handoff documents. Added the standalone proof `docs/SL_third_order_K1_proof.tex` and PDF, plus `tools/third-order-minimal-K1.md`. The c=1 even anchor is STRICT; general K(c) and source-term control remain OPEN. The Blueprint deterministic integration helper failed before process creation with `helper_unknown_error`; this workflow caveat is recorded in the run and does not change the independently audited mathematical proof.
- 2026-08-25: 依据用户提供的三臂 pilot 方案制定并启动适配版 (A=本插件, B=空白, C=QED 1219009). 已生成 runs/three-arm-pilot-v2/PLAN.md, blind-main/task.md, BLOCKER.md; calibration 运行目录与 run-a/b/c.sh 已就绪 (F:\benchmark\PILOT-V2-20260825\calibration). 尝试启动时 GPT-5.6 proxy 172.22.112.1:7898 不可达, 校准未产出结果, 等待 proxy 恢复后重跑.
- 2026-08-25: Execute pilot v3: five arms x 3 new QED tasks (Bessel/exponential mixing/lamplighter) with 30-min cap under DeepSeek. A/T2 and D/T2 independent reviews PASS; B/T2 and C/T2 REPAIRABLE_GAP; T1/T3 mostly incomplete. Results in runs/three-arm-pilot-v2/pilot-v3/RESULTS.md.
- 2026-08-25: Pilot v4 long-run launched. Synced collaborator remote e2d652d; merged and pushed origin+fork to ff11cf9. Chose U1 Batchelor-scale liminf, U2 TV asymptotics, U3 LICT_Z over Z; 15 runs (A/B/C/D/E x U1/U2/U3) with DeepSeek, 2h watchdog in F:\benchmark\PILOT-V4-LONG-20260825. Old v3 T1/T2/T3 lingering processes stopped. Repo skeleton runs/three-arm-pilot-v2/pilot-v4-long/ prepared.
- 2026-08-25: Pilot v4 long-run recovered from API billing outage and completed. GitHub sync fully merged collaborator e2d652d and pushed origin+fork to a6e9961. Results: U3 had PASS from B (86), C (92), D (93); A/U3 REPAIRABLE_GAP (78); U2 C/U2 WRONG_PROBLEM, E/U2 PARTIAL; U1 no completed proof. Details runs/three-arm-pilot-v2/pilot-v4-long/RESULTS.md, INDEPENDENT_REVIEWS.md, RECOVERY.md.
- 2026-08-25: Preregistered pilot v5 real-Codex U2 three-arm benchmark after quota reset. Clarified `(0,2)` as all lamps off with base at 2, fixed A/B/C isolation and scoring, and adopted a 75 percent per-five-hour work cap with 25 percent reserve. Arm A uses gpt-5.6-sol xhigh plus rigorous-open-math-research v1.6.0 and bounded research subagents.
- 2026-08-25: Pilot v5 Arm A first Windows launch classified INFRA_INVALID and excluded because the managed profile became read-only, preventing v1.6.0 phase reads and artifact writes. Stopped at primary quota 32 percent. WSL replacement passed explicit workspace read/write and proxy preflights; details in pilot-v5-codex-u2/INFRASTRUCTURE_LOG.md.
- 2026-08-25: Pilot v5 WSL replacement hit the preregistered five-hour stop during full v1.6.0 protocol loading (primary 32 -> 46 percent, secondary 5 -> 7 percent) before mathematics began. Marked PAUSED_QUOTA and excluded from scored Arm A. Next run starts from a fresh directory after the 300-minute reset.
- 2026-08-27: 用户确认五小时额度恢复并要求继续, 后报告周额度剩余 18%. 完成 v1.7 closure-first 匹配回归首段: 1311.844 s 后触发五小时硬限制, 3 个子 agent 中 Route A/C 返回, Route B 未落盘; 指标为 56 responses, 44 tools, 211820 uncached, 101940 output, USD 3.5672448 proxy. 独立中性审计对保留部分定理 `PASS`; 新 STRICT 可见包络 TV 等式, 端点下界, 两个显式对数上界, Route A 耦合障碍与 Route C 精确公式/反例已归档并更新 `tools/lamplighter-range-translation-tv.md`. 原 `C/sqrt(t)` 上界仍 OPEN. 结果在 `runs/three-arm-pilot-v2/pilot-v5-codex-u2/v17-regression/`; 状态 `PAUSED_QUOTA_WITH_AUDITED_PARTIAL_RESULT`.
- 2026-08-27: 用户报告五小时剩余 57%, 周额度剩余 11%, 要求继续. 已预注册 v1.7 同 session 续跑: 使用原 CLI 0.149.0-alpha.4.3, 剩余 root wall 1727 s, 禁止新子 agent/Route B 重试/新研究波次, 仅合并 Route A/C, 登记 Route B 未返回, 执行 files-only convergence check 并完成诚实 partial package. 预检见 `runs/three-arm-pilot-v2/pilot-v5-codex-u2/v17-regression/CONTINUATION_PREFLIGHT.md`.
- 2026-08-27: Pilot v5 三臂完成并同步 (A plugin PARTIAL_NOT_COMPLETE, B blank FATAL_GAP, C QED PARTIAL_NOT_COMPLETE); 数学合并结果为 `1/(2sqrt(t)) <= TV` 和 `TV <= (2log(t)+15)/sqrt(t)` (`t>=16`), 常数阶上界仍开放. 结果提交 `fe7eb1f`.
- 2026-08-27: 基于 pilot v5 的 307 responses/7 child sessions/1,108,074 uncached input 诊断插件调度冲突, 发布 rigorous/workflow v1.7.0 closure-first 协议. 父插件 `957d80b` 已推 origin+fork; DSH `0a852d1` 已推送; Codex 本地重装 1.7.0. 静态校验 parent 81/81 + 10 smoke, DSH 51/51 + 14 smoke + BUNDLE OK.
- 2026-08-27: 预注册 U2 v1.7 matched regression `R-20260827T063025Z-u2-v17-regression`, 复用字节相同 Arm A prompt, fresh CODEX_HOME, 75 min cap, 不重跑 controls; 目标验证 closure-first 是否在保持审计质量的同时降低 wall/responses/tools/child sessions/tokens/cost.
- 2026-08-26: Pilot v5 scored Arm A ran 2764 active seconds before the service hard limit. Preserved two STRICT partial results: an explicit O(log(t)/sqrt(t)) range-triple upper bound and a matching logarithmic obstruction for reflection-then-synchronization with optimal conditional lamp coupling. Added same-thread WSL resume harness with 2036 seconds remaining under the original 80-minute cap. General O(t^-1/2) upper bound remains OPEN.
- 2026-08-26: Pilot v5 Arm A same-thread continuation completed at 4052 total active seconds. Final status PARTIAL_NOT_COMPLETE with internal fresh audit PASS for the partial theorem: lower 1/(4sqrt(t)), upper (2log(t)+15)/sqrt(t), one-sided 12/sqrt(t), fixed-reflection obstruction, killed-kernel and coarea reductions. Scored metrics and full artifacts copied under pilot-v5-codex-u2/arms/a-plugin; added tools/lamplighter-range-translation-tv.md. External anonymous audit pending; original constant-order upper bound remains OPEN.
- 2026-08-26: User removed the pilot v5 emergency reserve after quota reset. Recorded USAGE_AMENDMENT.md at primary 3 percent and secondary 9 percent; frozen task and arm definitions remain unchanged. WSL Arm A launcher now accepts an explicit fresh work-root argument.
- 2026-08-26: Pilot v5 Arm A post-hoc label-blind external audit returned PASS for the claimed partial theorem and explicitly left O3 open. Review SHA256 0ad06b9eb728a40afa779a68d954dbde21b1b3d93c75b3b62f8192a98bb05bea; review usage excluded from scored Arm A metrics.
- 2026-08-26: Prepared pilot v5 Arm B blank-control WSL harness. It uses a fresh content-only workspace, gpt-5.6-sol xhigh, project_doc_max_bytes=0, and disables agents, memories, skills, plugins, apps, browser, computer use, and network tools. A prompt-input leakage probe is mandatory before the 45-minute run.
- 2026-08-26: Pilot v5 Arm B blank control completed in 1254.674 s with 17 model responses and 16 tool calls. It claimed C=12, but label-blind audit returned FATAL_GAP: the load-bearing one-turn fiber claim is false at t=48,w=8,e=4 with exact signs +,-,+,-. Lower bound c=1/4 and range-kernel reductions are certified; constant-order upper bound remains OPEN. Full raw output, metrics, audit, and exact replay are preserved under arms/b-blank.
- 2026-08-26: Prepared pilot v5 Arm C QED harness at pinned commit 121900964e6572aaf094412d434b5ac2a792a65f. The offline-safe adapter strips search and sandbox bypass flags, disables base Codex skills, memory, plugins, and multi-agent features, and retains QED's own decomposition and verification prompts. Arm C has a 90-minute wall cap and no quota reserve stop.
- 2026-08-26: Pilot v5 Arm C QED run1 was terminated and excluded as INFRA_INVALID. Despite CLI search stripping, sandbox network=false, and a clean prompt probe, code_mode_host exposed nested web__run; the survey made 44 web calls among 46 tools. It consumed 47 model responses, primary 48->68, and produced no proof. Protocol evidence is preserved under c-qed-infra-invalid-run1; replacement adapter now disables code_mode_host and must use a fresh workspace.
- 2026-08-26: Arm C replacement policy: code_mode_host is fail-closed, and the fresh QED workspace pre-seeds only neutral Hard/no-external-literature metadata so the offline benchmark skips incompatible Stage 0 and enters the pinned decomposition/prover/verifier core. This adaptation supplies no proof hint and must be disclosed in scoring.
- 2026-08-27: Pilot v5 Arm C run2 was excluded as INFRA_INVALID because fail-closed Code Mode also prevented all QED roles from reading path-only inputs. It consumed 6 sessions and 242392 input tokens but received no problem contents. Compact evidence is retained under arms/c-qed-infra-invalid-run2.
- 2026-08-27: Pilot v5 scored Arm C completed with QED 1219009 and an offline content-inline adapter. QED structural verification rejected the complete target; fresh blind audit accepted the partial theorem `1/(2sqrt(t)) <= TV <= (5+3log(t))/sqrt(t)` for all `t>=1`. Result is PARTIAL_NOT_COMPLETE. Seven roles used 2198.87 s, 131517 uncached input, and 67782 output; constant-order upper bound remains OPEN.
- 2026-08-27: Pilot v5 three-arm benchmark finalized. A=PARTIAL_NOT_COMPLETE with the broadest audited package, B=FATAL_GAP from a false one-turn fiber lemma, C=PARTIAL_NOT_COMPLETE with the best audited lower constant and lower cost. Combined STRICT project theorem uses Arm C lower `1/(2sqrt(t))` and Arm A upper `(2log(t)+15)/sqrt(t)`. Full comparison is in pilot-v5-codex-u2/RESULTS.md; tools index updated.
- 2026-08-27: v1.7 closure-first matched regression 同 session 收口完成. 两段 root wall 合计 1881.050 s, 72 responses, 58 tools, 3 child sessions, 338812 uncached input, 125692 output, USD 5.183904 proxy. 相对 v1.6 Arm A 的七项预注册效率阈值全部通过. 最终独立审计对 `O1/O1b/O2/O3p/O5` PASS, 原固定 `C/sqrt(t)` 上界仍 OPEN at `O3`. 数学工件, 指标, convergence check, 审计与 hash manifest 已归档至 `runs/three-arm-pilot-v2/pilot-v5-codex-u2/v17-regression/`.
- 2026-08-28: Pilot v6 Hs-domain Arm A 完成并入库. v1.7 插件在 1514.327 s root wall 内闭合三项目标, 得到 STRICT 充要条件 `Q_n^(s) in D(K_c^(s/2)) iff n in {0,1}` for all `c>0`, integer `s>=4`. 证明区分代数多项式逆与真正算子逆, 并修正旧工具和 `SL_hs_orthogonal_systems_proof` tex/pdf 的算子域解释. 内部审计 PASS, 外部匿名盲审 PASS 99/100, 无修复. 工件与指标在 `runs/three-arm-pilot-v2/pilot-v6-hs-domain/arms/a-plugin/`. 隐藏金标准尚未查看, B/C 尚待运行.
- 2026-08-28: 用户报告周额度与五小时额度均重置并要求继续. 预注册 pilot v6 H^s operator-domain OOD 三臂主实验. A=v1.7 plugin with max 3 research children, B=blank Codex, C=QED 1219009, all gpt-5.6-sol xhigh and pinned CLI 0.149.0-alpha.4.3. 一轮每臂一次, 依次 A/B/C, hidden gold 0f9b2b0 在 solver 全部冻结前隔离. 计划与 harness 在 `runs/three-arm-pilot-v2/pilot-v6-hs-domain/`.
