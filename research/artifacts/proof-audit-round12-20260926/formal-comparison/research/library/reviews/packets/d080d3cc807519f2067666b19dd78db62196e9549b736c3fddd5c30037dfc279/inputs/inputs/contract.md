# 第十二轮局部 Lean 作者 contract

状态: 作者提交, 独立盲读和独立实际执行语义复核均待完成. 编译成功只认证本文件明确列出的有限代数. 本文不构成最终检验者的回执.

## 对象和量词

任意 n : ℕ, 包含 n=0. 配对坐标 I_n = Fin n ⊕ Fin n. 标量域为 ℝ, K 是任意 I_n × I_n 实矩阵. 不要求 K 对称、与反转对易、来自 Green 核、来自自洽点或具有任何谱符号. 原顺序坐标 J_n = Fin(n+n), 即 2n 个坐标, 从 0 起编号.

order : I_n ≃ J_n 定义为 order(inl i)=i, order(inr i)=2n-1-i. 它是实际 Lean Equiv, 不是附加的双射假设. Fin.rev 在 J_n 上是 r ↦ 2n-1-r. 定义 paired(K₀)_{ij}=K₀_{order(i),order(j)}. 因 order 是双射, 原顺序中的任意矩阵都被覆盖.

P_{ij}=1 当且仅当 swap(i)=j, 否则为 0. 因而 Px 是镜像反转后的向量. E=diag((-1)^i) 是左半区的交错符号. S=diag(sign), 其中 sign(inl i)=(-1)^i, sign(inr i)=-(-1)^i. orderedP_{rs}=δ_{rev(r),s}, orderedS=diag((-1)^r).

采用无归一化列 Be=[I;I], Bo=[I;-I], 每列分别是同一镜像对的和与差. I 是矩阵单位元, 不是常值为 1 的函数. orderedBe(r,i)=Be(order⁻¹(r),i), orderedBo 同理; 它们正是原顺序列 e_i+e_{2n-1-i} 和 e_i-e_{2n-1-i}. normalizedBe=(√2)⁻¹ Be, normalizedBo=(√2)⁻¹ Bo. 缩放桥接在 Lean 中证明, 并未将无归一化压缩冒充源码采用的归一化压缩.

分别定义:

- rawKe(K)=Beᵀ K Be.
- rawKo(K)=Boᵀ K Bo.
- Kp(K)=S K S.
- KpOdd(K)=rawKo(Kp(K)).
- KpEven(K)=rawKe(Kp(K)).

命名约定是对象区分, 不是假设它们相等. 当前源的一基约定 j=1,...,2n 下 ε_j=(-1)^(j+1), 首项为 +1; 令零基 i=j-1, 则 ε_j=(-1)^(i+2)=(-1)^i, 与本文 S 的首项 +1 完全一致, E 就是 S 的左半对角块. 旧 half 卡混合一基/零基的 beta 表述不能据此解释为当前源需要首项反号. convention_bridge 中的 -S、-E 仅是一般整体改号约定转换, 并非对接当前源的必需修正. 实际 eigen_data 用 np.sign(u_np1/u_n) 计算 eps; 本轮对接交错符号的坐标约定, 不形式化证明该数值程序或谱模型对任意输入都会产生交错符号.

## 九项数学声明与一个汇总根

1. `coordinate_bridge`: 对所有 n, 证明 order 的左右数值位置, order(swap i)=rev(order i), sign(i)=(-1)^order(i), paired(orderedP)=P, paired(orderedS)=S. 这把配对模型绑定到原顺序的反转和真正交错对角矩阵.
2. `involutions`: P²=I, E²=I, S²=I, 且 P、E、S 均等于其转置.
3. `basis_relations`: P Be=Be, P Bo=-Bo; BeᵀBe=BoᵀBo=2I, BeᵀBo=0; S Be=Bo E, S Bo=Be E. 对 n>0, Gram 关系排除零映射/降秩的伪基底; n=0 时是合法的空矩阵恒等式.
4. `sector_exchange`: 对任意 n,K, KpOdd(K)=E rawKe(K) E 且 KpEven(K)=E rawKo(K) E. 无交换假设, 无对称假设, 无 n=2 限制.
5. `ordered_compressions`: 对任意原顺序实矩阵 K₀, orderedBeᵀ K₀ orderedBe=rawKe(paired K₀), 奇列同理; 并直接证明
   orderedBoᵀ (orderedS K₀ orderedS) orderedBo = E (orderedBeᵀ K₀ orderedBe) E,
   orderedBeᵀ (orderedS K₀ orderedS) orderedBe = E (orderedBoᵀ K₀ orderedBo) E.
