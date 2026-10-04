# 第十四轮独立软件及数值身份复审

日期: 2026-10-04.
结论: **APPROVE**, 仅批准下述精确 code-v3 冻结输入在 R14-01/R14-02 软件合同与有限数值验收范围内的修订. 本批准不认证解析补证, 无限维定理或全参数结论.

审查者的原生任务身份是 `/root/r14_software_review`. 任务指定作者为 `/root` 和 `/root/kernel_repair`; 我未编写或修改任何冻结项目源. 未请求或伪造旧工具 UUID, `fork_context` 字段或 Lean 回执. 我只读取协调器指定的 code/code-v2/code-v3 清单及其列明文件, 和自己写入 reviews 的证据. 未读取记忆, 技能, 作者会话记录, 其它审查结论或真实工作区. 作者自检数量不作为本批准证据.

## 输入与执行绑定

最终输入目录是 `F:/tools/math-audit-round14-20261004/final-review/code-v3/`. 清单列明 22 项, 不包含自身. 执行前及全部执行后, 22 项 SHA256 均与清单一致. 清单本身的 SHA256 是:

`efdf30825c1ed5533508431a6cfa460fc547db616285e101fee9199cbdfb298d`.

逐文件身份分别保存于 `software-v3-input-hashes.json` 和 `software-v3-post-run-hashes.json`. 相对 v2, 最终只改变了 `checks.py` 和 `_gapn2_ktilde_positivity.py`; 我重新阅读了这两项, 其余源按已独立阅读过的精确字节身份绑定. 关键身份如下:

| 文件 | SHA256 |
| --- | --- |
| checks.py | 4b8f5cdc5b31c0c5a8ae4d85321a114017f7dab73baae77cf28153d615055311 |
| kernel_checks.py | 4afedff806e2d724ff664a33d6e3311786f718e279bd973da7818d785d6e6fa6 |
| _gapn2_ktilde_positivity.py | 57d920da125e0ec39436092fc2d83de2f8044209ec902bc90b513053aacd42ba |
| independent_physical.py | 79de8bed29436b2c04f51a064b0274f6a2465ebb9bc38d6da9fd60ccad65eef3 |
| independent_threeblock.py | d0126efead63b396b24fd6e78a7475d5a3d267ecb2655ca4fb293dcb2fbe56f6 |

实际解释器为 `C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe`, Python 3.10.11, 64 bit. 实际库版本为 numpy 2.2.6, scipy 1.15.3, sympy 1.14.0, mpmath 1.3.0, 保存于 `software-runtime-dependencies.json`. 六次执行均以 `F:/tools/math-audit-round14-20261004/reviews` 为 cwd, 使用 `-B` 禁止字节码写入, 普通和 `-O -B` 分别启动进程. kernel_checks 的四组独立进程导入顺序检查也实际退出 0. 补充探针核对导入的项目模块全部在最终清单内.

| 执行文件 | 普通 | -O | 进程退出 |
| --- | --- | --- | --- |
| 冻结 checks.py | 62/62 PASS | 62/62 PASS | 均为 0 |
| 冻结 kernel_checks.py | 143/143 PASS | 143/143 PASS | 均为 0 |
| 审查者 software-supplement-v2.py | 26/26 PASS | 26/26 PASS | 均为 0 |

这些记录有重叠义务, 不宣称其总和是不同的数学性质. 六份完整输出为 `software-v3-{checks,kernel_checks,supplement}-{normal,optimized}.json`, 对应 stdout/stderr 保存为同名 `.stdout.txt`. 实际逐次命令, cwd, exit code, 输出 SHA256 和补充探针源码 SHA256 完整保存于 `software-v3-executions.json`.

以下六条是实际解释器调用, 每条均带显式冻结根和独立输出路径:

