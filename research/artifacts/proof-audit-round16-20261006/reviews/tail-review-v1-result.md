# C16-TAIL 独立审查回执

日期：2026-10-06。审查者：`/root/r16_tail_review`。

**结论：APPROVED_FOR_SCOPED_ANALYTIC_INTEGRATION。** 在有限长度区间的真实 DD 问题、固定有界正密度、实有界线性密度方向及真实加权归一化模态的假设下，T1、T2、T3 正确，与冻结 `q_formula` 的符号及系数一致。给出的常密度余弦例确实使 T3 的左界取等。没有发现需要推翻或改动该有限解析命题的缺口。下面给出独立推导及认证时必需的输入条件；此结论不认证现有浮点谱根、求积或完整 CLI。

## 1. 冻结输入与实际审查范围

清单核对在阅读正文前完成，结束时再次核对三项输入，均未变化：

| 文件 | 字节 | SHA-256 |
| --- | ---: | --- |
| `analytic_notes.md` | 8100 | `c4e3eac6884ed2a387d14a92226e0c8e7b4a52a4a5279646f483af18dc283c31` |
| `variation.py` | 28108 | `82c829770d80743bd65018326f4e8f4a3be3a42209bba76066d0f7e8059f2cf3` |
| `physical.py` | 25078 | `4f418bdca359c64e7ad6298ad01b6b80f0dc46d8484b2155bcf18623bc529713` |

`manifest.json` 的 SHA-256 为 `c510a0dbb68c068ef177d7bd67c10dcb6056f46444a7b97a7a7dc608e72ec24f`。

数学判断使用笔记 111–151 行的 C16-TAIL、线性密度/DD/单位区间的所需定义、`variation.py` 的 Q 定义与 `q_formula`（246–269 行），以及 `physical.py` 的频率约定和 `eigenfunction_states`/`eigfun` 归一化（155–192 行）。为判断 `Cu` 的意义读取了 `SpectralProbe.pairings`（232–243 行）。首次按行打印短笔记时工具实际返回整份笔记，相关 `rg` 检索也返回了一些旁支片段；这些额外文本没有被作为其它发现、执行结果或本次尾界结论的验收依据，不能称未曾看到。未读项目 AGENTS、记忆或既往审查回执，未导入项目模块，未改实际源码或笔记。独立检查使用外部目录及自写工具；这不是 OS 沙箱。

## 2. 模型、完整性与二阶公式

令区间为 `(0,L)`，`L>0`，`rho,h` 为实可测函数，

\[
0<m\le\rho(x)\le M<\infty,\qquad h\in L^\infty(0,L).
\]

采用 DD 问题

\[
-u_k''=\lambda_k\rho u_k,\qquad u_k(0)=u_k(L)=0,
\qquad\int_0^L\rho u_k^2=1.
\]

模态可以且在本回执中确实选为实数。特征值按真实完整谱编号为 `0<lambda_1<lambda_2<...`；它们不是频率。冻结代码以 `s` 为频率，`lambda=s**2`，与此定义相符。

加权空间 `H_rho=L²((0,L),rho dx)` 的 DD 解算子可以写成

\[
(Tf)(x)=\int_0^L G_D(x,y)\rho(y)f(y)\,dy.
\]

其中 `G_D` 是 `-d²/dx²` 的 DD Green 核。由于加权与非加权 L² 范数等价，T 是紧算子；核的对称性及能量恒等式给出其自伴正性。T 的核为零：`Tf=0` 会推出 `rho f=0`。紧自伴谱分解因此给出真实模态在 H_rho 中的完备正交基。DD 简单性来自有界系数 ODE 的初值唯一性：一个满足左 DD 条件的解由左端导数决定，特征空间至多一维。这是后续 Parseval 及分母严格正性的理由。

对线性路径 `rho_t=rho+t h`，取足够小的实 `t` 使密度仍为正。二阶微分也可直接由射击函数获得：左解 `v(0)=0,v'(0)=1` 满足

\[
v(x)=x-\lambda\int_0^x(x-y)(\rho(y)+t h(y))v(y)\,dy.
\]

有界系数的 Volterra 迭代给出其关于 `(lambda,t)` 的局部解析性。在 DD 根处，Lagrange 恒等式给出

\[
v'(L)\,\partial_\lambda v(L)=\int_0^L\rho v^2>0.
\]

因此射击根可解析续接，加权质量的正平方根也可解析归一化。这一步无需假设驻点、ND 或 G1。

记

\[
c_{kl}=\int_0^L h u_k u_l,\qquad \dot u_k=\left.\partial_tu_k(t)\right|_{t=0}.
\]

在变动密度质量归一化下，微分特征方程及质量条件分别给出

\[
\lambda_k'=-\lambda_k c_{kk},\qquad
\langle\dot u_k,u_l\rangle_\rho
=\frac{\lambda_k c_{kl}}{\lambda_l-\lambda_k}\quad(l\ne k),
\qquad
\langle\dot u_k,u_k\rangle_\rho=-\frac{c_{kk}}2.
\]

