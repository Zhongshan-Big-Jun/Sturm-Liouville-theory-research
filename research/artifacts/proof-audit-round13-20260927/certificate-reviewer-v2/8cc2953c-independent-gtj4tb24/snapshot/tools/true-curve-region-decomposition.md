---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0e2aa-7f3b-7c71-87a6-16e984423a97"], "created": "2026-08-09", "evidence_status": "ROUND13_SCOPED_CORRECTION_REQUIRES_CURRENT_RECEIPT", "source": "自研 (O3a I3 去证书化路线, 会话 39/40, 2026-08-09)", "sources": [{"locator": "Current exact certificate and closed-parameter-box scope", "path": "docs/SL_gap_n1_O3a_phase_rigidity_proof.tex", "sha256": "a557625fe277b37a9d8ae5a5cdc432b717fec01bbc53ada3ca80f36078da11ad"}, {"locator": "Independent-review corrections F1-F3; prior rejection retained", "path": "research/artifacts/proof-audit-round13-20260927/certificate-repair-v2.md", "sha256": "faae1284b8ba8b4e9e863140e61461597cde4d393b9047b868145e53a8172f79"}], "status": "第十三轮修订；按精确版本回执检索", "summary": "保留真曲线 T1/T2 原解析分解范围；T2 单变量事实使用修订后的精确有理证书。旧 Decimal 和历史 PASS 标签不作当前可信入口。", "tags": ["mathtool", "self-developed"], "title": "真曲线区域分解 (true-curve-region-decomposition)", "tool_id": "true-curve-region-decomposition", "updated": "2026-09-27"}
---

# 真曲线区域分解 (true-curve-region-decomposition)

## 解析
目标: 把二维盒证书 `J1_2d > 0` (盒 [0.841,1.1220]x[1,2]) 与 `J2_2d < 0`
(盒 [0.655,1.0472]x[1,2]) 缩小到真曲线区域并完全解析化.

1. **真曲线区域** (E1 定义): `T1 = {(x,q): 0.841<x<1.1220, 1<q<2, 0.4<c1(x,q)<0.5}`,
   `T2 = {(gamma,q): 0.655<gamma<1.0472, 1<q<2, 0.4<c2(gamma,q)<0.5}`.
   内部盒 `Q°=(1,2)x(0.4,0.5)` 的相位像包含于 `T1,T2`；闭盒
   `Q=[1,2]x[0.4,0.5]` 的像包含于相应闭包，由相位连续性及内部点逼近得到。
   例如 `q=1,c=1/2` 给出 `alpha1=gamma=pi/3`，不在严格的 `Ti` 内。
   边界严格符号分别由 T1 闭包上的统一下界 `6499/7500` 与整个闭盒上的 J2 定理保证，
   不能只靠严格不等式的连续延拓。
2. **分解恒等式** (E1): `G = u(H-A)`, `u = x*Phi_q/(q+c*Phi_q)`,
   `A = 3/x + 2*cot x`, `H = 2c(q^2-1) sin x cos x/(q+c*Phi_q)`;
   沿真实曲线 `c = c1(x,q)` 有分解
   `J1_2d = G^2 + G_c - (x*Phi_q/(q+c*Phi_q)) * G_x`,
   其中 `G_c = partial_c G`, `G_x = partial_x G` 是 G 在固定 `(q,c)` 下的偏导数
   (不是沿相位曲线的导数); `J2_2d` 有同构分解.
   [更正 (会话 40): 旧版声称 `dG/dx|_q = c1'(x,q)*J1_2d`, 该恒等式不正确,
   已删除; 正确表述见上 (证明文档 eq:jdec).]
3. **q=1 单变量闭式** (E1, 已证):
   `J1_2d(x,1) = (2x/pi)^2 * N(x)`, `N(x) = 12 + 16 x cot x + 2 x^2 cot^2 x - 2 x^2`.
   对 `x in [pi/3, 5pi/14]`: `z = x cot x >= (pi/3) tan(pi/7) > 1/2`, 故
   `N >= 2(1/4+4+6) - 2(5pi/14)^2 > 17.9 > 0`.
   对 `x = pi - gamma in [2pi/3, 5pi/7]` (即 gamma in [2pi/7, pi/3]):
   `J2_2d(gamma,1) = x^2 N(x)/pi^2`, `z = -x cot x in [2pi/(3 sqrt3), (5pi/7) cot(2pi/7)]`,
   `N <= 2(4 - 8*8pi/21 + 6) - 2(2pi/3)^2 < -7 < 0`.
   角点: `J1_2d(pi/3,1) = 4N(pi/3)/9 ~= 8.98`, `J2_2d(pi/3,1) = 4N(2pi/3)/9 ~= -5.87`.
