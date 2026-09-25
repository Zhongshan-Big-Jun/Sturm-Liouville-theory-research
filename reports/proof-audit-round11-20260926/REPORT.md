# 第十一轮审计修订与余有限闭包补证

日期: 2026-09-26. 输入为用户提供的 `C:\Users\HuangZY\Downloads\sl_audit_round11`. 用户补充“重新看一眼”后目录已可读取. 基线为 `4f6b35cbdc433d2d319cd3e483b6dbf0af3f9d87`. 指定的 math-research-workflow 2.0.1 及相关已安装模块按原版使用.

两项程序错误已复现并修复. 新的余有限闭包证明在固定 c>0、整个 0<=s<7/2 窗口内通过独立解析审查, 含三个临界点. 当前工具库的纠错、版本批注、实际检索和独立局部 Lean 检验已分别完成. 这些结论不表示全仓库数学认证、全参数数值认证或完整形式化.

阅读入口: [余有限证明 PDF](../../docs/SL_cofinite_all_orders.pdf), [精确工具卡](../../tools/krein-cofinite-closure-all-orders.md), [Jacobian 修订契约](../../research/artifacts/proof-audit-round11-20260926/jacobian-repair.md), [研究地图](../../research_map.md), [项目理解](../../docs/PROJECT_UNDERSTANDING.md).

## 1. 输入核实与错误修复

[输入核实记录](../../research/artifacts/proof-audit-round11-20260926/intake-verification.json)保存12项提交清单检查, 并核对附件恢复的两份源码与当前 Git blob/工作树字节. 附件及作者提出的证明均作为待核查证据, 没有直接沿用其中的验收标签. 附件20组检查在隔离副本中以普通模式及 `-O` 回放通过.

| 发现 | 核实与实际修改 | 保留的边界 |
| --- | --- | --- |
| R11-01: 对反对易 Jacobian 取了零对角块 | `jacobian_cross_blocks` 检查 JP=-PJ, 提取求和/作差坐标中的 C,D, 使用 detJ=(-1)^n detC detD. 原 `sym_antisym_decomp` 保留入口, 返回语义为 C,D. O3 调用和输出解释同步修正 | Hessian及跳量加权矩阵可以与P对易, 继续采用其自己的对角分块; 未把所有矩阵统一换块 |
| R11-02: 裁剪与归一化改变了差分路径 | `jac_fd` 从独立接口坐标构造正负端点, 步长按相邻宽度缩小, 有界回退, 校验基点、正宽度、总长和真实往返位移. 无法忠实实现或无法分辨时明确报错. P3 保存每列实际端点和接受步长 | 默认返回仍是 ndarray. 可选诊断不是严格误差证书; 足够窄的合法基点可能被保守拒绝, 不保证所有可行几何都能计算 |

实际 R=1、n=2 的常密度驻点给出

$$
\det J=\frac{7030400000\pi^4}{4782969}>0,
$$

旧分块函数却返回两个零矩阵. 窄层反例使用宽度 `(0.25,3e-7,0.4999994,3e-7,0.25)`. 在解析残差适配器下, 旧 Jacobian 最大误差约6.3617339224; 新实现约2.42e-8, 独立实际 Recon 核对约7.49e-9. 这些误差属于对应浮点试验, 不构成通用误差界.

静态调用清单含64个相关文件, 其中21个命名 `jac_fd` 调用文件及2个交叉分块调用文件. 清单不表示所有历史入口均已执行. 实际修改限于 `_gapn2_jacobian_probe.py`, `_gapn2_o3_scan.py`, `_gapn2_second_variation_probe.py`; 连续相位引擎和反射种子保持原字节. [调用清单](../../research/artifacts/proof-audit-round11-20260926/caller-inventory.json)绑定最终活动源.

## 2. 数值与实际程序验证

作者86项针对性检查以普通模式及 `-O` 通过. 全新隔离软件检验者另写92项检查, 亲自运行四个实际入口, 检查所加载模块确实来自冻结副本, 并用独立高精度物理传递计算复核 P3 界面二次型.

