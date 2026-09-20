---
title: 一阶摄动片层法 (R->1+ 片层)
tags: [mathtool, self-developed]
source: 自研 (会话 33 续, run R-20260807T163000Z)
status: 一阶闭式已得 (DERIVATION); phi' > 0 于 [a0,1) CERTIFIED + STRICT; b_top* >= 7/10 > b0 STRICT; 余留 Gap 1 (显式 O(eps) 界)
created: 2026-08-08
---

# 一阶摄动片层法 (r1plus-perturbation-sheet)

## 解析
对 Dirichlet 弦 $-y''=\lambda\rho y$, $\rho=1+\varepsilon 1_{(a,b)}$ (势垒族,
$\varepsilon=R-1$), 记 $R_1=f(a)$, $f=\lambda_1 w_1^2-\lambda_2 w_2^2$ ($w_k$ 为
$L^2(\rho)$-归一化模态), 其零点集 $\{R_1=0\}$ 含经过 $(a_{\rm fp},1-a_{\rm fp})$
的分支 S3. 当 $R\to 1^+$ 时 S3 的结构是竖直片层:

$$a = a_0 + \varepsilon\,\varphi(b) + O(\varepsilon^2),\qquad b\in[a_0,\,b_{\rm top}],$$

其中 $a_0=\arccos(1/4)/\pi$, $b_0=1-a_0$, 且

