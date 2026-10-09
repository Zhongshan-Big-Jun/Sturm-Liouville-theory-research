# manage 问题知识复用的本地增量

本轮已实现 manage 2.1.0 的当前问题检索、完整条件、来源导航和经验复用.
当前执行源码为本机冻结 v13, 工作树与其逐项配对; 全局已安装入口未升级.
五问正向 v5 与最终软件 v13 独审分别通过, 所审版本与范围分开.
[源码配对和真实回执](SOURCE-PAIRING.json) 保留身份与原退回.

## 实际能力与复用

- 原 `query --context` 接受可选问题/目标/对象/条件/范围/类型. 查询词命中先于目标词和纯上下文建议, 每项保留理由、完整条件和未核对的桥梁. 排名及字符串相同不证明数学适用性.
- 新 `read` 有界读取当前正文及覆盖. 派生摘要随当前正文重建; 继承的作者断言保留旧来源和待重验状态, 不继续作为当前断言排序.
- 原 CLI 的 `context` 生成有界知识视图及阅读顺序. 明确区分数学依赖、方法相似、实现、引用、替代; Markdown 链接不造证明边, 未声明依赖保持未知. 超预算材料整项省略并给继续读取指针, 不截去关键条件.
- 原 `compare` 增加目标、容许类、假设、损失、已完成步骤、失效点及互补引理. 宿主提供解释/预测/检验; 候选依据重新过门禁, NO_RETURN 仍非数学反例.
- 理解页复用现有 `docs/PROJECT_UNDERSTANDING.md`, 只管理标记区域, 人的原前缀保持字节. 人工/并发冲突拒绝覆盖. 导出重新检查输入、批注、纠错及载入源码身份, 代码更新需要新 Python 进程.
- `source_id` 按捕获元数据、原始文件和提取文本聚合实时门禁. 对原 URL/version/raw/text 相同的已登记元数据快照追溯别名; 换标题、等价元数据路径或旧live文件缺失均不解除原隔离. 不同原来源或版本的元数据保持独立; 捕获格式及whole-file release义务不改. 双重path/source_id均核对, 矛盾选择拒绝; 元数据正常登记后不借共同文件名误合并不同来源, 精确别名与依赖义务仍有效. path-only三个成员也聚合门禁, 缓存投影字段不能授权复用; 首次纠错改变状态时旧包须重建, 导出实查来源/关系许可并保留旧字节. 当前声明ID高于缓存ID, 门禁从绑定快照同时保留耐久旧ID与源码声明的纠错义务, 不倒改旧登记.
- Lean 默认保持未知机器状态; 显式选中时调用原 lean-verify 收据/语义身份接口, 分开精确根、语义审查、开放连接与接收.

复用版本卡片、source capture/分段读取、批注、锁/原子写/journal、原纠错协议、
Blueprint gateway 和前轮唯一原生 `research_review` 适配. 没有新调度器、验证器或审批协议.
适配源码保持原字节. 使用指南见 [task-context.md](../../../_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/references/task-context.md).

## 同语料五问

[五问及常见误用](../../work/manage-context-20261009/cases.json) 使用同一12张卡片与11份原文,
[来源身份](../../work/manage-context-20261009/source-origins.json) 保留原路径/哈希.
[旧版](before-cases-final.json) 与 [冻结v13](after-cases-v13.json) 分开保存.
旧关键词本已找到主要有用材料, 新增价值主要是范围/缺桥/来源与防止旧错误复用.

| 问题 | 可复用范围 | 下一步数学检查 |
| --- | --- | --- |
| 整数阶 Riesz | 固定 c>0, 逐个整数阶的 Hermite-Legendre 替代系, 奇数阶需 r+1 个低提升; 原稀疏族障碍另列 | 对拟用 r 核对端点 jet、真实幂域和双向范数桥; 非整数阶与一致 c 界另证 |
| 任意删项 | 复 Krein 幂域 0<=s<7/2, 两支倒数和、发散侧闭包/密度和收敛侧无限余维; 临界值较少迹一侧 | 选择具体收敛保留集, 刻画闭包/连续零化泛函, 不将无限余维当完整元素描述 |
| 谱尾到界面 | 正有界实密度、实有界 h、完整排序归一 DD 谱及可靠包络 | 证明真实接口路径可微性、集中余项, 组合有限 -sum s_i*d_i^2*f'(a_i) 项; Q 为二阶导数的一半 |
| 全局谱隙 | G2 在固定 n>=2、紧 R 区间上的全部精确零点, 包括 R=1 | 全部 R>1/全部精确零点的 ND 与条件化唯一性分开; ND/G1、无条件唯一仍开放 |
| 修正旧工具/路线 | 连续有限核、总变差与带符号质量收敛; 窄脉冲仅否定旧发散理由, 有界方向替代卡另有范围 | 常密度/真实切空间标定后补齐接口项与严格集中误差; 原 issue/下游精确义务不释放 |

宿主与独立使用者均阅读所供原文合同. 知识包仍有深度、大小和索引覆盖限制:
整数问可能省略一项前置材料并给指针; repair 仍附加三个明确的上下文建议,
默认查询未直接找到全部替代材料, 需继续读来源及使用历史精确 ID 替代导航.
不宣称全面语义检索或性能提升. 独审的范围与未做检查保留完整原件.

## 本项目整合与 Lean