4. **T1 侧完全解析化** (E1, 定理 5.8, 会话 40): 七步初等链, 记
   `D = q + c*Phi_q(x)`, `Phi = Phi_q(x)`, `W = 3 + 2x cot x`:
   - (i) `Phi/D >= 2/3`: 因 `x > pi/4` 故 `cos 2x < 0`, 且
     `d/dq(Phi - q) = 2q sin^2 x - 1 >= -cos 2x > 0`, 于是 `Phi >= q`, `q/Phi <= 1`,
     `Phi/D = 1/(q/Phi + c) >= 1/(1 + 1/2) = 2/3`;
   - (ii) `u >= 2x/3` 且 `u_x >= 2/3`: `u_x = Phi/D + 2xq(q^2-1) sin x cos x/D^2 >= 2/3`;
   - (iii) `G < -2` 故 `G^2 >= 4`: `D - c(q^2-1) sin^2 x = q + c > 0` 给出
     `H < 2 cot x`, 于是 `G = u(H-A) < -3u/x <= -2`;
   - (iv) `G_c = t1 + t2 >= 187/100`, 其中
     `t1 = Phi^2 W/D^2`, `t2 = 2x Phi (q^2-1) sin x cos x (q-c Phi)/D^3`;
     `t2 >= 0` (因 `q - c Phi >= q(1-cq) >= 0`); `t1` 分两段:
     `x <= pi/3` 用 `t1 >= (2/3)^2 (3 + 2pi/(3 sqrt3)) = 4/3 + 8pi/(27 sqrt3) > 187/100`
     (有理界 `pi > 3.1415`, `sqrt3 < 1.7321`); `x >= pi/3` 沿曲线
     `t1(x,q) >= t1(x,1) = (2x/pi)^2 W(x) =: f(x)`, `f` 递增因
     `3 + 3x cot x - x^2 csc^2 x > 0` (用 `tan t >= t + t^3/3 + 2t^5/15` 于
     `t = pi/7` 与 `pi in (3.1415, 3.1416)` 的有理界);
   - (v) `C := 3/x^2 + 2 csc^2 x <= 8`: C 在 `(0, pi/2)` 递减, 且
     `sin(841/1000) >= 841/1000 - (841/1000)^3/6 > 0.7418`, `sin^2 > 0.55`;
   - (vi) `u <= 89/100`: 记 `theta = c1(x,q)*x`; 由 `c1 > 0.4` 与 `2theta <= x < pi/2`
     得 `sin 2theta >= sin(4x/5)`, 进而 `u <= u_c(x) = x sin 2x/(sin(4x/5) + 0.4 sin 2x)`;
     `u_c <= 89/100` 等价于 `F(x) >= 0`,
     `F = (89/100) sin(4x/5) - (x - 89/250) sin 2x`;
     用 `g(y) = (y/2 - 89/250) sin y - cos y` 与交错级数有理包络
     (`sin(8976/10000) <= 0.78193`, `cos(13/100) >= 0.99155`,
     `cos(14596/10000) >= 0.11047`) 证 `F'' >= 3/2`; 又
     `F'(24/25) in (-1/20, 0)`, `F'(97/100) > 0`, `F(24/25) >= 49/1000`,
     `F(97/100) >= 49/1000`, 故 F 在 `[841/1000, 1122/1000]` 先减后增且
     `F >= 49/1000 > 0`. [更正 (会话 40): 旧交接 `F'' >= 1.7` 的有理界方向有误
     (sin(2x) 下界取点错), 现链为 `F'' >= 3/2`.]
   - (vii) 组合: 由 `H_x < 0` (因 `cos 2x < 0`), `H - A < -3/x`,
     `G_x = u_x(H-A) + u(H_x - A_x)`, `A_x = -C`, 得
     `uG_x <= u^2 C - 3uu_x/x`; 由 (ii)(v)(vi) 得 `3uu_x/x >= 4/3`,
     `u^2 C <= (89/100)^2 * 8`; 于是
     `J1_2d = G^2 + G_c - uG_x >= 4 + 187/100 - ((89/100)^2*8 - 4/3)
     = 6499/7500 > 1733/2000 > 0` 于 T1 闭包.
   [旧归约 `J1_2d >= 2.8^2 + 1.87 - 2.14*(561/450)` 依赖 (M1)--(M3) 单调性,
   已随 T1 侧解析化废弃.]
   **T2 侧完全解析化** (E1, 定理 5.14, 会话 40 续): 旧 (M1')--(M3') 单调性
   路线被废弃. 新链: 沿真实曲线 `c2 = t/A` (`t = arctan(q tan gamma)`,
   `A = pi - gamma`) 精确分解 `J2_2d = N/(16 Delta^4)`, `N = 32 A^2 cg W`,
   `W = W1+...+W8` (括号因子 `B1,B2,M,B4,B5,B7,G5`, 模 sg^2+cg^2=1,
   st^2+ct^2=1 下精确多项式恒等式, 符号计算验证); 轨迹几何
   (`t in [gamma,tau]`, `z = ct^2 in [z-,z+]`, `t st ct^5 >= 2 tau sg cg^5/D^6`,
   `h(t) >= m`, `D <= 2`); 括号符号/单调性; 26 端点有理界; 分段组合
   `mu = T_A+T_B+T_C-T_D >= 139/100` (角点精确值 `27921/20000 = 1.39605`)
   给出 `W <= -mu < 0`, 故 `J2_2d < 0` 于整个盒 `[0.655,1.0472]x[1,2]`.
   55 项解析事实由当前 [[rational-envelope-certificates]] 的有理包络支持；57 条台账合同完整验收。退役 Decimal 引擎不再作为依据。
