# -*- coding: utf-8 -*-
import io
p = r"AGENTS.md"
src = io.open(p, encoding="utf-8-sig").read()
entry = r"""
### 2026-08-10 会话 51 (INF 侧阱族小 R 相位刚性定理 + Sun 2022 判定收尾)
- 任务: 承接交接 (INF 侧阱族刚性: 全局 inf 是否在对称阱 [R,1,R] 达到), 完成小 R
  定理 1<R<=3/2 的完整严格证明, 整理文档/工具库/台账; 用户纪律重申: 数值不得当结果,
  严格区分 严格证明/STRICT 与 数值证据/EVIDENCE.
- 数学突破 (STRICT): 阱族相位比刚性定理 - 1<R<=3/2 时阱族任意 sign-consistent
  good root 必为对称根 a+b=1. 证明链 (全部 E1): (i) 相位范围引理 (y2 唯一零点 z in
  (a,b), 阱区显式解在 x=pi/(ms2) 的零点矛盾 => tau*A, tau*B < pi); (ii) 传输能量
  守恒 (中间低密度区旋转 P(psi) 保持 X^2+Y^2 => y(b)^2/y(a)^2 = J~(B)/J~(A),
  J~(x)=sin^2x/(sin^2x+m^2cos^2x)); (iii) 残差消元 (R1=R2=0 => r_tau(A)=r_tau(B));
  (iv) 相位比严格单调: 关键因式分解 W~^2 sin^2x Psi~' = -(q+1)(2N0+qN1)/8,
  N0=4x-2sin2x>0; N1<0 时归约到 H=4N0+N1>0; H>0 引理用 u=2x 代换
  H=2[u(4+c^2+c)-sin u(5+c)], 分 (pi,2pi) 平凡与 (0,pi) 经 h' 分解, (0,2pi/3) 上
  h'=sin u*G(u), tan(u/2) 半角有理化 G=N(t)/(1+t^2), N''>0 且 N'(0)=N(0)=0 =>
  N>0. 故 Psi~'<0 于 (0,pi) (0<=q<=1/2), r_tau 于 (0,pi/tau) 严格递减 =>
  A=B => a+b=1. 阈值 R=3/2 对机制精确: R>1.5 时 r_tau 非单调且离轴 E=0 分支出现
  (EVIDENCE).
- 8 条符号恒等式 (A1-A8: 因式分解/H=4N0+N1/u 代换/h' 公式/G-N(t) 关系/N'' 公式/
  d log J~/d log r_tau) 由 scripts/_well_rigid_verify.py 用 sympy 精确验证全部
  True; 数值探针 B1-B5 记录阈值 (q=0.5 处 max Psi~' ~ -6.9e-13, q=0.5001 变正),
  R=1.5 good root (a,b)=(0.40879841,0.59120159), a+b=1 至 1e-10, |A-B|<=4e-13,
  r_tau(A)=r_tau(B)=0.2189882504, 符号 y2(a)>0>y2(b), 零点 x=0.5; R=4 离轴分支
  N1 in [-2.76,-2.61] < 0, 对称线 N1 在 v* 穿越 0; 全部为 EVIDENCE.
- 文献判定收尾: Sun 2022 (JMAA 516:126513) 全文仍不可达 (非 OA/captcha/Sci-Hub 无);
  colab.ws 恢复官方完整摘要 (最优性条件+直接法刻画极值密度), zbMATH 评论 (Erdogan
  Sen, Zbl 1506.34110) 明确密度类为 "piecewise continuous with a bounded of jumps",
  非全可测盒类; 判定: 不能闭合我们的盒类 INF 侧, 潜在重叠需全文 (登记
  research_cache/zb_review_1506.34110.txt + lit_sun_qixie_notes.txt + colabws_sun_jina.txt).
  下载 papers/ashbaugh1991_gaps.pdf (Schrodinger L^p 势类 gap 极值, 机制相关非同一
  问题, 不抢注).
- 诚实登记缺口 (开放/CANDIDATE): (a) 对称线 1D 分析 (f(v) 零点唯一性, D(v) 单峰,
  端点极限) 未严格证明 - 闭合后小 R INF 侧即完整; (b) R>3/2 阱族刚性开放, 候选路线
  = 证明 good root 处 N1=0 恒等式 + 离轴 E=0 分支 N1<0; (c) 定理 A (INF R->inf 极限)
  独立复核 CANDIDATE; (d) 极值点存在性与 good-root 条件全局论证部分开放 (边界情形).
  全部 EVIDENCE 与缺陷脚本登记 (scripts/_well_mc.py Psi 定义缺 q 项; misc/_well_fh.py
  R1/R2 数值与已验证 fval/FH 不一致; _well_system_derive.py sec_value 多 1/m 因子,
  仅探索用) 见 misc/_well_explore_log.md.
- 文档交付: docs/SL_gap_n1_well_rigidity_R32.tex/.pdf (11 页, 零警告, 含 STRICT/EVID
  标注、主定理证明、缺口登记、R>3/2 候选路线、附录恒等式清单、涉及到的数学知识);
  修正注 rem:fh 的 FH 符号公式 (dD/da=-(R-1)f(a), dD/db=+(R-1)f(b), f=lam2*y2^2/n2
  -lam1*y1^2/n1; 单特征值 FH 由 _well_fh2.py 验证到 1e-8; f 符号分布 R=4 对称 good
  root: f(0.2)=+4.12, f(0.5)=-2.28, f(a)=f(b)=0). 编译产物入 docs/build/.
- 工具库: 新增 tools/well-family-rigidity.md (阱族相位比刚性, 解析/适用范围/验证
  状态, 阈值 R=3/2 与缺口登记) + tools/README.md 索引/速查表/维护日志更新.
- 台账/状态: 本运行 research_ledger.md 追加 R-112 (见下); state/current.json 与
  state/RESUME.md 更新 (INF 侧: 小 R 已证, 一般 R OPEN); 未调用 update_goal
  (目标持久); validate_project.py 已知 INVALID (knowledge/ 缺 Blueprint 结构文件,
  既有问题与本会话无关).
- 待办/后续: 缺口 (a) 对称线 1D 严格证明 (小 R INF 闭合的关键一步); (b) R>3/2
  候选路线; (c) 定理 A 独立复核; 之后按综述开放问题清单推进.
"""
src = src.rstrip() + "\n" + entry
io.open(p, "w", encoding="utf-8-sig", newline="\r\n").write(src)
print("AGENTS.md appended; new length", len(src))
