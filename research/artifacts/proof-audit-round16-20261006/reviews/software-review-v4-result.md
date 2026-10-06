# 独立最终软件审查 v4

日期：2026-10-06。实际原生审查身份：`/root/r16_software_review_v4`。

结论：**APPROVED_FOR_SCOPED_SOFTWARE_INTEGRATION**。这份冻结软件在 R16-01、R16-02、R16-03 的指定有限合同内通过静态审阅、普通／优化重放及独立补测；没有发现阻断本合同的实际软件错误。结论绑定下面的 15 项文件字节，不认证任意黑箱函数的误差包络、无限谱尾或 Q 的符号。

唯一项目输入为 `F:/tools/math-audit-round16-20261006/software-review-v4/manifest.json` 和其 `root/` 下 15 项完整文件。没有读取 AGENTS、记忆、其它审查回执／报告、作者会话或包外项目文件；没有委派，没有修改冻结包。只在 `software-review-v4-*` 包外路径保存本次执行与审查输出。

## 输入身份

清单 SHA-256：`8bd0cbcf6ce99c2376bc6d83e4aa98e1b6fb98553eb59859be97186c37b6cce0`。
开始及结束各实际核对 **15/15** 字节数与 SHA-256，全部与清单相同。原始核对分别保存在 `software-review-v4-start-sha.json`、`software-review-v4-end-sha.json`。

| root 内路径 | 字节数 | SHA-256 |
| --- | ---: | --- |
| misc/rigid1d.py | 14408 | 4ade74f1274bbfd296736410ac18953e5f0c64ffb107980e1d6175f80cefec55 |
| misc/e1_certgen.py | 9751 | db92fc5dbeaa0f2ec5f399320210d7d4246c08b7e146d86d8602ba1429bdb829 |
| scripts/_gapn2_second_variation_probe.py | 40265 | 6410e71518c7e59ffd7f67342a809ab2dd827a5de66c2bc984172d68dd190f44 |
| scripts/op03_gap_fixed.py | 4898 | 5dab895bc9c574ea48aa35eff337f33e38a6a3d11d4b4eb7d5e48e58fe54d9df |
| scripts/op03_gap_fh.py | 749 | 9cea8a73ade19abe5e7d530eab553571fc5cc5ff87242db2997a78a9efb1c0b8 |
| scripts/op03_gap_table.json | 11319 | dbad285bddf2bfeb728b67f98a303f25e5fe3f7e59d4219f1470d360e53790bd |
| research/artifacts/proof-audit-round16-20261006/checks.py | 15654 | a183247c3a43f8fbe884bf2d2fdf4e0015919eea5e2b2bf8c890fa35a2c474f8 |
| scripts/_sl_prufer.py | 7125 | 489f14986ea61f1560b338a0ae6a33e0da3f2c1fc30c77e8272c9f0ca6a34042 |
| scripts/_gapn2_symmetry_recon.py | 25078 | 4f418bdca359c64e7ad6298ad01b6b80f0dc46d8484b2155bcf18623bc529713 |
| scripts/_gapn2_jacobian_probe.py | 10274 | 793705efee95718b7917ba3669e1bc2108fc5f7ed1205b226f9ed5679451b7dd |
| scripts/_gapn2_jacobian_analytic.py | 10412 | 4d7cb5385b6f2b8d668ec4c5c417876a57713b6780bb11e1478cb0fcbc00aa02 |
| scripts/_gapn2_jacobian_spectral.py | 4926 | 227c40a23cdd04e3c64c56e4d8895cb3355a952001603f184ce65de6e0ab149e |
| scripts/_sl_spectral_identity.py | 7711 | c763b576b6af23f4b2db33b198059eea69560a5949d4119571daccefc75cebe9 |
| scripts/reflection_seeds.py | 17364 | 66f0473302b56b3cca3d8e2b0b70dd733d024da33b449ea166692d85b51fe317 |
| misc/e1_certificate_io.py | 17819 | 65bab32c155fae9402b35a10d1c482c220cbf85648ae133e9a219cdd39c3a940 |

## 实际执行

