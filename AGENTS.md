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

## 会话记录

- 完整历史会话日志: `state/AGENTS_SESSION_LOG.md` (由 `scripts/split_agents_log.py` 维护, 本文件只保留指针与近期摘要).
- 每次变更后在本节追加一行近期摘要; 长日志一律写入归档文件.
- 2026-08-16 会话 108: 清查未跟踪文件并交接 (session log 归档, G1' EVIDENCE 脚本, 社区蒸馏缓存, 维护脚本); 同步状态; 尝试闭合 P1/M3 或 DensBC O1.
- 2026-08-16 会话 109 (R-20260816T000000Z-densbc-o1): DensBC O1 求解 run. 新 STRICT 结构定理 (投影稠密性 P_V(Pi)=V, 障碍矩系统, 游程/首个障碍, 对角归约 Theorem E, 有限秩分类); 诚实化约核 O1' (矩可实现/成员步). 独立对抗审计 (fresh subagent) REPAIRABLE_GAP 并已修复. 未 commit/push.