6. `normalization`: normalizedBeᵀ normalizedBe=normalizedBoᵀ normalizedBo=I, 且对任意 K, 两种归一化压缩分别为 (1/2)rawKe(K)、(1/2)rawKo(K). 使用 ℝ 上的正平方根, √2≠0 是已知数值事实而非额外未证假设.
7. `odd_rank_one`: 对任意 v:Fin n→ℝ, w=(v,-v), outer(w)=wwᵀ. 证明 rawKo(wwᵀ)=4vvᵀ, rawKe(wwᵀ)=0, KpOdd(wwᵀ)=0; v≠0 蕴含 rawKo(wwᵀ)≠0. 这是奇向量外积项在 raw-K 奇压缩中存留的有限代数事实. 归一化压缩系数 2 是结合第 6 项得到的推论. 未证明一般矩阵秩定理、完整 Green 展开或特定谱项系数公式.
8. `convention_bridge`: (-S)K(-S)=Kp(K), (-S)Be=Bo(-E), (-S)Bo=Be(-E); 两条交换恒等式也直接以 normalizedBe、normalizedBo 表述. 前半部分只讨论一般的整体改号约定, 不声称当前源码首项为 -1; 后半部分对接原源码的 1/√2 列, 两条恒等式仍成立.
9. `distinct_sectors_counterexample`: 存在 n=1 的对称实矩阵 K, 满足 PK=KP, 但 rawKo(K)≠KpOdd(K). 证明中的具体见证为 K=P=[[0,1],[1,0]], 两个一维无归一化压缩分别为 -2 和 +2. 归一化后分别为 -1 和 +1. 因此加入反转对易也不能将一般的扇区交换错误地改成同一奇扇区相等.
10. `audit_root`: 上述九项完整、带量词的命题之合取, 有实体证明. 它不是以正确性谓词、预先假设的交换式或已通过标记替代结论.

`contract.json` 为插件 exact-root 接口, expected_type 写出上述实际完整合取. build_contract.py 仅从作者源码头部复制类型以避免 JSON 转义错误; 这是作者提供的机械类型契约, 不是独立语义审计. 人类目标是否与该类型一致仍由后续两个全新检验者判断.

## 证据与边界

- 正文 `project/AuditRound12.lean` 只导入只读 Mathlib, 不依赖旧轮次证明、负对照或作者导出程序.
- `declarations.json` 从实际编译环境枚举 AuditRound12 命名空间的声明, 导出显式类型、所有隐参数/实例 binder、universe、非定理定义体和 Lean collectAxioms 的传递公理. `declarations.txt` 是该 JSON 的可读转换, 不是人工重述.
- `blind/` 提供去注释正文、实际导出和校验清单, 不附本 contract 或作者解释. 名称保留, 不伪称作者已经做过盲读. 汇总根的导入模块闭包与运行环境由插件 evidence 清单绑定.
- 所有实际编译命令及 stdout/stderr、退出码、PID、前后源码 SHA256 和不可覆盖的输入快照保存在 commands/ 和 evidence/. 开发失败原样保留; 控制程序只验证所针对的错误, 不是全库测试.
- 最终机器结果只在 summary.json 引用的精确 manifest 与哈希上成立. 允许基础公理集合是 {propext, Classical.choice, Quot.sound} 的子集. sorryAx、额外公理、未知/unsafe 依赖不能被作者判为合格.
- 只读复用指定 Lean 4.31.0 Windows 编译器及仓库 .lake/packages. 不运行全 lake build、不下载包、不安装运行时、不写仓库/插件/缓存/历史、不 commit/push、不创建子 agent.
- 不主张完整惯性理论已形式化. Eᵀ=E、E²=I 和交换式给出合同变换表达, 此轮未引入惯性指标的定义或 Sylvester 定律. 不主张 Green、Pruefer、数值 Python 或完整 Sturm-Liouville 论证已获 Lean 认证.
