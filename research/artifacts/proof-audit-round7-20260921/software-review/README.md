# 第七轮软件修订候选与可重放回归

本包由软件作者提交, 等待新的 stateless agent 独立复跑与审稿. 只写 `/mnt/f/tools/math-audit-round7-20260921/software-author`. 主库、历史输出、插件、旧 Blueprint 均未写入, 未 commit/push.

修订对象恰为协调器分配的 **10 个脚本**. `candidates/scripts/` 另有 **8 个原字节依赖** (7 个 Python 文件、1 个 JSON 表), 它们不是额外修订文件. `originals/scripts/` 保存同名 18 个原字节文件. 完整身份与清单见 `manifest.json`; 逐项说明见 `change-notes.md`; 文本差异见 `change.patch`.

## 可在复制目录内执行的完整入口

复制整个本包到审查者自己的隔离目录后, 在该目录执行:

```bash
/usr/bin/python3 -B regression/replay.py --label independent-review
```

可先执行 `/usr/bin/python3 -B regression/verify_package.py` 检查冻结文件哈希. 该检查仅验证包完整性, 不代替行为回归.

重放脚本只使用本包相对路径, 自动再复制冻结源码与验证程序到新的 `work/replay-<UTC>-<id>/`. 每次产生新的目录, 不覆盖已保存的回执. 无需读取主库, 无网络下载, 无历史扫描, 不运行报告所写的命令. 运行时需要 Python、NumPy、SciPy; 本次实际环境为 WSL Python 3.14.4、NumPy 2.5.2、SciPy 1.18.1. 系统也有 SymPy/mpmath, 此回归不依赖它们. Windows bundled Python 已定位但未执行, 不声称跨平台通过.

入口依次执行:

1. 原版正常模式: 117 项, 38 通过、79 失败, **进程退出 1 是预期负对照**.
2. 候选正常模式: 117/117 通过, 退出 0.
3. 候选 `op03_gap_fh.py` 直接 CLI: 原四个 u 点, 无注入, 返回 0, 逐行对照真实打印的 FD/FH 数值.
4. 原版 `-O`: 同样 117 项、79 失败、退出 1.
5. 候选 `-O`: 117/117 通过, 退出 0.
6. 候选 `op03_gap_fh.py` 的 `-O` 直接 CLI: 四点通过, 退出 0.

回归门禁使用显式条件而非 Python `assert`, `-O` 不会跳过判断. 主入口仅在预期失败和候选成功都符合、全部用例实际运行、无测试异常、复制输入字节不变、项目模块均在隔离目录内时返回 0. 它不将原版的退出 1改写为原程序成功.

仅重跑单个测试树可用:

```bash
/usr/bin/python3 -B regression/regression.py --tree candidates --output work/manual-candidate.json
/usr/bin/python3 -B -O regression/regression.py --tree originals --output work/manual-original-O.json
```

第二条预期退出 1. 完整入口额外捕获原始 stdout/stderr、实际 argv/cwd/退出码/时间、输入 SHA-256 与输出 SHA-256; 手动单测不自动生成这些外层回执.

## 数学接口及适用前提

模型是 `-u''=lambda*rho*u`, 区间 `[0,1]` 上 Dirichlet 边界. 本次只处理固定的正分块密度, 内部接口严格有序、各块正宽, 接口在局部开集内独立右移. 假定目标特征值为简单特征值、局部特征对可微 (二阶公式需要相应二阶可微), 实特征函数按 `integral rho*u_k^2=1` 归一化. 不把固定普通 L2 范数的势算子公式用于这里.

定义 `D=lambda_(n+1)-lambda_n`, `s_i=rho_(i+1)-rho_i`, `f_i=lambda_n*u_n(x_i)^2-lambda_(n+1)*u_(n+1)(x_i)^2`. 接口右移将密度变分形式地写为 `delta rho=-s_i delta_(x_i) dx_i`, 因而

```text
d lambda_k / dx_i = lambda_k s_i u_k(x_i)^2
grad_x D = -diag(s) f
F = f/lambda_(n+1),   J = dF/dx
H = -diag(s) [lambda_(n+1) J + outer(F, grad_x lambda_(n+1))]
```

这里 `J` 是包含采样接口移动的总导数, 行是残差分量, 列是接口坐标. 梯度式**不要求驻点**. 当 `F=0` 时才约化为 `H=-lambda_(n+1)*diag(s)@J`. 跳量固定是上述乘积法则的前提; 本包未实现随参数变化的跳量或变 R 的导数. 驻点测试重新求根并检查 `max(abs(F))<1e-9`, 实际约 `1e-13`; 浮点近似等于零不是解析证明.

对于 paired 路径 `x_left+=e, x_right-=e`, 用 `B` 表示该坐标嵌入, 则 `g_reduced=B.T@g`, `H_reduced=B.T@H@B`. 对称三段 SUP 的导数为 `-2(R-1)f`, INF 为 `+2(R-1)f`. 两接口的一般表达是有方向的贡献相加, 不是所有 full-interface 量都乘 2. `gap_n1_grad` 的 `(a,b)` 是前两块宽度, 接口为 `(a,a+b)`; 其 SUP 梯度 `((R-1)(f2-f1),(R-1)f2)` 正确, INF 整体反号.

这些是修订与检验的接口合同和局部形式推导. 本包没有补全分布形状微分的解析正则性证明、谱级数余项估计或其它研究推导. 原脚本中的旧 STRICT/历史 PASS 字样不是本轮认可, 旧研究结论与数值输出未重写.

