# 第七轮直接传播候选交接

角色: 文档/工具卡作者, 不是最终审稿人. 候选已完成, 最终隔离审查待协调器安排.
所有写入仅在 `/mnt/f/tools/math-audit-round7-20260921/tool-author`.

## 交付文件

| 原主库路径 | 整份正文候选 | metadata 更新意图 |
| --- | --- | --- |
| `tools/band-selfconsistency-equivariance.md` | [band 候选](/mnt/f/tools/math-audit-round7-20260921/tool-author/candidates/tools/band-selfconsistency-equivariance.md) | [metadata-update.json](/mnt/f/tools/math-audit-round7-20260921/tool-author/metadata/band-selfconsistency-equivariance/metadata-update.json) |
| `tools/half-problem-regularized-green.md` | [half 候选](/mnt/f/tools/math-audit-round7-20260921/tool-author/candidates/tools/half-problem-regularized-green.md) | [metadata-update.json](/mnt/f/tools/math-audit-round7-20260921/tool-author/metadata/half-problem-regularized-green/metadata-update.json) |
| `tools/green-half-inertia.md` | [green 候选](/mnt/f/tools/math-audit-round7-20260921/tool-author/candidates/tools/green-half-inertia.md) | [metadata-update.json](/mnt/f/tools/math-audit-round7-20260921/tool-author/metadata/green-half-inertia/metadata-update.json) |
| `docs/SL_gap_nge2_symmetry_recon.tex` | [recon 候选](/mnt/f/tools/math-audit-round7-20260921/tool-author/candidates/docs/SL_gap_nge2_symmetry_recon.tex) | 不涉及工具卡 metadata |

另附 [完整差异](/mnt/f/tools/math-audit-round7-20260921/tool-author/changes.patch),
[逐段行号对照](/mnt/f/tools/math-audit-round7-20260921/tool-author/changed-lines.json),
[作者结构检查](/mnt/f/tools/math-audit-round7-20260921/tool-author/author-checks.json),
[输入身份](/mnt/f/tools/math-audit-round7-20260921/tool-author/inputs-manifest.json)
及本目录 [AGENTS](/mnt/f/tools/math-audit-round7-20260921/tool-author/AGENTS.md).
`inputs/` 是实际读取材料的字节快照, 不是新的历史输出或运行依赖.

## 改动位置与数学含义

表中旧行号指 `inputs/` 保存的原字节, 与 checks-author 的原提交源码快照一致;
新行号指 `candidates/` 中整份文件. 全部零碎修改见 changed-lines.json, 不将历史行号用于漂移后的主库.

| 文件 | 原行 | 候选行 | 修订内容 |
| --- | --- | --- | --- |
| band | 109-111 | 139-156 | 保留 determinant 恒等式, 删除 detK>0 与 Hessian 定性的无条件等价; SUP/INF 目标符号分开. 加一般矩阵反例的适用边界与连续分支惯性前提. |
| band | 174-176, 228, 246-247 | 231-235, 291-293, 311-314 | LDL^T 主元、双扇区与 Sherman-Morrison 都针对更强定性判据, 不再称为 bare G1' 的无条件等价归约. |
| band | 122, 152-154 | 175, 208-211 | 未归一化 f'/s 补 lambda_(n+1); 原 K 对角式与 d_h 保持不变, 分别见候选 203、281 行. |
| band | 116 | 167-169 | SUP 的 evK 全正若成立, 必有 sgn detJ=(-1)^n. 更正原 (+1)^n 对奇数 n 的冲突, 不伪装重跑历史扫描. |
| band | 63-65 | 85-92 | 4pi^2 限定为 n=1; 固定 n 盒类上确界极限改指向 (n+1)^2*pi^2 新证明, 与自洽分支全 R 延拓及最优性分开. |
| band | 47, 55 | 61-67, 76-77 | 同一已核实直接传播点: 修常密度 W; 保留 n=2 根式和正确的精确归一化行列式. 依据本轮实际收到的报告第 3 节, 不声称读过缺失附录. |
| band | 16, 49; 新说明 | 27, 30-32, 69-70, 158-163 | 统一 2n 个独立接口及 F=f/lambda_(n+1); 区分密度块边界与特征函数节点, 用 B_mir 区分镜像坐标矩阵与 Jacobian 交叉块 B. |
| half | 149-156 | 161-181 | G1' 仅是两块 determinant 的正乘积; I1+I2 是更强的完整 K 定性. 显式列出起点惯性、连续连接路径和沿途非退化. |
| half | 181-193 | 209-230 | 以 B^T H_full B 替换混淆维度的半隙 Hessian 式, 说明半隙仅控制 Ko, 严格局部极值本身也不等价于 Hessian 定性. |
| half | 81, 158, 197-200, 247-248 | 93, 183-186, 234-242, 292-293 | 旧显式 mu_1^D/mu_2^N 和两点核按 n=2 阅读; 历史锚点和 M1-M3 强化路线保留边界, 不默许全 R 分支, 不重审 M3/KP. |
| green | 46-54 | 56-67 | 有限点 Green 核惯性等式保留为未核验的历史主张, 不凭算子谱计数或理论名称直接认证. |
| green | 56-73 | 69-110 | 保留原 Green 显示式, 将可逆合同解释为奇扇区定性等价; 补完整矩阵 determinant 条件、另一扇区义务及分支前提. |
| recon | 196-197 | 196-209 | 唯一一处局部替换: n=1 特例、固定 n 上确界极限、新证明/REPORT 入口及未证全 R 分支边界. |
| 三卡 | frontmatter 与局部说明 | 见完整差异 | 更新 source/status/updated, green 另改 title; 增加当前入口与历史未复核标记. 没有改变 canonical_key 或 tags. |

