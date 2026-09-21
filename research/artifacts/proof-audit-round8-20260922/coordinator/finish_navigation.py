from pathlib import Path
import json
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922')
for name in ['math-review','certificate-review','formal-semantic']:
	if json.loads((O/(name+'-received.json')).read_text())['verdict']!='APPROVED':raise RuntimeError('Review not approved '+name)
def replace(n,old,new):
	p=R/n;t=p.read_text()
	if new in t:return
	if t.count(old)!=1:raise RuntimeError('Ambiguous navigation anchor '+n+' '+old[:60])
	p.write_text(t.replace(old,new,1))
def prepend_section(n,body):
	p=R/n;t=p.read_text()
	if body in t:return
	a=t.index('\n')+1;p.write_text(t[:a]+'\n'+body+'\n'+t[a:])
zh='2026-09-22 第八轮修订: 对称阱族 INF 极限改用连续相位下界覆盖整个薄层区域, 初等差量估计修复大 w 比较, T1 不再依赖旧网格或 T3 高精度数值. 固定内部 u 的首项为 C(u)/R; 最优值满足 0≤R m_R−M=O(1/R). 四张工具卡、精确有理证书、局部 Lean 与隔离检验见 [第八轮报告](reports/proof-audit-round8-20260922/REPORT.md).\n\n'
replace('README.md','2026-09-21 第七轮修订:',zh+'2026-09-21 第七轮修订:')
replace('README.md','谱隙条目按第七轮修订更新.','谱隙条目按第七、八轮修订更新.')
row='| 对称阱族 INF 极限 | R m_R→M≈24.9438661384, 非负误差 O(1/R); Rη_R→0 的近极小化子收敛 | [第八轮连续证明](docs/SL_gap_n1_inf_limit_proof.tex); 相位薄层界与大 w 比较覆盖 R≥1500; 非对称族及全盒类须另核对 |\n'
replace('README.md','| n>=2 间距结构 |',row+'| n>=2 间距结构 |')
en='Eighth-round repair (2026-09-22): the symmetric-well INF limit now uses a continuous phase bound over the entire thin-layer region and elementary positive-margin comparison for large w. T1 no longer depends on the old grid or high-precision T3 values. For fixed interior u the leading correction is C(u)/R, and 0<=R*m_R-M=O(1/R). Four revised tool cards, exact rational certificates, scoped Lean and fresh independent reviews are recorded in the [eighth-round report](reports/proof-audit-round8-20260922/REPORT.md).\n\n'
replace('README_EN.md','Seventh-round repair (2026-09-21):',en+'Seventh-round repair (2026-09-21):')
replace('README_EN.md','the gap entry in round7.','the gap entries in rounds7-8.')
replace('README_EN.md','| n>=2 gap structure |','| Symmetric-well INF limit | R*m_R tends to M≈24.9438661384, with nonnegative O(1/R) error; near-minimizers converge when R*eta_R tends to zero | [Continuous proof](docs/SL_gap_n1_inf_limit_proof.tex); non-symmetric/all-box conclusions require their own evidence |\n| n>=2 gap structure |')
replace('docs/research-guide.md','## 谱比值与间距极值','## 谱比值与间距极值') if False else None
prepend_section('docs/research-guide.md','第八轮当前入口: [INF 极限证明](SL_gap_n1_inf_limit_proof.tex)与[修订报告](../reports/proof-audit-round8-20260922/REPORT.md). 连续相位方法覆盖完整薄层域, 大 w 用初等正余量比较; T1 的解析收敛与 T3 的数值定位分开. 旧05/16/19证书不再承担当前证明. 固定内部参数误差为1/R, 不能据此推断最优参数收敛率.\n')
replace('PROJECT.md','The n>=2 finite-R global problem remains open;', 'Round8 repairs the symmetric-well INF asymptotic proof with continuous phase coverage and an elementary large-w comparison, exact T3 enclosures and fixed-u 1/R expansion. It does not re-audit the separate all-R or nonsymmetric chains. The n>=2 finite-R global problem remains open;')
replace('research_map.md','Last updated: 2026-09-21 (round7 scoped repairs; older runs retain their original dates)','Last updated: 2026-09-22 (round8 scoped INF repairs; older runs retain their original dates)')
row='| B4-INF-LIMIT | Symmetric [R,1,R] first-gap scaled infimum and near-minimizers | SOLVED | docs/SL_gap_n1_inf_limit_proof.tex; round8 report | R*m_R→M≈24.9438661384 with nonnegative O(1/R) error; near-minimizers require R*eta_R→0. Entire thin-layer region covered by continuous phase speed; large-w comparison has positive margin. T1 uses T2 analytically, not T3 numerical constants. No new all-box/nonsymmetric/n>=2 claim |\n'
replace('research_map.md','| B5 |',row+'| B5 |')
replace('research_map.md','B4 --solved subproblem--> B4-SUP-LIMIT via thin heavy intervals + min-max','B4 --solved subproblem--> B4-SUP-LIMIT via thin heavy intervals + min-max\nB4 --solved symmetric-well subproblem--> B4-INF-LIMIT via phase speed + elementary A-doubleprime + analytic T2\nB4-INF-LIMIT --separate numerical localization--> exact rational T3 (not a prerequisite of T1)')
replace('research_map.md','  B5["B5 MDE unify (OPEN)"]','  B4I["B4-INF-LIMIT (SOLVED): symmetric well, continuous coverage"]\n  B5["B5 MDE unify (OPEN)"]')
replace('research_map.md','  B4 -->|solved asymptotic subproblem| B4L','  B4 -->|solved asymptotic subproblem| B4L\n  B4 -->|symmetric-well asymptotic subproblem| B4I')
extra='''
## Round8 research knowledge (2026-09-22)

- Reusable phase-speed bound: for the symmetric three-layer string, all R>=1 and 0<u<1/2 satisfy G>=pi^2/[2epsilon(w+ell)(w+epsilon*ell)]. True mode indexing and the continuously unwrapped angle are part of the contract.
- The failed rectangle route omitted curved B/D strips, arbitrarily small w and part of the R-infinity tail. A finer grid does not repair inward coverage. Historical scripts remain unchanged; the current proof replaces their role.
- Fixed-u 1/R expansion and optimized-value O(1/R) are separate statements: the latter also uses the global lower bound. The exact optimized coefficient and parameter rate have not been proved here.
- Possible next idea, not a theorem: propagate unwrapped angle derivatives through more layers or general transfer matrices to obtain uniform mode separation. Each interface, mode index and parameter domain must be re-established.

Four revised card versions and their exact issue releases are linked from reports/proof-audit-round8-20260922/REPORT.md. This human research map update does not change canonical Blueprint.
'''
p=R/'research_map.md';t=p.read_text();p.write_text(t+extra) if '## Round8 research knowledge' not in t else None
extra='''
## 第八轮: 连续相位、覆盖与误差层次 (2026-09-22)

本轮薄层缺口的关键是整个参数区域的覆盖. 原矩形在曲线边界内缩, 还遗漏任意小 w 与无穷 R 尾部; 提高网格精度不能改变覆盖方向. 以射击解的连续展开相位代替固定正切分支后, 可同时控制相位速度、第一频率和相邻频率间隔, 得到一个全域解析下界. 它使 T1 只依赖 T2 的解析余量, 数值定位 T3 成为独立的结果.

粗而透明的界有时比细数值常数更适合证明主链. 大 w 区域的 d1>4alpha、d2<3alpha 给出正余量 ell/(R*u^3); 辅助细常数仍可留在工具库, 但不必增加主定理的必要依赖. 旧成功输出、失败覆盖与新替代均保留, 使后续研究能判断失败来自实现、量词还是策略.

收敛率也有不同层次: 固定内部 u 的隐函数展开给 C(u)/R; 再结合全域下界才得到最优值 O(1/R). 精确最优值首项和极小化参数速度仍需另证. 形式化局部代数或错误分支见证, 不会自动补上无限维谱比较、隐函数余项或全域分析的证明.

维护层面的反馈: 综合文档的整文件哈希把无关段落绑定在同一审查中. 本轮仅更新INF段落, 也使八张左定卡的有效审查失效. 应保留这种保守的失效检查; 后续可把被复用的证明拆成内容独立、身份明确的输入, 减少无关修改引发的续审, 但不能靠忽略变化或沿用旧通过结论解决. 本轮仅记录这一改进方向, 插件机制保持原样. 实际检索还发现另一层独立状态: 当前正文和放行都正确, 索引却可能继承旧版本摘要. 三张卡分别残留旧增长分类、Krein边界/完备性状态及已反证的尾部候选. 因而验收需把检索返回摘要与当前正文或显式summary逐字比较, 不能只检查卡片哈希和可用数量.

后续可讨论的想法 (未证): 对更多材料层传播连续相位导数, 寻找不依赖最小块宽的模态分离下界; 或把“参数域覆盖义务”显式附在数值工具接口上. 迁移前必须重新识别模态、界面变换和允许参数. 当前可用结论与检验范围见[第八轮报告](../reports/proof-audit-round8-20260922/REPORT.md).
'''
p=R/'docs/PROJECT_UNDERSTANDING.md';t=p.read_text();t=t.replace('更新于 2026-09-20.', '更新于 2026-09-22.',1);p.write_text(t+extra) if '## 第八轮:' not in t else None
prepend_section('lean-proof/STATUS.md','''## 2026-09-22 第八轮局部形式化

新增[AuditRound8.lean](SL/AuditRound8.lean): 显式谱上界前提下的相位反例界、真实三角根与S的代数桥接、固定u系数恒等式及驻点系数正性、0.8256有理比例、B/D曲边漏区的明确见证. 九合取根契约、47项实际公开声明(含编译器辅助声明)、传递公理、正对照和三个错误目标均留有实际新编译及独立复核. 精确次数和环境身份见[第八轮报告](../reports/proof-audit-round8-20260922/REPORT.md).

谱min-max仍为显式前提; 完整相位速度/T1证明、隐函数展开和余项、全域连续覆盖并未全部形式化. 保留48份旧SL源及原环境字节, 本轮没有运行全项目Lake build.
''')
prepend_section('scripts/README.md','''第八轮 INF 的当前精确入口为[certificate.py](../research/artifacts/proof-audit-round8-20260922/certificate/certificate.py), 证明算术仅用有理数, Machin/Taylor余项及显式守卫; 十进制仅负责向外显示. [第八轮报告](../reports/proof-audit-round8-20260922/REPORT.md)给出普通/-O/-S执行、反例对照和独立复核.

原 INF run 的05/16/19以及本目录 `_theoremA_recheck_*` 的旧抽样保留溯源. 05的像端点与16/19超越函数包络不能继续作为当前认证; 16的域覆盖由新的解析相位下界替代. 17/18及其它未重跑扫描没有获得本轮认证. 复用工具时从当前卡及精确版本回执进入.
''')
prepend_section('tools/README.md','''## 第八轮修订 (2026-09-22)

[INF极限](inf-limit-comparison.md)、[大w比较](lemma-A-doubleprime.md)、[相位括号](delta-bracketing.md)、[余切余项](cot-series-certificate.md)已按当前精确版本修订. 新连续相位覆盖替代旧薄层网格, 固定u误差改为1/R; 根像端点、Laurent幂次、局部一致收敛与arctan极限同步修正. 默认复用须通过当前纠错回执, 旧证据和批注按原版本保留. [第八轮报告](../reports/proof-audit-round8-20260922/REPORT.md)分别列明解析、精确证书和局部Lean范围.
''')
print('Navigation, research map, understanding, tools and formal status updated.')