| 实际入口 | 配置 | 结果与限度 |
| --- | --- | --- |
| Jacobian probe | R=1,4; n=2; SUP/INF | 退出0; 正确交叉块、奇偶维符号和真实差分位移 |
| O3 scan | n=2,3; R=4; SUP/INF; N=80 | 退出0; N=80实际保留81个模态. 独立检验还比较N=80,160,320的有限细化 |
| second variation | n=2,R=4,SUP | 默认61模、64点求积、固定bump半宽0.0005, 退出0 |
| second variation | n=2,R=4,INF | 同上, 退出0 |

和第十轮默认 P3 数据比较, P1/P2/P2b 数值完全一致; 六个 P3 `Qedge` 变化的最大绝对值约1.63e-6. 因而不能把该错误笼统解释成所有旧 R=4 驻点表都错误. [精确比较](../../research/artifacts/proof-audit-round11-20260926/software-author/round10-comparison.json)及[独立执行档案](../../research/artifacts/proof-audit-round11-20260926/software-execution/)保留实际配置、端点、命令、退出码和输出.

驻点 Hessian 识别需要 F=0; 非驻点还存在含F的归一化项. R=1的密度跳量为零, 不能按跳量相除定义K. 当前没有给出严格谱尾、求积、bump极限或差分截断误差界, 也没有证明全参数非退化、定性符号、G1或全局唯一性.

## 3. 新增解析结果: 全成员窗口内的余有限闭包

固定实数c>0, 在复空间中采用实际Krein算子

$$
K_cf=-f''+cf,\qquad
D(K_c)=\{f\in H^2(-1,1):f'(1)=f'(-1)=(f(1)-f(-1))/2\},
\quad \mathcal H_c^s=D(K_c^{s/2}).
$$

原族为 `D={0,1}∪{4,5,...}`, p0=1,p1=x,
`p_(2m)=x^(2m)-m/(m-1)x^(2m-2)`,
`p_(2m+1)=x^(2m+1)-m/(m-1)x^(2m-1)`, m>=2.
对每个余有限保留集N⊂D、每个0<=s<7/2,

$$
\overline{\operatorname{span}_{\mathbb C}\{p_n:n\in N\}}^{\mathcal H_c^s}
=\bigcap_{j\in I(s)\setminus N}\ker\tau_j,
\qquad \operatorname{codim}=|I(s)\setminus N|,
$$

其中τ0f=f(0), τ1f=f′(0), τ4f=f″(0). 下标4指原族成员, 不是四阶导数.

| 阶数s | 稠密所必须保留的指标I(s) |
| --- | --- |
| 0<=s<=1/2 | 无 |
| 1/2<s<=3/2 | 0 |
| 3/2<s<=5/2 | 0,1 |
| 5/2<s<7/2 | 0,1,4 |

三个等号点均属于迹较少的一侧. 特别地, s=5/2删除p4仍稠密; 高于5/2才出现对应的连续二阶中心迹障碍. 删除p6在整个窗口都保持稠密, 所以原族经任何逐项非零复缩放和双射重排后仍不是Schauder基, 因而也不是Riesz基. 这不涉及相容Legendre、正交化或重新组合的替代系.

补证不只引用s=3的结论. [冻结作者稿](../../research/artifacts/proof-audit-round11-20260926/cofinite-author/cofinite-all-orders.md)重新展开实际算子的正性、自伴性、全指标成员性和四阶图范数, 构造高消失阶相容多项式核心. 两个固定内部乘子经显式二次K泛函估计给出包括临界阶数在内的局部双向范数控制; 最高非零复迹的对数Fourier序列排除所有不连续迹组合. 没有把多项式闭包与插值未经证明地交换.

作者94项辅助检查中43项为符号代数、48项为有限有理样本、3项为预期拒绝. 独立解析审查检查完整证明链, 并另写18项标准库精确检查. 审查者因其环境缺少SymPy而未完成作者脚本回放, 原始失败保留; 其解析验收不依赖作者检查PASS或外部未供论文的结论. 该限制与独立检查见[独立证据](../../research/artifacts/proof-audit-round11-20260926/cofinite-execution/).

未解决一般无限删项、任意约束筛选/投影、c=0或c趋零一致性、逼近速度或frame界. s>=7/2原非仿射命名成员已出域, 不能照搬同一原族的闭包公式. 新结果登记为研究地图A12; A8的s=3结论是特例, A11的一般无限删项仍开放.

## 4. 隔离审查与局部Lean

