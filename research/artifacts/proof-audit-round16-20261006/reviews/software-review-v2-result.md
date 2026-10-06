# 第十六轮软件冻结包 v2 独立审查

结论：**REJECTED，R16-03 的近节点方向独有薄段仍有具体缺口。** R16-01 的精确 Taylor 修订与 R16-02 的有限配对/回调检查未发现新的阻断项。不得把本回执转换成批准或作为后续修订的验收。

实际审查任务身份为 `/root/r16_software_review_v2`，日期 2026-10-06。此身份来自原生 collaboration 任务路径；没有生成或声称旧式 UUID、Lean 回执、自动工具库接收或 canonical 接收。

只使用 `F:/tools/math-audit-round16-20261006/software-review-v2/manifest.json` 及其 `root/` 下清单所列 15 项完整文件。未读取实际项目 AGENTS、记忆、其它审查回执、作者会话或 R16 交付报告；未委派、未改冻结输入。所有补测和报告在包外。

## 输入完整性

开始和结束核对均为 15/15 SHA-256 与字节数匹配，结束与开始逐项相同。manifest 的开始/结束 SHA-256 为 `4e9fd94185d4edb8678df619ef8c195fe3f10ba039c51e34080637e92e7fa98e`。

逐项记录见 `software-review-v2-start-hashes.json` 和 `software-review-v2-end-hashes.json`；路径均位于 `F:/tools/math-audit-round16-20261006/`。

| 冻结 root 相对路径 | SHA-256 |
| --- | --- |
| misc/rigid1d.py | 4ade74f1274bbfd296736410ac18953e5f0c64ffb107980e1d6175f80cefec55 |
| misc/e1_certgen.py | db92fc5dbeaa0f2ec5f399320210d7d4246c08b7e146d86d8602ba1429bdb829 |
| scripts/_gapn2_second_variation_probe.py | 5d2caea2308f9140a3f037bf1c291d7643b68cc47a4429535e5b92a4d7fdaa80 |
| scripts/op03_gap_fixed.py | 5dab895bc9c574ea48aa35eff337f33e38a6a3d11d4b4eb7d5e48e58fe54d9df |
| scripts/op03_gap_fh.py | 9cea8a73ade19abe5e7d530eab553571fc5cc5ff87242db2997a78a9efb1c0b8 |
| scripts/op03_gap_table.json | dbad285bddf2bfeb728b67f98a303f25e5fe3f7e59d4219f1470d360e53790bd |
| research/artifacts/proof-audit-round16-20261006/checks.py | 85676b5c9d9c75a03bcf93da655ca5560471964157a9f4a51a8c6abed78bba9a |
| scripts/_sl_prufer.py | 489f14986ea61f1560b338a0ae6a33e0da3f2c1fc30c77e8272c9f0ca6a34042 |
| scripts/_gapn2_symmetry_recon.py | 4f418bdca359c64e7ad6298ad01b6b80f0dc46d8484b2155bcf18623bc529713 |
| scripts/_gapn2_jacobian_probe.py | 793705efee95718b7917ba3669e1bc2108fc5f7ed1205b226f9ed5679451b7dd |
| scripts/_gapn2_jacobian_analytic.py | 4d7cb5385b6f2b8d668ec4c5c417876a57713b6780bb11e1478cb0fcbc00aa02 |
| scripts/_gapn2_jacobian_spectral.py | 227c40a23cdd04e3c64c56e4d8895cb3355a952001603f184ce65de6e0ab149e |
| scripts/_sl_spectral_identity.py | c763b576b6af23f4b2db33b198059eea69560a5949d4119571daccefc75cebe9 |
| scripts/reflection_seeds.py | 66f0473302b56b3cca3d8e2b0b70dd733d024da33b449ea166692d85b51fe317 |
| misc/e1_certificate_io.py | 65bab32c155fae9402b35a10d1c482c220cbf85648ae133e9a219cdd39c3a940 |

## 实际执行

解释器是 `C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe`，实际 Python 3.10.11，64-bit AMD64。每次 Python 执行前均在 PowerShell 设置 `OPENBLAS_NUM_THREADS=1`、`OMP_NUM_THREADS=1`，并使用 `-X utf8 -B`；优化模式另外使用 `-O`。

