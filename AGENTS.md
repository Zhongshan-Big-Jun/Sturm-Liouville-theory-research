<!-- blueprint-project-layout:v1:start -->
# Blueprint v2.2 project layout (highest precedence)

- `blueprint-project.json` is the physical-layout authority.
- Canonical graph, inventory, submissions, and audit history are under `blueprint/`.
- Raw inputs and generated artifacts are under `research/`; disposable work is under `research/work/`.
- Do not run or copy project-local Python tools. Resolve the active plugin's `runtime/blueprintctl.py`, then run `ensure` once and use that gateway.
- Any legacy `statistics/.../tools/...` command below is documentation only and is superseded by this block.
<!-- blueprint-project-layout:v1:end -->

# 项目维护

## 目标与入口

- 维护 Sturm-Liouville 边值问题的长期研究: 正交系/左定空间, 相邻特征值比值与间距极值.
- 本仓库是 [rigorous-open-math-research](https://github.com/xsoc1/rigorous-open-math-research) 的使用成果仓库. 归属区分既有文献, 合作者工作与人机合作推导.
- 研究入门读 [研究导航](docs/research-guide.md); 接续具体问题读 [research_map.md](research_map.md), 相应 run 和证据. 理解变化与人的批注写入 [项目理解](docs/PROJECT_UNDERSTANDING.md).
- 具体证明, 反例, 构造和严格审计使用研究插件. 工具卡及其索引在 [tools/README.md](tools/README.md); 形式化范围见 [lean-proof/STATUS.md](lean-proof/STATUS.md) 与脚手架登记.

## 工作方法

1. 进入项目先读根与相关子目录 AGENTS.md. 每次维护后在本文件写简短摘要, 具体对话与方法记入 [state/AGENTS_SESSION_LOG.md](state/AGENTS_SESSION_LOG.md).
2. 如实区分 STRICT, EVIDENCE, 待检验与 OPEN. 数值样本不能替代证明; NO_RETURN 和超时不构成数学失败. Lean 编译, 陈述保真, 假设闭合与 canonical 接收分别描述.
3. 从论文或路线提炼工具时记录实际来源版本, 可定位内容, 假设与用途. 成功, 反例, 方法局限和实现错误都可以记录; 自由批注注明来源与证据状态. 再检视旧路线时说明改变了什么条件或获得了什么新信息.
4. 保留被 hash manifest, 审计, checkpoint 或引用绑定的文件路径与字节. 新批注另写, 原始证明包保持可复核. 既有未提交工作先比较与备份, 按本轮 scope 修改.
5. 清理按 [归档规则](docs/archive-policy.md) 查引用和可再生性. 不按 mtime, 名称或重复字节删除研究内容. 常规导航与人类批注不需要复制整个研究台账.
6. canonical 操作使用顶部指定的插件运行时 gateway. 历史本地 Python 维护或 Blueprint 命令仅作记录, 不直接执行. 普通仓库清点可以用 shell 或独立临时检查程序.
7. 文档使用英文标点. 新代码 tab 缩进, 多词函数 snake_case, 多词变量 PascalCase; 适用语言中大括号独占行, if/for/while/switch 与左括号间无空格. C++ main 的末三句依次为 cout << endl;, system("pause");, return 0;.
8. 外部临时仓库放 F:\tools\. 数学结果引用文献时核对实际读取内容, 不凭摘要猜测定理.
9. 已授权同步时先推主仓库 Zhongshan-Big-Jun/Sturm-Liouville-theory-research, 再推 xsoc1/Sturm-Liouville-theory-research fork. 本轮并行成果仓库 agent 不 commit/push, 由协调器处理交付.

## 当前数学边界

- M3: n=2 对称 INF large-R 有限非零内部 chart 内 STRICT 闭合, canonical 接收与独立复现已保存. 旧 staged D-side mass 的 odd/log 障碍已 SUPERSEDED.
- KP-DET: sequence-26 的完整 0<c<=2/3 分支与 P20-P21 求积约化经审计 PASS. P1-P4 的 pivot/phase 部分已 canonical 接收; 后续 run 包与 canonical 分开登记. 本地主 run 的 Q9 仍 OPEN.
- 插件公开 benchmark 另有三份 Q9 完整证明及匿名外审 PASS, 尚未接入本 canonical 或 Lean. 不据此宣称全局 G1', KO-DET 或完整 n>=2 极值问题已解决.
- 旧文档中 G2 的闭合范围表述存在差异, 需要按定义与量词对齐. 本轮维护不改写历史证明来消除差异.
- Lean 工程含已检查的证明片段, 条件化接口和带 sorry 的脚手架. 历史全库计数不得复述为当前形式化结论.

## 近期维护记录

- 2026-09-09: 补查归档的 Git clean 转换. Windows Git 的 autocrlf=true 会改写两份旧 README 和完整会话日志; 在 docs/history 与 state 新增只匹配这 3 个归档文件的 -text 属性. 原根 .gitattributes 保持不变. 通过独立对象目录的 hash-object/show 核对实际提交字节, 精确暂存集更新为 157 个路径, 未 stage/commit/push.
- 2026-09-09: 中断后续接导航发布依赖检查. [发布依赖清单](reports/repository-cleanup-20260909/publication-dependencies.json) 列出 12 个需按原字节纳入版本的既有 KP-DET 证据, 递归绑定检查, 历史绑定限制和协调器精确暂存范围. 只更新文档与报告, 未 stage/commit/push 或接收 canonical.
- 2026-09-09: 按用户 2.0 落地任务并行整理成果仓库. 重写中英文首页, 归档旧首页与长 AGENTS, 新建研究导航, 项目理解和脚本导航. 删除 10 个无引用的过时维护程序与 115 个可再生 TeX 中间物; 4,392 个原文件字节不变, 61 份文档 PDF 解析通过, canonical gateway 校验通过. 具体哈希, 原 68 项工作树保护和验证见 [清理报告](reports/repository-cleanup-20260909/REPORT.md). 未 commit/push.
