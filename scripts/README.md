# 研究脚本导航

[数学问题与证明](../docs/research-guide.md) | [工具卡与门禁](../tools/README.md) | [目录与复现](../docs/repository-guide.md)

以下按实际用途选择当前入口. 这次文档整理未执行数学程序或重认证历史扫描; 表中的测试范围来自对应冻结报告. 从仓库根运行, 为新实验指定独立输出位置, 保留旧证据文件.

## 当前数值计算与诊断

| 入口 | 用途与接口语义 | 已记录验证及限制 |
| --- | --- | --- |
| [_sl_prufer.py](_sl_prufer.py)::indexed_roots, [op03_gap_fixed.py](op03_gap_fixed.py)::lams_precise | 按提升相位给模态逐项括根. fixed 兼容名称返回首 k 个**频率 omega**, 特征值为 omega². DD 是默认边界, 半问题 RightBoundary='N' 对应 DN 的半整数相位 | [R15](../reports/proof-audit-round15-20261005/REPORT.md): 普通/-O 各 92 项性质, 审查者各 103 项独立补测; 13 个直接导入者只作静态清点, 未重跑全部历史 CLI |
| [op03_gap_fh.py](op03_gap_fh.py), [gap_n1_grad.py](gap_n1_grad.py) | 物理归一化特征函数与 FH/坐标导数. 保留平方转换, 区分单接口与镜像成对坐标; FH 系数不一律加倍 | [R7](../reports/proof-audit-round7-20260921/REPORT.md) 的局部回归及 R15 四个原 R4 FH 点; 不认证所有旧 R4 数据 |
| [_gapn2_symmetry_recon.py](_gapn2_symmetry_recon.py) | 分块谱, 一般残差/Jacobian, 驻点求解/续接. F=f/b 保留; 绝对残差, 局部相对平衡, 模态分辨和切换零点校正共用验收. 未收敛/不可判定拒绝; 纯 softmax 不设块宽地板 | [R14](../reports/proof-audit-round14-20261004/REPORT.md): 普通/-O 各 62 项驻点性质; optimizer 成功或小 F 本身不证明驻点 |
| [_sl_spectral_identity.py](_sl_spectral_identity.py), [_gapn2_half_problem_probe.py](_gapn2_half_problem_probe.py) | 谱表绑定几何, 边界, 一基目标, 覆盖与未删分母. half_spectrum 的默认 ndarray 保留, return_table=True 给只读表; mumax 不足报错. _spectral_green 兼容零基 pole_idx, 内部核对一基身份 | [R12](../reports/proof-audit-round12-20260926/REPORT.md), [R14](../reports/proof-audit-round14-20261004/REPORT.md): 后者普通/-O 各 143 项核性质及独立补测; 有限浮点诊断 |
| [_gapn2_jacobian_probe.py](_gapn2_jacobian_probe.py), [_gapn2_sector_decomposition.py](_gapn2_sector_decomposition.py), [_gapn2_green_inertia_probe.py](_gapn2_green_inertia_probe.py) | JP=-PJ 的 Jacobian 使用交叉 C,D, detJ=(-1)^n detC detD; sym_antisym_decomp 返回 C,D. 与 P 对易的 Hessian 另处理. Ke/Ko 属 raw K, Kp* 属 SKS; c_e/c_o 属 Kp 秩一分解 | [R11](../reports/proof-audit-round11-20260926/REPORT.md), R12/R14: 实际有限差分路径及核对象核对; 21 个 jac_fd 命名调用者静态清点不等于全量运行. 无全参数导数误差/符号证书 |
| [_gapn2_second_variation_probe.py](_gapn2_second_variation_probe.py) | 有界方向配对及 P1/P2/P2b/P3. BlockDirection 保留所有 rho/h 断点, 每共同小段局部解析积分, 原共同质量与模态身份复用; 近节点/小相位稳定回退, 折叠/下溢拒绝 | [R16](../reports/proof-audit-round16-20261006/REPORT.md): 普通/-O 各 205 项, 各 105 项独立补测及 n=2,R=4 SUP/INF 完整 CLI. 浮点误差估计不认证 Q 符号 |
| [d4_third_order_theory.py](d4_third_order_theory.py), [d3_stability_verify.py](d3_stability_verify.py), [op12_dichotomy_verify.py](op12_dichotomy_verify.py) 等 | 指定递推族的有理恒等式或有限向后诊断; 一般递推与 B=0 乘积模型分开. solve_u_log 用输入精确有理比值决定符号, 不恢复输入前舍入 | [R3](../reports/proof-audit-round3-20260920/REPORT.md), [R4](../reports/proof-audit-round4-20260921/REPORT.md): 对应明确程序的行为检查. 有限 N/部分和不是无穷极限证明 |

### 容易误用的参数

