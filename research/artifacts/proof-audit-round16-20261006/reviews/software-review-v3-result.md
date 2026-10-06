# Round16 软件冻结包 v3 独立审查

日期：2026-10-06。实际审查身份：`/root/r16_software_review_v3`。

**结论：REJECTED_FOR_SCOPED_SOFTWARE_INTEGRATION。** R16-01 的精确类型修复与本轮已测配对、薄段、拒绝合同大部分通过；v3 的混合大小相位局部积分仍有可复现消去误差，因此不放行 R16-02/03 的最终软件整合。此结论只针对下述冻结字节，不评价协调者随后可能形成的修订版本。

## 输入与独立性

仅使用 `F:/tools/math-audit-round16-20261006/software-review-v3/manifest.json` 和其 `root/` 下清单列出的 15 项完整文件。未读取项目 AGENTS、记忆、其它审查或项目报告，未加载技能，未委派，未修改任何输入。独立辅助程序与全部输出均写在包外。

开始和结束核对 15 项 SHA-256 与字节数全部一致。manifest SHA-256：

`566f6a18d8869b83b61544e39abfb61c9520a294afe121634c15d56b8dfb9287`

输入核对实据为 `software-review-v3-start-sha.json` 与 `software-review-v3-end-sha.json`。没有伪造 UUID、旧自动接收、Lean 或 canonical 接收身份。

## 实际执行

解释器：`C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe`，Python 3.10.11；NumPy 2.2.6、mpmath 1.3.0。每次科学 Python 调用均设置 `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=1`，使用 `-X utf8 -B`，优化重放另加 `-O`。

| 执行 | 实际结果 | 输出 |
| --- | --- | --- |
| 包内 `checks.py --root <frozen root>` 普通 | 192/192 PASS，退出 0 | `software-review-v3-checks-normal.json` |
| 同一包内检查 `-O` | 192/192 PASS，退出 0 | `software-review-v3-checks-optimized.json` |
| 独立辅助检查普通 | 131 项，125 PASS、6 FAIL，退出 1；执行异常为 null | `software-review-v3-independent-normal.json/.log` |
| 同一独立辅助检查 `-O` | 同样 125 PASS、6 FAIL，退出 1；执行异常为 null | `software-review-v3-independent-optimized.json/.log` |
| 完整 CLI `2 4 sup --modes 12 --quad-order 64 --dps 45 --fd-steps .001 .0001` | 退出 0；P1/P2/P2b/P3 全执行，分别 3/8/6/3 条 | `software-review-v3-cli-sup.json/.log` |
| 完整 CLI 同参数 `inf` | 退出 0；同样完整 3/8/6/3 条 | `software-review-v3-cli-inf.json/.log` |

独立辅助程序：`software-review-v3-independent.py`。可用上述解释器及环境运行 `--output <outside.json>` 复现；结果有其 SHA-256、实际优化标志、所有检查数据与失败项。汇总在 `software-review-v3-summary.json`。

## 通过范围

1. R16-01：两通用 Taylor 入口任何端点运算前均转 Fraction；独立五分区检查所有区间相接且完全覆盖，负相邻浮点端点亦保留完整精确实区间。要求的整数 `[0,1]` 三分区反例及 `[1,nextafter(1,2)]` 反例在固定/自适应入口均不返回 True。严格端点零、无效类型/顺序/计数/宽度与不可越过预算等检查通过；False 文本明确为 unproved。诚实正负例通过。
2. E1 仅 AST 静态追踪：`e1_certgen::_taylor` 第一条语句是 `a,b,Target=F(a),F(b),F(Target)`，没有通用 `der_sign2/der_sign_adaptive` 导入或调用。未运行 57 条账、未改写其身份、未调用退役 Decimal。
3. `rho=2,h=2` 保留 61 模态，在独立 Order=8/16 下得到配对单位阵；n=1/17/58/60 的有限 Q 与 `(2n+1)pi²/2` 比对通过，原包还实际执行其它阶数/分块/阶次。默认四数组携带 diagnostics，Parseval 原始残差不截零，不认证符号。
4. 薄密度/方向断点完整合并。除包内 `2^-50` 外，独立检查了宽密度内部方向独有 one-ulp 段、rho=3.7 的二进制 2/7 节点、rho=.25 的 1/7、rho=7 的 1/3、内部 rho=9/.125 的对称节点、四段非对称密度中独立高精度定位的第六模态内部节点，以及 `2^-50,rho=7` 薄密度段与另一个方向断点。它们与同一 binary64 频率、100 位物理 IVP 及独立质量积分比对通过；没有用精确 DD 频率替换给定浮点频率。
5. 上述 oracle 直接传播物理 `(u,u')` 并独立积分 `rho*u²`，不调用包内 mp reference、相位函数或配对助手作为数值真值。共用初始导数归一化与独立质量比对通过。
6. 实际普通 Gauss one-ulp/薄段节点折叠拒绝；callback 相位分辨守卫在不满足时先拒绝、尚不调用回调。61 模态中 256/512/1024 阶实际形成两次连续比较；仅到 512 阶仍 unresolved。收敛预算、NaN、形状错误、无效预算、局部正积分下溢与能量溢出拒绝通过。
7. 冻结材料中可执行的 R14/R15 合同检查通过：高反差 k=1/2/4/7/9 枚举前缀不变；不可能精度请求拒绝；DD/DN Green 在乱序/重复坐标、零/负参数与极点附近正确处理；谱表几何/边界/覆盖/删极点身份守卫保持；一般非驻点商导数 M1 修正、驻点相对守卫、无块宽地板、Jacobian 交叉块与错误 commuting 输入拒绝均通过。没有在此最小包外重跑完整 R14 核程序或历史扫描。

