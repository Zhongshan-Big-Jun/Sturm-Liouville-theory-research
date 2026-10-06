# 有界真实密度方向的 Parseval 剩余能量与两侧谱尾界

本轮活动解析补证. 解析证明、有限数值诊断和区间输入认证是不同的证据; 当前审查状态见第十六轮交付报告. 本命题不使用第十五轮删项扩展, 也不要求驻点或 ND.

## 1. 精确对象和量词

固定长度 L>0, 实可测密度 0<m<=rho<=M<infinity 及实方向 h in L-infinity(0,L). 采用真实 DD 问题

\[
-u_k''=\lambda_k\rho u_k,\quad u_k(0)=u_k(L)=0,
\qquad \int_0^L\rho u_k^2=1.
\]

模态选为实数, 按完整谱的一基指标排序 0<lambda_1<lambda_2<.... 特征值 lambda 与频率 sqrt(lambda) 不可混用. 内积对第一变量线性. 置

\[
c_{kl}=\int_0^L h u_k u_l,\qquad
J_k=\int_0^L\frac{h^2}{\rho}u_k^2,\qquad
E_{k,N}=J_k-\sum_{l=1}^N|c_{kl}|^2.
\tag{1}
\]

配对不额外乘 rho. 对任意整数 n>=1 和 N>=n+1, a=lambda_n, b=lambda_(n+1), 令 Q=D_n''(0)/2, D_n(t)=lambda_(n+1)(rho+t h)-lambda_n(rho+t h). Q_N 是下述精确二阶公式中保留前 N 个真实模态的值. 结论为

\[
-\frac{b^2E_{n+1,N}}{\lambda_{N+1}-b}
\le Q-Q_N\le
\frac{a^2E_{n,N}}{\lambda_{N+1}-a}.
\tag{2}
\]

## 2. 完整模态和二阶公式

加权空间 H_rho=L2((0,L),rho dx) 与普通 L2 范数等价. DD Green 算子
Tf(x)=integral G_D(x,y)rho(y)f(y)dy 将 H_rho 有界映入 H0^1, 再通过紧嵌入返回 H_rho. 对称核和能量恒等式给出 T 紧、自伴、正; Tf=0 推出 rho f=0, 所以核为零. 紧自伴谱分解给出上述模态的完备正交基. 左 DD 解由其左端导数唯一决定, 因而每个特征空间一维, 所有相邻谱隙严格正.

选足够小的实 t 使 rho+t h 保持正. 射击解 v(0)=0,v'(0)=1 满足

\[
v(x)=x-\lambda\int_0^x(x-y)(\rho(y)+t h(y))v(y)dy.
\]

有界系数 Volterra 迭代关于 (lambda,t) 局部解析. 在 DD 根处, Lagrange 恒等式给出
v'(L) partial_lambda v(L)=integral rho v^2>0. 根和其正质量平方根可解析续接. 所以对模态作两次参数微分合法. 微分方程及变化密度下的归一化给出

\[
\lambda_k'=-\lambda_k c_{kk},\qquad
\langle\dot u_k,u_l\rangle_\rho=
\frac{\lambda_k c_{kl}}{\lambda_l-\lambda_k}\ (l\ne k),
\qquad \langle\dot u_k,u_k\rangle_\rho=-c_{kk}/2.
\]

于是

\[
\frac{\lambda_k''}{2}
=\lambda_k c_{kk}^2-\lambda_k^2\sum_{l\ne k}
\frac{|c_{kl}|^2}{\lambda_l-\lambda_k},
\tag{3}
\]

以及

\[
Q=b c_{n+1,n+1}^2-a c_{nn}^2
+a^2\sum_{l\ne n}\frac{|c_{nl}|^2}{\lambda_l-a}
-b^2\sum_{l\ne n+1}\frac{|c_{n+1,l}|^2}{\lambda_l-b}.
\tag{4}
\]

下一节的 Parseval 恒等式使级数绝对收敛: 低于目标指标的项有限, 其余分母至少为一个正谱隙. 配对泛函在 H_rho 有界, 因而也可把模态导数的 L2 展开代入配对. (4) 对应活动 q_formula 的 Python 下标 n 为上模态、n-1 为下模态; Cw 不进入该物理公式, 对角数据必须等于 Cu 的真实对角.

## 3. 剩余能量和两侧估计的证明

在 H_rho 中取 g_k=(h/rho)u_k. 由于 h/rho 有界, g_k 属于 H_rho,
其平方范数为 J_k, 且 <g_k,u_l>_rho=c_kl. 完备正交展开和 Parseval 给出

\[
J_k=\sum_{l\ge1}|c_{kl}|^2,\qquad
E_{k,N}=\sum_{l>N}|c_{kl}|^2\ge0.
\tag{5}
\]

