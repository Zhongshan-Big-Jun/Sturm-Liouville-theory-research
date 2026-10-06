# R15-01 独立软件审查

结论：**APPROVED，仅限本报告明确的 R15-01 浮点软件修复范围。** 当前冻结版 `scripts/op03_gap_fixed.py::lams_precise` 正确委托共享按指标 DD 相位引擎，保留频率返回单位、首模态及前缀身份，并执行公开的 `tol` 与弃用 `smax_scale` 合同。本轮没有发现阻碍上述范围批准的缺口。不能据此批准未提供的其它调用者、全部历史数据、解析无限维命题、Lean、区间证书或工具库接收。

日期：2026-10-05。真实原生审查 task_name：`/root/r15_software_review`。

审查根：`F:/tools/math-audit-round15-20261005/review-input/software`。只主动读取此根下清单中的冻结输入及本审查自己生成的输出；没有主动读取工作区、AGENTS 文件、记忆、技能、作者会话、其它审查或基线源码。冻结输入始终只读。没有执行外部项目程序或历史大规模扫描。审查者新增检查脚本仅写入批准的 `reviews/software-run/`。

## 输入身份

我分别通过 PowerShell `Get-FileHash -Algorithm SHA256` 和自写检查脚本中的 `hashlib.sha256` 核算全部 11 项；执行后再次核算，11/11 均仍与 `hashes.json` 一致。最终复核保存于 `reviews/software-run/input-hash-final.json`。

| 冻结相对路径 | 亲自核算的 SHA256 |
|---|---|
| research/artifacts/proof-audit-round15-20261005/checks.py | 997d3f1fc84f54058e1cf1d4f2bdf33ae6c0d7c914fbd24586d743a39bce8a48 |
| research/artifacts/proof-audit-round15-20261005/independent_physical.py | 79de8bed29436b2c04f51a064b0274f6a2465ebb9bc38d6da9fd60ccad65eef3 |
| scripts/op03_gap_fh.py | 9cea8a73ade19abe5e7d530eab553571fc5cc5ff87242db2997a78a9efb1c0b8 |
| scripts/op03_gap_fixed.py | 5dab895bc9c574ea48aa35eff337f33e38a6a3d11d4b4eb7d5e48e58fe54d9df |
| scripts/reflection_seeds.py | 66f0473302b56b3cca3d8e2b0b70dd733d024da33b449ea166692d85b51fe317 |
| scripts/_gapn2_jacobian_analytic.py | 4d7cb5385b6f2b8d668ec4c5c417876a57713b6780bb11e1478cb0fcbc00aa02 |
| scripts/_gapn2_jacobian_probe.py | 793705efee95718b7917ba3669e1bc2108fc5f7ed1205b226f9ed5679451b7dd |
| scripts/_gapn2_jacobian_spectral.py | 227c40a23cdd04e3c64c56e4d8895cb3355a952001603f184ce65de6e0ab149e |
| scripts/_gapn2_symmetry_recon.py | 4f418bdca359c64e7ad6298ad01b6b80f0dc46d8484b2155bcf18623bc529713 |
| scripts/_sl_prufer.py | 489f14986ea61f1560b338a0ae6a33e0da3f2c1fc30c77e8272c9f0ca6a34042 |
| scripts/_sl_spectral_identity.py | c763b576b6af23f4b2db33b198059eea69560a5949d4119571daccefc75cebe9 |

## 实现核对