5. **导数分子结构**: 在曲线坐标 `(x, theta)`, `theta = c*x`, `q = cot x cot theta`,
   每个 q 方向导数的分子是六个正变量 (sin x, cos x, sin theta, cos theta, x, theta)
   的带整系数多项式, 分母恒正; 因此 T2 侧剩余证明链不含超越区间运算.

## 适用范围
- 适用: 相位方程可显式反解、真实曲线位于薄带、J 可分解为初等量平方和的场景;
  把证书目标收缩到真曲线区域可放大安全裕量 (T1 上 J1 约 [9.0,18.6],
  T2 上 J2 约 [-17.7,-6.0], 远大于盒证书的 0.42/0.062).
- 边界情形: 角点闭式 (arccos(2/3), 5pi/14, pi/3) 与 q=1 线已单独处理 (E1);
  T2 侧 (M1')--(M3') 单调性路线已废弃, 由 W-分解链完全解析化取代 (定理 5.14).
- 不适用: 单调性不成立的参数域 (例如 dJ2_2d/dq 在 T2 上可取正, 故 q=1 归约失败);
  直接区间单叶盒 (依赖性问题导致区间过宽, 旧尝试需 11553 叶盒, 不可行).

## 验证与备注
- **E1 侧 (T1)**: 定理 5.8 七步链由 `scripts/verify_o3a_i3_t1_e1.py`
  (内容哈希 L6 = 64e24ace3117772b6cd2ea2ac53986a75cad6c3fd797b61369472ac87ec6ab04)
  逐项交叉检验: PART A 9 恒等式 528 点 0 失败; PART B 14 个 E1 目标
  (含 u>=2x/3, u_x>=2/3, uu_x>=4x/9); PART C F 分析的有理包络; PART D 两段
  t1 常数; PART E 组合链 6499/7500. 全部 PASS. (E1 证明独立于脚本, 脚本仅复核.)
- **E1 侧 (T2)**: J2_2d<0 完全解析化由定理 5.14 完成; 55 项单变量事实
  由当前 [[rational-envelope-certificates]] 的解析包络与精确有理证据支持；第十三轮重新验收 57 条完整台账命题，包含原非零阈值。
  `misc/e1_certgen.py` / `misc/e1_cert_receive.py` 是当前生成与接收入口；旧 Decimal 三件套和 L7/L8/L9 仅保留历史身份。此链不再需要 67 叶盒证书
  (旧 `scripts/verify_o3a_i3_2d.py` 不再承担证明职责).
- E3 数据 (mpmath 40 位, 仅侦察, 不作为结论依据): T1 上 G in [-3.72,-2.81],
  Gc in [1.87,3.89], Gx in [-1.07,1.28], x*Phi/D in [0.68,0.84];
  T2 上 G in [-0.38,1.82], Gc in [-2.64,0.26], Gx in [4.49,9.84],
  x*Phi/D in [1.40,1.86].
- 恒等式经 sympy 精确生成与核验; 数值经 mpmath 40 位交叉检验 (仅侦察).
- 探索用临时脚本 (根目录 _*.py) 已于 2026-08-09 清理; 可复现验证见
  scripts/verify_o3a_i3_t1_e1.py (E1 侧) 与 scripts/verify_o3a_i3_2d.py (E2 侧).
- 相关: [[phase-param-2d-certificate]], [[key-lemma-decomposition]], [[interval-ad-certificate]], [[interval-dec-directed-rounding]].

第十三轮修复的是原语包络、证书显示与完整谓词/失败传播；保留 T1/T2 原解析目标。旧浮点扫描不据此升级为区间认证，未扩展全局 G1/M3/KP。