作者和最终检验者分离, 所有最终检验实际使用 `fork_context:false`. 独立检验只接收冻结快照及任务内的数学/执行契约. 原生spawn/wait、精确packet和原版receiver/verify回执分别保存. 接收层的信任标签为 `COORDINATOR_ATTESTED_TOOL_TRANSCRIPT`, 不将其描述为平台签名认证.

| 检验 | 独立agent身份 | 义务与结果 | 证据 |
| --- | --- | --- | --- |
| 当前四卡及Jacobian解析修订 | `01a0d9ac-2bfe-76e2-b5a7-069d529717ea` | 17项, APPROVED | [精确回执](../../research/library/reviews/runs/49f2a0c03c6198d2a1f35d3b8aea6810bbf3255e233d6c748ae96df3d2a36119-01a0d9ac-2bfe-76e2-b5a7-069d529717ea/report.json) |
| 四张未变卡的精确续审 | `01a0d9ad-0b0d-7f61-9148-1faf4d016a36` | 5项, APPROVED | [精确回执](../../research/library/reviews/runs/e4f8d89f8a82fc277a0aae9a18cf0b6b5dbb6358b126c4242cc0b13a9aa8d51e-01a0d9ad-0b0d-7f61-9148-1faf4d016a36/report.json) |
| 实际软件及有限数值执行 | `01a0d989-d4d6-7cd1-a94a-acead3e1a89d` | 3项, APPROVED | [精确回执](../../research/artifacts/proof-audit-round11-20260926/software-review/research/library/reviews/runs/d92449b8a6bba4a665de23ab6d575d919e16c5c27d87ffc38befba83a2e1845d-01a0d989-d4d6-7cd1-a94a-acead3e1a89d/report.json) |
| 全窗口余有限解析证明及拟入库卡 | `01a0d99b-7b2d-7af2-8d43-dd358bfd1cc9` | 4项, APPROVED | [精确回执](../../research/artifacts/proof-audit-round11-20260926/cofinite-review/research/library/reviews/runs/378992ac556e3daba6664dd14c637d8850a3f4b75ca91f454d924e15e02e9957-01a0d99b-7b2d-7af2-8d43-dd358bfd1cc9/report.json) |
| 37声明盲读 | `01a0d9a0-df41-7411-b2a4-17c791a134fc` | 37项, APPROVED | [精确回执](../../research/artifacts/proof-audit-round11-20260926/formal-readback/research/library/reviews/runs/6e916e3a1580dccb784566aed6aeba4320cc37f82cc814ea9ee913a6ed070a1d-01a0d9a0-df41-7411-b2a4-17c791a134fc/report.json) |
| 独立Lean编译与契约比对 | `01a0d9aa-a195-7bd2-8a3a-7f4f7de8592f` | 3项, APPROVED | [精确回执](../../research/artifacts/proof-audit-round11-20260926/formal-comparison/research/library/reviews/runs/96a6a726749351139af2db393e13a9fb267866eec0139df1cd556a3c97904423-01a0d9aa-a195-7bd2-8a3a-7f4f7de8592f/report.json) |

汇总和完整路径见[审查汇总](../../research/artifacts/proof-audit-round11-20260926/review-summary.json). 旧回执或本轮作者自检没有被当作新审查的证明前提.

[AuditRound11.lean](../../lean-proof/SL/AuditRound11.lean)的14个具名主定理包含一个13项显式合取根, 另有12个定义/缩写; 实际完整导出37项声明, 包括编译器生成项. 它证明实矩阵的和/差相似变换、条件反对易/对易分块、奇偶维行列式符号、仿射反射增量以及两个显式边界矩阵的行列式、正性和唯一实修正. 自然维数n允许0; 行列式恒等式中的L为任意实数, 正性要求实L>=4, 唯一修正接口要求自然L>=4.

作者及另一个全新检验者分别执行Windows PE Lean4.31.0和未修改的lean-verify2.0.1. 独立执行的实际根类型与精确契约一致, 全部37项声明、12个定义体及传递公理与冻结导出一致; 实际加载3917个模块、11745个外部工件, 路径和哈希均核对, 本地对象来自新私有构建. 根公理仅为propext、Classical.choice、Quot.sound. 四个错误数学目标在预期断言处失败; 原版验证器接受闭合目标, 并拒绝隐藏公理、错误预期类型和缺失声明. 审查者补充正例时的一次Fin1证明失败及报告诊断匹配失败均保留, 后续只修正该审查辅助代码. [独立执行记录](../../research/artifacts/proof-audit-round11-20260926/formal-execution/verification-record.json)与[无损档案清单](../../research/artifacts/proof-audit-round11-20260926/formal-execution-archive-manifest.json)给出完整身份. 这里仍信任已记录的Lean编译器和预构建依赖, 未采用第二独立内核或重建全部依赖.

