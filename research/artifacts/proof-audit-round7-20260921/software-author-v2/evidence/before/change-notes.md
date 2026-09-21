# 十文件最小变更记录

原字节: `originals/scripts/`. 候选: `candidates/scripts/`. 除下表外的求根、扫描、谱和研究逻辑保留. `change.patch` 是便于阅读的文本差异; 文件精确身份以 manifest 中 SHA-256 为准.

| 文件 | 确认问题 | 修订 |
|---|---|---|
| op03_gap_fh.py | paired SUP 少 2; precise 的实际特征函数归一化失真妨碍正确检查 | `2*(1-R)*f`; 仅导入切到现有 fixed, 两个实际调用接口核实兼容 |
| gap_n1_grad.py | 对宽度作 FD, SUP 式直接用于 INF | SUP 保留, INF 将两个分量整体反号, 不统一加倍 |
| _tmp_fh_paradox.py | 忽略镜像运动方向而将两端相减; fh2 未分模式 | 两端相加, SUP 负/INF 正; 对称式分别为 -2/+2 |
| tmp_fh_test.py | INF 特征值导数和 gap 对照符号反 | fh1/fh2 增负号; gap 改 +2; 同步输出标签 |
| tmp_verify_endpoints.py | SUP/INF 双接口 gap 符号都反 | INF +2, SUP -2; 输出中性标签 |
| _gapn2_hess_verify.py | f 的低模态误乘较高特征值; 梯度和 Hessian 符号反 | 恢复 ed['lam_n']; -s*f; H1/H2 负号, 显式 F=0 限制与非驻点秩一项 |
| _gapn2_hess_sign_and_bigR.py | sign*diag(s)*lam*J 逐元素乘法抹去非对角元 | `(sign*lam*diag(s)) @ J`; 正/负对照均保留, 简式仅限驻点 |
| _gapn2_jacobian_analytic.py | 主例 Hessian 逐元素乘法, 相邻注释缺负号 | `(-lam_np1*diag(s)) @ Jfd`, 修正注释. 未修改 analytic_jacobian 的求和公式 |
| _gapn2_o3_scan.py | evH 的逐元素乘法 | 对完整 `(-lam_np1*diag(s)) @ J` 求 eigvalsh, 注明驻点及独立 K 缩放 |
| _gapn2_second_variation_probe.py | P3 比较矩阵抹去非对角项 | `(-lam_np1*diag(s)) @ Jfd`; 未改密度变分路线或其历史记录 |

## 行为负对照

同一测试程序对真实原版表达式和候选表达式执行, 没有手工把旧错式写成假对象. 原版正常/-O 各 117 项, 79 项失败; 候选各 117/117. 这些是有限样本上可重放的软件回归, 不是 117 个解析定理.

- 原 op03 在 u=.3 的打印式给出约 41.5172, 实际 FD 为 89.2907. 同时包含漏 2 和坏范数; 后端分离检查保存了两种故障的证据.
- 原 paradox SUP 两端相减近 0, 实际导数约 89.2907.
- 原 hess_verify 非驻点低模态项错误产生约 9.87 的 f 分量偏差.
- 原 analytic 主例的 n=2 SUP Hessian 非对角元全为 0, 实际 FD 的最大非对角元约 1949.13. 修订后完整矩阵与 FD 最大差约 0.00573 (矩阵量级约 4.5e3).
- 非驻点秩一项省略后仍会错误; 回归显式证明这种省略不合法. 候选驻点公式没有为了非驻点测试被改造成全域式.

## 执行范围

唯一直接跑 main/CLI 的候选是四点 n=1 的 `op03_gap_fh.py`, 正常和 -O 两次. 其它目标的改动行为由实际函数及原 AST 表达式在小样本中验证, 未执行原顶层扫描、扩展 R 扫描、O-3 扫描、全谱数值研究或 P1/P2/P3 试验. Hessian 输入 J 采用实际 jac_fd 作隔离注入, 不能据此认证原 main 中另一个解析/谱截断 J 后端.

后端修订没有增加第 11 个改动文件: fixed 本来存在且按原字节复制. 旧 precise 保留作负对照; 即使本次对称输入的根正确, 也不将其加权函数认证为正确.
