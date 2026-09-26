# 研究脚本导航

第十二轮程序接口: [_sl_prufer.py](_sl_prufer.py) 的 `indexed_roots` 新增仅关键字参数 `RightBoundary='D'` (默认不变), 可选 N 对应左 D/右 N 的半整数相位. [_gapn2_half_problem_probe.py](_gapn2_half_problem_probe.py) 的 `half_spectrum(..., return_table=True)` 返回只读数值谱表; 原默认仍返回 ndarray. `mumax` 若不足容纳所需 N 阶会报错. `_spectral_green` 保留零基 `pole_idx` 调用兼容, 内部按一基模态核验目标、几何、边界和分母; N/2N 主调用共用同表.

[_gapn2_sector_decomposition.py](_gapn2_sector_decomposition.py) 的 `Ke/Ko/He/Ho/Ee/Eo` 已统一为原 K 的块, 显式 `Kp*` 键提供 SKS 的块, `c_e/c_o` 仍属于 Kp 的秩一分解并在元数据标明. [_gapn2_green_inertia_probe.py](_gapn2_green_inertia_probe.py) 的交叉 Green 比较目标为 `KpOdd=E Ke E`. 四份活动程序与两份历史 debug 调用的修改及检验范围见[报告](../reports/proof-audit-round12-20260926/REPORT.md); 不据这些检查重认证所有旧扫描或全 R 定性.

第十一轮修订: [_gapn2_jacobian_probe.py](_gapn2_jacobian_probe.py) 对残差Jacobian提取交叉块C,D, 校验JP=-PJ, 使用detJ=(-1)^n detC detD. `sym_antisym_decomp`保留调用签名, 返回值语义已改为C,D. 与P对易的Hessian/K仍使用其自己的块结构.

`jac_fd`默认仍返回ndarray; `return_diagnostics=True`同时返回真实接口端点、接受步长和往返误差. 每列从独立接口坐标出发, 按相邻块宽缩步, 核验裁剪/归一化后的实际路径; 不可分辨或不忠实的方向明确报错. [_gapn2_o3_scan.py](_gapn2_o3_scan.py)与P3二阶变分实际入口已重跑, 四组有限配置见[本轮报告](../reports/proof-audit-round11-20260926/REPORT.md). 21个jac_fd命名调用文件已静态清点, 不表示这些文件的全部历史CLI均重跑. 无严格导数误差界或全参数符号证书.

第十轮修订入口: [_sl_prufer.py](_sl_prufer.py)、[_gapn2_symmetry_recon.py](_gapn2_symmetry_recon.py) 与二阶变分诊断. 固定网格变号不保证谱序号; 当前每个n*pi相位水平单独括根, mp细化和FD端点保持指标, 不能分辨时明确报错. 反射种子按几何作用-J区分preserve/break, 校验实际接口及可行步长. 具体执行范围见[报告](../reports/proof-audit-round10-20260925/REPORT.md); 未重跑76项调用闭包的全部历史实验.

从仓库根目录运行时，为新实验指定独立输出位置。例如在 WSL 中：

```bash
python3 scripts/_gapn2_symmetry_recon.py 2 4 16 both 4 --output-dir /tmp/sl-round10-new-recon
python3 scripts/_gapn2_second_variation_probe.py 2 4 sup --output /tmp/sl-round10-new-variation.json
```

侦察的五个位置参数依次是 n、R、普通随机种子数、图案、工作进程数。纯破缺/保持种子另由 `--break-repeats`、`--preserve-repeats` 控制，默认每种图案分别112和24个，输出的 `*-seeds.json` 保存实际步长、坐标转换检验和拒绝原因。普通随机种子不冒充纯扇区；初始标签也不约束后续优化轨迹。二阶变分 JSON 的 `root_index_records` 保存逐根指标证据，`certified:false` 表示浮点数值检查，不能作为严格区间证书。

第九轮当前诊断入口为 [_gapn2_second_variation_probe.py](_gapn2_second_variation_probe.py). 投影用 A_i=∫I_i f 而非块平均; 另外直接积分检查一阶变分, 谱配对在真实密度/方向断点分段. 记录截断、求积和有限差分步长敏感性, 拒绝通过截断负密度制造可行扰动. 脉冲宽度或实际求积节点在浮点坐标中不能分辨时明确报错, 防止假零贡献. R=1 保留兼容. 有限样本符号不是 Hessian 定性证明或盒约束全局最优性.

[_gapn2_k_global_rank2.py](_gapn2_k_global_rank2.py) 本轮只修正文档范围: 保留有限的移动界面加速度贡献, 不以 Green 对角发散推导其符号. 其 K 实现及历史 R206 扫描没有因此得到重认证. 原错误程序和失败解释保留在历史证据, 当前替代与复现入口见 [第九轮报告](../reports/proof-audit-round9-20260923/REPORT.md).

第八轮 INF 的当前精确入口为[certificate.py](../research/artifacts/proof-audit-round8-20260922/certificate/certificate.py), 证明算术仅用有理数, Machin/Taylor余项及显式守卫; 十进制仅负责向外显示. [第八轮报告](../reports/proof-audit-round8-20260922/REPORT.md)给出普通/-O/-S执行、反例对照和独立复核.

原 INF run 的05/16/19以及本目录 `_theoremA_recheck_*` 的旧抽样保留溯源. 05的像端点与16/19超越函数包络不能继续作为当前认证; 16的域覆盖由新的解析相位下界替代. 17/18及其它未重跑扫描没有获得本轮认证. 复用工具时从当前卡及精确版本回执进入.


