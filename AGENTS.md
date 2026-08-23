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
