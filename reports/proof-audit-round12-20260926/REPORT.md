# 第十二轮审计修订

本轮已修复半谱漏模、去极点身份漂移及原矩阵/共轭矩阵扇区混淆，并处理它们在程序和三张工具卡中的传播。独立检验结果、当前工具库回执和形式化范围分别列在下文。Git 提交和两个远端的实际读回保存在项目外的 `F:/tools/math-audit-round12-20260926/DELIVERY.json`；本报告不预写自己的提交哈希。

用户输入是 `C:\Users\HuangZY\Downloads\sl_audit_round12`，指定工作流 2.0.1，要求“继续修订”。基线 `be7c0912849a50a46869773eab4b3a2ec655ce88` 的 16541 个跟踪文件、134 个原未跟踪文件和 6 项既有改动均保存字节身份。附件中的建议和结论均作为待核实材料。

## 修复内容与数学对象

| 事项 | 核实的原因 | 当前处理 |
| --- | --- | --- |
| R12-01 半谱漏模 | 独立 mu 网格可能把两个根放在同一单元内，端点不变号；请求 N 改变网格后，谱前缀也改变 | DD/DN 共用提升相位；第 j 阶分别由 jπ 与 (j−1/2)π 定位，逐阶比较括区 |
| R12-02 错删极点 | 重新枚举的数组与目标谱值不属于同一前缀，只按下标删项会留下真正极点 | 同一谱表绑定几何、边界类型和模态身份，核对目标值、覆盖和全部分母；主调用的 N/2N 共用谱表 |
| R12-03 扇区混淆 | 交叉 Green 式实际表示 Kp=SKS 的奇压缩，被标为原 Ko | 明确 KpOdd=E Ke E；原 Ko 使用自身极点处的约化核，并保留秩一项 |
| P12-01 直接传播 | `sector_data` 的旧 Sigma/H/E 组装属于 Kp，而字段称为原 K；第三卡继承同一标签 | 无前缀 Ke/Ko/He/Ho/Ee/Eo 统一按原 K 返回，另给显式 Kp* 字段；旧 c_e/c_o 明示属于 KpEe/KpEo |
| P12-02 负秩一判据 | 历史卡片将 λmin(Ho−Eo)+min d>0 当作含 Ho+Eo 块的充分条件 | 撤回此解释，写入带正确对象和正定前提的 Sherman–Morrison 等价条件；纯矩阵反例不冒充 SL 驻点反例 |
| 独立软件检验 F1 | 极端合法浮点输入使谱值减目标值溢出，得到无穷分母后求和伪造有限零值 | 减法进入受保护算术区，所有差值须有限；新增回归并由新的隔离检验者复验 |

完整条件和证明在[解析修订](../../research/artifacts/proof-audit-round12-20260926/analytic-repair.md)。它区分三个层次：任意有限 n、任意实矩阵的镜像压缩恒等式；DD/DN 每阶相位与全/半谱交错；固定有限 R>1、n=2 对称五层驻点的归一化 Green 和形状导数公式。任意矩阵的压缩交换不需要 K 与反转对易，真正的镜像不变子空间分块另需对易。

原 Ko 的半问题式保留自身去极点项和系数 4a(b−a)/b² 的秩一项。交叉式属于原 Ke 的合同矩阵。这一区分决定下一步应分别控制哪两个核，不能仅改函数名后沿用旧定性解释。历史扫描保存原字节，其个别扇区标签、余量和全参数解释没有在本轮重新认证。

## 输入核对与实际执行

附件 MANIFEST 的 16 项哈希通过；两份摘录的 9 个源函数 AST 与基线完整 Git blob 相同。摘录与完整源码仍分别记录。附件的 34 项检查在普通和 `-O` 模式回放，其中有些检查确认旧错误，并不代表 34 条证明。旧完整模块另行复现漏低模态及保留真正极点后出现无穷的行为。

