# 第七轮独立可执行检查作者交付

**正常模式 25/25, `python -O` 25/25, 数学结果逐组一致.** 包含 24 个数学/反例检查组和 1 个执行完整性组, 不是 25 个定理认证. 两个额外的旧 FH 公式负对照进程均按预期退出 1, 证明优化模式没有跳过失败门.

本目录是新实现的作者成果. 输入报告所提缺失附录和原 `checks.py` 未提供, 没有重放它们. 本任务未写主库, 未执行仓库程序/旧 Blueprint/Lean/历史证书, 未评价其它作者修订候选.

| 核心结果 | 实测/精确值 |
|---|---|
| W, n=2,x=1/2 | 正确 -4pi, 旧式 -6pi |
| 固定 n 的 f 端点 x² 系数 | `2pi^4(n^4-(n+1)^4)` |
| n=2 t 根与归一化 det | `(11+-2sqrt(10))/36`; `7030400000*pi^4/4782969` |
| `[1,4,1]`, a=1/4, n=1 双接口导数 | `53.880972160240571523695242987489...`; 旧式为一半 |
| 独立中心差分末步误差 | h=1e-11, 约 `9.23e-20`, 三步显示 h² 收敛 |
| 同一第一模态的 `[u'']` | `-4.383575835224494279617373829...`, 非零 |
| R7-P01 固定 L2、rho=2 | 旧预测 1, 真导数 2 |
| R7-P02 | 正 det 不蕴含定号; f'/s 与归一化 K 的因子不同; 逐元素乘法可抹掉 Hessian 非对角元并改变惯性 |

一般 n 构造检验包含平台的精确积分、20 组平台界、12 组有限中心取零多项式子空间界、4 个高精度谱样本及标量极限. [推导说明](derivations.md) 明确 n 维平台与余维 n 子空间的变分接口. **有限测试不构成无限维证明, 不认证全部 G1'/G2 或局部定理整条证明链.**

文件入口:

- [checks.py](checks.py): 独立实现, 所有验证门显式 raise, AST 检查无 assert.
- [outputs.json](outputs.json), [outputs.optimized.json](outputs.optimized.json): 每组结果、精度、环境、源码/输入哈希.
- [执行汇总](receipts/execution-summary.json): 两模式和两个负对照的真实退出状态.
- [normal 回执](receipts/normal.execution.json), [optimized 回执](receipts/optimized.execution.json): 命令、时间、退出码、stdout/stderr 与输出哈希. 同名 `.stdout.log`/`.stderr.log` 保存原日志.
- [propagation.md](propagation.md): 直接调用、参数约定、R7-P01/R7-P02 与需主库更改的路径/行号. 另发现 4 处 ndarray Hessian 逐元素乘法, 已列明; 主库修订由协调器负责.
- [输入身份](inputs/manifest.json), [扫描身份与命令](receipts/source-scan-manifest.json), [产物清单](artifact-manifest.json).
- [AGENTS.md](AGENTS.md): 工作方法及本任务具体对话/维护记录.

重跑本目录的新检查:

```bash
cd '/mnt/f/tools/math-audit-round7-20260921/checks-author'
python3 -B run_checks.py
```

实际环境为 Python 3.14.4, SymPy 1.14.0, mpmath 1.3.0, mp.dps=90. 需要已安装这两项第三方依赖. 运行器实际启动 normal、`-O` 和负对照, 并写回本目录. 高精度计算使用解析分块积分, 不是严格有向舍入区间计算.

`receipts/initial-24/` 保留用户追加 R7-P02 前的 24 组源码、输出及回执; 其历史 cwd/output 路径描述的是当时运行位置, 移入该子目录后仍以原哈希核对. 最终 25 组以根目录文件与当前 execution-summary 为准. `outputs.development.json` 和 development 日志为首轮试跑, 不替代正式回执.