每次 Python 调用均先设置 `OPENBLAS_NUM_THREADS=1`、`OMP_NUM_THREADS=1`；解释器为 `C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe`，参数 `-X utf8 -B`，优化运行另加 `-O`。

| 执行 | 结果 | 主要输出 |
| --- | --- | --- |
| 包内完整 checks.py，普通模式 | PASS 205 项 | software-review-v4-checks-normal.json |
| 包内完整 checks.py，优化模式 | PASS 205 项 | software-review-v4-checks-optimized.json |
| 本审查独立补测，普通模式 | PASS 105 项 | software-review-v4-independent-normal.json / .log |
| 本审查独立补测，优化模式 | PASS 105 项 | software-review-v4-independent-optimized.json / .log |
| 完整 R4 SUP CLI，一次 | 退出 0，P1=3 / P2=8 / P2b=6 / P3=3，8 项 P2b 投影诊断 | software-review-v4-cli-R4-sup.json / .log |
| 自拟大反差谱的有界 30 个候选 | 20 个可分辨、10 个明确拒绝，拒绝项未返回配对/Q | software-review-v4-case-search.py / .json |

命令的实际参数为：

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -B 'F:/tools/math-audit-round16-20261006/software-review-v4/root/research/artifacts/proof-audit-round16-20261006/checks.py' --root 'F:/tools/math-audit-round16-20261006/software-review-v4/root' --output 'F:/tools/math-audit-round16-20261006/software-review-v4-checks-normal.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -O -B 'F:/tools/math-audit-round16-20261006/software-review-v4/root/research/artifacts/proof-audit-round16-20261006/checks.py' --root 'F:/tools/math-audit-round16-20261006/software-review-v4/root' --output 'F:/tools/math-audit-round16-20261006/software-review-v4-checks-optimized.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -B 'F:/tools/math-audit-round16-20261006/software-review-v4-independent.py'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -O -B 'F:/tools/math-audit-round16-20261006/software-review-v4-independent.py'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -B 'F:/tools/math-audit-round16-20261006/software-review-v4/root/scripts/_gapn2_second_variation_probe.py' 2 4 sup --modes 12 --quad-order 64 --dps 50 --fd-steps 0.0001 --output 'F:/tools/math-audit-round16-20261006/software-review-v4-cli-R4-sup.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -B 'F:/tools/math-audit-round16-20261006/software-review-v4-case-search.py'
```

独立补测脚本 SHA-256：`2e3d3750d44c793f4a85ff5a715ee78cbb42095e13bde94d710b27ec9b4465a2`。不导入包内 checks.py；接受逻辑不用 `assert`，所以优化运行仍真正执行。

## 合同判定

**R16-01 通过。** 两入口在顺序比较、跨度、分区端点、中心及半宽的算术前转为 Fraction。整数 `[0,1]` 的三分区假正例、相邻浮点端点假正例均实际不返回 True。类型、布尔标志、正整数计数、顺序、最小宽度与预算检查在普通及优化模式有效；自拟巨大整数端点、负浮点相邻端点、非二进制有理分区和诚实正例通过。自拟三盒预算只调用回调六次，耗尽后不再评估下一盒。另一个确实处处导数为正的函数在粗分区 False、细分区 True，验证 False 只表示未证。E1 只静态检查其专用 `_taylor` 的首条赋值已转 Fraction，且无两受影响入口调用；未运行 57 账或 Decimal 退役引擎。

**R16-02/03 通过指定有限数值检查。** rho=2、h=2 的 61 模态矩阵为数值单位矩阵，独立补测额外核对 n=1,3,17,59,60 的 `Q=(2n+1)pi²/2`。包内与独立补测均覆盖 `2^-50` 薄密度／方向段及完整 rho/h 切点；实际普通 Gauss 节点折叠明确拒绝。解析路径不依赖薄段全局浮点中点或节点掩码，采用局部半宽和真实密度归属，保留已有物理采样器的一份共同质量。

独立参考从相同二进制频率的物理 IVP `y(0)=0,y'(0)=1` 出发，用 110 位传播、不同于包内中点/Taylor 公式的高精度直接块质量，再在真实方向段积分。不将二进制频率换成精确 DD 根。one-ulp 方向独有薄段覆盖常密度半点、rho=3 的二进制舍入 1/3、非恒定对称密度的内部近节点，以及另一个非恒定密度 1/3 点；近节点平方及交叉项吻合，局部半宽与小振幅未丢失。`1e-60`、`1e-140` 与大波数混合的局部 sine/cosine 积分也与独立 MP 积分吻合；正局部积分或正相位下溢均拒绝。

