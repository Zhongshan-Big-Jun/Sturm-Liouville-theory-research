---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0bfab-5af3-7352-a134-deabd755066c"], "created": "2026-08-05", "evidence_status": "ANALYTIC_PROOF_SCOPED", "scope": "Specified even and odd P,Q,R only; c>0; finite/normalized terminal conventions and eventual nonzero ratio domains are explicit.", "source": "自研 (会话 11, 方向 4), 路线 A 副产品系统化", "sources": [{"locator": "Fourth-round exact-coefficient recurrence, all-index proofs and scope", "path": "docs/SL_third_order_recurrence_theory.tex", "sha256": "71f45bf0a48eb3b6b2007597e1209f7757b45bcbdccb770eaf39d5407887633e"}, {"locator": "Existing frozen all-degree root-1 proof", "path": "runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse/candidate_proof.md", "sha256": "37a2a5009d097fab438153089ce2284bd9f341a623a5a16a0edea2aafae7f703"}], "status": "第四轮解析修订; 精确适用范围与复用状态见纠错记录", "tags": ["mathtool", "self-developed", "recurrence", "poincare-perron", "minimal-solution"], "title": "固定系数三阶递推: 差分分解、最小解与有理比值", "tool_id": "third-order-recurrence"}
---
# 固定系数三阶递推: 差分分解、最小解与有理比值

本卡只讨论下列明确的两组系数, c>0, epsilon=0 或1分别表示偶、奇侧. 不将其结论推广为任意 Poincare 型或变系数三阶递推的定理. 第四轮修订的独立验收及当前可复用状态由纠错记录决定.

## 精确变换

对 j>=3,

```text
c^2 mu_j = P_j mu_(j-1) - Q_j mu_(j-2) + R_j mu_(j-3),
P_j = 4cj(2j+2epsilon-1) + c^2 j/(j-1),
Q_j = 4j(j-1)(2j+2epsilon-1)(2j+2epsilon-3) + 4cj(2j+2epsilon-3),
R_j = 4j(j-2)(2j+2epsilon-3)(2j+2epsilon-5).
```

令 v_j=c^j mu_j/(2j+epsilon)!, theta_j=c/[2(j-1)(2j+2epsilon-1)]. 精确得到

```text
v_j=(2+theta_j)v_(j-1)-(1+2theta_j)v_(j-2)+theta_j v_(j-3),
d_j=v_j-2v_(j-1)+v_(j-2),   d_j=theta_j d_(j-1),
a_j=j c^j/(2j+epsilon)!,    d_j=C a_j (j>=2).
```

因此两个显式阶乘解对应仿射 v. 偶侧 mu+=(2j+1)!/c^j、mu-=(2j)!/c^j; 奇侧 mu+=(2j+3)!/[6(j+1)c^j]、mu-=(2j+1)!/c^j. 它们从j=0定义并在j>=3满足递推. 前三个初值自由, 不擅自加入j=2方程.

## 正项尾级数给出最小解和归一化

定义绝对收敛的正项尾和

```text
Phi_j=sum_(r=j+2..infinity) (r-j-1) r c^r/(2r+epsilon)!.
```

全部解为 v_j=A+Bj+C Phi_j. Phi_j->0, 因而衰减的v支是一维; 与任一不成比例的其它解之比趋零. 归一化mu0=z0=1的唯一最小解为

```text
mu_j^*=(2j+epsilon)!/c^j * Phi_j/Phi_0,
z_j^*=mu_j^*/[(j!)^2(4/c)^j].
```

终端 mu_N!=0、mu_(N+1)=mu_(N+2)=0 的有限向后解, 先除以其mu0再取固定j极限. 将Phi上限改为N+2就得到有限归一化公式. Phi_0^(N)>0保证除法有定义. 这项终端约定与旧K1卡的另一约定不同; 二者的归一化固定指标极限相同, 不混用未归一化公式.

首尾项比估计给出 j^3 mu_j^*->K_epsilon(c), 即

```text
z_j^* ~ K_epsilon(c) (c/4)^j j^(-3)/(j!)^2,
K_even(c)=c^2/[4(c cosh(sqrt(c))-sqrt(c) sinh(sqrt(c)))],
K_odd(c)=c^(5/2)/[4((c+3)sinh(sqrt(c))-3sqrt(c)cosh(sqrt(c)))].
```

