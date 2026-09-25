# round10 纯反射扰动生成器: 作者集成说明

候选模块为 `reflection_seeds.py`, 仅依赖 NumPy, 导入时无文件读写或项目依赖. 建议主作者审核后放入 `scripts/reflection_seeds.py`, 由 `_gapn2_symmetry_recon.py` 导入. 本交付没有改项目文件, 没有 commit/push. 本目录的测试是实现作者自检, 不是独立验收.

## 接口与几何含义

`R(x) = 1 - x[::-1]`, 因此 `DR(v) = -v[::-1]`.

| 接口 | 返回与约束 |
| --- | --- |
| `reflection_direction(Vector, Sector, Normalize=False)` | 实际 `Normalize` 为 keyword-only. `preserve` 返回 `(v-v[::-1])/2`, `break` 返回 `(v+v[::-1])/2`. `Normalize=True` 给欧氏单位方向. 两种模式均拒绝零投影. |
| `generate_sector_seed(BaseEdges, Sector, Step, ...)` | 选单位方向, 依次尝试 `Step/2**k`. 返回 `ReflectionSeed`, 含 `BaseEdges`, `Direction`, `RequestedStep`, `UsedStep`, `ActualStep`, `Widths`, `Edges`, `Z`, `Evidence`. |
| `interfaces_to_widths(Edges, MinWidth=1e-7)` | `MinWidth` 为 keyword-only. 检查严格内部接口及所有实际宽度严格大于下限, 返回 `diff([0, *Edges, 1])`. |
| `check_sector_seed(BaseEdges, Widths, Sector, ...)` | 从调用者提供的最终宽度重建接口并复查; 不修复数据. `Direction` 和 `ExpectedStep` 应一并传入以检查实际步长和方向. 返回可 JSON 序列化的检查记录. |

`preserve` 是接口位移反转后变号, 使镜像对称基点继续对称. `break` 是接口位移反转后不变号, 非零扰动打破基点的镜像对称. 不能再把二者混用为含糊的 `sym`/`asym` 标签, 更不能把普通随机宽度种子算作纯扇区种子.

## 直接接入 Recon

```python
from reflection_seeds import generate_sector_seed, SeedGenerationError, ZeroProjectionError

Rng = np.random.default_rng(20260925)
SeedRecords = []
for Sector in ('preserve', 'break'):
	for SeedIndex in range(16):
		try:
			Seed = generate_sector_seed(
				CenterEdges, Sector, 0.03,
				Rng=Rng,
				WidthsToZ=ReconObject.widths_to_z,
				ZToWidths=ReconObject.z_to_widths,
				SymmetrizeBase=True,
			)
		except (SeedGenerationError, ZeroProjectionError) as Error:
			SeedRecords.append({
				'Origin': 'pure_reflection_sector', 'Sector': Sector,
				'Index': SeedIndex, 'Status': 'failed',
				'Reason': str(Error), 'Evidence': Error.Evidence,
			})
			continue
		Label = f'pure_reflection:{Sector}:{SeedIndex}'
		Jobs.append((n, R, Mode, np.asarray(Seed.Z), Label))
		SeedRecords.append({'Label': Label, 'Status': 'accepted_seed', **Seed.to_dict()})
```

由主程序将 `SeedRecords` 写入其证据输出, 包括生成失败. 输入错误以 `ValueError` 明确拒绝; 非对称中心须由主程序显式报告并跳过该中心或重新获取合格基点. 不以一般根中“最对称”的一个自动当作合格基点. 求解器迭代后的根可能离开种子扇区; 这些标签只描述初始种子.

必须提供 `Vector` 或 `Rng` 中恰好一个. `Vector` 是待投影的原向量, 不是无条件被信任的方向. RNG 只负责给原向量, 投影后为纯扇区; 默认最多抽样 32 次, 零投影耗尽即失败. 指定向量零投影立即失败. 所有生成方向为单位向量, `Step` 必须为正; 反向扰动通过改变向量符号获得. 默认最多 80 次减半, 不裁剪或排序接口.

`BaseEdges` 的所有宽度也须 `>1e-7`. 默认要求浮点成对和正好为 1; 近似对称中心只在显式 `SymmetrizeBase=True` 且残差 `<=SymmetryTolerance` 时平均成镜像对, 中心接口置为 0.5. 默认容差为 `1e-12`, 可设范围为 `[0,1e-8]`; 明显不对称中心直接拒绝. 修正后的基点会再次检查宽度. 原基点、有效基点、修正最大量和是否实际修正均记录, 实际位移相对于有效基点测量. 成对和为 1 是浮点判据, 不声称位级实现精确实数反射.

## 回转检查与证据