若 N>=k, 全部遗漏分母均满足 lambda_l-lambda_k>=lambda_(N+1)-lambda_k>0. 逐项比较得

\[
0\le T_{k,N}:=\sum_{l>N}\frac{|c_{kl}|^2}{\lambda_l-\lambda_k}
\le\frac{E_{k,N}}{\lambda_{N+1}-\lambda_k}.
\tag{6}
\]

由 (4), Q-Q_N=a^2 T_(n,N)-b^2 T_(n+1,N). 两个 T 非负, 代入 (6) 即得 (2). 这是两个符号各自控制的两侧界, 没有把谱尾假设成零.

另外,

\[
0\le E_{k,N}\le J_k\le\|h/\rho\|_\infty^2.
\tag{7}
\]

DD Rayleigh 商和 min-max 比较给出 lambda_j>=j^2 pi^2/(M L^2). 可用 d=(N+1)^2 pi^2/(M L^2) 替代 (2) 中的 lambda_(N+1), 前提是 d>b; 区间运算须先检查 d_lower>b_upper. 这个粗下界不足以超过 b 时, 该替代分母不可使用.

## 4. 取等与零尾例子

单位区间 rho=2,h=2 时, u_k=sin(k pi x), lambda_k=k^2 pi^2/2, c_kl=delta_kl, J_k=1. 所以 N>=k 时 E_(k,N)=0 恰由解析恒等式成立, 不是由负浮点残余截零得到. 对所有 n>=1 和 N>=n+1, Q_N=Q=(2n+1)pi^2/2. 欠分辨求积仍可能把这个精确零尾例算成错误 Q, 证明求积误差与谱截断误差是两回事.

取 rho=2,h=2cos(pi x), n>=2,N=n+1. 三角恒等式给出 c_kl=1/2 当 l=k-1 或 k+1, 其余为零. 下模态无遗漏配对; 上模态只遗漏 l=n+2. 因此 E_(n,N)=0,E_(n+1,N)=1/4, 且

\[
Q-Q_N=-\frac{b^2}{4(\lambda_{n+2}-b)}
=-\frac{\pi^2(n+1)^4}{8(2n+3)}.
\]

这精确达到 (2) 的左界. 对符号认证而言, 模型的 rho/h 和这些积分恒等式仍须对应实际输入.

## 5. 可靠包络与数值接收边界

若可信的包络给出 J_k in [J_k^-,J_k^+] 和 c_kl in C_kl, 定义
S_k^- 为各 |C_kl|^2 下端之和、S_k^+ 为上端之和. 则
E_(k,N) 属于 [J_k^- - S_k^+, J_k^+ - S_k^-] 与 [0,infinity) 的交.
若其上端为负, 输入与已证明的 Parseval 预算矛盾, 必须拒绝. 交集的合法性来自 (5) 和可靠输入包络, 不是把任意负浮点剩余改成零. 尤其未经包络的微小负浮点值也不能证明尾部消失.

设 a in [a^-,a^+],b in [b^-,b^+],lambda_(N+1)>=d^- > b^+, E 的可信上端分别为 e_a^+,e_b^+, 并且有限公式 Q_N in [q^-,q^+]. 可信包络可能很宽, 不能从 d^->b^+ 直接推断 d^->a^+. 先利用真实谱序 0<a<b<=b^+, 令

\[
\widehat a^+=\min(a^+,b^+).
\]

于是 0<a<=widehat a^+<=b^+<d^-, 两个分母均严格正. 函数 x^2/(d^--x) 在 0<x<d^- 单调递增, 所以

\[
Q\in\left[q^- -\frac{(b^+)^2e_b^+}{d^--b^+},\quad
q^+ +\frac{(\widehat a^+)^2e_a^+}{d^--\widehat a^+}\right].
\tag{8}
\]

只有整个区间严格在零的一侧, 才能在这些输入前提下认证符号; 含零则未决. 有限配对、总能量积分、特征值、一基谱身份和 Q_N 本身均须有可靠包络. 普通 Gauss 差值、mp 近似或浮点解析三角计算都不会自动成为这种包络.

活动 SpectralProbe 优先对完整分块方向采用局部解析积分, 并报告数值舍入尚未包络. 一般回调要求全部已知方向断点、实际不折叠的内部节点、保守模态相位分辨检查及预算内两次连续求积比较; 输出误差为估计, 未收敛或不可分辨即拒绝. 任意有界黑箱在采样点外可有未观测结构, 因此这些数值诊断不能认证任意黑箱的真实积分. CLI 逐项保存该诊断, 原始浮点剩余保留且 sign_certified=false.

此结论只用于实际有界实密度方向. delta/delta' 接口方向不是该 H_rho 中的有界乘法方向. 本证不给出脉冲宽度趋零的一致界, 不关闭接口 Hessian 的符号、ND/G1、无条件全局唯一性或 M3/KP.