- `op03_gap_fixed.py:35` 实际调用 `SpectralBackend.indexed_roots(Values, k, Refine=Refine, RightBoundary='D')`。后端以每个独立目标 `n*pi` 二分，比较界不依赖请求数量，既无固定频率网格也无行列式交替变号假设。源码检查及运行中的后端调用 spy 均核对了这个委托。
- 返回 `Frequencies`，没有平方。齐次 `[length=1,rho=1]` 实际返回 `[pi,2*pi,3*pi]`；故障注入的后端哨兵频率也被原样返回。`op03_gap_fh.py:12` 的实际调用者随后明确作 `lam=s**2`。
- `tol`、`smax_scale` 拒绝布尔、复数、非数值、非正、NaN 和 infinity；`k` 由后端按正整数合同检查，含 numpy 布尔和浮点数负对照。这些守卫均使用实际异常，普通及 `-O` 下都有效。
- `tol` 的合同是返回频率括号宽度至多 `tol*max(1,omega)`。wrapper 在后端输出后逐项比较宽度；真实 `tol=1e-30` 请求及人为注入的过宽后端括号均抛出 `ArithmeticError`。`tol=1e-8,1e-15,0.5` 的高反差结果均保持物理序号和位级前缀。此为浮点括号合同，不是严格真根误差包络。
- 正非默认 `smax_scale=.001,2,100000` 实际各发出一条 `DeprecationWarning`，频率与默认值位级相同；默认 5 无警告。参数不再扩大扫描范围。后端故障会向上传播，没有扫描或重标模态的回退。
- `lams_precise` 及其 `positive_blocks` 后端只检查严格正几何及浮点可分辨性。长度 `1e-12` 的输入保持原值，实际计算通过；没有把短块裁剪为 `1e-7` 或其它固定宽度。冻结包中反射种子模块原有的 `MinWidth` 是另一接口的已有种子限制，本审查不把“频率入口没有宽度地板”扩大为“所有项目接口没有限制”。
- `prop_to` 当前采用 `P(block) @ M_old`，`eigfuns_precise` 当前闭式块积分的交叉项及统一质量归一化正确。审查者以独立 80 位完整物理传递矩阵、逐块 mpmath 求积及 48 点 Gauss 求积检验了实际函数。没有提供旧版源码，因此本审查认证当前实现的物理质量，不认证新旧函数逐字节相同。

## 实际执行

工作目录均为冻结审查根。解释器为 `C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe`，Python 3.10.11，Windows 10 build 26200。运行依赖为 numpy 2.2.6、scipy 1.15.3、mpmath 1.3.0、sympy 1.14.0；已保存 `runtime-versions.json`。

```powershell
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -B 'research/artifacts/proof-audit-round15-20261005/checks.py' --root 'F:/tools/math-audit-round15-20261005/review-input/software' --output 'F:/tools/math-audit-round15-20261005/reviews/software-run/properties-normal.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -O -B 'research/artifacts/proof-audit-round15-20261005/checks.py' --root 'F:/tools/math-audit-round15-20261005/review-input/software' --output 'F:/tools/math-audit-round15-20261005/reviews/software-run/properties-optimized.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -B 'F:/tools/math-audit-round15-20261005/reviews/software-run/reviewer_checks.py' --output 'F:/tools/math-audit-round15-20261005/reviews/software-run/reviewer-normal.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -O -B 'F:/tools/math-audit-round15-20261005/reviews/software-run/reviewer_checks.py' --output 'F:/tools/math-audit-round15-20261005/reviews/software-run/reviewer-optimized.json'
```

四个进程实际退出 0；冻结测试普通/优化各 92/92，审查者自写测试普通/优化各 103/103，无错误。没有仅阅读或采信作者已有 PASS 结果。

审查者测试独立写出完整物理 `(y,y')` 传递矩阵，作 220 次高精度局部二分，按块三角函数的所有内部零点核对物理模态，并独立计算加权质量；没有导入冻结的 `independent_physical.py`。局部频率种子来自待查实现，所以高精度细化本身不证明序号；序号依据是实际物理解的内部零点数。新增负对照还覆盖遗漏首两模态、把 lambda 错当 omega、过宽后端括号和后端异常传播。

## 有限验证结果

高反差 `[(.021,10000),(.958,1),(.021,10000)]` 的前六频率：

```text
0.7462197727914001
0.7604843852750858
2.2352811194758186
2.246563445569171
3.2657957507789526
3.7389256563222855
```