再微分第一式，得到

\[
\frac{\lambda_k''}2
=\lambda_k c_{kk}^{\,2}
-\lambda_k^2\sum_{l\ne k}\frac{c_{kl}^{\,2}}{\lambda_l-\lambda_k}.
\tag{R1}
\]

这里配对必须是无额外 rho 权的 `int h u_k u_l`。配对泛函在 H_rho 上有界，下面的 Parseval 控制也保证级数绝对收敛：低于 k 的项仅有限个，高于 k 的分母至少为 `lambda_(k+1)-lambda_k>0`。

令 `a=lambda_n,b=lambda_(n+1)`，`D_n=b-a`，则

\[
Q=\frac{D_n''}2
=b c_{n+1,n+1}^{\,2}-a c_{nn}^{\,2}
+a^2\sum_{l\ne n}\frac{c_{nl}^{\,2}}{\lambda_l-a}
-b^2\sum_{l\ne n+1}\frac{c_{n+1,l}^{\,2}}{\lambda_l-b}.
\tag{R2}
\]

冻结 `q_formula` 对 Python 下标 `k=n` 使用 `Sign=+1`，对 `k=n-1` 使用 `Sign=-1`，每项为 `Sign*(lambda[k]*Diagonal[k]**2-lambda[k]**2*sum(...))`；正好对应 R2。`Cw` 只做历史兼容输入而不进入该公式。此核对要求 `dr_sq[k]` 确实等于 `Cu[k,k]=c_(k+1,k+1)`；任意不相容矩阵/独立对角参数不能借本命题获得物理意义。

## 3. Parseval 残余及两侧尾界

在 H_rho 中取

\[
g_k=(h/\rho)u_k.
\]

它属于 H_rho，且

\[
\langle g_k,u_l\rangle_\rho=c_{kl},\qquad
\|g_k\|_\rho^2
=J_k:=\int_0^L\frac{h^2}{\rho}u_k^2.
\]

故真实完备模态的 Parseval 恒等式为

\[
J_k=\sum_{l\ge1}|c_{kl}|^2,
\qquad
E_{k,N}:=J_k-\sum_{l=1}^N|c_{kl}|^2
=\sum_{l>N}|c_{kl}|^2\ge0.
\tag{R3}
\]

这证明 T1。若 `N>=k`，则所有遗漏模态均满足

\[
0<\lambda_{N+1}-\lambda_k\le\lambda_l-\lambda_k\quad(l>N).
\]

逐项比较及求和给出

\[
0\le T_{k,N}:=\sum_{l>N}\frac{|c_{kl}|^2}{\lambda_l-\lambda_k}
\le\frac{E_{k,N}}{\lambda_{N+1}-\lambda_k}.
\tag{R4}
\]

这证明 T2。以真实配对和真实特征值构造前 N 项 `Q_N`，且 `N>=n+1`，R2 的差正好是

\[
Q-Q_N=a^2T_{n,N}-b^2T_{n+1,N}.
\]

两个 T 都非负，所以

\[
-\frac{b^2E_{n+1,N}}{\lambda_{N+1}-b}
\le Q-Q_N\le
\frac{a^2E_{n,N}}{\lambda_{N+1}-a}.
\tag{R5}
\]

没有漏掉额外的 2、rho 权或对角项。这证明 T3；有限求积误差不是 R5 中的谱尾。

另有

\[
0\le E_{k,N}\le J_k
=\int\rho|(h/\rho)u_k|^2
\le\|h/\rho\|_\infty^2\int\rho u_k^2
=\|h/\rho\|_\infty^2.
\tag{R6}
\]

Rayleigh 商及 min–max 比较给出

\[
\lambda_j(\rho)\ge\frac1M\lambda_j(1)
=\frac{j^2\pi^2}{M L^2}.
\tag{R7}
\]

因此可令 `B=(N+1)²pi²/(M L²)` 替代 R5 分母中的 `lambda_(N+1)`，但必须先满足 `B>b`，而区间实现必须满足 `B_lower>b_upper`。比较下界不超过 b 时，不能用该粗分母；真实谱排序仍保证原分母为正，二者不能混淆。

## 4. 左界精确取等

单位区间上取

\[
\rho=2,\quad h=2\cos(\pi x),\quad
u_k=\sin(k\pi x),\quad\lambda_k=k^2\pi^2/2.
\]

`int rho u_k²=1`。对 `k>=2`，三角恒等式及正交性给出

\[
c_{kl}=\frac12(\delta_{l,k-1}+\delta_{l,k+1}),\qquad J_k=\frac12.
\]

令 `n>=2,N=n+1`。第 n 行的两个非零配对都被保留，所以 `E_(n,N)=0`。第 n+1 行仅遗漏 `l=n+2`，其平方为 1/4，所以

\[
E_{n+1,N}=\frac14,\qquad
T_{n+1,N}=\frac{1}{4(\lambda_{n+2}-b)}.
\]

于是

