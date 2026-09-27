# 第十三轮修订：证书、谱接口与复用边界

审计基线及实际接手 HEAD 为 `4a82d3c2c8c7c3e5f3f027efcf2be3c54a612983`。从实际工作区编辑，未用附件旧源码覆盖新版。[原包](../../research/artifacts/proof-audit-round13-20260927/submitted/REPORT.md)与 41 项清单哈希原样保存；3 个完整源码和 57 个抽取函数分别核对完整字节/AST 身份，见[输入核对](../../research/artifacts/proof-audit-round13-20260927/source-identity.json)。R13-01 至 R13-12 在基线仍存在相应问题或状态缺口；R13-05 的旧引擎已被主证明退役，但工具卡仍误导可信复用。

当前 57 条完整证书命题已重算通过，非零目标及严格不等式不变。谱接口与一般 Jacobian 已修复。下面区分实际修复、适用范围和仍未覆盖的工作；这些结论不等于全仓库数学认证。

## 逐项关闭表

| 项目 | 状态 | 实际处理和证据 | 剩余限制 |
|---|---|---|---|
| R13-01 | 已修复 | [证书 IO](../../misc/e1_certificate_io.py) 用整数 floor/ceil 分别处理两端；[台账](../../misc/e1_cert_ledger.json)存完整有理端点、中心、斜率、半径、最终界和裕量；[表格](../../misc/e1_cert_tables.tex)及活动正文重导出。B1(.85) 显示区间 `[.009851718322,.009851718323]` 保留 `>=1/200`。 | 显示表须连同精确台账和包络论证使用，不能把小数中心当证书。 |
| R13-02 | 已修复 | [生成器](../../misc/e1_certgen.py)和接收器实际验收 `TA_B2>=27/10`、`TC>=19/10`；另发现并修正 `tau<13/10` 的严格比较。全 57 条合同逐一核对。常数 1 负对照被拒绝。 | 接收器核验合同及有限算术，不是独立超越函数引擎。 |
| R13-03 | 已修复 | [rigid1d.py](../../misc/rigid1d.py) 的偏移余弦值域包含 1；宽区间给保守 `[-1,1]`。有界导数余项和实际调用域见[解析论证](../../research/artifacts/proof-audit-round13-20260927/interval-author/analytic_justification.md)。 | 宽区间可能不能判定目标；这不是可将失败改成成功的理由。旧 Decimal 不随此获得修复身份。 |
| R13-04 | 已修复 | 反正切改为单调端点计算，奇性/倒数/π/4 逐点归约，跨 0、±1 均终止。正常和 `-O` 检查支持域及拒绝逻辑。 | 有限有理输入合同；没有任意精度耗时保证。 |
| R13-05 | 适用范围澄清；可信复用已阻断 | [旧引擎卡](../../tools/interval-dec-directed-rounding.md)改为退役失效提示；真曲线及有理证书卡改用当前 Fraction 入口。旧代码、原台账及旧 PASS 保留，不伪造历史。 | 旧 Decimal 算法本身未修复；确需使用须建立新版本另验。它不再支撑当前主证明，不能据其错误撤回当前主定理。 |
| R13-06 | 已修复 | 真实生成路径中，假事实/不可判定退出 1，异常退出 2；本次状态与台账哈希绑定。失败后[接收器](../../misc/e1_cert_receive.py)及表格程序均拒绝，保留旧发布文件原字节。普通/`-O` 负对照见[运行记录](../../research/artifacts/proof-audit-round13-20260927/certificate-checks-v2/results.json)。 | 不能把接收合同检查等同于完整证明内核；I/O 中断留 RUNNING 也必须重新验收。 |
| R13-07 | 已修复 | [共享物理解](../../scripts/_gapn2_symmetry_recon.py)一次质量积分同时归一化值与导数；[eigen_data](../../scripts/_gapn2_jacobian_analytic.py)不再使用点值比。R=1/R=4 节点由独立高精度质量积分核对。 | binary64 数值计算；近浮点端点的取样容差有明确范围，不用于放宽 Green 越界检查。 |
| R13-08 | 已修复 | Green 按坐标 min/max 选择左右解，覆盖重排、重复点、合法端点并明确拒绝越界；匹配方程和解析常密度例独立核对。 | 数值极点检测是浮点守卫，不是严格预解集证书。 |
| R13-09 | 已修复／适用范围限定 | 普通 DD/DN Green 实现零参数线性与负参数双曲传播及极限；[半问题约化核](../../scripts/_gapn2_half_problem_probe.py)显式限于正特征值，非正参数转用普通核。 | 未缩放双曲传播溢出会明确报错；不声称任意参数规模均可计算。 |
| R13-10 | 已修复 | 三个 Jacobian 入口共用完整归一化/分母导数项；[独立推导所审作者稿](../../research/artifacts/proof-audit-round13-20260927/spectral-author/derivation.md)给出补项，F=0 时严格恢复原正确驻点公式。真实驻点及非驻点分别与独立隐式求导核对。 | 有限谱和仍有截断误差；未认证统一尾界。不得把原缺项解释为谱尾。 |
| R13-11 | 已修复 | [Helly 卡](../../tools/helly-compactness.md)补充统一 TV、拓扑、容许类闭性及极小/极大对应半连续性；保留连续单调端值类不取到 `π²/R` 的反例。直接 bang-bang 使用桥同步修正。 | 其它 SL 模型须另证连续性。完整可测盒沿弱星紧性路线的正确存在性保留。 |
| R13-12 | 已修复 | [研究地图](../../research_map.md)、[活动总览](../../docs/SL_spectral_topics_summary.tex)、[稳定性稿](../../docs/SL_stability_moment_jump.tex)、工具卡和导航对齐 A1/A12；G2 区分全零点且含 R↓1 的一致要求与历史符号相容、R0>1 的结论。 | G1、完整 G2 桥梁、全局唯一性及全部 M3/KP 仍开放；局部 s=3 证明及历史日志不被机械改写。 |

