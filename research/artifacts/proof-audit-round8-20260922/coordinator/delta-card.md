# 对称阱族的相位分支与括号

模型为 Dirichlet 弦 -y''=lambda*rho*y, rho=R on (0,u) union (1-u,1), rho=1 on (u,1-u), R>1, 0<u<1/2. 令 epsilon=R^(-1/2), ell=1/2-u, mu_k=R*lambda_k, theta_k=u*sqrt(mu_k), z_k=ell*sqrt(lambda_k).

全域首先使用不除三角因子的匹配方程:

    even: cos(theta)*cos(z)-epsilon*sin(theta)*sin(z)=0,
    odd: epsilon*sin(theta)*cos(z)+cos(theta)*sin(z)=0.

第一模态为偶, 第二模态为奇; 振荡定理及半区间正性给出 0<theta_k<pi, 0<z_1<pi/2, 0<z_2<pi. 偶模还满足 0<theta_1<pi/2. 奇模不在全域满足 theta_2>pi/2: R=1600,u=1/1600 时, rho>=1 给 lambda_2<=4*pi^2, 因而 theta_2<=pi/20.

下述括号明确限于 R>=1500, w=u*sqrt(R)>=2. 此时 c=epsilon*ell/u=1/(2w)-epsilon<1/4, 故 z_2<pi/4. 奇匹配方程于是强制 cos(theta_2)<0, 确定 pi/2<theta_2<pi. 分母不为零后才能写 delta_1=pi/2-theta_1, delta_2=theta_2-pi/2 及

    tan(delta_1)=epsilon*tan(z_1), z_1=(pi/2-delta_1)*c,
    tan(delta_2)=epsilon*cot(z_2), z_2=(pi/2+delta_2)*c.

在这个范围内:

- 0<=delta_1<=delta_1^+=atan(epsilon*tan((pi/2)*c))<=epsilon*tan(pi/8)<0.011.
- 0<=delta_2<=delta_2^+=atan(2u/(pi*ell))<pi/2.
- z_2<=pi/8. 用 h(x)=x*(pi/2+atan(2epsilon/(pi*x))) 在 0<x<=1/4-epsilon 上递增及 h(1/4-epsilon)<=pi/8 证明.
- theta_2<=a(u), 其中 a(u) 是 tan(a)=-a*ell/u 在 (pi/2,pi) 的唯一根. 比较严格递增的 g(theta)=theta-pi/2-atan(epsilon*cot(c*theta)) 并用 cot(z)<=1/z.

完整模式识别、分母检查和不等式链见 [当前证明的相位章节](../docs/SL_gap_n1_inf_limit_proof.tex). 参数 u->1/2 时 delta_2^+ 趋于 pi/2, 是有界量; 发散的是 arctan 的自变量, 不是 arctan 值.

w<2 的薄层区域须使用自己的正确分支和下界. 本卡不把这些 delta 方程作为全参数的根选择规则, 不自动适用于垒族或高阶模态. 旧采样只作历史证据; 第八轮修订的解析检验及局部 Lean 范围见 [报告](../reports/proof-audit-round8-20260922/REPORT.md).
