# 第十四轮: 两个共享入口与两份解析补证

基线及实际开始 HEAD 均为 `a815803a6492951cbed010624b42805fb1b49bd8`. 输入 33/33 清单哈希及 7/7 上游源码 Git blob 核对通过; 使用当前完整源码修订, 未用摘录覆盖新版. 基线逐字节记录保存在 `F:/tools/math-audit-round14-20261004/baseline.json`.

| 义务 | 实际结果与边界 | 完整证据 |
| --- | --- | --- |
| R14-01 | 已修复并独立软件复审. 薄块伪驻点被拒; 共用绝对/相对平衡、分母/导数分辨与局部零点校正. 未收敛、拒绝、不可判定均不作为驻点. 纯 softmax 不设块宽地板, F=f/b 与一般 J_F 保留. | [源码](../../scripts/_gapn2_symmetry_recon.py), [软件复审](../../research/artifacts/proof-audit-round14-20261004/software-final.md), [基线复现](../../research/artifacts/proof-audit-round14-20261004/baseline-reproduction.json) |
| R14-02 | 已修复并独立软件复审. 全 DD、半 DD/DN 约化核及直接装配共同核对几何/边界/一基目标/覆盖/未删分母; 错误配对拒绝. 正确公式、非正普通 Green、坐标重排、共同质量、一般 Jacobian 和 raw K/SKS 区分保留. | [共享身份](../../scripts/_sl_spectral_identity.py), [核专项检查](../../research/artifacts/proof-audit-round14-20261004/kernel_checks.py), [软件复审](../../research/artifacts/proof-audit-round14-20261004/software-final.md) |
| C14-G2 | 已证明并经最终独立解析/整合复审通过 (proofs-v4). 每个 n>=2、两图案、全部精确零点在 [1,Rmax] 上有统一正块宽, 包括 R↓1. G2+全部零点 ND 只给条件化唯一分支; ND 本身未证. | [核实后的完整证明](../../docs/SL_G2_compactness_proof.md), [最终独立复审](../../research/artifacts/proof-audit-round14-20261004/proofs-final-review.md), [初审](../../research/artifacts/proof-audit-round14-20261004/g2-initial-review.md), [活动正文](../../docs/SL_gap_nge2_symmetry_local_proof.tex) |
| C14-A11 | 已证明并经最终独立解析/整合复审通过 (proofs-v4). 固定 c>0、真实复 Hc2、任意 J/Se/So: 稠密当且仅当仿射两列保留且两支倒数和发散; 发散侧精确两迹闭包, 任一收敛侧无限余维. | [核实后的完整证明](../../docs/SL_H2_arbitrary_deletion_proof.md), [最终独立复审](../../research/artifacts/proof-audit-round14-20261004/proofs-final-review.md), [初审](../../research/artifacts/proof-audit-round14-20261004/a11-initial-review.md), [地图 A11](../../research_map.md) |

**接收缺口另列, 不冒充关闭.** 四项数学/软件义务的当前证据与旧工具库自动回执是两层. 原版 API 已保存四张活动卡的旧/新版本、两项纠错事项及三个卡路径的修订. `check_spawn` 实际拒收当前 `collaboration.spawn_agent` 的 `fork_turns=none`/`task_name` 原生身份, 因其只支持旧 `multi_agent_v1__spawn_agent`、`fork_context=false`、UUID 格式. 因而对应自动纠错放行及受整文件绑定影响的旧回执续发尚未完成; 门禁保持, 不伪造身份或改插件绕过. [真实拒收](../../research/artifacts/proof-audit-round14-20261004/review-adapter-rejection.json), [版本操作](../../research/artifacts/proof-audit-round14-20261004/card-operations.json). [当前查询读回](../../research/artifacts/proof-audit-round14-20261004/library-readback.json) 的全库 blocked=34; 查询涉及整文件旧绑定, 不把此数写成四项数学失败或本轮前基线数量.

四项软件/数学内容在各自声明的范围内完成修复或证明并独立复审; 自动接收缺口保留上述明确状态. 最终软件审查原生身份为 `/root/r14_software_review`, 数学审查为 `/root/r14_final_proof_review`, 均显式 `fork_turns=none`, 输入清单执行/读取后实算一致. 作者身份 `/root` 与软件作者 `/root/kernel_repair` 分别登记, 评审没有修改作者源. 这不是旧工具 UUID 接收回执. 两份证明审查独立于有限脚本. G2 直接从全部接口 F=0 得到 K=-2D、自动符号相容, 通过 L1 权稳定性、归一化 C1 模态与跨移动跳点统一 Volterra 余项排除端点, 再用 Rolle 排除内部同时相撞. 不声称整个闭单纯形边界无形式零点. A11 使用真实 Kc 等距、复内积和有界三次归一化 Mellin 函数; 只在保留指标写正交式, 经 Blaschke 延拓及 m=2 边界连续性得到完整高尾, 以已证两迹闭包收尾. Cauchy Gram 距离乘积和有限维商给真实 Hc2 无限维障碍.

