# 第七轮直接传播文档与工具卡作者

## 工作方法

- 唯一写入根为本目录. 主库、library registry、canonical、插件和历史输出均只读; 不编译 PDF, 不 commit/push.
- 以 checks-author/propagation.md、原三卡和原 recon TeX 为输入, 只处理已确认的直接传播问题. 数学作者检查与最终审查分开; 最终验收由协调器另启全新隔离 agent.
- 完整候选保存在 candidates/. 每卡的 metadata-update.json 仅表达字段更改和真实依赖意图; currentmetadata 解析及 exact hashes 由协调器绑定.
- 保留正确公式和历史来源, 将未经本轮核查的 Green、M3/KP、全 R 分支与历史强化结论明确标界. 每次修改同步本记录, 行号和范围记在 change-notes.md.

## 对话与维护记录

2026-09-21 用户指定本角色为第七轮直接传播文档/工具卡作者, 不是最终审稿人. 要求三张完整候选卡、每卡 metadata-update.json、recon TeX 最小修订和 change-notes. 具体要求: 修 det>0/惯性错误等价, band 未归一化 f'/s 补 lambda_(n+1), 限定 n=1 的 4pi^2, 更正 SUP 奇数 n 历史符号; 对称参数通过 B 转换全接口 Hessian, 不统一乘 2. diag(1,1,-1,-1) 仅是一般矩阵反例. docs/SL_spectral_topics_summary.tex 保留原字节, notes 说明 n=1 范围. 主库 AGENTS 的维护规则在当前唯一可写边界内落实, 不写回主库.

首次维护: 已读主库及写入祖先的 AGENTS, 指定传播报告和原三卡; 定向核对原 recon 与 summary 中的 n=1 上下文. 已读到本轮提交报告给出的常密度 W 修正式及 n=2 行列式, 作为 band 同一直接传播点的修订依据. 创建本目录记录与输入快照, 不运行仓库程序.

维护更新: 从输入快照创建三卡与 recon 的完整候选副本. 后续只修这些候选; 确定半隙 Hessian 用 B^T H_full B 说明维度和扇区, 原一般 n=偶的半问题展开仅保留其显式 n=2 索引范围, 不扩查原推导.

维护更新: band 候选已修行列式/惯性等价、Sylvester 主元与扇区充分性、f'/s 因子、奇数 n 的 SUP 符号、常密度 W 和上确界极限范围. half 候选保留 Green 主体, 分开行列式与 I1/I2 定性, 用镜像坐标修正半隙 Hessian 与完整 Hessian 的关系; 历史强化结论显式标为本轮未核验. 尚未执行作者检查或独立审查.

维护更新: green 候选将单扇区合同判据与完整 G1' 分开, 有限点核惯性等式保留为待核验历史主张. recon 只替换原开放条件末项, 限 4pi^2 于 n=1, 加固定 n 上确界新证明入口及分支延拓边界. 所有候选已指向第七轮 TeX/REPORT, 不伪造验收或绑定哈希.

维护更新: 为三卡分别生成 metadata-update.json, 仅含有变化的 title/source/status/updated 字段和当前证明、REPORT、权弦 FH 的真实依赖意图. 未生成版本/hash/review/reliability 接收字段, 不操作 registry. currentmetadata 解析与依赖更新由协调器决定并绑定.

维护更新: 作者通读差异后在 band 中区分密度块边界、常密度特征函数节点和镜像坐标矩阵 B_mir, 避免与原 Jacobian 交叉块 B 混用. 这些是直接公式的记号整理, 未扩查其它文件或旧程序.

维护更新: 实际完成 23 项限定作者结构/字节检查, 全部通过. 三卡、recon 与排除的 summary 主库字节仍等于输入; band 两条已归一化对角公式和 half/green 其余历史显示式保留. recon 仅替换原 196-197 行. 已生成 changes.patch、changed-lines.json 和 author-checks.json; 这些不是数学认证或最终审查.

交付维护: 已写 change-notes.md, 列出四份完整候选、三份 metadata delta、旧/新行号、已保留公式与未核验范围. 明确 summary 的 lambda_1/lambda_2 是 n=1 上下文, 按用户指定保留前轮 review 绑定源. 本作者交接完成; 最终隔离审查、PDF、currentmetadata 和 exact hashes 由协调器处理.
