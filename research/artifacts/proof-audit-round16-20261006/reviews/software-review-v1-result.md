# 第十六轮软件冻结包 v1 独立回执

日期：2026-10-06。审查任务身份：`/root/r16_software_review`。

**结论：REJECTED_SOFTWARE_V1 / REQUEST_CHANGES。** R16-01、R16-02 的受影响入口检查通过；R16-03 的规定 `2^-40`、`2^-50` 薄块与新增方向断点检查通过，但共同小段在密度块内部时仍可能丢失细小半宽。需修订下述具体入口，再冻结新字节另审。此回执只针对本次冻结包，不是工具库自动接收、Lean 回执或无限谱尾证明。

## 输入身份与隔离

唯一项目材料为 `F:/tools/math-audit-round16-20261006/software-review-v1/manifest.json` 及其 `root/` 下 15 项冻结文件。开始时与结束时逐项核对文件大小、SHA-256，均 15/15 一致。未读取实际工作区 AGENTS、记忆、其它审查、报告或作者会话；未修改冻结包；未委派其它 agent。

Manifest SHA-256：`cae843faf25316e86ed8cc753d69d1c81926ea6a9bd2b19b6cc780b545628e0d`。

受影响源码身份：

| 文件 | SHA-256 |
| --- | --- |
| `misc/rigid1d.py` | `4ade74f1274bbfd296736410ac18953e5f0c64ffb107980e1d6175f80cefec55` |
| `scripts/_gapn2_second_variation_probe.py` | `cb855ece3374129e794d9a922e779bd182ec0ef645f97e9823e401fb51373e85` |
| `scripts/_gapn2_symmetry_recon.py` | `4f418bdca359c64e7ad6298ad01b6b80f0dc46d8484b2155bcf18623bc529713` |

全部 15 项读回在包外 `software-review-v1-independent-manifest-check.json`，SHA-256 `115cd9405d96b8c8a77e2d2b827a1b6ff25c6b8ab512cfdfc23a9c2256505fb2`。补测输出另保存全部 15 项实际源哈希与实际导入路径，项目依赖均从冻结 root 加载。

解释器为 `C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe`，SHA-256 `3cce33d75d6fdae4e004d0bdf149320b3147482a9caf370079dcb9c191a1b260`；实际 Python 3.10.11、NumPy 2.2.6、SymPy 1.14.0、mpmath 1.3.0。所有数值执行设置 `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=1`，使用 `-X utf8 -B`，优化重放再加 `-O`。

## 确认通过的有限范围

| 实际执行 | 结果 | 包外原始证据 |
| --- | --- | --- |
| 原 `checks.py` 普通重放 | 170/170，exit 0 | `software-review-v1-independent-normal.json`、同名 `.log` |
| 原 `checks.py` `-O` 重放 | 170/170，exit 0 | `software-review-v1-independent-optimized.json`、同名 `.log` |
| 自编独立补测普通重放 | 174/174，exit 0 | `software-review-v1-extra-normal.json`、同名 `.log` |
| 自编独立补测 `-O` 重放 | 174/174，exit 0 | `software-review-v1-extra-optimized.json`、同名 `.log` |
| 完整 n=2、R=4、sup CLI，61 模式 | exit 0；P1 3、P2 8、P2b 6、P3 3 条 | `software-review-v1-independent-cli-sup.json`、同名 `.log` |
| 完整 n=2、R=4、inf CLI，61 模式，`-O` | exit 0；相同分组计数 | `software-review-v1-independent-cli-inf.json`、同名 `.log` |

上述 174 项不包含下一节另行追加的共同中点反例，因此全部通过并不支持整体批准。

R16-01：两个指定负例确实不能返回 True；独立核对了精确中心、半宽、二阶界和修正项，七个非二进制分区完整覆盖原区间。错误端点、顺序、计数、宽度、预算、布尔方向及回调返回类型按入口契约拒绝；1、2、3、4、8、13 个盒预算均未多执行下一个盒；诚实正性与负性正例通过。返回 False 始终按“未证明”解释。

E1 静态调用检查：`e1_certgen._taylor` 在分区前转换为 Fraction，专用证明路径没有引用或调用 `der_sign2` / `der_sign_adaptive`；57 个命名契约仍在且互异。独立精确分区边界试验通过，专用路径也拒绝指定整数负例。此次两助手缺陷没有构成撤回原 57 账的理由。