```powershell
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -B 'F:/tools/math-audit-round14-20261004/final-review/code-v3/research/artifacts/proof-audit-round14-20261004/checks.py' --root 'F:/tools/math-audit-round14-20261004/final-review/code-v3' --output 'F:/tools/math-audit-round14-20261004/reviews/software-v3-checks-normal.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -O -B 'F:/tools/math-audit-round14-20261004/final-review/code-v3/research/artifacts/proof-audit-round14-20261004/checks.py' --root 'F:/tools/math-audit-round14-20261004/final-review/code-v3' --output 'F:/tools/math-audit-round14-20261004/reviews/software-v3-checks-optimized.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -B 'F:/tools/math-audit-round14-20261004/final-review/code-v3/research/artifacts/proof-audit-round14-20261004/kernel_checks.py' --root 'F:/tools/math-audit-round14-20261004/final-review/code-v3' --output 'F:/tools/math-audit-round14-20261004/reviews/software-v3-kernel_checks-normal.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -O -B 'F:/tools/math-audit-round14-20261004/final-review/code-v3/research/artifacts/proof-audit-round14-20261004/kernel_checks.py' --root 'F:/tools/math-audit-round14-20261004/final-review/code-v3' --output 'F:/tools/math-audit-round14-20261004/reviews/software-v3-kernel_checks-optimized.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -B 'F:/tools/math-audit-round14-20261004/reviews/software-supplement-v2.py' --root 'F:/tools/math-audit-round14-20261004/final-review/code-v3' --output 'F:/tools/math-audit-round14-20261004/reviews/software-v3-supplement-normal.json'
& 'C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe' -O -B 'F:/tools/math-audit-round14-20261004/reviews/software-supplement-v2.py' --root 'F:/tools/math-audit-round14-20261004/final-review/code-v3' --output 'F:/tools/math-audit-round14-20261004/reviews/software-v3-supplement-optimized.json'
```

## R14-01 的实际验收

我独立阅读了 `Recon.stationarity_diagnostics`, `solve`, `one_solve`, `symmetric_root`, 各续接调用和驻点专用组装. 接收实际检查 F=f/b 的绝对残差, 局部相对平衡, 模态能量分母的可分辨性, 简单 switching 零点导数, 相对相邻宽度的线性校正及真实局部零点校正. optimizer success 不能绕过这些检查, optimizer failure 直接归为 not_converged. 失败和 unresolved 不返回已接受驻点.

指定 n=2, R=4 SUP, delta=1e-6 的宽度反例实际产生 `absolute_max=5.702438102321175e-10`, 而局部相对缺陷最大值约为 0.670103092936. symmetric_root 拒绝它, one_solve 返回 None, full_report.stationary 为 false, sector_data 和专用 Kp 公式拒绝输入. 独立物理参考在 65 位精度下用实际 ODE 传递, 逐块三角零点计数和独立求积质量重现该相对缺陷. delta=1e-12 的分母为 unresolved, 不接受. 没有用删除反例或任意宽度地板掩盖问题.

Recon/Reduced 坐标转换使用无截断 softmax. Reduced first/last/both 的实际 one() 路径及 solve 不接受折叠伪根或未收敛候选; targeted 和 kidentity 的约化候选路径也调用同一 solve.stationary 接口. 现有 reflection-seed helper 的采样地板属于有限种子生成约束, 没有进入 Recon/Reduced 的坐标转换或最终接收规则, 也不能解释为排除所有更窄数学构型.

R4 SUP 和 INF 内部正对照均得到接受. 在我另行启动的 80 位物理参考中, 一基模式 2/3 分别有 1/2 个内部零点; 独立求积质量得到的界面值与导数和工作源共同归一化状态最大差不超过 3.56e-15. 所以正对照不是只靠旧表或同一谱枚举器自证身份.

残差仍为 F=f/b. 一般 `jacobian_terms` 保留完整规范化项及 quotient 项 `-outer(f,v^2)`, 没有改成相对残差的 Jacobian. 非驻点一般 J_F 仍可计算, 驻点 Wronskian 专用身份返回 None. 与独立三块物理隐式导数参考比较, N=160/640 的最大误差分别是 0.035981854601316865 / 0.009079604788056361. 这验证本例的截断收敛, 不证明一般尾界.