本轮保留的核心接口是

\[
\det J=(-1)^n(R-1)^{2n}\det K,\qquad
H_{\rm full}=-\lambda_{n+1}(R-1)^2K.
\]

在同一量化解集上, G1' 等价于每点 detK>0. SUP 的 K 正定和 INF 的 K 负定是更强的充分条件.
`diag(1,1,-1,-1)` 只反驳一般矩阵推理, 没有被宣称为 SL 实现例.
沿支使用惯性不变性时, 起点惯性、实际连续连接路径和全程非退化均须另有依据;
这一条件化论证不建立全 R 分支, 也不自动涵盖其它连通分支.

half 中采用 n=2、全区间 L2(rho) 归一化, B=(e1-e4,e2-e3)=sqrt(2)Bo.
因此

\[
\nabla_a^2g=B^TH_{\rm full}B=-2\lambda_3(R-1)^2Ko.
\]

这里是 4x4 矩阵经坐标映射成为 2x2 矩阵, 不是把 full-interface Hessian 统一乘 2.
I2 控制半隙的二阶充分条件, I1 控制另一扇区; 不能由半隙极值倒推 I1.

## metadata 与依赖的交接

每个 metadata-update.json 只有 `field_updates` 和 `dependency_intent`.
前者是变化的可读字段, 与候选 frontmatter 一致; 后者只表达当前证明、REPORT、权弦 FH 一阶公式的真实用途.
REPORT 是修订/审查状态记录, 不是数学证明依赖或自动通过凭据.
这些文件不是已解析的 currentmetadata 或可以直接提交的 registry 事务.
既有其它真实依赖不因未列在 delta 中而删除, 也不将所有 related wikilinks 升级为证明依赖.
请协调器负责 currentmetadata 字段映射、最终 exact hashes 与适用的纠错/审查绑定;
本作者没有生成 source/content/version hashes 作为 metadata 占位, 没有生成 review/acceptance 回执.
inputs-manifest 的哈希仅标识本作者实际读取的输入字节, 不能替代最终依赖版本绑定.

三卡正文使用主库落位后的相对链接. 当前入口分别是
[第七轮证明](</mnt/f/LaTeX/BVE research/docs/SL_gap_nge2_symmetry_local_proof.tex>) 和
[REPORT](</mnt/f/LaTeX/BVE research/reports/proof-audit-round7-20260921/REPORT.md>).
读取时 REPORT 明确为修订/作者检查进行中; 本作者没有据入口存在宣称解析稿或卡片已获验收.

## 明确保留的文件与未核验范围

- `docs/SL_spectral_topics_summary.tex` 未生成候选, 主库字节与输入相同. 原 583-588 行承接 n=1 扫描, 587-588 行明确写 lambda_1->0、lambda_2->4pi^2; 原 990 行同样是这两个指标. 此处按 n=1 解释. 用户明确指定该源绑定前轮 review, 本任务不改它, 也没有重新审查那份 review.
- band 的 I1/I2/I4、C1/C2、Green 预解式和旧支配不等式保留历史来源. 特别是旧 Green 强化、近简并主导性、有限样本向全 R 的推广均未在本轮认证. 当前候选不重新宣布全局 G2 闭合.
- half 的 B/P/A1/A2、半问题核和谱分裂主体没有全盘重推. 其显式固定索引只按 n=2 阅读, 不是本轮提供了一般偶数 n 的新公式.
- green 的有限点核负指数等式只是待核验历史内容, 不是已得到新的反例或证明. 未扩大为旧 Green/M3/KP 全链审计, 未更改既有有限 chart 的历史验收.
- 本轮没有重新运行旧 FD/Hessian/Green 扫描、仓库程序、旧 Blueprint 程序、Lean 或历史证书. 没有编译 PDF, 没有修改主库、registry、canonical、插件或历史输出, 没有 commit/push.

## 作者检查与下一责任方

实际完成 23 项限定作者结构/字节检查, 全部通过, 详见 author-checks.json.
包括 3 个 JSON 的变更字段与依赖路径、4 份候选的环境配对、目标原字节保护、单段 recon 差异、候选清单和写入路径边界.
band 两条已归一化对角公式逐行原样保留; half 除所修 Hessian 式以外的 16 个显示式及 green 原有 5 个显示式原样保留.
这只确认文件组织、范围和保留要求, 不等同数学证明通过或 TeX 编译通过.
三卡与 recon 应由协调器提供给全新隔离 agent 独立审查; 编译 PDF、解析 currentmetadata、最终依赖哈希绑定和主库集成均由协调器处理.