两分母由严格正的Phi_0级数保证非零. K_even(1)=e/4; c下降到0时两侧分别趋于3/4和15/4. 一般c的闭式仅属于本卡明确的系数和归一化, 不覆盖其它三阶族. 高阶形式渐近展开的余项需另证.

## 有理相邻比值及参数表示

对最终非零的解, 相邻比值是有理函数当且仅当 C=0. 因而所有有理比值为

```text
e_j=(1+(2epsilon-1)/(2j)) * (A+Bj)/(A+B(j-1)), (A,B)!=(0,0).
```

证明将C!=0的假设化为一个有理R满足

```text
R(j)-2D_j R(j-1)+D_j D_(j-1) R(j-2)=1,
D_j=2(j-1)(2j+2epsilon-1)/c.
```

选实部最小的有限复极点排除所有有限极点, 再以多项式最高次项排除R. 论证没有次数上限, 也排除最小解的有理比值. 不能据此把每个非有理的齐次root-1解也当成上述族.

若要求z0=1, 则A=1. B!=0时令B=1/(tau+1), 得E^(tau), tau!=-1. 若只要求最终定义, A=0也允许; 如果要求从j=1开始逐项定义比值, 还需A+B(j-1)!=0对每个所用指标成立.

首一二次表示e_j=(j^2+a j+b)/(j^2+cc j+d)还须计入可约参数. 下面先列d=0的表示 (cc=t), 随后补充必须单列的A=0尾部分支:

| 奇偶与分支 | a | b |
| --- | --- | --- |
| 偶自由族 | t+1/2 | -(t+1)/2 |
| 偶E+可约表示 | t+1/2 | t/2 |
| 偶刚性E- | t-1/2 | -t/2 |
| 奇自由族 | t+3/2 | (t+1)/2 |
| 奇E+可约表示 | t+3/2 | 3t/2 |
| 奇刚性E- | t+1/2 | t/2 |

此外令sigma=epsilon-1/2, A=0的尾部比值为(j+sigma)/(j-1). 它还有全部可约表示(a,b,cc,d)=(sigma+t,sigma*t,t-1,-t), t任意, 因而不能断言所有四参数表示都满足d=0. 例如偶侧(3/2,-1,1,-2)给出这一合法尾部. 该解z0=0, 不能归一化为z0=1.

这些表描述有理函数恒等式. 对未约分表达式逐点求值, 仍须检查j^2+cc*j+d!=0及所用原序列非零条件; 约分后的延拓不能自动赋予原0/0表达式数值. 参数表示不同可以给出同一比值函数. 完整分类通过约分后的互素一次/二次形式及其全部一次共同因子证明, 不依赖有限参数扫描.

## 降阶与失败路线

对z_j=a1*z_(j-1)+a2*z_(j-2)+a3*z_(j-3), 基准解E必须在所用所有指标逐项非零. 设r_j=z_j/E_j, s_j=r_j-r_(j-1), 则

```text
0=E_j s_j+(a2 E_(j-2)+a3 E_(j-3))s_(j-1)+a3 E_(j-3)s_(j-2).
```

反向构造用r0,s1,s2初始化. E0=1或“非零解”都不足以代替逐项非零; (1-j/3)E-_j是E0=1却E3=0的反例. 变差常数若再除以s_j, 也必须逐项检查s_j!=0.

旧d4的四处整除破坏闭式, 其旧降阶公式和双精度长向后迭代又分别产生False和nan而未失败退出. 当前活动程序为`scripts/d4_third_order_theory.py`: 精确有理除法与降阶、正差分有限向后计算、显式失败退出. 数值结果不证明无穷指标收敛.

## 证明、历史和未闭合范围

- 当前完整解析证明: `docs/SL_third_order_recurrence_theory.tex`, 第四轮修订. 输入补证和原字节在`research/artifacts/proof-audit-round4-20260921/`.
- 既有root-1高次排除: `runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse/candidate_proof.md`及对应审计, 保留冻结版本. 本轮的极点证明同时处理明确递推的最小支.
- c=1锚点的既有独立证明: `docs/SL_third_order_K1_proof.tex`, 其原终端归一化见`tools/third-order-minimal-K1.md`.
- 仍未覆盖: 一般变系数族、非齐次源项控制、完整盒不变性及历史高阶形式级数的统一余项证明. 这些缺口不因本卡的一般c闭式而消失.
- Lean只认可当前验证报告列出的局部目标; 这里的尾级数、全有理分类及极限结论仍依靠解析证明, 不是全部形式化.