[研究导航](../docs/research-guide.md) | [工具库](../tools/README.md) | [目录与复现](../docs/repository-guide.md)

第七轮的当前诊断入口是 `op03_gap_fh.py`、`gap_n1_grad.py` 及报告列出的八个接口/矩阵诊断程序. 修订针对镜像坐标、SUP/INF 符号、两特征值权重和完整 Hessian 的矩阵乘法. [第七轮报告](../reports/proof-audit-round7-20260921/REPORT.md)区分实际 CLI、函数/AST 小样本回归与未重跑的历史扫描; 不将有限点通过理解为全部解析 Jacobian 后端或全 R 研究已经认证.

已确认的遗留问题: `op03_gap_precise.py` 的特征函数传播顺序会破坏权归一化, 不能作为新的特征函数/FH 验证依据. 当前 `op03_gap_fh.py` 使用现有 `op03_gap_fixed.py`, 并以独立分块 ODE 积分核对有限样例. 其它仍导入 precise 的旧 `op03_gap_fh2`-`fh10`、`dbg*`、`shoot*`、`scan*` 等程序保留历史原字节, 不因名称含 precise 而获得可靠性保证. 单接口的 FH 系数本身不应一律加倍; 复用旧程序前必须同时核对参数坐标和特征函数后端.

`docs/SL_gap_extremals.tex` 是2026-08-05的历史数值报告，仍保留当时的故障归因。它不属于本轮逐段重审的当前证明；尤其不能把其中“传播顺序导致特征值错误”的归因视为本轮已核实结论。当前工具卡只按其注明的历史数值范围引用该来源，新的谱编号依据见第十轮报告。

本目录积累了不同阶段的数学程序. `num_*`, `h3_*`, `op*`, `_gapn2_*` 等名称是历史命名, 不表示统一 API 或严格性等级. 保留研究程序的输入条件, 精度, 输出与证明接口, 才能判断它能支持什么结论.

| 需要做的事 | 先读什么 |
| --- | --- |
| 查找相位, 转移矩阵或谱极值方法 | [研究图的 B 系列](../research_map.md), [谱研究导航](../docs/research-guide.md) |
| 查找矩递推或稠密性程序 | [研究图的 A 系列](../research_map.md), [工具索引](../tools/README.md) |
| 重放精确证书 | 对应 run 的 `repro_manifest.md`, `reproducibility/` 或证明中的程序清单 |
| 理解一次失败尝试 | 原 run 的研究台账, 反例记录与后续修正, 再看 [项目理解](../docs/PROJECT_UNDERSTANDING.md) |
| 维护 Blueprint | 当前安装插件的运行时 gateway, 见 [维护规则](../AGENTS.md) |

数值网格和浮点优化通常提供 EVIDENCE. 符号恒等式或有理数证书可以成为严格论证的一部分, 前提是数学证明说明了覆盖范围, 精确算术和从计算结论到定理的连接. 目录位置不能替代这项判断.

部分程序在 run 中还有相同副本. 例如 `densbc_v1_*` 至 `densbc_v6_*` 被历史台账按当前路径引用, run 副本又承担固定复现包的用途, 因此本轮保留两者. 没有把 scratch, 超时或无返回任务自动判为废弃研究.

本轮移除了经检查无调用或证据引用的一次性维护程序, 清单见 [清理报告](../reports/repository-cleanup-20260909/REPORT.md). 新增可复用数学程序时, 可在工具卡记录用途和指针, 让后续研究找到它, 不需要再复制一份通用执行框架.

第三轮审计修订了 `d3_stability_verify.py`, `d3_stability_verify2.py`, `op12_dichotomy_verify.py`, `op12_threshold_verify.py`, `op12_sparse_check.py`. 这些程序区分一般递推与 B=0 乘积模型, 保留正确的 c0 归一化、扰动系数及稀疏跳点. 有限部分和与浮点曲线只作诊断, 不据此判定无穷级数收敛. 实际执行及独立检验见 [第三轮报告](../reports/proof-audit-round3-20260920/REPORT.md).

`scripts/_patch_stability12*.py` 是历史文本补丁, 包含本轮已撤回的陈述, 仅为溯源保留原字节. 它们不是当前证明、验证程序或文档更新入口. 本轮修订以现行 TeX、上述五个诊断程序及第三轮报告为准.

第三轮独立程序检验另发现多步相减的符号误判. 最终 `solve_u_log` 用输入系数的精确有理数比值递推决定正负, 只把对数输出交给浮点; 它不会恢复输入前的舍入信息, 且分母增长可能增加计算成本. 首次拒收与修订后检验分别保留, 见报告.


第四轮审计的当前活动入口为 `d4_third_order_theory.py`. 它用有理除法检验四个闭式, 使用带逐项非零前提的正确降阶系数, 并以正的二阶差分作有限向后计算. 数值部分采用任意指数范围, 不把有限 N 的结果当作无穷极限证明; 检验失败显式返回非零退出码. 原程序曾输出 False 和 nan 而退出0, 原字节与实际日志保存在第四轮审计工件中.

`d4_third_order_theory2.py` 与 `h3_v56_odd_explicit.py` 包含已更正的旧降阶公式, 仅供追踪失败路线. `d4_verify*.py` 和 `op13_*.py` 属历史实验, 本轮没有把它们的旧打印、符号求解或有限扫描重新认证为完整证明; 复用时先检查现行三阶递推文稿的适用范围.