独立物理零点数逐项为 `0,1,2,3,4,5`。请求 `k=1,3,6` 的结果与六项序列相应前缀位级一致，冻结测试还实际检验了 `k=12`。审查者检测把第 3、4 模态谎标为第 1、2 模态时，内部零点计数为 `[2,3]`，能够识别遗漏；将齐次 lambda 当频率也不能满足 DD 端点条件。

对于旧网格尺度 `smax=pi*100*5+20, npts=30000`，我只计算了包含首两根的一个单元及端点物理值，没有重跑历史扫描。单元 `[0.7423964656698073,0.7954247775033649]` 包含两根，物理 DD 端点值分别为约 `0.0002738185639672711` 和 `0.006695304264906702`，同号。因此“逐单元端点变号”会漏掉这对根，当前按指标引擎避免这个具体机制。

R4 正对照 `[(.30,1),(.40,4),(.30,1)]` 的前三频率为 `1.7663647015038946,4.2893028029585105,7.097161081408613`，内部零点数为 `0,1,2`。冻结测试还实际核对了 `u=.40,.43,.45,.458` 的 FH 差分关系以及 SUP/INF 两个给定驻点的独立质量平衡。这些通过结果不能推出所有旧 R4 数据都错，也不能替代对某一其它历史数据的单独核查。

| 输入 | prop_to 最大相对/绝对混合矩阵误差 | 归一化样本最大绝对误差 | 实际 eigfuns 加权质量偏离 1 |
|---|---:|---:|---:|
| 高反差，6 模态 | 4.8406e-14 | 8.6944e-15 | 3.1086e-15 |
| R4，3 模态 | 4.8300e-16 | 1.8564e-15 | 2.2204e-15 |
| 齐次，3 模态 | 3.4626e-15 | 1.1102e-15 | 3.5527e-15 |
| 含 1e-12 短块，3 模态 | 2.5080e-15 | 1.8410e-15 | 3.7748e-15 |

矩阵误差按每项 `abs(double-mp)/max(1,abs(mp))` 计算。样本含端点、接口及乱序坐标。质量求积来自实际返回的特征函数，独立于实现使用的闭式积分。

## 范围与剩余边界

本次批准 R15-01 当前冻结版本的共享引擎委托、omega 单位、首模态和前缀行为、参数异常及弃用合同，并确认指定正对照下 `prop_to/eigfuns_precise` 的物理质量。未发现需返修的 R15-01 阻断项。

未验证的具体边界：未提供的全项目调用者及新旧完整源码字节差异；任意巨大反差/极高指标/所有浮点几何的成功可算性；遗留特征函数接口对 `s=0`、负频率或区间外点的扩展合同；任意历史扫描数据；严格浮点误差证书。后端对不可分辨问题抛异常是公开限制，不应把异常解释为不存在数学根。冻结测试中符号代数及有理括号的有限通过不等于解析无限维定理认证。本审查没有执行 Lean，没有颁发区间证书，没有执行或批准工具库接收。

## 本审查输出身份

| 输出 | SHA256 |
|---|---|
| software-run/properties-normal.json | 5158d44d668910735496a02af998e43bdf5b03caf34a8913861bcefb59ea3802 |
| software-run/properties-optimized.json | d3e1284394842aeee7da2124a2b3f8caa59325938dc7beda596b48d0ed76d940 |
| software-run/reviewer-normal.json | 95f266a01ebcd009cc7035ec2ec6714eb2e4ae4d4e3a4455758199f726c4477e |
| software-run/reviewer-optimized.json | 52b566389eed656d6a192f56a41ec107cf405f9ac8faf6b30e55933b88547a6b |
| software-run/reviewer_checks.py | 32eff9a508284174b622964f04842f5ab488d507f6310afea0e75452b87f4f4d |
| software-run/input-hash-final.json | 51f139a4785d0e09dd7b89f0918661c61f31ef77af496c1b1c13b72e914d1f34 |
