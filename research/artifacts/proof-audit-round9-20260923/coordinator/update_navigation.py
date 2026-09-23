from pathlib import Path
R=Path('/mnt/f/LaTeX/BVE research')
def edit(Name,Fn):
	P=R/Name;B=P.read_bytes();NL='\r\n' if B.count(b'\r\n') and B.count(b'\r\n')==B.count(b'\n') else '\n'
	S=B.decode().replace('\r\n','\n');T=Fn(S)
	if T==S: raise ValueError('no edit: '+Name)
	P.write_bytes(T.replace('\n',NL).encode())
def prepend_after_title(S,T):
	A,B=S.split('\n',1);return A+'\n\n'+T.strip()+'\n'+B
CN='2026-09-23 第九轮修订: 二阶变分程序改用真实块积分约束, 补齐本征函数导数的归一化核项; 撤回一维 Green 对角发散的错误解释. 物理世俗函数带频率因子, 严格反射对称的是归一化函数. 新的 Jacobi 证明给出平衡候选值随 n 严格递减及其极限, 尚未证明它就是全局最优值. 证据与检验范围见 [第九轮报告](reports/proof-audit-round9-20260923/REPORT.md).'
EN='Ninth-round repair (2026-09-23): block tangency now uses actual integrals, the normalized eigenfunction derivative includes its kernel component, and the false one-dimensional Green-diagonal divergence argument is withdrawn. Reflection preserves the normalized secular function; the physical function has a frequency factor. A Jacobi proof establishes strict decrease and the limit of the prescribed balanced candidate sequence, without identifying it with the global optimum. See the [ninth-round report](reports/proof-audit-round9-20260923/REPORT.md) for evidence and verification scope.'
edit('README.md',lambda S:S.replace('2026-09-22 第八轮修订:',CN+'\n\n2026-09-22 第八轮修订:',1).replace('谱隙条目按第七、八轮修订更新.','谱隙条目按第七、八轮修订更新, 固定 n 候选谱按第九轮修订更新.').replace('| n=1 相邻间距 |','| 固定 n 平衡候选比值 | 完整 2n 简单根计数; 候选 c_n 严格递减至 ((pi−phi)/phi)² | [当前证明](docs/SL_fixed_n_supremum.tex); phi=arccos((sqrt(R)−1)/(sqrt(R)+1)), R>1; 全局最优性仍开放 |\n| n=1 相邻间距 |',1).replace('固定 n 比值的全局最优值与剩余单调性问题. 后续研究已经证明的 2n 根计数见','固定 n 比值的全局最优值及真正上确界序列的性质. 平衡候选的 2n 根计数、单调性与极限见'))
edit('README_EN.md',lambda S:S.replace('Eighth-round repair',EN+'\n\nEighth-round repair',1).replace('gap entries in rounds7-8.','gap entries in rounds7-8 and the fixed-n balanced candidates in round9.').replace('| n>=2 gap structure |','| Fixed-n balanced ratio candidates | Complete 2n simple-root count; c_n strictly decreases to ((pi-phi)/phi)^2 | [Current proof](docs/SL_fixed_n_supremum.tex); phi=arccos((sqrt(R)-1)/(sqrt(R)+1)), R>1; global optimality remains open |\n| n>=2 gap structure |',1))
edit('PROJECT.md',lambda S:S.replace('2. **SL ratio extremals**: sup lambda_{n+1}/lambda_n = nu(R) proved (session 5); fixed-n and inf problems open.','2. **SL ratio extremals**: the all-index supremum nu(R) and infimum 1 are proved in their documented classes. Round9 corrects the physical/normalized secular distinction and proves all-n root count, strict monotonicity and the limit of the prescribed balanced candidates. Equality with the fixed-n global supremum remains open (O1/O2).').replace('## Key files','Round9 also repairs the true-integral tangent projection and eigenfunction normalization, and replaces the false Green-diagonal divergence argument with a finite concentration limit. These corrections do not resolve global G1 or certify historical scans.\n\n## Key files').replace('- Status/proof navigation:', '- Latest scoped correction: `reports/proof-audit-round9-20260923/REPORT.md`; two revised PDFs and three versioned tool cards.\n- Status/proof navigation:',1))
edit('docs/research-guide.md',lambda S:prepend_after_title(S,'第九轮当前入口: [二阶变分解析修复](../research/artifacts/proof-audit-round9-20260923/analytic-repair.md)、[固定 n 候选谱证明](SL_fixed_n_supremum.tex)和[修订报告](../reports/proof-audit-round9-20260923/REPORT.md). 真正切空间由块积分定义; 归一化导数、有限 Green 核与移动界面加速度分别处理. 物理函数反射有 y/(pi−y) 因子, 归一化后才严格对称. 平衡候选 c_n 的单调性和极限已给出解析证明; 完整全局极值问题仍开放.').replace('[早期相位文档]','[当前候选谱证明]').replace('极大子的精确 2n 开关结构及平衡世俗函数的 2n 简单根计数已有后续 STRICT 结果; 全局最优值及其余单调性问题仍开放','精确 2n 开关结构保留原审查范围; 本轮重证全部 2n 简单根及平衡候选 c_n 的严格单调与极限. c_n=Lambda_n^sup 尚未证明, 全局 O1/O2 仍开放'))
edit('scripts/README.md',lambda S:prepend_after_title(S,'第九轮当前诊断入口为 [_gapn2_second_variation_probe.py](_gapn2_second_variation_probe.py). 投影用 A_i=∫I_i f 而非块平均; 另外直接积分检查一阶变分, 谱配对在真实密度/方向断点分段. 记录截断、求积和有限差分步长敏感性, 拒绝通过截断负密度制造可行扰动. R=1 保留兼容. 有限样本符号不是 Hessian 定性证明或盒约束全局最优性.\n\n[_gapn2_k_global_rank2.py](_gapn2_k_global_rank2.py) 本轮只修正文档范围: 保留有限的移动界面加速度贡献, 不以 Green 对角发散推导其符号. 其 K 实现及历史 R206 扫描没有因此得到重认证. 原错误程序和失败解释保留在历史证据, 当前替代与复现入口见 [第九轮报告](../reports/proof-audit-round9-20260923/REPORT.md).'))
def map_edit(S):
	S=S.replace('2026-09-22 (round8 scoped INF repairs; older runs retain their original dates)','2026-09-23 (round9 variation and balanced-candidate repairs; older runs retain their original dates)')
	S=S.replace('reflection symmetry STRICT; ratio-extremizer exact-2n-switch structure STRICT (2026-08-22); 2n root count STRICT (2026-08-22); equal-width optimum O2 and global value O1 OPEN','physical reflection has a frequency factor; normalized symmetry and all-n root count repaired in round9. Historical extremizer 2n-switch structure retains its scope; global equality/optimality O1/O2 OPEN')
	S=S.replace('| B4 | Adjacent gap','| B3-CANDIDATE-LIMIT | Prescribed balanced candidate ratios c_n(R), fixed R>1 | SOLVED | docs/SL_fixed_n_supremum.tex; round9 analytic repair | Jacobi principal submatrix argument gives c_n strictly decreasing to ((pi-phi)/phi)^2, phi=arccos((sqrt(R)-1)/(sqrt(R)+1)). Does not identify c_n with the global supremum |\n| B4 | Adjacent gap',1)
	S=S.replace('B3 --uses--> Fixed-n configuration tools','B3 --uses--> Fixed-n configuration tools\nB3 --solved candidate subproblem--> B3-CANDIDATE-LIMIT via nested Jacobi matrices\nB4 --uses--> true-integral projection + normalized derivative + finite Green concentration; G1 remains OPEN')
	S=S.replace('  B4["B4 gap extremals (PARTIAL)"]','  B3C["B3-CANDIDATE-LIMIT (SOLVED): prescribed balanced sequence"]\n  B4["B4 gap extremals (PARTIAL)"]')
	S=S.replace('  B1 -->|informs| B4','  B3 -->|balanced candidate subproblem| B3C\n  B1 -->|informs| B4')
	S+='''
## Round9 research knowledge (2026-09-23)

- Tangency depends on the integral functional A, while the chosen projection metric determines which normal represents it. Unequal block widths expose the lost factors in projection against averages. Zero A means every direction is tangent; it does not license division by zero.
- Spectral perturbation formulas must retain the component fixing the moving weighted normalization. The exact h=rho check gives u'=-u/2 and distinguishes this derivative from a reduced-inverse particular solution.
- In regular one-dimensional Dirichlet problems the Green finite part is bounded. Unit-mass midpoint pulses at rho=1 give lambda1''→6*pi², lambda2''→0 and half-gap Q→−3*pi². This refutes the divergence argument, not every possible finite-kernel/interface route. Actual moving-interface acceleration remains a separate finite contribution.
- Reflection of the physical secular value includes y/(pi-y); multiplying by the nonzero frequency preserves its zeros but changes its value law. An all-n Jacobi compression then turns a former candidate-limit conjecture into a proof, while leaving global optimality separate.
- Possible next idea, unproved: combine the finite regularized-kernel matrix with the correctly signed interface acceleration on the actual tangent space. First test against the constant-density midpoint limit and width-unequal directions; establish analytic concentration/tail control before attempting a sign theorem. A numerical negative direction alone is insufficient for the constrained extremum problem.

Current proofs, correction receipts and version-bound annotations are linked from reports/proof-audit-round9-20260923/REPORT.md. Historical R206 and older B3 runs retain original bytes and dated claims. Canonical Blueprint was not changed.
'''
	return S
