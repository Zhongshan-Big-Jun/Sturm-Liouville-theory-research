from pathlib import Path
import json
import sys

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = 'research/artifacts/proof-audit-round12-20260926'
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as Library

Baseline = json.loads((Out / 'baseline.json').read_text())
Done = json.loads((Out / 'cards.json').read_text()) if (Out / 'cards.json').exists() else {}
Coordinator = '01a06f46-dd03-7c83-9267-32048412c359'
AnalyticAuthor = '01a0dce3-b8a0-7d83-b359-03a8073d76d4'
Common = r'''## 第十二轮: 半谱身份、去极点与扇区对象

半区间的旧独立 mu 网格会漏掉成对低模态, 且请求 N 与 2N 时前缀会变.
旧求和只删除数组下标, 因而可能保留真正极点. 两个错误已用原完整源码复现.
当前 DD/DN 共用提升相位引擎, 第 j 阶目标分别为 j*pi、(j-1/2)*pi.
正坐标缩放保持这两类轴向目标. 共享谱表绑定几何、边界类型和一基模态序号;
去极点核对目标值, 截断覆盖和其余分母, 失配或不可分辨时拒绝计算.
这些是浮点诊断守卫, 不是区间证书; Richardson 也不认证尾项误差.

在 2n 维镜像基 Be/Bo 中, S=diag(1,-1,...,-1), E=S 的左半对角块.
对任意 K 均有 Bo^T SKS Bo=E Ke E、Be^T SKS Be=E Ko E.
压缩恒等式不需要 K 与反转 P 对易; 作为不变子空间分块则需要该条件.
因此交叉奇偶 Green 式代表 Kp=SKS 的奇块, 对应原 K 的偶块 Ke.
原 Ko 必须使用自身极点处的约化核及存留的秩一项.

直接传播还涉及 sector_data: 旧输出把 Kp 两块标为 raw Ke/Ko.
当前返回 Ke/Ko 及 He/Ho/Ee/Eo 均按原 K 命名, 另有显式 Kp* 字段;
历史 c_e/c_o 系数属于 KpEe/KpEo. 旧扫描文件不改写, 其单个扇区标签和
支配解释不能直接复用. 本轮 n=2 Green 恒等式有独立推导, n=2/3 R=4
程序对照是有限数值证据, 不关闭全参数符号、G1'、唯一性或历史全部路线.

精确条件与推导见[第十二轮解析修订](../research/artifacts/proof-audit-round12-20260926/analytic-repair.md),
执行与隔离检验范围见[本轮报告](../reports/proof-audit-round12-20260926/REPORT.md).
可复用性以本卡当前字节的原版纠错回执和实际查询为准.

'''
GreenSection = r'''### 交叉 Green 判据的正确对象 (第十二轮修订)

令 $K_p=SKS$, $E=\operatorname{diag}(1,-1,\ldots)$ 为左半符号矩阵.
旧段将交叉奇偶 Green 式标为原 $K_o$, 此标识撤回. 本轮精确重推的范围是
$n=2$, 固定有限 $R>1$, 对称五层带自洽点, 全区间特征函数以
$\int_0^1\rho u_k^2=1$ 归一化并取 $u_k'(0)>0$.
写 $a=\lambda_2$, $b=\lambda_3$, $U=\operatorname{diag}(u_2(x_1),u_2(x_2))$,
$q=(u_2(x_1)^2,u_2(x_2)^2)^T$, $E=\operatorname{diag}(1,-1)$,
$d_j=f'(x_j)/(b s_j)$, $s_j=\rho(x_j+)-\rho(x_j-)$.

半区间单位归一化使 $R_2^\perp=G_N(a)/2$, $R_3^\perp=G_D(b)/2$.
正确的交叉式为
\[
 (K_p)_o=E K_e E
 =\operatorname{diag}(d)+2aU\left[E G_D(b)E-\frac abG_N(a)\right]U.
\]
也可写作 $\operatorname{diag}(d)+(4a/b)UMU$, 其中
$M=bE R_3^\perp E-a R_2^\perp$. 这是原 $K_e$ 的定性判据.
当 $u_2(x_j)\ne0$ 时, 可逆对角合同给出其定性等价于
$\operatorname{diag}(d/u_2^2)+(4a/b)M$ 的定性. 它不能代替原 $K_o$.

原奇块为
\[
 K_o=\operatorname{diag}(d)+\frac{4a(b-a)}{b^2}(Eq)(Eq)^T
 +2aU\left[\widetilde G_N(b)-\frac abE\widetilde G_D(a)E\right]U.
\]
其中两项约化核均在自身极点去除正确模态, 分母约定为特征值减谱参数.
其秩一项不能因 $q$ 镜像偶而删去: 原完整 $K$ 的秩一向量是 $Sq$, 镜像奇.
交叉式对应的 $K_p$ 才有镜像偶秩一向量.

本轮没有把前节有限点核惯性等式升级为定理, 也不由 n=2/3 的有限数值
观测建立一般 n 或全 R 的定性. 原 M 与同名 Ko 的历史数值比较需要按
上述对象重新解释. 控制另一原始镜像扇区仍是完整定性路线的义务.

'''
BandSection = r'''### 镜像扇区分解 (第十二轮纠正对象)

取 $K_p=SKS$, $E=\operatorname{diag}(\varepsilon[:n])$.
原程序的两个 Sigma 核组合及秩一项应记为
$H^p_e,H^p_o,E^p_e,E^p_o$, 它们合成 $K_p$ 的偶/奇块:

\[
 (K_p)_e=\operatorname{diag}(d_h)+E^p_e+H^p_e,\qquad
 (K_p)_o=\operatorname{diag}(d_h)+E^p_o+H^p_o.
\]
旧系数 $c_e=4D/(\lambda_n\lambda_{n+1}^2)$ 和
$c_o=-4(\lambda_n^2+\lambda_{n+1}^2)/(\lambda_n\lambda_{n+1}^2D)$
对应 $E^p_e=c_e w_hw_h^T$、$E^p_o=c_o(Ew_h)(Ew_h)^T$.
原 $K$ 的块由交换与合同得到
\[
 K_e=E(K_p)_oE,\qquad K_o=E(K_p)_eE.
\]
因此原 $H_e=EH^p_oE$, $E_e=EE^p_oE$, $H_o=EH^p_eE$, $E_o=EE^p_eE$.
当前 `sector_data` 返回的无前缀字段遵守原 K 约定; `Kp*` 字段保留
共轭对象, `c_e/c_o` 的对象在返回元数据中明确标注. 不能把旧输出字段
的名称当作实际矩阵身份的证明.

这条扇区交换是任意有限 n 的矩阵恒等式. n=2 Green 系数从归一化形状
导数重推; 当前 n=2/3 R=4 谱截断与完整 Jacobian 对照是程序检验,
不重新认证所有历史 Sigma 核推导、扫描参数或全 n 的定性.
在对称点 K 与反转对易时, K 与 $K_e\oplus K_o$ 正交相似.
SUP 两块正定或 INF 两块负定仍是 G1' 的更强充分条件;
bare G1' 要求的是 $\det K_e\det K_o>0$.

'''

