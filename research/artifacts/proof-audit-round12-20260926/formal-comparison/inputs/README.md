# Round 12 finite mirror-sector Lean author packet

作者提交, 最终独立语义验收待完成. 任意 n 的实矩阵交换式, 原顺序坐标桥、归一化桥和对象区分见 contract.md. 当前一基 ε_j=(-1)^(j+1) 与零基 (-1)^i 均首项 +1; E=S 的左半块. -S 引理仅为一般约定转换.

- 源文件: project/AuditRound12.lean (9 数学主引理 + 1 汇总根).
- 人类契约: contract.md; 插件契约: contract.json.
- 实际声明: declarations.json / declarations.txt, 包含自动辅助声明、显式类型、定义体及传递公理.
- 盲读输入: blind/, 不含作者的人类契约和解释. 两个检验者仍需由协调方另行安排.
- 精确根执行: evidence/exact-root/run-manifest.json, 完整输入、命令与日志在同目录运行子文件夹.
- 作者命令与所有失败: commands/. main 源码不导入任何控制程序.
- 环境、读集和交付 SHA256: environment.json, read-set.json, delivery-manifest.json; 核实结果入口 summary.json.

从 WSL 直接复制运行以下命令. 每次新建唯一的命令标签和输出目录, 不覆盖已有证据. 只读使用指定 Windows Lean 4.31.0 和仓库 .lake/packages, 不执行 lake build 或安装操作.

```bash
python3 -B /mnt/f/tools/math-audit-round12-20260926/formal-author/run.py compile "replay-source-$(date -u +%Y%m%dT%H%M%S)"
python3 -B /mnt/f/tools/math-audit-round12-20260926/formal-author/run.py verify "replay-root-$(date -u +%Y%m%dT%H%M%S)" contract.json
```

第二条命令会重新编译根源文件、提取实际声明并检查完整契约及传递公理. 它的返回 0 和 exact_root_passed=true 仍不是独立语义验收.

可复制重放机器契约负对照 (预期 strict-exit 返回 1, 且 root_closure 为 target_mismatch; 环境不可用或编译失败不是该负对照的成功):

```bash
python3 -B /mnt/f/tools/math-audit-round12-20260926/formal-author/run.py verify "replay-negative-$(date -u +%Y%m%dT%H%M%S)" negative-contract.json
```

PositiveControls.lean 覆盖任意 n 的使用、n=0、n=3 镜像位置、n=1 非相等见证和非零奇外积. NegativeWrongSector.lean、NegativeMirrorSign.lean、NegativeNormalization.lean 故意不编译, 分别检查错误对象、镜像同号和漏掉 Gram 系数 2. 它们不属于最终根的导入链.

执行日志保留实际失败, 包括开发中的错误定义/证明和导出辅助程序的早期失败. 最终合格证据必须使用 summary.json 绑定的最终源码、导出、环境和运行, 不能把失败阶段误报为通过.
