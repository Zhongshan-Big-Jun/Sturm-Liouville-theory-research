---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c22b-f107-7520-9d75-33258752765c"], "conditions": "Both central traces are continuous in the equivalent left-definite and Sobolev H2 norms. Complete sufficiently high tails are used for the closure argument.", "dependencies": [{"location": "tools/left-definite-theory.md", "sha256": "d944d1dd15e9e10af7d0e0d1a2a5ed3df0664a00e8f60963a728161dffd47945"}], "evidence_status": "ANALYTIC_PROOF_SCOPED; HISTORICAL_BRANCHES_NOT_REAUDITED", "related": ["[[constrained-denseness-runs]]", "[[denseness-criteria]]", "[[left-definite-moment-recurrence]]"], "scope": "Fixed real c>0; complex Hc2=D(Kc) with specified Krein boundary conditions; cofinite subsets of D={0,1} union {4,5,...}. No general non-cofinite or s=3 conclusion.", "slug": "leftdef-o1pld-l2-structural", "source": "docs/SL_cofinite_left_definite.tex, fifth-round correction of R-20260823T030000Z-leftdef-o1pld", "sources": [{"locator": "Fifth-round Green kernels, cofinite closure and monomial correction", "path": "docs/SL_cofinite_left_definite.tex", "sha256": "ed07e47fd370a9db3b6a6a2d125d9eec996288e53a6024a0e9fb533ca1b3c0bb"}, {"locator": "Section2, positive self-adjoint shifted Krein operator and isometry", "path": "docs/SL_h2_completeness_proof.tex", "sha256": "f679150677f87217f4e6ab047163b7d32631ab6780b503db4fedac9c23b0b71d"}, {"locator": "Historical Lemma1 and refuted Claim4/Theorem5/Corollary6; unchanged branches scoped separately", "path": "runs/rigorous-open-math-research/R-20260823T030000Z-leftdef-o1pld/candidate_proof.md", "sha256": "cc358526dfd62dd799741c106407317429791f21486326fd48da8ed0b917f20c"}], "status": "s=2余有限解析分类; 原三条候选声明REFUTED; 一般O1pLD开放; 当前复用以纠错回执为准", "tags": ["稠密性", "左定", "L2", "余有限", "Green函数", "迹", "矩问题", "O1pLD"], "title": "第二左定空间的余有限稀疏族: 两条迹与L2障碍", "tool_id": "leftdef-o1pld-l2-structural"}
---
# 第二左定空间的余有限稀疏族: 两条迹与 L2 障碍

固定实数 c>0. 这里 Hc2 是满足 Krein 边界条件的 D(Kc), 范数为 ||Kc f||_2, Kc f=-f''+cf. 它不是全部普通 Sobolev H2. 函数和线性空间允许复数, 内积对第一变量线性. 指标 D={0,1}∪{4,5,...}, p0=1,p1=x, p_(2m)=x^(2m)-m/(m-1)x^(2m-2), p_(2m+1)=x^(2m+1)-m/(m-1)x^(2m-1), m>=2; q_n=Kc p_n.

## 被反证的旧候选声明

旧 run R-20260823T030000Z-leftdef-o1pld 的 Claim4、Theorem5、Corollary6 原状态均为 NOT-YET-STRICT. 以下按原量词均为 REFUTED: 尾部三项递推迫使全部 L2 矩为零; 任意余有限 q_n 子族在整个 L2 稠密; 任意真闭 V 必排除无穷多项. 旧 run 保留历史身份, 不能继续把这三条当作待证任务.

最短反例为 V={f∈Hc2:f(0)=0}. 求值连续, V 真闭, 却恰好只排除 p0. 明确的对偶障碍是

$$g_{0,c}(x)=\frac{\cosh(a(1-|x|))}{2a\sinh a},\qquad a=\sqrt c.$$