实际检查:

| 检查 | 普通 | -O | 范围 |
| --- | --- | --- | --- |
| 当前性质 checks.py | 62/62 | 62/62 | 伪驻点/约化候选/未收敛拒绝; R4 SUP/INF 独立 65 位物理、零点数和质量正对照; 一般 J 及 raw/SKS 对照 |
| 当前 kernel_checks.py | 143/143 | 143/143 | 几何/边界/目标/覆盖/分母负对照, 闭式正配对, 前缀、坐标、非正 Green、一般 J 和导入次序 |
| 独立软件复审自加补测 | 26/26 | 26/26 | raw/SKS、目标扰动、覆盖及共享调用; 审查者亲自执行上述两套检查 |
| 第十二轮相关旧回归 | 136/136 | 136/136 | 保留原测试及阈值, 只在临时副本重定位源码根 |
| 第十三轮相关谱回归 | 469/469 | 469/469 | 质量/坐标/非正参数/一般 Jacobian 等; 原证据不改写 |

可重放命令 (使用有 numpy/scipy/mpmath/sympy 的 Python 3.10.11):

```powershell
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -B research/artifacts/proof-audit-round14-20261004/checks.py --output 'F:/tools/r14-properties.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -O -B research/artifacts/proof-audit-round14-20261004/kernel_checks.py --output 'F:/tools/r14-kernels.json'
```

两套脚本均支持 `--root`; 使用显式异常作接收, 不依赖会在 -O 下消失的 assert. [结果与回归](../../research/artifacts/proof-audit-round14-20261004/old-regressions.json), [最终版本绑定](../../research/artifacts/proof-audit-round14-20261004/final-review-bindings.json). 没有运行 Lean、重审全部扫描、重算冻结证书或认证区间谱尾. 附件 33 项原检查的基线错误期待保留; 修后脚本将 inf/伪驻点改为拒绝期待.

独立软件首轮发现直接装配的截断覆盖与 raw K/SKS 误名, 修复后以新 code-v3 精确包重新审查通过; 旧 CHANGES_REQUIRED 和前期清单/依赖装配失败保留. 核自检保留低截断误差失败, 以及额外误用 Richardson 误差单调性的一次失败; 保留全部原点和 2e-6 误差界, 后续两档截断各自通过同一界. 协调器测试返回类型/参考路径的早期错误也保留, 不计作通过.

两份活动阅读版由已有 XeLaTeX 重建为 16/22 页, 正文及 build 镜像字节相同, 已看修改页. 内置编译器因环境标准目录错误未成功; latexmk 缺 Perl, 直接使用既有 XeLaTeX, 未安装工具. 构建不等于证明审查. [构建和版面证据](../../research/artifacts/proof-audit-round14-20261004/pdf-verification.json). 综述原有未改表格仍有 overfull 提示, 修改页无新增溢出.

剩余研究目标: 全部精确零点 ND/G1、无条件全局唯一性及对称性, 剩余 M3/KP 与 KP-DET Q9; A11 收敛侧全部元素描述、其他阶数、一般非对角 H 的 A3/A4、稳定基与误差率; 既有 O1/O2 等不在本轮关闭范围. 本轮到四项有限义务与交付边界结束, 不自动展开这些目标. [最终字节保护检查](../../research/artifacts/proof-audit-round14-20261004/preservation.json) PASS: 19190 个原 tracked 中 34 个本轮活动文件改变, 其余 19156 个及 134 个原 untracked 字节不变. 13842 个受保护历史/canonical/Lean/旧库版本路径没有改动; 22 个软件与 11 个解析审查输入逐项实算一致, 两份 PDF 主文件与镜像一致. diff --check 使用 cr-at-eol 识别保留的 Windows 行尾后通过; 不以换行归一化改写审查源. canonical、冻结作者稿/旧回执、旧 Lean、本科讲义及所有无关原工作按基线保护. 此前交付是未提交的实际工作区修改. 2026-10-04 用户随后明确要求 "上传上云", 授权本轮精确提交并依次同步主仓库/fork. 上传收录本报告列明内容及必要字节保护规则, 不修改已审查软件/证明或把自动接收缺口写成放行. 最终提交及双远端实际读回身份见 F:/tools/math-audit-round14-20261004/publication/DELIVERY.json 和真实远端; 本报告不以本地准备状态冒称远端成功.