修复后的 136 项针对性回归在普通和 `-O` 模式通过。第二位独立软件检验者在自己的副本中重新执行这些检查、两个半问题入口、两个 raw-Ko 入口及四个 Green 惯性实例；另用 85 位传递计算和物理零点计数核对 48 个分层模态，并比较 96 个常密度有限谱和。n=2、R=4 的原 Ko 与物理接口差分最大误差低于 4.38e−10，交叉 KpOdd 与 E Ke E 低于 4.49e−10；独立逐模组装的 H/E 分量与对应字段最大差异 5.44e−13。这些是有限数值结果，不是误差区间证书。

改动共六份程序：四份活动谱/Green/扇区程序，以及两份历史 debug 的共享谱表调用。后两份仅检查导入、改动调用链和定点调用，没有运行其大规模求积 main；其他历史扫描亦不算重验。[调用者清单](../../research/artifacts/proof-audit-round12-20260926/caller-inventory.json)记录跟踪脚本的直接引用及精确字节。

第一次真实 CLI 对照暴露的扇区传播失败、第一次独立软件检验的 CHANGES_REQUIRED、修复前溢出见证和后来通过的复验均保留。作者的 50 项有限符号/格式自检也独立存档，不代替解析审查。

## 独立检验

所有最终检验由不同的 `fork_context:false` 会话完成，仅接收原版模块生成的精确冻结包。原生派遣、等待结果和接收回执均保存。其信任标签为 `COORDINATOR_ATTESTED_TOOL_TRANSCRIPT`，不是平台数字签名。

| 检验 | 独立 agent 身份 | 义务与结果 | 证据 |
| --- | --- | --- | --- |
| 三张修订卡及解析证明 | `01a0dd1c-1e46-74b0-9733-c49591248881` | 18 项，APPROVED | [精确回执](../../research/library/reviews/runs/50a0194967d98888b86a5d5124bbd76165accdbd3e7f7736c4f3765bbbb350d4-01a0dd1c-1e46-74b0-9733-c49591248881/report.json) |
| 未变卡精确版本续审 | `01a0dd1d-4f43-7723-8591-fd962c7389b8` | 8 项，APPROVED | [精确回执](../../research/library/reviews/runs/37a3f144d73aec8ebff2a57d5ef956aa07eee3752c48e0297962147accff1a2a-01a0dd1d-4f43-7723-8591-fd962c7389b8/report.json) |
| 实际软件与有限数值执行 | `01a0dcfd-182d-7e01-8635-c71a9d8e110f` | 3 项，APPROVED | [精确回执](../../research/artifacts/proof-audit-round12-20260926/software-review2/research/library/reviews/runs/4f2474bf0339e94c1669667171f07f7e277b9d7002beff0383ef5b16f0dde7ae-01a0dcfd-182d-7e01-8635-c71a9d8e110f/report.json) |
| 59 项完整声明盲读 | `01a0dd15-6130-7a41-9eb7-4d6e40f72aa6` | 59 项，APPROVED | [精确回执](../../research/artifacts/proof-audit-round12-20260926/formal-readback2/research/library/reviews/runs/a267ae3b28472c9ae5d16c19f8a05a00af07f6e084e2254ce39bb7c16c399317-01a0dd15-6130-7a41-9eb7-4d6e40f72aa6/report.json) |
| 独立 Lean 执行及契约比对 | `01a0dd20-531f-7342-b836-2fa34b17c3f6` | 3 项，APPROVED | [精确回执](../../research/artifacts/proof-audit-round12-20260926/formal-comparison/research/library/reviews/runs/d080d3cc807519f2067666b19dd78db62196e9549b736c3fddd5c30037dfc279-01a0dd20-531f-7342-b836-2fa34b17c3f6/report.json) |

解析审查的每一项纠错义务均绑定当前工具卡字节。未变卡因先前共享证据包中的输入变化而需要续审，字节未变本身不构成数学通过。当前与历史回执的区别见[审查汇总](../../research/artifacts/proof-audit-round12-20260926/review-summary.json)。

## Lean 的实际覆盖