两个转换回调必须同时给出, 并应是确定性的无外部副作用函数. 模块传入副本, 返回前实际计算 `ZToWidths(WidthsToZ(TargetWidths))`. 旧 Recon 的编码器含 `[2e-7,1-2e-7]` 裁剪, 所以目标宽度满足 `>1e-7` 还不足以保证回转忠实. 模块会同时检查扇区、方向和请求位移, 必要时减半重试. 如果基点附近的编码器本身无法忠实表示该扰动, 有界失败是预期行为, 不制造成功种子.

没有回调时 `Z=None`, 返回的 `Widths` 已按最终 `cumsum` 接口检查. 后续转换必须调用:

```python
from reflection_seeds import check_sector_seed

Z = ReconObject.widths_to_z(Seed.Widths)
ActualWidths = ReconObject.z_to_widths(Z)
Check = check_sector_seed(
	Seed.BaseEdges, ActualWidths, Seed.Sector,
	Direction=Seed.Direction, ExpectedStep=Seed.UsedStep,
)
```

后续转换如果失败, 应改为向生成器传入两个回调重新生成; 原无回调证据不能覆盖后来改变的几何. `check_sector_seed` 检查给定宽度和固定端点 `[0,1]` 重建的实际宽度, 二者均须严格大于下限. 宽度和的允许舍入差为 `8 * 宽度个数 * eps64`, 不进行归一化.

- `RequestedStep`: 调用者最初请求, 沿单位方向的长度.
- `UsedStep`: 最终接受的减半步长, 转换前的目标长度.
- `ActualStep`: 回转后位移在该单位方向上的实测投影系数. `FinalCheck.ActualLength` 另存实际位移欧氏范数.
- `FinalCheck.Displacement`, `CheckedEdges`, `InterfaceWidths`: 回转后的实际几何. `FinalWidths` 为转换器实际输出的宽度向量.
- `SectorResidual`: 实际位移落在另一扇区的投影最大范数. `SectorRelativeResidual` 除以实际位移最大范数, 默认容差 `1e-8`.
- `DirectionRelativeResidual` 和 `ExpectedRelativeResidual`: 方向拟合及目标位移误差, 分母同为实际位移最大范数, 默认容差 `1e-8`. 容差可在 `(0,1e-6]` 内设置, 实际数值均留证.
- `ResolutionFloor=32*eps64`: 实际位移最大范数未超过此阈值即报错. 微小但未通过相对残差检查的扰动也会拒绝. 这是保守的浮点解析度约束, 不声称可枚举所有数学上非零扰动.
- `Draws` 与 `Attempts`: 原向量、零投影重采样、逐次步长、不可行原因和回转检查. `Origin='pure_reflection_sector'` 配合 `DirectionSource='provided_vector'/'projected_rng'`; 普通随机宽度种子应沿用独立来源分类.

`Seed.to_dict()` 可用 `json.dumps(..., allow_nan=False)` 保存. `SeedGenerationError.Evidence` 和生成阶段的 `ZeroProjectionError.Evidence` 保存失败证据. 模块不自行写文件. 坐标属性为不可变 tuple, `Evidence` 是调用者持有的记录字典.

## 作者回归

在本目录运行:

```bash
python3 -B -W error test_reflection_seeds.py --evidence author-evidence-final.json
python3 -B -O -W error test_reflection_seeds.py --evidence author-evidence-optimized.json
```

可用 `--recon-source /absolute/path/to/_gapn2_symmetry_recon.py` 指定读取文件. 单次运行固定一份读取快照, 只 AST 选取并执行 `Recon.widths_to_z` 与 `Recon.z_to_widths`, 记录完整文件和两方法的 SHA-256 及方法原文. 不导入旧模块, 不执行 `main`, 不执行根枚举.

测试覆盖 `[1,2,3,4]` 的两个投影、互补/正交/归一化、零及非法输入、对称基点、显式微小对称化、大步长减半、真实 softmax 回转、保持扇区但改变步长的裁剪负例、无可分辨位移、恶意及修改输入的回调、有界 RNG 重采样和固定随机序列重现. 检查通过只支持本模块的有限行为回归, 不涵盖求解器收敛、完整谱枚举、Lean 或独立验收.

最终作者运行: normal 21/21, `-O` 21/21, 均开启 `-W error`, 绑定同一模块和测试文件字节. 原生日志为 `author-tests-final.log` 与 `author-tests-optimized.log`; 完整数值、运行环境和来源为同名对应 evidence JSON. `HANDOFF.json` 与 `HANDOFF.sha256` 绑定最终候选和证据, 可在本目录运行 `sha256sum -c HANDOFF.sha256` 检查. 这两条测试命令仅供后续重放; 重放时建议更换 evidence 输出名, 保留交付时的固定字节.