edit('research_map.md',map_edit)
edit('docs/PROJECT_UNDERSTANDING.md',lambda S:S.replace('更新于 2026-09-22.','更新于 2026-09-23.',1)+'''
## 第九轮: 约束、归一化与失败路线的再解释 (2026-09-23)

这次四项错误都涉及从一个表示转到另一个表示时遗漏了什么. 分块方向的约束是 b·A=0, A_i=∫I_i f; 使用欧氏或块宽加权内积会改变投影公式, 不会改变约束本身. 独立检验必须再算原始积分, 只检查投影程序自己构造的点积容易循环确认错误.

本征函数的规范也在随密度变化. 方程的约化逆仅给一个特解; 还须补核方向以满足加权归一化导数. h=rho 的精确缩放例使遗漏直接可见. 类似地, 非零频率缩放保留世俗函数零集, 但不保留函数值的反射恒等式. 对象、表示、规范和不变量应在工具卡中分别说明.

旧窄脉冲路线使用了一维 Green 对角发散的错误前提. 当前有限核和常密度中点极限反驳了这条推导; 它没有反驳所有有限核与界面加速度组合的方法. 可重新研究有限矩阵在真实切空间上的符号, 先以不等块宽和常密度反例校准, 再证明所需的集中极限与余项. 这是待检验方向, 不是新的 G1 结论.

固定 n 的候选谱显示了另一种可复用结构: 把相位根变为嵌套 Jacobi 矩阵的最小特征值, 通过主子矩阵、末行递推和显式试探向量证明严格单调与极限. 这证明的是选定平衡配置的 c_n; 全局极大子还必须证明具有该块宽结构. 不能从“候选有完整解析谱”跳到“候选全局最优”.

实际独立检验、纠错传播及数值与局部 Lean 的边界见[第九轮报告](../reports/proof-audit-round9-20260923/REPORT.md). 综合文稿的整文件哈希变化还会使无关数学段落的旧审查失效; 续接必须核对精确依赖及当前检索摘要, 不能只检查卡片数量.
''')
print('Navigation and research understanding updated; final review outcomes remain in progress.')