## 具体缺口：混合相位的 sinc 差与和消去

`scripts/_gapn2_second_variation_probe.py::_cos_sin_integrals`（冻结行 249–276）只在全部相位小于 .05 时使用双变量 Taylor；其余情况下，正弦积分的 mp 回退由 `minAngle<1e-4` 或近乎完全消去判据触发。稍高于阈值仍可能丢失多位有效数字；余弦积分的 sinc 和没有对应稳定回退。

独立 100 位直接积分观察如下，均按同一二进制输入值提升再运算：

| 数值对象 | 输入 | 相对误差 |
| --- | --- | --- |
| 正弦 S00 | Waves=[.01,1,100], Length=.02 | `1.5179701311887922e-8` |
| 正弦 S02 | 同上 | `1.4387873465420446e-12` |
| 余弦 C01 | Waves=[.01,100], Length=2*float(pi)/100 | `5.300346563112645e-9` |
| 余弦 C01 | Waves=[.0001,100]，同 Length | `5.3011885496594355e-5` |
| 余弦 C01 | Waves=[1e-7,100]，同 Length | `0.3653263540863396` |

这 5 项按独立审查的 `4e-13` 相对比对门槛失败。最后一项积分本身很小；此处相对误差专门检查局部消去，不将它误称已发生大的整体 Q 错误或符号证书错误。

更关键的是实际合法公开配对入口也触发同一问题（第六项失败）：

```python
delta = 2.**-20
blocks = [(.5,1.), (delta,4e10), (.5-delta,1.)]
P = SpectralProbe(blocks, 61, 8)
h = block_direction([1e10,0.], [0.,.021,1.])
R = P.pairings(h)
```

首/末频率为 `.010239958516243496` / `163.36277503636384`。最小局部半相位 `.00010751956442055672` 未触发 mp 回退。实际 `Cu[0,0]=3.2369520159398766`；同一首频率的 100 位物理 IVP 与独立质量给出

`3.236952023951395600396694160128588876282`。

相对误差 `2.475019388557898e-9`，绝对约 `8.01e-9`，不满足独立真实入口 `3e-12` 相对检查。当前 Gram 误差 `2.8328e-9<2e-8`，因此入口返回数据。它仍正确标记 `sign_certified=False`、无 roundoff enclosure；**本审查没有发现伪造符号认证**。缺口是声称稳定局部解析计算的实现仍有可放大的消去误差。

4 个方向宽度 .02/.021/.023/.05 的实际入口观察保存在 `software-review-v3-mixed-phase-observation.json`；余弦问题另存在 `software-review-v3-cosine-cancellation.json`，最终普通/-O 辅助结果包含直接复现。

建议下一版本对每对模态分别处理小相位和相对消去，同时稳定 sinc 差与和，并按所需消去位数选择高精度回退。该建议尚未在 v3 中实施或验收；不能将作者后续修复意向当作本冻结版通过。

## 失败记录与未执行边界

最初辅助程序用 `ast.unparse` 文本比较时漏计 Python 3.10 的目标 Tuple 括号，18 项处失败。这是审查 harness 错误，已改为 AST 结构检查；原输出保留 `software-review-v3-independent-attempt1-harness-error.json`。随后首次发现消去缺口的 80 项执行保留 `software-review-v3-independent-attempt2-mixed-phase-gap.json`，完整 126 项阶段保留 `software-review-v3-independent-attempt3-126.json`。最终 131 项普通/-O 均跑完，六项同一局部稳定性问题不通过，未抹除失败。

能量溢出负例产生一次 RuntimeWarning 后抛 ArithmeticError；这是实际执行的拒绝结果，不是接受非有限能量。

未进行区间认证、无限尾/全模态符号认证、任意 callback 的证明、完整一般整数定理审查、Lean、57 账重算、旧 Decimal 复活、旧自动工具库接收、canonical 接收、历史数据重认证或云端发布。包内 r=1..6 的有限代数例已实际随 192 项执行，但不作为一般整数解析定理的证明。

最终 15 项输入 SHA 与字节数仍全部匹配；软件包不放行，具体待修点限于上述稳定局部积分路径。
