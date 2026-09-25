from pathlib import Path
import hashlib,json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
Cards=json.loads((O/'cards.json').read_text())
Renewals=json.loads((O/'renewals.json').read_text())
Cards['gap-band-extremals']=next(X['target'] for X in Renewals if X['target']['location']=='tools/gap-band-extremals.md')
Rows=[
('band-selfconsistency-equivariance','2026-09-25 reflection geometry','几何反射是R(x)=1-Jx, 其微分为-J. 保持方向为(I-J)v/2, 破缺方向为(I+J)v/2. 旧asym赋值只是-Jv; 旧(a,-reverse(a))及反对称坐标网格实际保持几何反射. 当前标签只描述初始点, 不能约束后续求解轨迹. 实际接口转换后再次检验扇区、非零位移和可行性. 精确修订与独立回放见reports/proof-audit-round10-20260925/REPORT.md.'),
('green-half-inertia','2026-09-25 spectral identity before precision','残差小不保证根的谱指标正确. 高反差三块反例中旧首项3.2671480773之前还有四个Dirichlet根. 现先按连续提升相位的n*pi水平定位, 再在同一指标内细化. 双精度及mp相位共享数学方法, 相互符合不是独立枚举证据; 本轮另用物理解零点计数和有限有理端点括区检查. 尚非全参数区间认证.'),
('half-problem-regularized-green','2026-09-25 bounded propagation','共享根引擎的静态导入闭包含76项, 修复影响其下次执行. 本轮只重跑报告列明的程序与配置; 历史Green/Jacobian数值不因共享引擎修好而自动重新认证. 四个默认配置前61根的新旧最大差约5.7e-14, 因此不能笼统断言所有旧R4结果错误. 旧解析det/惯性反例及范围保留.'),
('second-variation-weighted-eigenvalues','2026-09-25 same-index variation','高精度细化、谱截断与有限差分端点必须使用同一指定指标. 排序且为正的根表仍可能跳过低根; checked_roots增加相位指标检验. 本轮有限重算保留真积分切向、固定窄脉冲、61模截断、64点求积与有限步长局限. 局部界面解析公式另有证明; 数值符号不证明G1或整个约束空间上的定性符号.')]
Rows.append(('gap-band-extremals','2026-09-25 historical propagation diagnosis, line46','当前卡第46行关于P*M与M*P的历史故障归因未经核实, 不应作为可复用的故障结论. 已核实的列状态(y,y\')从左到右传播为M_new=P_new*M_old; 若旧实现采用其他约定, 须先找到原实现再判断. 本轮未变卡续审仅批准其列明的解析修正, 明确没有认证这条历史归因. 原卡正文作为版本史保留, 当前检索应连同本版本批注及research/library/reviews/runs/665b4761a3d8b19dd39eaaa343a600d53a0e8893f7a3b0422069da5add70db3a-01a0d77d-c885-7532-ae36-d32f820ee134/report.json中的限制阅读; 本批注不新增数学定理.'))
Notes=[]
for Name,Locator,Text in Rows:
 Card=Cards[Name];Notes.append(L.annotate(R,Card['location'],Card['sha256'],'agent:round10-20260925','correction-experience',Locator,Text))
(O/'annotations.json').write_text(json.dumps(Notes,ensure_ascii=False,indent=2)+'\n')
print('Saved5 exact-version correction annotations, including the uncertified historical diagnosis.',flush=True)
Result=L.make_index(R,ReadmePath='tools/README.md');(O/'index-result.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({K:V for K,V in Result.items() if K!='issues'}),flush=True)
if Result['verdict']!='INDEXED' or Result['indexed']!=89 or Result['blocked']!=1:raise RuntimeError('Unexpected final index state')
