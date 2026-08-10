# Problem contract

## Title
J2_2d < 0 证明中 55 项单变量事实的完全解析化 (E1), 消除 O3a 文档对区间验证器 (E2) 的依赖

## Objects and definitions
区间 gamma in [0.655, 1.0472], q in [1,2], 记号 (docs/SL_gap_n1_O3a_phase_rigidity_proof.tex, ss:j2e1):
- A = pi - gamma, sg = sin gamma, cg = cos gamma, D2 = 1 + 3 sg^2, D = sqrt(D2),
  t = arctan(q tan gamma), tmax = tau = arctan(2 tan gamma), z_- = cg^2/D2, z_+ = cg^2.
- B1 = A cg - 2 sg
- B2 = 4A^2 cg^2 - A^2 - 12A cg sg + 6 sg^2
- M  = 2A^2 cg^2 - A^2 - 8A cg sg + 6 sg^2 = B2 - 2A cg B1
- B4 = 7A cg^2 - A sg^2 - 4 cg sg
- B5 = A^2 cg^2 - A^2 sg^2 + 2A^2 + 12A cg sg - 12 sg^2
- B7 = 3A cg^2 + A sg^2 + 8 cg sg
- G5 = B5 - A B4
- TA_B2 = 4(-B2) A^2 sg^2 cg^4 / D2^2 ;  TA_M = 4(-M) A^2 sg^2 cg^4 / D2^2
- TB = 2 A^3 sg^2 tau cg^5 / (D2^2 D)
- TC = m G5 A sg cg^2,  m = 3164/10000
- z = ct^2 in [z_-, z_+]; Q(z) = 4A^2 z^2 - A B7 z + 6 cg^2 sg^2; Qlo = Q(z_-), Qhi = Q(z_+)
- Fv = tau^2 cg sg^2
- h(t) = t sin t cos t  (h(tau), h(gamma), h(t) 于 [0.655, 13/10])
- T_D = Fv * max(Qlo, 0)

## Hypotheses
gamma in [0.655, 1.0472], q in [1,2] (t in [gamma, tau] 由 lem:track(i) 给出).

## Target conclusion
以下 55 项事实全部由纯解析 (E1) 证明给出 (不再依赖区间引擎 rigid_dec.py):
(A) lem:brackets 25 项: B1 递减 + 2 端点值; B2<0, M<0, B4>0, G5>0, Qhi<0;
    Qlo 递增 + 2 端点值; Fv 递增于 [1.0014,1.0472] + Fv(1.0472)<=63/100;
    TA_B2 单调性 5 段 + >=27/10 于 [0.723,0.724]; TA_M 递减 2 段;
    TB 递减; TC 递增/下界/递减 3 段.
(B) lem:track(iv) 4 项: h(gamma)>=m, h(tau)>=m, h(t)>=m 于 [0.655,13/10], tau(1.0472)<13/10.
(C) eq:endpoints 26 项端点有理界 (T_A,B2/T_A,M/T_B/T_C/B4 在 9 个有理点).
完成标准: 上述每项事实在 tex 中以显式解析证明或显式有理区间表给出, 可人工复核;
rem:riv 的 55 项 E2 认证改为 E1 陈述; 文档证据分层只保留 E1 + E3(交叉检验);
重新编译零警告.

## Quantifiers and dependency of constants
所有常数均为显式有理数或由 pi in (157/50, 22/7) 型有理界给出; 不引入新参数.

## Equivalent formulations
无.

## Boundary and degenerate cases
gamma = 0.655 与 1.0472 端点含闭; q = 1 (t = gamma) 与 q = 2 (t = tau) 边界含在
t in [gamma, tau] 内; m = 3164/10000 为固定常数.

## Permitted outcomes
- 全部 55 项事实的 E1 证明 (affirmative)
- 若某项无法 E1, 明确记录为剩余 E2/E3 缺口 (不允许伪装成 E1)

## Completion criteria
1. 55 项事实逐一有显式 E1 证明或归约到显式有理区间表;
2. tex 更新 (lem:brackets/lem:track(iv)/eq:endpoints/rem:riv/tab:facts) 且
   证据标注一致 (E2 移除或仅历史);
3. xelatex 两次零警告; E3 交叉检验脚本全 PASS (不构成证明).

## Results that do not count as completion
- 仅数值扫描 (mpmath 采样) 通过;
- 区间引擎 (rigid_dec / mpmath.iv) 输出;
- 未写进 tex 的推导.

## Tool, citation, and search constraints
本任务为内部严格化, 无需文献检索 (定理契约已在文档中). 工具: sympy/mpmath 仅作
E3 交叉检验与推导辅助; 最终证明为人工可复核的初等估计.

## Ambiguities or competing interpretations
无.

## Contract audit
由本人 (求解者) 以第二遍视角复核: 事实清单与 ledger (misc/e1_facts_ledger.json)
55 项一一对应; 完成标准逐条可核.