形式化采用成对坐标 `Fin n ⊕ Fin n`, 第二半按镜像配对顺序排列; 与物理递增接口、Python数组的置换桥梁没有形式化. JP=-PJ是条件, 并非已形式化ODE微分结论. 边界矩阵由条目定义, 从多项式实际边界迹到这些矩阵的识别、复数延拓、Sobolev核心、临界迹和全部余有限闭包依然属于解析证明. 没有全工程Lake构建或完整Sturm理论形式化.

## 5. 工具库纠错与研究产物

四张修订卡按原版纠错模块登记新事项, 对当前版本合计15项既有/新事项义务重新审查. 四张未变卡由于整份旧审查包绑定了变化输入, 对4项精确义务另行续发; 保留原版本, 不忽略旧回执失效. 放行身份同时包含revision和新bundle, 共19项, 按依赖顺序释放. 新余有限卡单独比对审查过的拟入库字节.

实际索引及查询为 **90张可用、1张原撤回**. 原撤回卡仍是 `left-definite-orthogonal-systems.md`. 本轮核对12张关联卡, 包含8张纠错/续审卡和新增卡及其知识关联; 当前19项义务均绑定新回执. 保留90条历史警告, 未以删除旧证据或关闭门禁消除它们. [实际检索核对](../../research/artifacts/proof-audit-round11-20260926/integration/library-verification.json)保存精确版本、摘要、依赖和批注身份.

8条版本批注分别连接四张修订卡、新余有限卡、已有s=2/s=3卡与分数域字典. 批注记录修正经验和结果指针, 状态仍是候选批注, 不增加数学证明. 检索验收同时比较正文哈希、显式summary、source/evidence绑定、依赖及批注内容, 不只比较卡片数量.

研究地图增加A12和数值诊断B9; 项目理解、研究前沿、中英文首页、脚本入口和Lean范围同步更新. 新证明PDF为12页, 使用XeLaTeX编译并逐页检查. 401个TeX数学片段沿用冻结Markdown, 两处长式仅改分行; 审查后增加范围明确的状态说明, 原作者候选标签保留为历史. 两条underfull排版提示保留, 没有overfull、缺字或公式裁切. [排版记录](../../research/artifacts/proof-audit-round11-20260926/pdf-build/visual-inspection.json)绑定最终TeX/PDF.

## 6. 留证、保护与续接

原始检查、开发阶段的失败、缺依赖和工具封装错误均留在外部工作目录或对应档案, 不替换成最终通过日志. 巨大的形式化JSON/log以无损gzip保存, 同时登记原始和压缩哈希; 不复制完整Mathlib或本地二进制产物. 作者实际读取的外部论文整篇文本留在私有缓存, 本轮公共档案发布原创推导、定位和身份, 不新发布其全文. 本证明所需局部插值估计已独立推导.

基线15077个tracked文件、134个原untracked文件和6项原dirty均有逐字节身份. 本轮只修改明确活动文件, 原51份SL Lean源、canonical、旧冻结证明/审查/纠错事件保持原字节; 插件源与cache未改. [精确发布清单](publication-manifest.json)与[保护核对](protection-result.json)给出实际变更范围.

续接先读 `F:/tools/math-audit-round11-20260926/CURRENT.json`, 本报告和实际Git状态. 已完成的作者/审查不重跑, 已保存的API操作按结果继续. 研究检查点绑定最终报告、当前工具索引、活动证明、程序、Lean和审查回执. 若索引已经保存而进程退出异常, 先核对保存结果再执行缺少的query; 不重复放行. 只有所有写者完成且确认锁未占用后才清理空进度锁.

发布沿用用户授权: 先origin主仓库, 后fork, 不强推. 最终提交与两个远端的实际 `git ls-remote` 身份保存在外部 `DELIVERY.json`; 该文件避免把自身提交哈希写回同一提交. Git/PDF/查询成功不扩张上述数学与形式化范围.