\[
Q-Q_N
=-\frac{b^2}{4(\lambda_{n+2}-b)}
=-\frac{\pi^2(n+1)^4}{8(2n+3)},
\]

正好等于 R5 的左端；同时其右端为零。这是解析取等，独立样例不是靠有限浮点接近零推断取等。

## 5. 可靠区间如何用于符号认证

本解析命题没有使冻结浮点程序自动成为证书。有限配对、J、特征值及 Q_N 的包络必须确实绑定到同一真实 DD 模态和质量归一化；还须认证谱指标，有限和中每个非对角分母不得跨零。`physical.py` 的质量公式在模型层面是 `int rho v²`：中点的 `v` 系数乘余弦平方积分，`v'` 系数乘 `sin²/omega²` 积分，然后同时除以 `sqrt(Mass)`。其数值实现使用 binary64 和小相位有限 Taylor 展开，不提供外向舍入/截断余量，因此本回执只核对其归一化约定，没有认证其质量数值或正交性。

例如，若有可靠实区间 `c_kl in I_kl` 及 `J_k<=J_k^U`，可用外向舍入得到

\[
E_{k,N}\le E_{k,N}^U
:=J_k^U-\sum_{l\le N}\min_{z\in I_{kl}}z^2.
\]

区间跨零时平方下界为零。若此可靠上界为负，与 R3 冲突，必须拒绝/修复输入包络。单个负浮点残差 `J_hat-sum c_hat²` 不能擅自截为零。已经建立真实非负性的可靠区间与 `[0,infinity)` 取交是另一件事，不能替代对误差的控制。

若可靠包络满足

\[
Q_N\in[q_-,q_+],\quad a\le a_U,\quad b\le b_U,\quad
E_{n,N}\le e_a,\quad E_{n+1,N}\le e_b,\quad
\lambda_{N+1}\ge B>b_U,
\]

其中 `e_a,e_b>=0`，则安全的最终包络为

\[
Q\in\left[
q_- -\frac{b_U^2e_b}{B-b_U},\quad
q_+ +\frac{a_U^2e_a}{B-a_U}
\right].
\]

仅当该完整区间严格位于零的一侧才据此认证严格符号。求积、模态/谱根近似、舍入和有限谱尾应分别控制，不能把 Q_N 的有限积分误差塞给 E 或声称多保留模式会自动消除求积误差。

对于 delta、delta' 接口方向，`(h/rho)u_k` 不是本命题中的 L² 乘法向量，R3 不能直接套用。固定宽度且有界的脉冲可用本命题，但随宽度趋零其 L∞/J 预算一般不一致有界。以上也不证明 ND、G1、驻点非退化、一般接口 Hessian 定号或完整 CLI 可认证。

## 6. 实际自检、输出及未执行项

自检文件位于冻结目录之外：

- `F:/tools/math-audit-round16-20261006/tail-review-v1-selfcheck-01.py`
- `F:/tools/math-audit-round16-20261006/tail-review-v1-selfcheck-01.json`

实际命令：

```powershell
py -3.10 -X utf8 -B 'F:\tools\math-audit-round16-20261006\tail-review-v1-selfcheck-01.py'
```

解释器实际为 `C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe`，NumPy 版本 `2.2.6`。脚本仅提取执行冻结 `q_formula` AST，提供用于这些正常实输入的独立简单验证辅助函数；没有执行原模块或检验原辅助验证器。数学参考值使用有理数表示 Q/pi²，直接余弦乘积积分计算 J，独立配对选择规则计算有限支撑系数。

实际结果 **PASS，41 个样例**：11 个 `n=2,...,12,N=n+1` 左界取等例；24 个常密度缩放方向 `h=2` 的零尾例；6 个多频余弦方向的双侧界例。41 次提取出的真实 Q 主体与独立精确参考的浮点值比较均通过，容差为 `rel_tol=3e-13,abs_tol=3e-12`。另对每例取 `M=2,4,100`，51 个满足正粗分母的比较实际通过，72 个不满足条件的比较明确记为不可用。一般 R3–R7 的证明在上文，不由这 41 个例子代替。

脚本 SHA-256：`4a4fdfda2e3ebf76410ac99fafb9a3c974e91b2e0d76ec88ff364c45ca34b2cb`。

自检 JSON SHA-256：`c5984611c912915b6fef27dd5de75c3f1d6dc6840a53a4d77e71e140f0647c6f`。

提取的 `q_formula` 源片段 SHA-256：`c4484b16f007f893cab64db967a2ba813be5dd2f4d2349d28ce8d083f4c516e9`。

一次辅助 PowerShell JSON 读取因 `n`/`N` 键的大小写折叠而失败；改为 `ConvertFrom-Json -AsHashtable` 后实际读回 PASS/41。未改变自检文件或结果来规避该读取问题。

未执行：Lean、完整原 CLI、物理采样器/谱根求解的运行验收、可靠区间包络生成、任意密度方向的穷举验证。未修改冻结输入或实际项目文件。回执按要求只创建一次。
