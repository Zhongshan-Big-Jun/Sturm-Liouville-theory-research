# 对称阱族的 INF 极限与连续相位比较

模型为 Dirichlet 弦 -y''=lambda*rho*y, rho=[R,1,R], 两端重层长度 u, 0<u<1/2. 令 D_R=lambda_2-lambda_1, G=R*D_R, m_R=inf_u D_R, ell=1/2-u, epsilon=R^(-1/2), w=u/epsilon. 极限根 a in (pi/2,pi) 满足 tan(a)=-a*ell/u, Dbar=(a^2-pi^2/4)/u^2.

T2 的解析符号链给出 Dbar 的唯一极小点 u*. 端点行为为 u*Dbar(u)->4 (u->0), Dbar(u)->3*pi^2 (u->1/2), 故 M=Dbar(u*)<3*pi^2. T3 用精确 Fraction 区间、Machin 公式和 Taylor 余项单独定位:

    u* in [0.32992250812006654958, 0.32992250812006654960],
    M in [24.9438661384324768968, 24.9438661384324769084].

根像传播使用下端的下界、上端的上界; 普通超越函数值再加一次 nextafter 不构成当前证书.

T1 的新证明覆盖 R>=1500 的整个参数域:

- w>=2: [引理 A''](lemma-A-doubleprime.md) 给 G>Dbar+ell/(R*u^3)>=M.
- 0<w<=2: 连续展开相位给出 G>15*pi^2/4>3*pi^2>M, 包括 w->0、原曲边漏区以及 R 无穷尾部.
- 固定 u* 的点态展开给 G(R,u*)=M+O(1/R), 因而 0<=R*m_R-M=O(1/R) 且 R*m_R->M.
- 若 R_j->infinity, D_(R_j)(u_j)<=m_(R_j)+eta_j, eta_j>=0, R_j*eta_j->0, 则 u_j->u*. 原 eta_j=R_j^(-2) 是特例.

这里 T1 使用 T2 的解析严格余量, 不再依赖 T3 的高精度数值或旧二维矩形覆盖. 近极小化子论证分别排除 Dbar->infinity 与 Dbar->3*pi^2 两端.

可复用的新工具是整个 R>=1,0<u<1/2 上的相位速度界:

    G(R,u)>=pi^2/[2*epsilon*(w+ell)*(w+epsilon*ell)].

对射击接口向量 (y',k*y)=(cos(w*k),epsilon*sin(w*k)), 取连续展开辐角 A_epsilon. 半区间相位 Phi(k)=ell*k+A_epsilon(w*k), Phi'>0 且 Phi'<=ell+w/epsilon. 实际偶/奇基态满足 Phi(k1)=pi/2,Phi(k2)=pi; 分别控制 k2-k1 和 k1 后得到该界. 这避免了对奇模强加全域 theta_2>pi/2.

固定内部 u 的展开为

    G=Dbar+C(u)/R+O_u(R^-2),
    C=pi^2*b/(2*u^2)-2*a^4*b^3/[3*u^2*(1+b+b^2*a^2)], b=ell/u,
    C(u*)=pi^2*(1/2-u*)/[3*(u*)^3]>0.

余项在内部紧区间上一致. 这没有证明全端点一致展开、最优值的精确首项系数或极小化参数收敛率; 非零 R^(-1/2) 首项的旧表述已撤回.

完整证明见 [当前正文](../docs/SL_gap_n1_inf_limit_proof.tex), 精确算术、隔离检验、局部 Lean、失败记录和放行见 [第八轮报告](../reports/proof-audit-round8-20260922/REPORT.md). 历史05/16/19证书与旧点抽样保留溯源, 不继续作为当前连续域认证. 结果仅限所述对称阱族; 不据此授予一般非对称族、全盒类或高阶间距结论. 新相位方法向其它分层模型的推广只是研究线索, 尚无通用定理.