## 证据与实际执行

- 基线重放：原包 `run_e1.py` 和 `checks.py` 在普通/`-O` 下执行，确认 42 项旧行为观察。旧负对照“事实失败但 exit0”是待修缺陷；这些 exit0 不被当成修后成功。原包和[实际基线输出](../../research/artifacts/proof-audit-round13-20260927/baseline-replay-results.json)分别保留。
- 当前精确计算：[生成记录](../../research/artifacts/proof-audit-round13-20260927/certificate-checks/generator-run.json)真实退出 0，57 条完整命题均验收。两个区间目标最小保守裕量分别为 `0.002392350303`、`0.058681319813`；没有放宽阈值。B1 导数和 h 凹性也有实际包络检查，未硬编码 True。
- 区间作者测试：普通/`-O` 各 22 项，覆盖真实 E1 调用域、内部极值和跨 1 等精确反例。证书接收/失败传播测试：各 8 组性质测试，含同一真实 CLI 路径的正对照、3 次实际生成负对照、两个接收端明确的验证拒绝、篡改合同及向外显示检查。首次测试曾错误使用接收器参数，此缺陷由隔离审查指出；旧记录冻结，修后记录另存 v2。
- 谱作者测试：最终普通/`-O` 各 469 项性质检查及 136 项第十二轮回归；另完成 6 次真实 CLI，见[作者执行范围](../../research/artifacts/proof-audit-round13-20260927/spectral-author/AUTHOR_NOTE.md)。默认 R=4 的未触发旧节点缺陷样本不被宣布错误，也不豁免接口修复。
- 谱独立审查：全新 `fork_context:false` 审查者使用冻结源码，独立建立质量积分、Green 匹配和复步长隐式求导参照；普通/`-O` 各 701 项检查通过。未提供的种子模块以不会调用的拒绝哨兵隔离，原 CLI 由作者另行执行，二者不能混称独立端到端执行。
- 数学/工具续接独立审查通过 30 项限定范围义务（含 29 项纠错/续审）：核查 Helly、反例、可测盒存在性、A1/A12 及局部证明范围。未提供的其它证明全文未认证其文件版本；已提供定义和推导被独立核查。
- 首次证书审查实际重算全部 57 条，台账逐字节一致；但因负对照 CLI、旧引擎漏引用和闭盒/开区域混用三项问题整体退回。三项已修正，[补记](../../research/artifacts/proof-audit-round13-20260927/certificate-repair-v2.md)保留原因、边界反例与后续入口。修后由另一名全新隔离审查者验收通过。三份最终回执及当前哈希复验详见 [verification.json](verification.json)。

