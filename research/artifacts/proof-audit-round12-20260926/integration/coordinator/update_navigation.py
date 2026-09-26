from pathlib import Path
Root = Path('/mnt/f/LaTeX/BVE research')

def prepend(Name, Text):
	Path = Root / Name
	Raw = Path.read_bytes()
	At = Raw.index(b'\n') + 1
	Path.write_bytes(Raw[:At] + ('\n' + Text.strip() + '\n').encode() + Raw[At:])

def replace(Name, Old, New):
	Path = Root / Name
	Raw = Path.read_bytes()
	if Old.encode() not in Raw:
		raise RuntimeError('Missing anchor ' + Name)
	Path.write_bytes(Raw.replace(Old.encode(), New.encode(), 1))

prepend('README.md', '2026-09-26 第十二轮修订进行中: DD/DN 半谱改为按相位序号定位, 去极点求和绑定共享谱表; 修正原 K 与 SKS 的扇区对象及三个工具卡中的传播. 独立检验与工具放行状态见[本轮报告](reports/proof-audit-round12-20260926/REPORT.md). 第十一轮余有限分类保留原验收范围, 全局 G1\' 仍开放.')
prepend('README_EN.md', '2026-09-26 round12 repair in progress: DD/DN half spectra now use phase indices and pole sums bind a shared spectrum table. Raw K sectors are distinguished from those of S K S, including propagated program/card labels. See the [report](reports/proof-audit-round12-20260926/REPORT.md) for current independent-review and library-release status. Round11 cofinite results retain their scope; global G1 remains open.')
prepend('docs/research-guide.md', '第十二轮当前入口: [半谱身份、去极点与扇区修订](../reports/proof-audit-round12-20260926/REPORT.md). 正在进行独立检验. 区分原 K 的偶/奇块和交错共轭后的块, 以及解析 Green 恒等式、谱截断数值和局部 Lean 各自的范围.')
prepend('scripts/README.md', '''第十二轮程序接口: [_sl_prufer.py](_sl_prufer.py) 的 `indexed_roots` 新增仅关键字参数 `RightBoundary='D'` (默认不变), 可选 N 对应左 D/右 N 的半整数相位. [_gapn2_half_problem_probe.py](_gapn2_half_problem_probe.py) 的 `half_spectrum(..., return_table=True)` 返回只读数值谱表; 原默认仍返回 ndarray. `mumax` 若不足容纳所需 N 阶会报错. `_spectral_green` 保留零基 `pole_idx` 调用兼容, 内部按一基模态核验目标、几何、边界和分母; N/2N 主调用共用同表.

[_gapn2_sector_decomposition.py](_gapn2_sector_decomposition.py) 的 `Ke/Ko/He/Ho/Ee/Eo` 已统一为原 K 的块, 显式 `Kp*` 键提供 SKS 的块, `c_e/c_o` 仍属于 Kp 的秩一分解并在元数据标明. [_gapn2_green_inertia_probe.py](_gapn2_green_inertia_probe.py) 的交叉 Green 比较目标为 `KpOdd=E Ke E`. 六份活动程序修改与两份历史 debug 调用的静态范围见[报告](../reports/proof-audit-round12-20260926/REPORT.md); 不据这些检查重认证所有旧扫描或全 R 定性.''')
prepend('literature/maps/FRONTIER.md', '2026-09-26 round12: 半问题谱身份与原 K / SKS 的扇区对象正在修订及隔离检验. 新的研究入口是固定有限 R、n=2 对称带自洽点的归一化 Green 推导; 原 Ko 需要自身约化核与存留秩一项, 交叉核式对应原 Ke. 这些工具不自动关闭全局定性问题. 见[修订报告](../../reports/proof-audit-round12-20260926/REPORT.md).')
replace('docs/PROJECT_UNDERSTANDING.md', '## 第十一轮:', '''## 第十二轮: 计算对象的身份也是数学假设

低残差、递增根列和有限值都不能独自保证谱指标正确. 本轮半区间反例中, 同一段 mu 网格容纳两个根却没有端点变号; 增加所求根数又改变网格, 导致前缀变化. 当去极点继续使用旧数组下标时, 真正极点可能留下. 可复用的方法是先用结构确定每阶身份, 再把几何、边界条件、指标和目标值作为同一谱表的联合身份传递. 浮点守卫能拒绝部分不可信计算, 仍不能代替区间误差证明.

交错符号矩阵 S 与镜像反转 P 反对易, 所以共轭 SKS 交换了原 K 的两个镜像扇区. 总体惯性保持不意味着同名扇区保持. 实际源码曾把共轭块标为原块, 与文档的正确约定并存. 本轮把可复用关系写成 Bo^T SKS Bo=E Ke E, 同时用物理接口 Jacobian 的投影比较真实返回对象. 原 Ko 的 Green 表达式有存留的秩一项; 不能套用 Kp 奇块中的抵消.

由此得到的研究方向 (未证): 按正确对象分别估计交叉核对应的原 Ke 与自身约化核对应的原 Ko; 两条估计需不同的极点和秩一结构. 将二者混成一个“奇扇区判据”会遗漏义务. 固定 R 的恒等式不能自动给出整个分支的符号、存在或唯一性. 当前修订与独立验收状态见[第十二轮报告](../reports/proof-audit-round12-20260926/REPORT.md).

## 第十一轮:''')
replace('research_map.md', 'Last updated: 2026-09-26 (round11 cofinite closure analytically reviewed; cross-block/endpoint numerical repair independently checked)', 'Last updated: 2026-09-26 (round12 half-spectrum/pole/sector repair under independent review; round11 results retain their scope)')
replace('research_map.md', '\n## Dependency map', '\n## Dependency map') if '\n## Dependency map' in (Root/'research_map.md').read_text() else None
Path = Root / 'research_map.md'
Raw = Path.read_bytes()
Line = next(Line for Line in Raw.splitlines(keepends=True) if Line.startswith(b'| B9 |'))
New = '| B10 | Half-spectrum identity, bound poles and raw/conjugated sectors | UNDER REVIEW | reports/proof-audit-round12-20260926/REPORT.md; tools/green-half-inertia; tools/half-problem-regularized-green | DD/DN phase targets label each mode; shared tables bind pole deletion. KpOdd=E Ke E, while raw Ko has reduced own-pole kernels and a rank-one term. Finite diagnostics and local algebra do not certify full ODE execution, global signs or G1 |\n'
Path.write_bytes(Raw.replace(Line, Line + New.encode(), 1))
replace('research_map.md', 'B9 cross-block parity and actual edge differences --repairs numerical derivative tools for--> B7/B4; commuting Hessian parity remains distinct', 'B9 cross-block parity and actual edge differences --repairs numerical derivative tools for--> B7/B4; commuting Hessian parity remains distinct\nB10 indexed half spectra and sector object identity --repairs Green diagnostics for--> B7/B4; all-R signs remain open')
replace('research_map.md', '  B9["B9 cross blocks / actual differences (NUMERICAL)"]', '  B9["B9 cross blocks / actual differences (NUMERICAL)"]\n  B10["B10 indexed half spectra / bound poles / raw sectors (UNDER REVIEW)"]')
replace('research_map.md', '  B9 -->|derivative diagnostics| B7', '  B9 -->|derivative diagnostics| B7\n  B10 -->|Green diagnostics| B7')
print('Current navigation updated with pending review status')