for Name in ['band-selfconsistency-equivariance','green-half-inertia','half-problem-regularized-green']:
	Location = 'tools/' + Name + '.md'
	if Name in Done:
		if Library.digest((Root / Location).read_bytes()) != Done[Name]['sha256']:
			raise RuntimeError('Saved card drift')
		continue
	Front, Body, _ = Library.read_metadata((Root / Location).read_bytes())
	Data = json.loads(json.dumps(Front, default=str))
	if Name == 'green-half-inertia':
		Start = Body.index('### 奇扇区定性判据')
		End = Body.index('在完整 $2n$ 接口坐标下', Start)
		Body = Body[:Start] + GreenSection + Body[End:]
		Body = Body.replace('# 半问题 Green 惯性 (K_o 的 Green 函数化归)', '# 半问题 Green 与原 K / 共轭 Kp 的镜像扇区')
	elif Name == 'band-selfconsistency-equivariance':
		Start = Body.index('### 镜像扇区分解')
		End = Body.index('### 证伪', Start)
		Body = Body[:Start] + BandSection + Body[End:]
		Start = Body.index('- Sherman–Morrison 定性判据:')
		End = Body.index('- 扇区 Sylvester 主元:', Start)
		Body = Body[:Start] + r'''- Sherman--Morrison 判据的正确对象: 若 $(K_p)_o=A^p_o-|c_o|(Ew_h)(Ew_h)^T$,
  则 $(K_p)_o\succ0$ 当且仅当 $A^p_o=\operatorname{diag}(d)+H^p_o\succ0$
  且 $|c_o|(Ew_h)^T(A^p_o)^{-1}(Ew_h)<1$.
  它与原 $K_e$ 的正定性等价, 不是原 $K_o$ 的判据. 将其用于其它块或 INF
  必须重新核对符号. 这一有限维判据仍不能无条件取代 bare G1'.
''' + Body[End:]
		Body = Body.replace('R 阶梯续延 (根残差 <1e-8), 闭式 K, N=121 模:', '以下为未重跑的历史 N=121 阶梯扫描. 原文件以 Ke/Ko 命名的量实际采用 Kp 的扇区约定; 单个扇区及 H/E 标签必须交换合同后才对应原 K. 整体定性观测的范围仍限这些数值样本:')
		Body = Body.replace('充分不等式 λmin(H_o − E_o) + min d > 0 与 λmin(H_e + E_e) + min d > 0 每点成立', '旧记录声称 λmin(H_o − E_o) + min d > 0 与 λmin(H_e + E_e) + min d > 0 每点成立. 前者不是所写加法分解的充分条件, 该充分性解释撤回; 以下历史余量不认证正确判据')
		Body = Body.replace('历史待证路线 (SUP): λmin(H_o − E_o) > −min d (其与 K_o 的符号对应也未在本轮认证);', '旧 SUP 减号支配式已撤回为一般充分判据. 对 KpOdd 的有效 Weyl 充分式应使用 H^p_o+E^p_o, 或使用上述负秩一等价条件;')
	else:
		Start = Body.index('对称带自洽点处, $\\varepsilon_j')
		End = Body.index('### K 的两个镜扇区', Start)
		Body = Body[:Start] + r'''采用一基指标 $1\le j\le n$, 镜像配对 $j\leftrightarrow2n+1-j$,
$B_e^{(j)}=(e_j+e_{2n+1-j})/\sqrt2$, $B_o^{(j)}=(e_j-e_{2n+1-j})/\sqrt2$.
记 $S=\operatorname{diag}((-1)^{j+1})_{j=1}^{2n}$, $E=S[:n,:n]$.
则 $SB_o=B_eE$, $SB_e=B_oE$, 对任意 K 有
\[
 B_o^TSKSB_o=E(B_e^TKB_e)E,\qquad B_e^TSKSB_e=E(B_o^TKB_o)E.
\]
当前 `sector_data['Ko']` 已修为原 $B_o^TKB_o$; 第十二轮前同名返回值实际上是
Kp 的奇块. 旧文档的接口描述与旧代码不符, 此处明确撤回该实现描述.
下文 $\operatorname{diag}(\beta)$ 统一取 E, 不混用零基和一基符号.

''' + Body[End:]
		Body = Body.replace('### K 的两个镜扇区历史半问题闭式 (显式索引为 n=2, 原标记 STRICT)', '### n=2 原 K 的两个镜像扇区 (第十二轮重推, 条件见新解析稿)')
		Body = Body.replace('$n$ 偶 ($\\lambda_n=\\mu_{n/2}^D$ 奇全模, $\\lambda_{n+1}=\\mu_{n/2+1}^N$ 偶全模),', '$n=2$, $\\lambda_2=\\mu_1^D$ 为奇全模, $\\lambda_3=\\mu_2^N$ 为偶全模,')
	Data.update(content=Common+Body, updated='2026-09-26', author_ids=sorted(set(Data.get('author_ids', []) + [Coordinator, AnalyticAuthor])), sources=Data.get('sources', []) + [dict(path=Artifact+'/analytic-repair.md', locator='Sections 1-6: exact parity compression, indexed DD/DN phases, normalized n2 Green identities and explicit scope')], status='第十二轮半谱身份与扇区对象修订; 可复用性以精确版本独立纠错回执为准', evidence_status='ROUND12_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT', scope='Current round12 statements and retained earlier scoped repairs. n2 normalized Green and general finite matrix/phase identities; no all-R signs, historical full scans or complete formalization.', summary=Data.get('summary','')+' 第十二轮: DD/DN相位按序号定位, 去极点绑定同一谱表; 交叉Green式为Kp奇块=E Ke E, 原Ko需自身约化核及秩一项. sector_data和负秩一判据原扇区标签已修正, 数值守卫不等于区间认证.')
	Done[Name] = Library.save_card(Root, Data, Location, Baseline['tracked'][Location])
	(Out/'cards.json').write_text(json.dumps(Done, ensure_ascii=False, indent=2)+'\n')
	print('Saved', Name, Done[Name]['sha256'], flush=True)