新增 [AuditRound12.lean](../../lean-proof/SL/AuditRound12.lean)，含 22 个作者定义/缩写、10 个主要定理（包括九项合取根），实际导出 59 项声明及定义体、隐参数和传递公理。范围为所有自然数 n（含 0）、实矩阵、真实配对坐标到递增坐标的 Equiv、交错符号、归一化桥梁、任意 K 的扇区交换、奇向量秩一项及 n=1 的反例。

第一次盲读返回 INCOMPLETE：根声明的实际类型导出含 9 个省略号。协调器保留原证据，在新目录重新编译同一数学源码，提高导出完整度，再由新会话盲读。另一个独立会话实际重编译、核对完整类型和作者契约、运行原版 exact-root 检验器及正负对照。独立执行导出59项声明与完整冻结导出逐字一致，SHA256为 `ebb0d76e85d28afcfa8db75041d36530059662845bd9e20e8290e5e0bacdbf3a`。正确精确根通过；三个数学负对照在预期的错误断言处退出1，并有成功的补充正证明；错误契约在完成提取后得到 `target_mismatch`。根公理闭包仅含 `propext`、`Classical.choice`、`Quot.sound`，无额外公理、未知或unsafe依赖。记录核对3799个模块、11391个导入工件和234项执行工件；依赖按已记录二进制复用，没有重建第二套内核。[实际执行清单](../../research/artifacts/proof-audit-round12-20260926/formal-execution/execution-manifest.json)的SHA256为 `4a849bac125031088ba17e53c8aba5b048b0af03dcdc82eaff6e084ca7f010d6`，其中同时保留检验者失败尝试。

这不等于完整 Sturm–Liouville、Green、相位提升、浮点 Python 或惯性指标/Sylvester 定律形式化。现有 52 份 SL Lean 源、运行时和依赖保持原字节，没有全库 Lake 构建或 canonical 接收。第一次不完整导出及协调器过早启动导出造成的缺失模块失败也原样留存。

## 工具库、理解与续接

实际索引和查询为 **90 张可用、1 张原撤回**，原撤回卡仍为 `left-definite-orthogonal-systems.md`。本轮 8 张当前卡共 22 项纠错/续审义务经原版 API 放行，保留 109 条历史失效回执提示。[实际检索核对](../../research/artifacts/proof-audit-round12-20260926/integration/library-verification.json)保存精确版本及绑定。

三张卡均新增绑定当前 SHA256 的纠错经验批注；旧卡和旧注不改写。当前摘要、来源绑定、依赖、批注及实际查询均分别核对，不能只凭索引条数判定入库。使用安装的 2.0.1 原版纠错/工具库模块；本轮未改插件源码、缓存或全局环境。

[研究地图](../../research_map.md)新增 B10，维持全局 B4 的 PARTIAL；[项目理解](../../docs/PROJECT_UNDERSTANDING.md)记录谱身份贯穿计算、同名扇区不可混用及负秩一符号教训。前沿图、双语首页、脚本/工具/Lean 导航、AGENTS 对话记录和可续接检查点同步。第十一轮固定 c>0、0≤s<7/2 的余有限分类及其临界点保持原验收范围。

仍开放的义务包括：全 R 分支存在/唯一/延拓、两个原始扇区的统一符号、完整 G1′、严格谱尾和浮点区间误差。新矩阵反例只推翻错误的一般充分条件，没有给出相应 SL 驻点的反例。

## 证据与发布

[证据入口](../../research/artifacts/proof-audit-round12-20260926/README.md)区分外部材料、作者推导、自检、失败记录、独立审查与原版放行回执。大体积 JSON 采用无损 gzip，同时记录压缩前后 SHA256。精确提交清单见 [publication-manifest.json](publication-manifest.json)，导航与绑定核对见 [final-document-check.json](final-document-check.json)。

只提交本轮目标路径，保护原有 134 个未跟踪文件、6 项未提交改动、canonical 和冻结历史。发布顺序为 origin 后 fork；远端实际 HEAD 与本地提交一致才记为交付完成。