它属于 L2 且非零, 满足 <Kc f,g0,c>=f(0). 所以它正交于所有 n≠0 的 q_n; 两个奇偶尾部递推成立, 但 M0=∫g0,c=1/c≠0. 原 H2/H3 主证明包含的低位正交条件不能在尾部问题中删除. 此发现不推翻那些完备性主定理.

## s=2 的准确替代

对任意余有限 N⊆D,

$$\overline{\operatorname{span}\{p_n:n\in N\}}^{H_c^2}
=\{f\in H_c^2:0\notin N\Rightarrow f(0)=0,\quad1\notin N\Rightarrow f'(0)=0\}.$$

因此余有限 q_n 子族在整个 L2 稠密, 当且仅当 0,1 都在 N 中. 删去任意有限个高阶项不改变闭包; 删去低阶项则留下对应的连续迹障碍. 任意充分高的完整奇偶尾部闭包都是 V*={f:f(0)=f'(0)=0}.

导数迹的对偶函数为

$$g_{1,c}(x)=\frac{\operatorname{sgn}(x)[a\cosh(a(1-|x|))-\sinh(a(1-|x|))]}{2(a\cosh a-\sinh a)}.$$

它满足 <Kc f,g1,c>=f'(0); 零点处有单位跳跃, 只把它作为 L2 函数使用, 不误认为它在 D(Kc) 中. 余有限像族的正交补恰由缺失的低位指标对应的 g0,c/g1,c 张成. 特别地, 非零衰减矩可以由 L2 函数实现, 不能再将其全部排除.

对任意 m0>=2, 两条奇偶矩递推在所有 m>=m0 成立的 L2 函数恰为 span{g0,c,g1,c}. 以第一变量线性的 M_k=<u,x^k> 记矩, 精确表示为 u=cM0 g0,c+cM1 g1,c. 因而补上 M0=M1=0 才能恢复零解刚性.

若 V⊆Hc2 闭且实际保留集 N_V={n:p_n∈V} 余有限, 则 V 包含 V*. 此时 V=Γ^(-1)(S), Γ(f)=(f(0),f'(0)), S≤C2. 保留族闭包对应 S 中实际包含的两个坐标轴方向. 例如 V={f:f(0)=f'(0)} 包含 1+x, 却不包含 1 或 x; 其保留族闭包只是 V*, 严格小于 V. 余有限保留不自动保证在受约束 V 中稠密.

完整证明及域、范数、截断和边界修正细节见 [解析证明](../docs/SL_cofinite_left_definite.tex). 证明的核心是尾部多项式的代数消元、两个零迹下的 Sobolev 截断, 以及行列式为 2L² 的端点修正矩阵. 有限数值检查不承担这个闭包结论.

## 单项式引理的局部修复

L2 中删去有限个单项式仍然稠密. 若 f 正交于全部保留单项式, 删去集为空时取 M=0, 否则取 M 大于删去的所有次数, 则 x^M f 正交于所有多项式; 全体多项式的 L2 稠密性给出 x^M f=0, 再用 x^M≠0 几乎处处得到 f=0. 这也证明有限支撑矩刚性, 无需 Müntz 换元.

旧 Lemma1 的奇部范数换元系数应为1, 不是1/2; f_o=x 时左右正确值均为2/3. 这修复证明中的公式, 不撤回有限删除单项式的结论. 该结论不能转用到 q_n 像族.

## 其它分支与复用边界

- Cauchy-Schwarz 矩界、奇偶分解及 μ4 非稠密例仍按原 run 的相应局部证明引用. 本轮新证明聚焦两条审计发现与余有限 s=2 分类, 不重新认证原 run 的全部内容.
- 一般非余有限 O1'LD、s=3 的尾部可实现性及一般 O1' 仍开放. 不把上述结论外推到高阶左定空间.
- 新版的当前复用资格由版本化纠错回执决定. 历史来源和原错误文字不被覆盖. 局部 Lean 的实际范围另见 [第五轮报告](../reports/proof-audit-round5-20260921/REPORT.md), 不把代数片段当作完整解析形式化.