`N=160/640/2560` 的指定非驻点 Jacobian 误差约为 `.03598/.00908/.002275`，这是有限谱尾收敛观察，未升格为误差定理。解析包络、精确有理计算、有限浮点检查和已有局部 Lean 结果分别记录；本轮没有新运行 Lean，也不声称完整 SL 形式化。

使用 `python3 research/artifacts/proof-audit-round13-20260927/run_checks.py` 可从当前工作区复验，另加 `--optimized`。交付入口已在普通/`--optimized` 两种模式下实际完成四组检查，均退出 0；记录见 [普通模式](../../research/artifacts/proof-audit-round13-20260927/portable-final-normal/results.json) 和 [优化模式](../../research/artifacts/proof-audit-round13-20260927/portable-final-optimized/results.json)。谱测试需要 numpy/mpmath。证书源码若变化，须先重跑 `misc/e1_certgen.py`；旧成功状态不跨源码版本有效。

## 传播、阅读版与保留项

实际静态调用清点包含 54 个文件的 100 处导入及 76 个传递模块，不代表全部 CLI 都执行。[当前脚本导航](../../scripts/README.md)区分已修入口与未重认证的历史探测。未重算无依赖错误路径的历史全 R 扫描，也未笼统否定所有 R=4 数据。

四份活动阅读版均由当前源码实际编译并同步 `docs/` 与既有 `docs/build/` 副本：

- [O3a 证书正文](../../docs/SL_gap_n1_O3a_phase_rigidity_proof.pdf)：检查包络说明、端点表和两个区间下界表；二次编译另检查第 21 页的闭盒边界说明。
- [谱主题总览](../../docs/SL_spectral_topics_summary.pdf)：检查 A1/A12 分类、Helly 和 G2 范围；一处原有未改表格仍有 overfull 警告。
- [矩跳跃稳定性](../../docs/SL_stability_moment_jump.pdf)：检查更新的引言及原第一节证明衔接；原局部证明正文保持原范围。
- [比值总览](../../docs/SL_ratio_summary.pdf)：仅修正 Helly/bang-bang 使用前提。

[初次构建记录](../../research/artifacts/proof-audit-round13-20260927/reading-versions.json)与[最终 O3a 构建及第 21 页检查](../../research/artifacts/proof-audit-round13-20260927/reading-versions-v2.json)均保留；后三份阅读版沿用初次记录的源/PDF 哈希。未修改先前讲义 PDF。A1/A12 原证明、相容 Legendre 替代系、可测盒存在性、正确驻点公式、DD/DN 相位索引、极点身份、真实接口差分、反对易交叉块和 raw K/SKS 区分保留。

原始作者稿、旧证据、失败测试尝试、原回执和 canonical 保留。原工作区的 6 项未提交改动及 134 个原未跟踪文件不纳入本轮成果；最终保护核对与云端同步记录单列。完成本轮后不自行启动下一轮理论扩写。

最终工具库接收 31 项义务，涉及 20 张当前卡；默认检索实查 89 张可用、2 张阻断（原有撤回卡与退役 Decimal）。两条版本绑定应用批注已接入；这不把所有卡升级成全定理证明。