- lams_precise 的 tol 请求 bracket-width<=tol*max(1,omega); binary64 无法分辨时报错. smax_scale 默认 5 兼容静默, 非默认有限正值有弃用警告, 非法值拒绝; 不再控制网格.
- eigenfunction_states 的值/导数使用同一物理解和加权质量. real_green_matrix 按真实坐标组装, 可处理端点及非正参数; 半问题约化核仍限正特征值. 一般 Jacobian 公式只在精确 F=0 恢复驻点简式.
- jac_fd 默认 ndarray, return_diagnostics=True 给实际接口端点, 接受步长和往返误差. 反射种子按几何导数 -J 区分 preserve/break; 初始扇区标签不约束后续轨迹.
- 配对回调声明已知 Breaks, 节点须在段内部且互异, 在 MaxOrder 内通过两次连续误差比较; 未决抛 ArithmeticError. PairingResult 兼容四数组, diagnostics 保留, return_diagnostics=True 给第五项. CLI 保存诊断, sign_certified=false, 黑箱/舍入包络未提供; 原始 Parseval 浮点残余不截零.
- 二阶变分切空间用真实块积分 A_i, 不能用块平均替代; 不裁剪负密度制造可行方向. 固定宽度 P3 不等于脉冲极限, 移动界面的加速度另计.

需要运行侦察时的调用形式如下; 本轮未执行这些示例:

```bash
python3 scripts/_gapn2_symmetry_recon.py 2 4 16 both 4 --output-dir /tmp/sl-new-recon
python3 scripts/_gapn2_second_variation_probe.py 2 4 sup --output /tmp/sl-new-variation.json
```

侦察五个位置参数依次是 n, R, 普通随机种子数, 图案, 进程数; --break-repeats/--preserve-repeats 控制其他种子. 输出 seeds JSON 记录真实步长/坐标检查. 这些命令的默认预算应在实际运行前核对源码.

## 精确证书及验证

| 入口 | 合同 | 验证范围 |
| --- | --- | --- |
| [misc/e1_certgen.py](../misc/e1_certgen.py), [e1_cert_receive.py](../misc/e1_cert_receive.py), [e1_cert_tables.py](../misc/e1_cert_tables.py) | 有理端点, 原语包络, 完整目标谓词和失败传播; 生成, 接收, 台账三步分别检查. 失败不发布成功 | [R13](../reports/proof-audit-round13-20260927/REPORT.md) 的 57 条完整账及性质检查. 本轮未重算; R16 通用 Taylor 修订不改变该专用 Fraction 路径 |
| [INF 有理 certificate.py](../research/artifacts/proof-audit-round8-20260922/certificate/certificate.py) | 证明运算用有理数, Machin/Taylor 余项和显式守卫; 十进制仅作向外显示 | [R8](../reports/proof-audit-round8-20260922/REPORT.md) 的实际重放与 56 次预期失败负对照; 以相应覆盖域/解析桥为准 |
| [misc/rigid1d.py](../misc/rigid1d.py) 的两导数 Taylor 符号助手 | 先转精确端点再运算, 核对类型/顺序/分区/预算. True 仍依赖正确 D2 区间回调, False 表示未证明 | [R16](../reports/proof-audit-round16-20261006/REPORT.md) 有限性质与负例; 不是给任意黑箱导数自动认证 |

重放时先读绑定报告及完整冻结输入, 输出另存. R14/R15/R16 的 checks.py 和 R14 kernel_checks.py 是对应版本的验收 harness; 当前检索到它们不表示已对新版本运行. 本轮没有重跑这些研究测试.

## 历史与不推荐直接复用的实现

| 历史入口 | 已知限制或替代 |
| --- | --- |
| op03_gap_precise.py 及仍依赖它的 fh2--fh10/dbg/shoot/scan 等 | 旧传播破坏特征函数权归一化; 新 FH 使用 op03_gap_fixed.py. 不据此断言全部旧特征值/数据错误 |
| asym3/global/global2 的独立 lams_vec/lams_fast, _gapn2_largeR_probe2.py | 独立固定网格或首点比值路径未获共享相位入口的再认证; 新计算从 indexed_roots/fixed 进入 |
| _gapn2_jacobian_pieces.py, _gapn2_green_check.py, _gapn2_k_global_rank2.py | 旧符号/去极点/移动界面解释分别有限; 当前公式读一般 Jacobian, 身份守卫与有限界面证明. 未重认证历史扫描 |
| misc/rigid_dec.py, zz_verify_e1_dec.py, audit_o3a_cert_replay.py | 退役 Decimal 或旧可信接收路径; 当前用 E1 精确生成/接收接口 |
| 原 INF run 05/16/19, _theoremA_recheck_* | 旧像端点/超越包络/域覆盖或抽样不承担当前认证; 相应职责由 R8 解析相位界与有理证书替代. 17/18 等未重跑部分保留原范围 |
| d4_third_order_theory2.py, h3_v56_odd_explicit.py, d4_verify*/op13_* | 旧降阶公式或历史实验; 当前指定族读 d4_third_order_theory.py 与完整证明 |
| _patch_stability12*.py, _json_update.py, _tmp_update_state.py, archive_old_runs.py | 一次性旧文本/状态/mtime 维护逻辑, 不作当前更新或归档入口; Blueprint 操作走已安装插件 gateway |

[SL_gap_extremals.tex](../docs/SL_gap_extremals.tex) 是历史数值报告, 旧故障归因不等于当前已核实结论. densbc_v1--v6 的根目录/run 副本各有路径与冻结复现职责, 保留两者. 名称含 precise/final, scratch 或超时均不能独自决定可靠性或删除.

逐轮接口细节原文在 [本页整理前快照](../docs/history/scripts-README.pre-organization-20261008.txt), [会话日志](../state/AGENTS_SESSION_LOG.md) 和各轮报告. 快照路径按原 scripts/README.md 解释, 历史程序与证据字节未修改.