$$\varphi(b) = -\frac{R_1^{(1)}(a_0; a_0,b)}{f_{\rm const}'(a_0)},
          \qquad f_{\rm const}'(a_0)=\frac{15\pi^3\sqrt{15}}{4}.$$

闭式 (2026-08-09, 手算原函数, sym_phi_closedform3.py):
$$\varphi(b) = \frac{\sqrt{15}}{57600\pi^2}\Big[-1920\sqrt{15}\pi^2 a_0^2
  +1920\sqrt{15}\pi^2 a_0 b -64\sqrt{15}\pi a_0\sin(2\pi b)
  -448\sqrt{15}\pi a_0\sin(4\pi b) -2700\pi a_0
  +1920\pi b\cos^2(2\pi b) -960\pi b\cos(2\pi b) -960\pi b
  -960\sin(2\pi b) +480\sin(4\pi b) -1920\pi\cos^2(2\pi b)
  +960\pi\cos(2\pi b) +225\sqrt{15} +2310\pi\Big],$$

$$\varphi'(b) = -\frac{N}{60\pi},\qquad
  N = m u^2 + (2\pi a_0+3\sqrt{15})u + (3\sqrt{15}-58\pi a_0)
  + 2\sqrt{15}\pi(1-b)(1-4u)v,$$

$u=\cos(2\pi b)$, $v=\sin(2\pi b)$, $m=56\pi a_0-6\sqrt{15}>0$,
$n=2\pi a_0+3\sqrt{15}>0$. 因式分解形式:
$$\varphi'(b)\,60\pi = (1-u)\big(m(1+u)+n\big) + 2\sqrt{15}\pi(1-b)(4u-1)v.$$

一阶量 $R_1^{(1)}$ 由显式闭式给出 (零阶 $y_k^0=\sin(k\pi x)/(k\pi)$,
$u_k^0=\sqrt2\sin(k\pi x)$, $n_k^0=1/(2k^2\pi^2)$):

- 特征值一阶项: $\lambda_k' = -k^2\pi^2[(b-a)-(\sin(2k\pi b)-\sin(2k\pi a))/(2k\pi)]$;
- 解的一阶项 (Green 函数, 符号已核实): $y_k^1(x) = -\frac{1}{k\pi}\int_0^x
  \sin(k\pi(x-s))[\lambda_k'+k^2\pi^2 1_{(a,b)}](s)\frac{\sin(k\pi s)}{k\pi}\,ds$;
- $n_k^1 = 2\int_0^1 y_k^0 y_k^1 + \int_a^b (y_k^0)^2$;
- $w_k^1 = y_k^1/\sqrt{n_k^0} - u_k^0 n_k^1/(2n_k^0)$;
- $R_1^{(1)} = \lambda_1'(u_1^0)^2 + 2\pi^2 u_1^0 w_1^1 - \lambda_2'(u_2^0)^2
  - 8\pi^2 u_2^0 w_2^1$ (全部在 $x=a_0$ 处求值).

关键事实:
- 退化点 $(a_0,a_0)$ 对每个 $R$ 都在 $\{R_1=0\}$ 上 (空势垒:
  $R_1(a_0,a_0,R)=f_{\rm const}(a_0)=0$); $R$ 小时 S3 是过该点的分量,
  故 $g_1(a_0)=a_0$ 精确成立;
- $\varphi(a_0)=0$ (精确), $\varphi(b_0)=0.026021$, $\varphi'>0$ 于
  $[a_0,1)$ (2026-08-09: CERTIFIED 区间算术 [a0,0.999], 最坏下界 8.896e-6;
  STRICT 初等尾部 (0.999,1): phi'(1-e) 60 pi >= C_tail e^2, C_tail >= 9.651926);
- $h(a_0)=g_1(a_0)-1+g_1^{-1}(b_0)=u(a_0)-b_0 = (2a_0-1)+\varphi(b_0)\varepsilon
  +O(\varepsilon^2) = -0.160861+0.026021\varepsilon < 0$;
- $h(\beta)\to b_{\rm top}^*-b_0>0$, 且 $b_{\rm top}^*\ge 7/10 > b_0\approx 0.5804$
  (STRICT 结构引理: R1(a,b-bar,eps) 在 (a0,0) 处 IFT, b-bar in [a0,7/10],
  fp 弧落在 S3 上; 数值上 $b_{\rm top}\approx 0.936$);
- $G=g_1'=1/(\varepsilon\varphi')+O(1)>0$ (P0), $\Phi-1=1/(\varepsilon^2\varphi'\varphi'_u)-1>0$
  (小 $\varepsilon$ 时 U' 平凡成立, 零个零点).

## 适用范围
- 适用: 两参数势垒族 $R\to 1^+$ 极限分析; 把 E1/U'/P0 全部化为
  $\varphi'>0$ 与 $b_{\rm top}^*>b_0$ 的单变量微积分 (严格化路线见下).
- 边界情形: S3 在 $a_0$ 附近近竖直 ($db/da=O(1/\varepsilon)$), 逐 $a$ 追踪
  不可靠, 须按 $b$ 列根并甄别伪根; 端点 $b=a_0$ 处 S3 过退化点, 需单独处理.
- 不适用: $R$ 较大时 (临界 $R^*\in(1.05,1000)$ 之间某处) S3 脱离 $(a_0,a_0)$,
  片层描述失效, 改用大 $q$ 剖面 (见 [[gap-band-extremals]] 与 run A4-A5).
- 已知缺口 (归入 Gap 1): $A_\varepsilon(b)-a_0-\varepsilon\varphi(b)$ 的显式
  一致 $O(\varepsilon)$ 界, $b_{\rm top}(\varepsilon)$ 的显式上界
  $b_{\rm top}(\varepsilon)\le 1-\delta_0$, 以及 h/G/Phi 的一致误差界;
  完成后 E1/U'/P0 对 $R\in(1,1+\varepsilon_0)$ 全部成立.

## 验证与备注
- $\varphi$ 表与精确 secular 求解器的有限差分在 $b=0.45..0.95$ 吻合 6 位
  ($R_1^{(1)}$ 误差 ~1e-6); $\varphi$ 与 $R=1.001$ 的 $(a-a_0)/\varepsilon$
  吻合 3-4 位 (余项为 $O(\varepsilon)$).
- 2026-08-09 复跑: verify_phi_closedform2.py 闭式 vs 参考 R1_1 最大差 1.38e-6;
  verify_sheet_exact.py 在 eps=1e-4 时 a*(b,eps)-a0-eps*phi < 1e-9, phi' 闭式
  vs 有限差分 5 位; cert_phi_prime.py 全部 PASS (输出 JSON 入 repro_manifest).
- 发现并修复 bug (F-019): $w_k^1=y_k^1/\sqrt{n_k^0}-u_k^0 n_k^1/(2n_k^0)$ 曾误用
  乘法 (乘 sqrt(n_k^0)) 实现, 由逐项对比 (dbg_pieces3.py) 捕获, 在
  sym_phi_closedform3.py 修正; sym_phi_closedform.py/2.py 保留作历史.
- $h(a_0)$ 展开 $-0.160861+0.026021\varepsilon$ 与实测 $-0.16052$ (R=1.02),
  $-0.15975$ (R=1.05) 吻合到 $O(\varepsilon^2)$.
- 重要更正 (F-016): 旧主张 fp-分量极限曲线 $\sin(2\pi b)=-\sin(\pi a)/2$,
  斜率 1/14 被否证: S3 近竖直 ($db/da$ 在 R=1.05 时 48..531), $G(a_0)\to+\infty$
  而非 1/14; R=1 的旧公式第二项应为 $\sin^2(2\pi a)$ 而非 $\sin^2(2\pi b)$.
- (F-017) e15 首行 $b(a_0)$ 在 $R\le100$ 是 off-branch 伪根; (F-018) 首个
  cumsum 积分器 Green 函数符号错, 已用 leapfrog 与有限差分 (6 位) 校正.
- 脚本: runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/
  reproducibility/s33_r1plus.py (输出 s33_r1plus.json).