仅新增 [有界到界面缺桥](cards/sl-bounded-to-interface-route.md)、
[窄脉冲重开条件](cards/sl-pulse-obstruction-route.md) 与 [weighted-DD 局部候选](cards/sl-weighted-dd-local-lean.md).
它们经既有 API 登记, 使用 [范围索引](scoped-index.json); 主 `index/tools.json` 未改.
[原项目门禁](original-live-gate.json) 与隔离测试 issue 分开, 原34项阻断保留.
新的候选/替代导航不是旧工具 release 或工具库/Blueprint 接收.

前轮证明仍见 [Lean 入口](../lean-development-20261008/README.md).
[v4 实际选中重查](lean-recheck-summary-v4.json) 的 weighted-DD 精确根通过且语义审查身份匹配.
这是保存收据重查; 原检查器执行了 `lean --deps` 解析既有 import, 没有重放目标证明或重编全库.
v13 的消费接口与 v4 同源, 未伪称第三次重验. 一般密度完整谱/排序、B11、ND/G1 等连接仍开放.

## 重放

当前冻结 `F:/tools/manage-context-20261009/source-freeze-v13`, 244文件 manifest SHA256
`3a18b98aefb24764b4d038aa705a1787316cc7a82c6543d1d5894dd9b5087f74`.
版本 manage2.1.0/lean2.1.2/workflow2.0.2/rigorous2.0.1; 旧冻结及真实负面/中止记录原样保留.

```powershell
$Py = 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe'
$Freeze = 'F:/tools/manage-context-20261009/source-freeze-v13'
$ManageScripts = "$Freeze/plugins/manage-math-research-program/skills/manage-math-research-program/scripts"
$SL = 'F:/LaTeX/BVE research'
$Fixture = "$SL/research/work/manage-context-20261009"
$env:PYTHONPATH = 'F:/tools/lean-joint-20261008/plugin/test-deps'
$env:PYTHONDONTWRITEBYTECODE = '1'

& $Py -B -X utf8 "$ManageScripts/research_library.py" query --project $Fixture --index index/after.json --query '整数阶 Riesz'
& $Py -B -X utf8 "$ManageScripts/research_library.py" context --project $Fixture --index index/after.json --query '谱尾 界面' --limit 5 --depth 1 --max-chars 48000 --entry sources/research_map.md
& $Py -B -X utf8 "$ManageScripts/research_library.py" read --project $SL --index research/artifacts/manage-context-20261009/scoped-index.json --tool research/artifacts/manage-context-20261009/cards/sl-weighted-dd-local-lean.md

Push-Location $Freeze
& $Py -B -X utf8 -m unittest discover -s "$ManageScripts/tests" -p 'test_*.py' -v
& $Py -B -X utf8 scripts/validate_all.py
& $Py -B -X utf8 tests/smoke_research_library.py
& $Py -B -X utf8 tests/smoke_blueprint_gateway.py
Pop-Location

Push-Location "$SL/_xsoc1_work"
& $Py -B -X utf8 plugins/manage-math-research-program/skills/manage-math-research-program/scripts/tests/test_library_q9_reuse.py -v
& $Py -B -X utf8 scripts/regen_manifest.py plugins/manage-math-research-program/skills/manage-math-research-program
Pop-Location
```

Q9 源仓库检查使用其现有基准材料, 不将冻结便携套件的跳过计作通过.
manifest 重建在开发工作树执行; 冻结源码与已有证据保留原字节.
五问重复脚本在 `F:/tools/manage-context-20261009/run_cases.py`, 使用新 `--tag` 保留旧输出.
复杂上下文 JSON 见指南; 重建索引需显式原卡片根. `--include-affected` 只作历史讨论.
显式 Lean 重查在上述 context 加 `--recheck-lean --lean-tools`
`F:/tools/lean-joint-20261008/plugin/source-freeze-v4/plugins/lean-verify/scripts`;
默认不调用编译器. gateway 的 ensure/snapshot 已真实读取, 未写 canonical;
runtime API manage/1.7.0 与插件开发版本分开.

## 实际验证

冻结v13便携122项: 121通过/1可选Q9缺材料跳过; 源仓库Q9另实跑通过.
35项 context 检查包括三份捕获组成文件分别隔离、仅改标题的新ID及等价路径、
旧比较读回/理解页、关系/导出和耐久版本快照. 库7项、gateway及validate81通过; 官方manifest生成器已实跑并逐字节配对.
原生 receiver 保留 v3-v8/v11 软件真实退回, v9/v10中止且没有完成/批准.
[五问正向 v5](<F:/tools/manage-context-20261009/review-forward-receipt-v5.json>) 与
[最终软件 v13](<F:/tools/manage-context-20261009/review-software-receipt-v13.json>)
均实际APPROVED并已接收, 不据此批准完整数学证明.
[实跑命令和输出](<F:/tools/manage-context-20261009/TESTS-v13.json>) 保留通过/跳过区别.
测试模拟回执、研究复用审查与数学证明/形式化接收分别解释.

两边 AGENTS/历史及既有续接位置已同步实际状态.
[最终保护检查](<F:/tools/manage-context-20261009/preservation-final-v13.json>) 实跑通过: 原文件无丢失及范围外变化,
人的原文/历史、主索引、canonical/inventory、唯一适配器及Git身份保持; 244份源码与冻结配对.
随后只追加此说明并做小范围字节/链接复核, 未重跑软件或Lean检查.
上述验收交付时仅本地, 未提交/推送/发布/全局安装或接收canonical/解除原纠错义务.
后续用户已明确授权本轮两仓上传; [发布范围与Lean证据还原](../lean-development-20261008/PUBLICATION.md) 单独记录,
安装和数学/canonical接收状态不因发布升级.