## 真实检查与隔离边界

| 脚本 | 本次行为路径 |
|---|---|
| op03_gap_fh.py | 实际 Df_at, 实际导入后端, 原 print 中 FH 表达式; 四点直接 CLI 正常/-O |
| gap_n1_grad.py | make_blocks, D_of, f_vals, num_grad; 原 AST 的 gFH, 非对称非驻点 SUP/INF |
| _tmp_fh_paradox.py | D_and_f; 原 AST 的 fh、fh2, 对称非驻点 SUP/INF |
| tmp_fh_test.py | lam_of 与真实 y_at/norm2; 原 AST 的 fh1、fh2 及 gap 打印表达式, INF |
| tmp_verify_endpoints.py | D_and_f; 原 AST 的 fh, SUP/INF. 未运行其整段端点循环与 brentq 输出 |
| _gapn2_hess_verify.py | D_edges; 原 AST 的 f、梯度对照、H1/H2. 非驻点梯度及驻点矩阵 |
| _gapn2_hess_sign_and_bigR.py | 实际 hess_fd 的宽度到接口坐标变换; 原 AST 的 H 两种 sign |
| _gapn2_jacobian_analytic.py | 实际 eigen_data; 原 AST 的 H 与完整矩阵谱. 未重审其解析 Jacobian 公式 |
| _gapn2_o3_scan.py | 原 AST 的 evH 与真实驻点 FD Jacobian/Hessian 比较. 未执行 O-3 扫描 |
| _gapn2_second_variation_probe.py | 原 AST 的 Hess 与真实驻点 FD Hessian/谱比较. 未执行 P1/P2/P3 密度变分实验 |

`regression.py` 只在前五个有顶层循环的诊断文件中移除 module-level `For` 扫描与 `__main__` guard, 函数体不改写; 去除的节点范围记录在结果的 `loader` 字段. 其它已带 main guard 的模块正常导入. 对只存在于 `main`/打印里的修订表达式, 从**实际文件 AST** 提取原节点编译求值, 记录文件行号、AST 哈希和表达式. 不是寻找字符串后自行重写公式.

Hessian 表达式的上游 `J` 在本回归中绑定为原依赖 `_gapn2_jacobian_probe.jac_fd` 的真实输出, 测试点来自重新求得的 stationary root, `eigen_data` 与 `D_edges` 都实际执行. 这属于对上游数值参数的隔离注入, **不等价于运行使用 analytic_jacobian_hp / analytic_jacobian_spectral 的全部 main**. 它覆盖修订表达式的完整矩阵乘法、负号、特征值因子, 不认证未重跑的解析 Green/谱求和后端.

覆盖包括 R=4 的 n=1、n=2, SUP/INF; 一维单接口, 非对称双接口非驻点, 对称双接口路径, 2x2/4x4 完整驻点 Hessian, 镜像 B.T H B. FD 步长、容差、具体输入、矩阵、残差和误差均保存在结果 JSON. 非驻点 Hessian 单独保留秩一项并与 FD 比较; 刻意省略它时 SUP/INF 最大矩阵误差约为 136.59/146.92, 证明这两个点不能拿驻点简式比较.

## op03 后端故障及最小修订

`op03_gap_precise` 和 `op03_gap_fixed` 的 `eigfuns_precise(blocks,s_vals,x_pts)` 接口一致; 本调用仅使用 `lams_precise(blocks,k)`, 两者这部分兼容. 可选参数不同 (`s0` 与 `smax_scale`), 未概括成完全可替换接口.

旧 precise 在逐块累积和点值传播中使用 `M @ P`, 而沿 x 从左向右推进列状态应为 `P @ M`. 它还用这些错误的块起点构造范数. 在对称块 `(.3,1),(.4,4),(.3,1)` 上, 特征根和端点恰能看似正确, 但返回函数的真实加权积分是约 `0.9487027,0.9313559`, 因而只补因子 2 不足以使真实 FH 检查通过.

本包仅将已分配的 `op03_gap_fh.py` 导入改为现有 fixed. **没有改写 precise、fixed 或其它依赖**. 使用独立的分块 DOP853 IVP + 自适应积分对 fixed 验证对称与非对称低模态的函数值、Dirichlet 端点、加权范数, 另与 recon 比较根. 原双模态函数值对照误差约 `1.3e-12`. 没有据此宣称 fixed 在全部 R、全部模态和近退化参数上可靠.

## 证据及剩余事项

- 最终冻结复跑见 `results/author-replay-summary.json` 指向的 `work/replay-.../`, 含正常/-O 原始回执及候选、原版数值结果. 外层原始运行见 `receipts/05-portable-replay/`.
- `receipts/01-backend-before/` 保留最初后端失败, 退出 1. `02-original-regression/` 保留 harness 格式化 AST 选择器的早期歧义异常, 不作为最终完整回归. 随后修正选择器; `03-original-regression-complete/` 无异常, 79 项行为失败.
- 主库源文件的前后原字节比较另记 `results/source-integrity.json`; 未把此定向比较声称为全库字节认证.
- 未运行旧历史全扫描、未产生新的全局分支/极值/惯性结论, 未运行 Lean, 未读写 canonical, 未重审第二变分推导或 simple-zero 定理. K 在 O-3 文件中另含 lambda 缩放, 保留该约定; 不能与其它脚本的 K 值直接混称相同.
- 本地回归成功是作者证据, 最终批准由独立审查者给出.