独立实际大反差谱为 `[(.25,1),(2^-19,1e11),(.75-2^-19,1)]`，61 模态，方向 `3e8 * 1_[0,.018]`。最低／最高频率分别为 `0.00528790640009044`、`119.79746224979344`，局部半相位分别为 `4.7591157600813956e-5`、`1.078177160248141`，确实跨过整体小相位 Taylor 分支门槛。配对 (0,0)、(0,1)、(0,60)、(1,60) 的相同 IVP 参考相对误差约 `1.53e-16`、`1.57e-16`、`2.14e-15`、`2.71e-15`。

一般回调先做实际节点及模态相位检查，独立记录三次采样 `[16,32,64]` 后才满足两次连续比较；预算 16、32、63 分别拒绝，交替不收敛回调在 128 耗尽时拒绝，61 高模态而预算 128 时在调用回调前拒绝。成功返回的四数组保留 diagnostics，CLI 各 P1/P2/P2b/P3 及投影计算均实际保存诊断。原始 Parseval 残差逐元素与 `Energy-sum(Cu²)` 相同；独立常密度例的 11 项小负浮点残差（最小 `-2.220446049250313e-16`）原样保留。所有成功诊断 `sign_certified=False`，不把数值稳定估计当成可靠包络。

**既有合同的有限保留检查通过。** 包内共享物理质量、R4 驻点受理、Green 的真实坐标顺序及零参数极限、减极点目标身份／几何／边界／覆盖守卫、非驻点一般 Jacobian 的分母导数项、驻点 Jacobian 交叉分块和拒绝将 commuting Hessian 交给该接口均有实际补测。大反差 `lams_precise` 的 k=1,3,6 前缀逐位相同、相位指标正确；不可分辨 tol 拒绝，非默认 smax_scale 发出弃用警告。没有改写历史原/共轭核语义或将有限 Green 和浮点检查宣称为尾证书。这些检查只覆盖冻结包实际包含的入口，未全面重认证过去各轮源码或历史扫描。

## 失败记录及修正

首次独立补测在自拟更不易分辨的非对称大反差谱 `[(.375,1),(2^-19,1e11),(.625-2^-19,1)]` 的谱守卫中止，原 JSON／日志保存为 `software-review-v4-independent-attempt1.*`。有界候选搜索确认这一组的明确拒绝；最终补测保留该拒绝检查，并使用上面的可分辨实际谱继续 IVP 配对。没有放宽谱守卫或修改冻结软件。

第二次独立补测普通／优化均在我写的非驻点 Jacobian 等式检查中止：初始 harness 对代数重排的两种浮点求值要求 `np.array_equal` 过强。实际差为 `2.7755575615628914e-17`；修为明确的浮点求值误差比较后普通／优化各 105 项通过。原失败保存为 `software-review-v4-independent-attempt2-normal.*`、`software-review-v4-independent-attempt2-optimized.*`。这次修正仅发生在包外审查 harness，没有更改生产代码或数学恒等式。

## 执行边界与未执行项

- 这些是有限软件性质、独立高精度数值对照与一个完整 CLI 的实际运行，不是无限范围数学证明。
- 一般回调误差比较及 MP/解析浮点评估均没有区间包络；任意黑箱窄峰或未声明断点的误差没有获得认证。这是接口已明确报告的限制，不构成本轮合同的新阻断发现。
- 未运行 E1 57 条证书、退役 Decimal、历史扫描、第二项完整 R4 CLI、全部旧 R14/R15 回归、Lean、自动工具库接收或 canonical 接收；不声称这些工作已完成。
- 未审查 C16-TAIL 与 C16-A10-INTEGER 的完整解析论证。包内 checks 的有限 Hermite/Sympy 例子不代替这两项数学审查。
- 审查期间冻结包 15 项字节保持不变；开始／结束身份均已实际核对。