R16-02：rho=2、h=2、61 模式的解析配对恢复 `Cu=I`、`Cw=2I`，n=20、60 的 Q 与 `(2n+1)pi^2/2` 一致；3/61 模式前缀一致，值和导数使用同一质量。普通回调 MaxOrder=64、128、255、256、512、1023 均在不足预算内拒收并记录 UNRESOLVED，回调没有超过显式阶数预算；默认 1024 完成两次稳定比较。其状态是 CONVERGED_NUMERICAL_ESTIMATE，误差是估计，`black_box_error_enclosure=None`、`sign_certified=False`，没有冒充认证误差。

R16-03：多个方向新断点与真实密度薄块的 `delta=2^-40`、`2^-50` 配对、共同质量、Parseval 权重经 90 位物理 IVP 和直接积分对照通过；方向断点、密度断点及额外切点全部加入共同分块。折叠普通节点拒绝，`2^-40` 普通节点正例通过。另核对小相位 Taylor 极限、混合小/大相位消去回退、相近频率、块归属，以及带负号的浮点 Parseval 残余原样保留。

完整 CLI 的 P2b 和 P3 确实走活动配对入口；两组都以 256 阶结束回调适配，每条均保存配对诊断且 `sign_certified=False`。P3 的有限差值实际不为零，本回执未据此推出任何极限、发散或符号定理。

冻结包内的 R14 保留接口另实际核对：共享驻点守卫对普通已解点接受，对求解失败、非驻点扰动、微小分母配置拒绝；谱表几何/边界/一基目标及覆盖拒绝；零/负参数 Green、乱序及重复坐标；独立边中心差分的真实转换和 CROSS 分块；非驻点的一般商法则 Jacobian 项。R15 枚举器高反差 1/3/6 前缀、相位索引、不可分辨 tol 拒绝、弃用参数行为也通过。`op03_gap_fixed.py`、`op03_gap_fh.py`、`_sl_prufer.py` 字节与 manifest 一致。

raw K/SKS 装配模块不在这 15 项材料中，故未执行它的完整回归，也不声称全面重验所有 R14 或 R15 历史程序。没有审查或认证无限证明；原检查的 r=1..6 有限例子仅作为有限精确诊断。

## 唯一要求修改的发现：共同小段半宽在密度原点偏移中丢失

位置：`scripts/_gapn2_second_variation_probe.py:355`，`_analytic_pairings` 计算

```python
Offset = Left - self.edges[Index] + Length / 2
```

当方向切点在一个宽密度块内部、共同小段只有一个坐标 ulp 时，最后的加法可能把半宽舍掉。此时局部正弦积分仍使用非零 Length，但 Center 取在左端而非实际中心，从而遗漏局部位移；这正是该入口声称保留细小半宽的情形。

独立复现输入：

```python
Blocks = [(1.0, 1.0)]
Left = 0.5
Right = math.nextafter(0.5, 1.0)
Delta = Right - Left  # 2^-53
Probe = SpectralProbe(Blocks, Modes=4, Order=64)
Direction = block_direction([0.0, 1/Delta, 0.0], [0.0, Left, Right, 1.0])
Result = Probe.pairings(Direction)
```

该方向积分精确为 1，端点在二进制坐标中严格不同；结构化入口实际接受。v1 中 `Left + Delta/2 == Left`。

参考使用同一冻结引擎返回的二进制频率，并在 90 位精度下独立计算原物理初值 `(u,u')=(0,1)` 的质量与小段积分，因此不混入根身份或换一组归一化的差异。

| 配对（模态为一基） | 冻结 v1 | 独立 90 位参考 | 仅包外内存中以小段左端锚定的比较 |
| --- | ---: | ---: | ---: |
| C(1,2) | `+2.4492935982947064e-16` | `-4.526443397722557e-16` | `-4.526443397722557e-16` |
| C(2,2) | `1.110967067159104e-31` | `1.835449602266039e-31` | `1.835449602266039e-31` |

配对量级很小，处于全局浮点误差量级；本发现没有建立任何 Q 或数学符号结论翻转。要求修改的是实际共同小段推进的几何语义及局部消去精度，不能以普通样本全过关闭该具体义务。建议在每个共同小段左端取得现有共同质量归一化的值/导数，之后只推进局部 `Length/2`，或对不能保留半宽的输入明确拒绝。修后必须另外覆盖此方向独有切点的反例，而不只覆盖密度已有同一断点的薄块。

实际证据：`software-review-v1-midpoint-probe.py`、`.json`、`.log`。比较仅在包外测试脚本内进行，冻结活动实现从未被修改。

## 重放命令与输出身份

