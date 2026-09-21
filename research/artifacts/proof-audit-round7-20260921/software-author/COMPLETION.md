# 软件作者交付完成

状态: **SOFTWARE_AUTHOR_COMPLETE / INDEPENDENT_REVIEW_PENDING**.

- 协调器分配的 10 个候选脚本已完成本轮局部修订; 8 个原字节依赖未改. 主库、历史输出、插件、旧 Blueprint 未写入, 未 commit/push.
- 最终隔离复跑: 正常/-O 候选各 117/117; 原版各 79 项真实失败并退出 1. op03 四点直接 CLI 两种模式通过. 输入身份及原始进程回执已保存.
- 非驻点梯度、带秩一项的非驻点 Hessian 和驻点简式的适用范围分别记录. 数学推导及解析谱求和后端未获得整体验证.
- precise 的传播/加权范数故障按原字节保留为遗留限制; op03 只切换到已核对实际调用接口的既有 fixed. 没有额外依赖修复.
- 最后一次修改仅更正 README 的目标分配归属, 并完成元数据冻结. 不追加源码修订或行为测试.

独立复跑入口: 在复制后的整个包根运行 `python -B regression/replay.py --label independent-review`. 正常返回 0 表示候选通过且原版预期失败得到保留. 该脚本在新 work/replay 目录生成审查者自己的回执.

冻结清单为 `manifest.json`, 其 SHA-256 在 `manifest.sha256`. README、change-notes、候选、验证入口、现有结果与回执均由清单逐文件绑定. 最终打包回执见 `receipts/metadata-finalization/finalization.json`; 早期 manifest 和完整性检查保留溯源. 此处“冻结”指停止原位编辑并用哈希绑定, 不是声称挂载文件系统强制 WORM. 后续意见应产生新版本/新回执.

旧研究全扫描、完整数学推导、解析 Jacobian/Green 谱截断、密度二阶变分 P1/P2/P3、Lean/canonical 和 Windows 运行均未重新认证. 最终审稿结论由新的独立审查者给出.
