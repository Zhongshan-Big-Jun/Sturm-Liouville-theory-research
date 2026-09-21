# 第七轮软件作者隔离目录

## 工作方法

- 本目录是唯一写目录. 主库、历史输出、插件、旧 Blueprint 只读; 不 commit/push.
- originals/ 是原字节快照, candidates/scripts/ 是候选及必要原字节依赖. 修订限用户指定十个文件的直接公式、参数、矩阵乘法和确证的后端接线问题.
- 用户给定约定: s=rhoR-rhoL; int rho*u_k^2=1; grad D=-s*f; F=f/lambda_(n+1). 简式 H=-lambda_(n+1)*diag(s)@J 仅在 F=0 成立. 镜像用 chain rule, 不对 full-interface 梯度统一乘 2.
- 回归执行实际函数及原 AST 表达式, 与小型有限差分比较. 保留旧错误真实失败、正常及 -O 原始回执、输入和输出哈希. 明示隔离加载/注入与直接 CLI 的范围差异.
- 作者结果仅为候选与局部 EVIDENCE, 等待新的 stateless agent 复跑和审稿. 数学完整推导、历史扫描与求解器全域认证另计.
- 每次候选或验证维护后更新下方记录. 完整方法、覆盖及未验证事项写入 README.md 和 change-notes.md.

## 对话与维护记录

- 2026-09-21: 用户要求先读主库 AGENTS 和 checks-author/propagation.md, 原字节隔离指定十文件与必要依赖; 只修确认问题, 不运行历史全扫描. 本目录已保存十候选原件、七 Python 依赖、一份表格和只读上下文. 原始身份见 inputs/snapshot-manifest.json.
- 环境: WSL /usr/bin/python3 可导入 numpy/scipy/sympy/mpmath. 用户提示的 Windows bundled Python 作为可选交叉环境, 尚未运行.
- 2026-09-21: 后端真实 IVP/加权积分检查返回旧 precise 范数 0.94870/0.93136, fixed 样本误差约 1.3e-12. 仅在已分配 op03_gap_fh 切换到同签名所需接口的 fixed, 不改依赖文件. 十候选完成直接公式/符号/矩阵乘法修订, 原字节和差异已保存.
- 2026-09-21: 用户补充非驻点 Hessian 的秩一项与驻点简式边界. 回归分别覆盖两者, 不将简式推广到全域. 首次 harness 的格式化 AST 选择器有歧义, 保留原始失败并修正测试选择器; 修正后原版本 117 项中 79 项真实失败, 无异常.
- 2026-09-21: 候选首轮 117/117 行为检查通过. 新增单入口 regression/replay.py, 自动复制冻结输入, 分进程运行原版/候选的正常与 -O 测试及四点 op03 直接 CLI, 保留输入哈希/原始流/退出码. 未执行 n>=2 历史全扫描或重证解析 Jacobian 推导.
- 2026-09-21: 完整自动隔离重放已返回 0. 正常/-O 各 117/117 候选通过, 原版各 79 项失败且真实退出 1; 四点 op03 直接 CLI 两种模式数值对照通过. 新复制目录输入哈希不变, 所有项目模块位于该隔离目录. 主库 18 个定向输入仍与快照字节一致, 仅 10 个候选变更、依赖 0 变更. README/change-notes 已说明数学前提、AST/注入与 CLI 差别、未覆盖的解析求和/历史全扫描和独立审查待办.
- 2026-09-21: 最终交付冻结 README/change-notes、十文件差异、原始/候选/依赖哈希及全部现有回执. 新增只读 verify_package.py 校验包字节; 该检查与数学/软件行为结论分开. 完整测试入口为 regression/replay.py, 可在后续复制目录执行.
- 2026-09-21: 协调器阅览 diff/README 后要求将目标归属更正为“协调器分配的 10”, 并尽快冻结 manifest/completion, 不追加源码修复或行为测试. README 已更正. precise 仍是已记录的旧后端限制, 候选源码与此前行为测试输入不变. 最终状态为 SOFTWARE_AUTHOR_COMPLETE / INDEPENDENT_REVIEW_PENDING.