以下均是实际执行过的命令；输出根为 `F:/tools/math-audit-round16-20261006`，冻结 root 为 `F:/tools/math-audit-round16-20261006/software-review-v1/root`：

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
$reviewPython = 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe'
$frozenRoot = 'F:/tools/math-audit-round16-20261006/software-review-v1/root'
$reviewOutput = 'F:/tools/math-audit-round16-20261006'
& $reviewPython -X utf8 -B "$frozenRoot/research/artifacts/proof-audit-round16-20261006/checks.py" --root $frozenRoot --output "$reviewOutput/software-review-v1-independent-normal.json"
& $reviewPython -X utf8 -O -B "$frozenRoot/research/artifacts/proof-audit-round16-20261006/checks.py" --root $frozenRoot --output "$reviewOutput/software-review-v1-independent-optimized.json"
& $reviewPython -X utf8 -B "$reviewOutput/software-review-v1-extra.py" --output "$reviewOutput/software-review-v1-extra-normal.json"
& $reviewPython -X utf8 -O -B "$reviewOutput/software-review-v1-extra.py" --output "$reviewOutput/software-review-v1-extra-optimized.json"
& $reviewPython -X utf8 -B "$frozenRoot/scripts/_gapn2_second_variation_probe.py" 2 4 sup --modes 61 --quad-order 64 --dps 40 --fd-steps 0.001 --bump-width 0.0005 --output "$reviewOutput/software-review-v1-independent-cli-sup.json"
& $reviewPython -X utf8 -O -B "$frozenRoot/scripts/_gapn2_second_variation_probe.py" 2 4 inf --modes 61 --quad-order 64 --dps 40 --fd-steps 0.001 --bump-width 0.0005 --output "$reviewOutput/software-review-v1-independent-cli-inf.json"
& $reviewPython -X utf8 -B "$reviewOutput/software-review-v1-midpoint-probe.py"
```

命令实际经 PowerShell 将全部标准输出/错误保存到所列 `.log`。CLI 的 cwd 为冻结 root；没有隐式使用实际项目文件。

| 包外产物 | SHA-256 |
| --- | --- |
| `software-review-v1-extra.py` | `11307032dfa1acb89a6b588a8f28c016bd49526e00dd4308d27db7bf1c936cd6` |
| `software-review-v1-midpoint-probe.py` | `20be8ee2c49daebf3fd6f81e7b364a4a36abc8057a07c4661cf04c523d969723` |
| `software-review-v1-independent-normal.json` | `eaf26878d0eccfa51b0981c4619e0605ac7805f3ac92f9bb27175d51888342a9` |
| `software-review-v1-independent-optimized.json` | `247e60ccc342bbbad92c6be2f2e19fb30fe119dc37401fe29dd78719ef0f4e88` |
| `software-review-v1-extra-normal.json` | `967ff0c1e38f942b66b68baaa7fcb2069dcc6020bbd9e7c19611f1035967a0d5` |
| `software-review-v1-extra-optimized.json` | `bce877bfcc9bcb4804f6d17cc1e02751ba1fb74bce0872512fab823c062316cc` |
| `software-review-v1-independent-cli-sup.json` | `532626093440fecb5a01c79b2af30e3a1a2d8ad509b7ae18834b328bfbd5298c` |
| `software-review-v1-independent-cli-inf.json` | `2dfba9ba0b77dba02826f4898145c7817915342bd0de0337ae86ba835aefafab` |
| `software-review-v1-midpoint-probe.json` | `f81ef22519ded9661116cabf39ebcfce2e01c462235b8450adf50a1c82c90475` |

## 额外范围执行及停止记录

审查者曾额外启动 E1 全账生成：

```powershell
& $reviewPython -X utf8 -B "$frozenRoot/misc/e1_certgen.py" --output "$reviewOutput/software-review-v1-independent-e1-ledger.json"
```

协调器随后纠正本轮范围：专用 E1 57 项全账不属于新增重算范围，只做静态调用/类型边界核对。审查者据此匹配脚本、唯一包外输出及解释器后停止 PID 43404；原执行实际 exit -1。保留了 20 条部分 PASS 的原始日志和仍为 RUNNING 的原始状态文件，没有完整 ledger 输出；**未计作 57 项重验通过，也未更改或撤回原账**。这是审查者主动扩张执行范围后被纠正的记录，不能用这部分日志填补验收。

原始停止证据为 `software-review-v1-independent-e1-stop.json`，SHA-256 `9b1a385412f7f8fcb112eb6e8c0945c3545466e3bbdc42bb4ee26abc9e6d7bee`；部分日志 SHA-256 `621fba3b5524aaee714ee30bd78ed7bc47f991f7719dd58fcf294178496cd5ad`；RUNNING 状态 SHA-256 `a3e61bdcf36b3b62315f94f8e8f0d5b2f301118c600f8f6972f059d1d280b613`。本节只保存真实执行状态；本次结论仍为对冻结软件 v1 的上述具体退回。