## R14-02 的实际验收

全 DD gtilde, print wrapper, `_full_S`, 半 DD/DN 的谱和 closed reduced Green 均通过共同几何/边界/一基模式表验证目标身份与覆盖. legacy 零基 k/pole_idx 有显式检查和转换; closed reduced 的正参数须与指定 BC 的 indexed eigenvalue 唯一匹配. 每个未删除分母均检查有限性和数值可分辨性, 不能只因为删除一个数组项就声称 pole identity.

实际负对照覆盖错误 lam/k, 正特征值的小相对扰动 1e-9, 错边界, 错几何, 表覆盖不足, 列表外坐标, 非有限/复数/布尔非法标量, 不可分辨频率和分母溢出. 这些入口均以 ValueError/ArithmeticError 拒绝. n=2 的 positivity 组装在 N=1 时明确拒绝, 未把不覆盖相邻模式的有限表达式当成合格核.

半 DD/DN 常密度前 160 个模式及 4/80 模式前缀身份实际通过. 非正普通 Green 的 mu=0,-1, 任意坐标顺序, 重复点和端点行为保留. 指定常密度/跳密度 closed reduced 与 N=320/640/1280 谱和的有限 Richardson 比较通过, 最细比较的最大差均小于 1.4e-7; 这不是严格尾界.

## 首轮退回及最终扇区纠正

v2 的两套作者测试在我实际重放中均通过, 但审查者独立组装发现 `_gapn2_ktilde_positivity.run` 把 Kp=SKS 的偶/奇谱标成 raw K 的 evKe/evKo. 在相同 N=40, 我从实际一般 J_F 定义 raw K=diag(1/s)J_F, 再构造 SKS, 以正交反射偶/奇基分别投影. sector_data 与这两个实际对象相符, 而旧 positivity 返回值只与 SKS 相符. SUP/INF 的 raw 标记误差分别约为 1.9034364992 / 6.2262517130. 普通和 -O 均复现. 总行列式或整个矩阵谱在符号共轭下不变, 不能替代扇区身份.

该 v2 结论为 CHANGES_REQUIRED, 完整报告和两个失败 JSON 原样保存在 `software-v2-review.md` 与 `software-v2-supplement-{normal,optimized}.json`. 初版补充探针对 import-membership 记录的缩进导致重复记录, 不改变两条实质失败; 原执行源保存在 `software-supplement-v1.py`. 新补充源只将该记录移出循环并加入显式 Kp 输出验证.

v3 在源码第 78-96 行明确命名闭式 Kp, 通过 S=diag(eps) 共轭产生 raw K, 分别返回 evKe/evKo 和 evKpEven/evKpOdd. 我重新读取并重放整个最终冻结包. 当前 raw K 及显式 SKS 两个扇区, 对直接 J_F 组装的最大谱误差为 SUP 4.44e-14, INF 3.79e-12, 普通和 -O 一致. 因而此项具体拒收理由已在新字节上关闭, 旧拒收仍保留.

更早的清单自引用不匹配, 可移植测试路径修正及依赖闭包缺项保存在 `software-initial-observations.md`, `software-initial-input-hashes.json`, `software-second-input-hashes.json`. 我未执行初始不闭合 code/ 包, 不声称该版运行通过.

## 明确限制

本批准只绑定 code-v3 清单, 指定数值合同和实际检查. 未读取或认证解析补证. 有限 Gram/Mellin/端点代数检查不证明无限维定理, 正对照及局部求根也不证明全部参数的唯一性或无旁支. 误差半径和局部接收是 floating diagnostics, 不是区间证书. 旧 direct resolvent subtraction 仍有源码中的弃用警告, 未被本审查提升为可靠 Jacobian 入口.

冻结包没有提供 Lean 目标, 本审查没有执行 Lean, 也没有形式化陈述/公理审核结论. 没有运行大规模历史扫描, 修改项目/canonical/历史证据, 执行发布或借用工作区依赖. 任何进一步源字节变化均需新的精确输入绑定, 不能承接这份报告的 PASS.