以下命令中的 `$PY` 指上述解释器，`$ROOT` 指冻结 `root/`，`$OUT` 指 `F:/tools/math-audit-round16-20261006/`；实际工具调用使用完整绝对路径。

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
& $PY -X utf8 -B "$ROOT/research/artifacts/proof-audit-round16-20261006/checks.py" --root $ROOT --output "$OUT/software-review-v2-checks-normal.json"
& $PY -X utf8 -B -O "$ROOT/research/artifacts/proof-audit-round16-20261006/checks.py" --root $ROOT --output "$OUT/software-review-v2-checks-optimized.json"
& $PY -X utf8 -B "$OUT/software-review-v2-independent-checks.py" "$OUT/software-review-v2-independent-normal-v2.json"
& $PY -X utf8 -B -O "$OUT/software-review-v2-independent-checks.py" "$OUT/software-review-v2-independent-optimized-v2.json"
& $PY -X utf8 -B "$ROOT/scripts/_gapn2_second_variation_probe.py" 2 4 inf --modes 10 --quad-order 64 --dps 40 --fd-steps 0.001 --output "$OUT/software-review-v2-cli-inf.json"
```

- 包内 checks：普通与优化模式均 `PASS 184 properties`，退出 0。
- 独立补测：普通和优化模式各 71 项，67 通过、4 失败，均退出 1；无未处理组异常。4 失败是下列两个输入各自的平方和交叉配对，属于一个近节点锚点缺口。
- CLI：`n=2,R=4,INF`，10 模态、Order=64、40 位、一个 FD 步长、固定 bump 半宽 5e-4，退出 0；P1=3、P2=8、P2b=6、P3=3，逐行 diagnostics 已保存。输出见 `software-review-v2-cli-inf.json`，日志见 `software-review-v2-cli-inf.log`。正常执行不是截断 Q 符号或 P3 极限的认证。
- 最终独立脚本 SHA-256：`ac11977cd15485d025569e1f98d0e8e3021f9c4cc72bde5713aa7fb3d0c043b2`。

保留首轮审查脚本及结果 `software-review-v2-independent-checks-initial.py`、`software-review-v2-independent-normal.json`、`software-review-v2-independent-optimized.json`。首轮脚本额外报告一项 E1 静态检查失败，原因是比较 `ast.unparse` 文本时误要求赋值左端不含括号；实际 AST 和源码的首句均是先转 F。最终脚本改为检查 AST 结构，E1 项通过；没有改任何冻结输入，也没有删除首轮记录。

## 阻断缺口：局部半宽保留后，宽块内左锚点仍失真

`_analytic_pairings` 在第 343 行用 `eigenfunction_states(..., Knots[:-1])` 取得所有左锚点状态；第 355–362 行确实用局部半宽推进并积分，没有丢失一 ulp 小段的半宽。但左锚点由 `_sample_solution` 第 99–104 行经 `_transfer_matrix` 得到；后者第 72–76 行先把 `Wave * Length` 舍入为 binary64，再计算 cos/sinc。宽块内方向断点靠近模态节点时，这个相位乘法及传播消去的误差已经进入左端状态，后续局部 Taylor/sinc 不能恢复。

### 完整输入 A

```python
Blocks = [(1.0, 1.0)]
Modes, Order = 6, 8
Left = float(1/3)                       # 0.3333333333333333
Right = math.nextafter(Left, 1.0)       # 0.33333333333333337
delta = Right - Left                   # 5.551115123125783e-17 = 2^-54
Direction = block_direction([0., 1/delta, 0.], [0., Left, Right, 1.])
```

第 3 模态使用冻结程序实际返回的 binary64 频率 `9.42477796076938`；参考没有换成数学精确的 `3*pi`，没有高精度重求根。

| 配对 | 冻结 v2 输出 | 同一浮点频率的 110 位物理 IVP 参考 |
| --- | --- | --- |
| C33 | 8.433138578625724e-32 | 4.8107259030910521913246981525576427894187645257588786512066577927e-32 |
| C13 | -2.409723609052609e-16 | +6.1085911528233920259062943273823091074870782783996657203018841623e-17 |

C33 相对误差 `0.75298671105064429490756405297198073`，C13 绝对误差 `3.0205827243349481966884095553549812e-16`。交叉配对数值符号相反；这仅说明该局部配对的数值错误，不是任何 Q 符号证明。返回状态仍为 `NUMERICAL_ANALYTIC_EVALUATION`，Gram_error 约 8.88e-16，故目前 Gram 检查不能发现此缺口。

### 完整输入 B

```python
Blocks = [(0.25, 1.0), (0.5, 4.0), (0.25, 1.0)]
Modes, Order = 6, 8
Left = 0.5
Right = math.nextafter(Left, 1.0)       # 0.5000000000000001
delta = Right - Left                   # 2^-53
Direction = block_direction([0., 1/delta, 0.], [0., Left, Right, 1.])
```

小段完全位于宽密度块 `(0.25,0.75)` 的内部，密度没有对应断点。实际第 2 模态 binary64 频率为 `3.8212664724980367`。

| 配对 | 冻结 v2 输出 | 同频物理 IVP 参考 |
| --- | --- | --- |
| C22 | 6.620066623604503e-32 | 6.9624814255891543814655215723888108237125034069882816431163844514e-32 |
| C12 | -1.1279505597216472e-16 | -1.2156156244336319281214776723224548709682453137458572574516336635e-16 |

C22 相对误差 `0.049179995041161185916329776195952114`，C12 绝对误差 `8.7665064711984688466594011761045479e-18`。同样没有返回未决状态。

这些量的绝对尺度很小，因此本审查没有据此声称常规 Q、谱编号或整个研究结论错误。但 R16-03 要求宽密度块内部的方向独有一 ulp 段、近节点小相位消去可靠；仅修局部半宽不能完整关闭这项义务。应在活动修订中解决近节点左锚点相位和多块传播消去，或在无法可靠计算时明确拒绝该配对，然后另外冻结新版独立验收。不要提高 Gauss Order 或放宽此近节点验收阈值来消除失败。

参考在独立脚本中以分段常系数物理 IVP `(y,y')=(0,1)` 传播，用高精度直接积分计算共同质量；在每个一 ulp 小段以局部参数 `x=Left+delta*t`、`t∈[0,1]` 积分，不构造舍入的全局中点。90/110 位结果稳定；每个方向的质量 `Fraction(1/delta)*(Fraction(Right)-Fraction(Left))` 都精确等于 1。参考是高精度数值核查，不是区间认证。完整重放见 `software-review-v2-independent-checks.py`；首次 100 位探索及五个输入见 `software-review-v2-nodal-exploration.py/json`。

## 已通过的有限检查

- R16-01：源码的两通用入口均先经 `_sign_inputs` 把左右端点转 Fraction，之后才做跨度、分割、中心和半宽算术。整数/相邻 float 两个原假阳性在普通及 -O 下都没有 True；类型、次序、格数、宽度、预算负例通过。另测 400 位大整数、最小正 subnormal 端点、负相邻 float、非 bool 符号、非法 max_n 和严格五盒预算；False 明确写 unproved。回调提供有效 D2 包络是使用前提。
- E1：只作 AST/静态追踪，`_taylor` 首句将 a/b/Target 转 F，导入和调用均没有受影响的 `der_sign2/der_sign_adaptive`。没有重算 57 项台账或运行退役 Decimal。
- R16-02：包内 rho=2,h=2 的 61 模态在 Order 32/64/128 和不同密度分块下，配对 I 及 Q=(2n+1)pi²/2 检查通过。独立 rho=4,h=-3 的 41 模态配对 -.75 I、Q=9(2n+1)pi²/64 通过。普通回调实际依次评估 256/512/1024 节点并比较两次；缺预算时返回 UNRESOLVED 且抛出。折叠节点、错误形状、非有限样本和非法预算拒绝；估计误差、缺 enclosure、sign_certified=False 均保留。
- R16-03 的非节点范围：delta=2^-50 密度薄块及方向独有薄段的完整质量配对与独立高精度参考一致；密度/方向/额外切点联合的区间计数通过。不能解析的累计密度端点拒绝。常密度 dyadic .5 左锚点的一 ulp 近节点例通过，失败是上述更一般的左锚点。
- 保留范围：R15 高反差 indexed prefix 在请求 1/4/7 模态时一致，tol=1e-20 拒绝，非默认 smax_scale 的弃用警告及频率不变通过。DD/DN 谱身份、Green 几何/边界/覆盖/删极点负例、mu=0 的无序重复坐标、正极点拒绝、值/导数共同质量、无人工宽度地板、求解失败不当驻点、Jacobian 交叉块及远离驻点的 quotient 修正有限检查通过。没有据此重认证旧历史扫描或所有 Green 理论。

## 未执行和结论边界

没有读取或重放历史扫描、重新计算 E1 57 项、重认证退役 Decimal、做 Lean、自动接收/canonical 写入、云端发布或环境安装。没有用有限脚本证明无限谱尾或全整数定理。CLI 的有限截断、浮点 Parseval 残差和误差估计不构成区间包络或 Q 符号认证。

v2 输入始终未变；在同一明确软件义务内发现近节点缺口，因此本次只能退回该冻结版本。其它已通过项保留其有限证据身份。
