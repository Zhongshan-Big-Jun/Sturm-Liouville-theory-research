# 2026-10-09 研究 Lean 与插件联调的可重放入口

本轮完成一个真实且有范围的数学/工程增量. 源码配对与真实回执见 [SOURCE-PAIRING.json](SOURCE-PAIRING.json). 研究及插件仍是原 HEAD 下的未提交工作区; 联调显式执行外部源码冻结, 没有改全局安装缓存.

三个非空根在 [SLVerified](../../../lean-proof/SLVerified.lean), 独立预写合同在 [targets](../../../lean-proof/targets.json). 10 个主题模块证明实际区间复 L2、Krein 积分代表的商类不变迹/边界/作用、复线性、任意 L2 二阶数据构造与正向弱导数、原边界多项式的成员/作用/Green 能量, 以及任意正有界可测密度的真加权范数桥和全部正常密度 DD 指标的实际归一化积分解. 三根合取项数为 8/4/2. 这些子引理并没有 14 份单独严格回执; 实际合成的三个根由既有验证器验收.

最终 exact job `sl-exact-roots-v3-20261009` 已 SUCCEEDED/exit0, 三根 exact_root_passed=true. [机器汇总](verification-v3/development-result.json) 保留执行时 semantic=not_reviewed, 后完成的真实独立语义审查在 [单独身份绑定](semantic-review-v3/binding-results.json); 不覆盖旧机器 manifest. 正式入口 build 实跑成功. 原默认全库 build 实跑 FAILED/exit1, 错误是受保护的 B3 草稿第56行未闭合注释. 原 SL.+ 范围和 53 份旧源保持, SLDrafts 未单独构建.

最终插件源码 v4 的 lean-verify 为 2.1.2, manage/workflow 为 2.0.2, rigorous 为 2.0.1. 241 个冻结文件与工作区逐项一致. v3/v4 30 份运行脚本、template/schema 字节一致; v4 只修正测试故障注入时点, 因而 v3 的真实严格研究执行与原真实15项测试明确配对, 没有伪称 v4 重跑. v4 实跑新增开发11项、便携21+12项、workflow28项及仓库validate81项全部通过. manage87沿用先前相同源执行, 未在v4重跑. 原首次正负审查、打印省略失败、两根复现交叉生成失配和测试注入失败均保留.

新入口 lean_develop.py 复用现有 FeedbackSession/LSP/CLI、verify_lean_project/lean_evidence、lean_routes 与 workflow. 宿主写数学候选, 工具提供项目/mathlib 检索与真实类型探针、增量试验、反馈后新鲜保存、非空根清单核验及可续接任务. 它没有模型执行器, 不宣称自动证明. 新入口拒绝项目内或祖先输出目录, 绑定完整工具集合, 在慢读取后核对同一批次版本, 并对仍含省略符的类型返回未完成. cmd、Lean/Lake及辅助子进程隐藏运行; native GetConsoleWindow=0 已实际验证.

真实开发过程包括 Krein 与常 DD 候选的失败反馈、修订、经新入口保存, 随后编译真正的合取根. 初轮由 v1 入口完成; 修补后由最终 v4 入口对同字节根再次 trial/save, 再用最终 v4 status 核对 v3 已完成精确任务. 原型反馈、缓存和保存不被当作正式机器证据. 原冻结 v1/v2/v3, 旧 v2 目标清单和全部原始日志按原路径保留.

三个全新上下文分别完成实际类型盲读、另人原文/合同语义比对及软件修补审查, 均由真实 task_name/fork_turns=none 调用及既有 prepare/dispatch/receive 保存 APPROVED. 这些是冻结范围内的审查. 数学审查没有另行重跑内核, 软件审查的具体执行范围及限制见 [原始回执](reviews/). 自动核验不判断合同是否代表完整原文; 两种证据分别报告.

逆向经典弱 H2 等价, 全复域能量/自伴正性/真逆与 Hc 幂域仍未建立. 后续由这些基础接 A10 整数 Hermite-Legendre 替代系、A1/A12 完整族与余有限闭包、A11/有限约束; weighted 由真实谱存在/完整谱及排序接 B11/谱比/谱隙. DN 当前只落实边界谓词, 一般密度模型没有缩成连续或有限分块密度. ND/G1/无条件唯一没有作为公理. 没有 Linux/WSL、云CI、全局安装、工具库/canonical 接收或发布验收; 没有统计性提速结论.

以下命令使用固定 Windows 原生工具链. `--output` 必须在 lean-proof 外, 重放到新的目录. 新目录验证不会覆盖已有 verification-v3 证据. 状态命令只续读已经结束的任务; 不再次 start 同一个 job.

```powershell
$TaskPython = 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe'
$LeanDev = 'F:/tools/lean-joint-20261008/plugin/source-freeze-v4/plugins/lean-verify/scripts/lean_develop.py'
$LeanProject = 'F:/LaTeX/BVE research/lean-proof'
$LeanExe = 'C:/Users/HuangZY/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe'
$LakeExe = 'C:/Users/HuangZY/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lake.exe'

# 保存证据的新鲜度核对; 不重做内核证明.
& $TaskPython -X utf8 $LeanDev --project $LeanProject --output 'F:/LaTeX/BVE research/research/artifacts/lean-development-20261008/verification-v3' --lean $LeanExe --lake $LakeExe --direct --timeout 600 status --job-id 'sl-exact-roots-v3-20261009'

# 在新目录从独立合同重新验证三个根; 实际执行可能耗时.
$ReplayOutput = 'F:/tools/lean-joint-20261008/replay-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
& $TaskPython -X utf8 $LeanDev --project $LeanProject --output $ReplayOutput --lean $LeanExe --lake $LakeExe --direct --timeout 600 verify --targets 'F:/LaTeX/BVE research/lean-proof/targets.json'

# 当前项目和固定 mathlib 的源码搜索, 然后实际核对选定接口.
$DiscoveryOutput = 'F:/tools/lean-joint-20261008/discovery-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
& $TaskPython -X utf8 $LeanDev --project $LeanProject --output $DiscoveryOutput --lean $LeanExe --lake $LakeExe --direct search --query 'HasDerivAt' --limit 20
& $TaskPython -X utf8 $LeanDev --project $LeanProject --output $DiscoveryOutput --lean $LeanExe --lake $LakeExe --direct --timeout 180 probe --import 'SL.Weighted.ConstantDD' --name 'SL.Weighted.ConstantDD.constant_dd_l2_root'

# 正式入口和默认旧全库使用独立命令, 后者的已知历史错误仍在.
Set-Location -LiteralPath $LeanProject
& $LakeExe build SLVerified
& $LakeExe build
```

小步试写/保存使用同一全局参数后接 `serve --backend cli`, 将外部完整候选交给 trial, 确认实际 candidate_checked 后按返回的 receipt 调用 save. 最终v4实际交互原件在 SOURCE-PAIRING 引用的 final-root-roundtrip-v4/host-protocol.json; 该文件也包含真实调用参数. 插件通用 fixture 和研究数学结果分开记录.


## 2026-10-09 后续上传授权

上文保留本地验收时的实际状态. 用户后续明确授权上传最新插件与研究仓库; [上传范围与大证据还原](PUBLICATION.md) 单独登记, 原证明、源码冻结与回执字节不修改. 远端结果以实际commit及读回为准, 发布不补齐开放数学连接.
