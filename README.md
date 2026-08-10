# Sturm-Liouville 边值问题研究 (BVE research)

本项目研究 Sturm-Liouville (SL) 边值问题的前沿数学问题, 重点关注两个主题:

1. **特征函数系/多项式系的完备性**: SL 边值问题的解在多大的 Hilbert 空间 (左定空间)
   中等价于该空间内的所有正交函数系. 基准论文: Littlejohn-Quintero-Roba,
   *Krein-Sobolev Orthogonal Polynomials* (Springer 2025).
2. **特征值间距与比值的最优界**: 对加权 Dirichlet 问题 -y'' = lambda rho y,
   1 <= rho <= R (可测盒类), 优化相邻谱隙 D_n = lambda_{n+1} - lambda_n 与比值
   lambda_{n+1}/lambda_n.

## 主要结果 (截至 2026-08-10)

- **相邻比值上确界** (严格证明): sup_{n,rho} lambda_{n+1}/lambda_n = nu(R),
  闭式由 arccos 给出; 全序列下确界 = 1 (Weyl 渐近, 下确界不达到).
- **n=1 相邻间距极端值** (严格证明): SUP/INF 由对称三块 [1,R,1] / [R,1,R] 达到,
  全部义务 O1/O2/O3a/O3b 闭合 (相位比刚性, 2026-08-09); INF 侧 R -> infinity
  极限定理 A 已证.
- **n >= 2 相邻间距极端值** (严格证明, 2026-08-10):
  - 有限块约化: 最大/最小值达到; 每个全局极值子 bang-bang, 至多 2n+1 块 / 至多 2n 开关.
  - 精确 2n 开关定理: 每个全局极值子合并相邻同值块后恰有 2n 个有效内部开关;
    最大化子首尾块取 1, 最小化子首尾块取 R; 不假设对称或唯一.
- **H^s 左定空间多项式完备性** (严格证明): 第二左定空间 H^2 与一切整数 s >= 1 的
  左定空间 H^s 中, 缺 2, 3 次的多项式基解析完备 (矩跳跃判据 + 增长引理).
- 文献检索结论: 未检索到与上述 n >= 2 定理直接等价的已发表结果; 项目明确不声称首创,
  Willner-Mahar 1979 等早期文献为既有工作风险 (详见 docs/ 内各证明文档).

## 目录结构

| 目录 | 内容 |
|---|---|
| docs/ | 研究文档与完整证明 (tex/pdf, 含证明包与综述) |
| scripts/ | 数值审计, 复现与探索脚本 (Python) |
| tools/ | 数学工具库 (Obsidian 兼容 Markdown, 含解析/适用范围/验证状态) |
| papers/ | 参考文献全文 (含版权文献, 仅个人研究, 仓库私有) |
| research_cache/ | 文献检索缓存与元数据 |
| images/ | 扫描页与测试图 |
| misc/ | 失败/测试产物与调试工件 |
| runs/, index/, state/, agenda/, knowledge/ | Blueprint v2.2 研究运行, 索引, 状态与问题记录 |
| literature/, archive/, reports/ | 文献条目, 归档与报告 |

## 文档编译

所有 LaTeX 文档使用 xelatex (ctexart), 中间产物输出到 docs/build/:

```powershell
cd docs
xelatex -output-directory=build <file>.tex   # 运行两遍
```

零警告编译. 综述见 `docs/SL_spectral_topics_summary.pdf`.

## 复现与审计

- Python 3.10 (需 numpy/scipy/mpmath), Windows 下建议设置 `PYTHONUTF8=1`.
- 关键审计脚本: `scripts/audit_o3a_pdf_part1..4.py` (O3a 证明),
  `scripts/audit_nge2_pdfs.py` (n >= 2 证明: Part A 40/40 + Part B 16/16),
  `scripts/_hp_nge2.py` (mpmath 50 位), `scripts/_smooth_nge2.py` (光滑权 4/4).
- 证据分层约定: 严格证明 (STRICT) / 数值证据 (EVIDENCE, 不构成证明) / 猜想 (OPEN),
  全项目统一标注, 见 AGENTS.md 与各文档.

## 工作记录

会话与详细工作日志见 [AGENTS.md](AGENTS.md) (含审计记录, 工具库更新与开放问题).
