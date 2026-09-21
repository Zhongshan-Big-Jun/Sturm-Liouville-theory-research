# 第五轮解析作者提交

角色: 证明作者, 非最终或独立审查人. 本稿等待另一个新会话独立复核.

唯一新增仓库文件: `/mnt/f/LaTeX/BVE research/docs/SL_cofinite_left_definite.tex`.

最终源文件 SHA256:

`ed07e47fd370a9db3b6a6a2d125d9eec996288e53a6024a0e9fb533ca1b3c0bb`

源文件大小: 29161 bytes. 基线: `c0b36b90004cffb0552c9fa9f229e1f7cec8a706`. 最终编译副本与该源文件逐字节一致. 作者在本提交后不再改源稿.

## 数学范围

固定 c > 0, 复 H_c^2 = D(K_c), Krein 边界条件, 第一变量线性内积. 稳定 ID 为 R5-OP, R5-GREEN, R5-REFUTE, R5-ALG, R5-CUT, R5-POLY, R5-TAIL, R5-COFINITE, R5-OBSTRUCTION, R5-TAIL-MOMENT, R5-SUBSPACE, R5-OBLIQUE, R5-MONOMIAL, R5-ODD-FACTOR.

- 原 Claim 4, Theorem 5, Corollary 6 是按原量词被反证的 NOT-YET-STRICT 候选, 不是推翻已验收的 H2/H3 主结论. g_0,c 的 M_0 = 1/c 且所有高阶正交成立.
- 任意完整高阶尾部闭包恰为 V_* = {f: f(0)=f'(0)=0}. 任意所选余有限 N 的闭包只取决于是否保留 p_0=1 和 p_1=x.
- 实际 N_V 余有限的闭 V 恰为 Gamma^{-1}(S), S 是 C^2 的复线性子空间; 它必保留全部 n >= 4. 保留族在 V 内稠密当且仅当 S 由它包含的标准坐标轴张成. 非坐标例 f(0)=f'(0) 的缺失方向为 1+x.
- 用户追加要求已完成: 两条奇偶矩递推在充分高指标成立, 当且仅当 g 属于 span{g_0,c,g_1,c}; 精确公式为 g = c M_0 g_0,c + c M_1 g_1,c. 第一变量线性使系数不取共轭. g_1,c 的一阶矩 1/c 已由 Green 配对和直接积分分别证明, 两个交叉矩为零. 追加 M_0=M_1=0 恢复刚性.
- 有限删除单项式引理用 x^M g 重新证明, 奇部换元范数系数为 1.

## 所供替代证明的核查与补足

作者没有发现附件主闭包结论的新反例或结论级错误. 以下是原先简写环节的补足, 并非都属于附件的新错误:

1. 正性通过端点能量计算证明. 满射性直接解非齐次 ODE 并用齐次端点矩阵修正, 行列式为 2 a sinh(a) [a cosh(a)-sinh(a)] > 0. 不循环使用密度定理. 补出一阶导数控制及迹连续估计.
2. 两个 Green 核列出两端和 0± 的全部必要数据. 界面项为 f'(0) overline([g]) - f(0) overline([g']), 端点项另行抵消. 不把核函数误放进 D(K_c).
3. 截断误差分别由 delta^2 E_delta, delta E_delta, E_delta 控制, E_delta 是收缩邻域内的 f'' 范数. 全区间常数界不能代替收敛. 明确 0<r<=1.
4. 固定 delta 后才对 f_delta/x^L 作 H^2 多项式逼近, 随后用 [[L,L],[-L,L]] 修正端点残差; 修正保持 x^L 整除性. 没有交换极限或假设除法乘子的一致界.
5. 实际子空间分类给出必要充分条件及余维差, 区分任意所选 N 和实际 N_V.
6. 尾部矩用全指标闭包求正交补, 不在缺失的低阶方程处擅自反向递推. 两个低阶核矩唯一确定系数.

## 实际运行的检查

外部新脚本 `check_author_math.py` 未导入或运行所供审计脚本和项目旧 Python 工具. `python3 check_author_math.py` 实际退出 0, 208 个具名检查通过:

- 57 项符号或精确代数检查: 半区间 ODE, 跳跃和端点数据, 四个低阶核矩, 齐次端点行列式, q_n 系数, 复多项式能量/左定内积, m_0=2,3,5 的有限截断尾部秩比较等.
- 136 项 60 位 mpmath 数值检查: c=0.01,1,7,64; Green 配对的 n=0,1,4,5,8,13,24,25; 非实系数核组合的 m=2,...,7 两条递推, 低阶矩, 归一化重构与复共轭.
- 15 项局部截断检查: 对 |x|^(7/4)(1-x^2)^2, 用显式 C^2 五次过渡截断, 在 delta=1/8,1/16,1/32,1/64 上精确积分幂函数, 再数值比较局部误差界与下降. 该样本的二阶导数在 0 附近无界但属于 L2. 不把有限下降样本称为极限证明.

运行环境: Python 3.14.4, SymPy 1.14.0, mpmath 1.3.0. 脚本 SHA256:

`6f196e316f967e6bf3a415a3c95f9dfba14cc8b9d7da7990911c1aa25d384f87`

三个错误注入均实际退出 1: `--negative-control g1_sign`, `--negative-control odd_half`, `--negative-control conjugation`. 分别检出 g_1,c 符号错误, 旧奇部额外 1/2, 和遗漏第二变量系数共轭. 实际诊断见 `negative_controls.json` 及对应 stderr 日志.

两次初始符号运行未通过, 分别因 SymPy 保留未求值积分和生成未识别分母正性的 Piecewise. 未计为通过, 未忽略条件. 后将积分变量无关的分母先提出, 对指数形式分子积分, 等式精确化简为零. 原输出保存在 `checks_attempt_01.*.log` 和 `checks_attempt_02.*.log`.

有限检查是作者侧补充证据, 不替代 R5-TAIL 的全指标分析证明, 不属于独立验收或 Lean 认证. 在协调器要求停止增加测试后, 没有新增或扩展测试.

## 实际编译结果

通过已安装 LaTeX 技能的官方 helper 编译外部源副本:

`python3 /mnt/c/Users/HuangZY/.codex/plugins/cache/openai-bundled/latex/0.2.7/scripts/compile_latex.py /mnt/f/tools/math-audit-round5-20260921/analytic-author/compile/SL_cofinite_left_definite.tex --compiler texlive --engine xelatex --output-directory /mnt/f/tools/math-audit-round5-20260921/analytic-author/compile/build --json`

最终实际退出 0. TeX Live 2026 / XeLaTeX, PDF 共 10 页. 最终日志无缺字, 无未定义引用, 无 overfull box; 存在一处参考文献长路径导致的 underfull hbox (badness 1701, 源码706-709行). PDF 仅在外部目录, 未写仓库 PDF.

初始编译曾因未安装且实际不需要的 mathtools 包, 以及作者草稿换行转义而失败; 删除无用依赖并修正后成功. 原失败和中间成功回执分别保存在 `compile/attempt_01_missing_mathtools.json`, `compile/attempt_02_alignment.json`, `compile/attempt_03_success_before_final_clarification.json`. 未修改系统安装.

在最后两处文字澄清前的成功 PDF 上已提取全部10页并目视第2,3,4,6,7,8页, 覆盖主要公式. `pdf_check/` 保存的是该预览, 对应 TeX SHA256 `34c45c0e245f752cb0a94d8363e58397da68849b9c22450d997eb500564f41b9`, 不冒充最终源版本的页面图. 最后的变动仅补明 r 的取值范围和两递推阈值可取最大值; 最终源已重新编译成功, 未重新声称逐页目视.

## 证据路径和剩余边界

- `AUTHOR_CONTRACT.md`: 用户具体授权, 追加尾部矩要求, 作者职责边界.
- `source_manifest.json`, `sources/`: 6 个输入文件的原字节及 SHA256. `input_recheck.json` 记录核对时六个来源均匹配原快照.
- `author_checks.json`, `author_checks.stdout.log`, `author_checks.stderr.log`: 208 项实际结果.
- `negative_controls.json`, `negative_*.stderr.log`: 3 项实际错误注入回执.
- `compile/compile_result.json`, `compile/build/SL_cofinite_left_definite.pdf`: 最终编译回执及 PDF.
- `submission_manifest.json`: 最终交付文件哈希绑定.

作者未识别出上述固定 c>0、s=2、余有限/完整尾部定理内尚待补证的步骤; 这仍是作者判断, 待新会话独立审查. 一般非余有限 O1'LD, s=3 或其他阶, c=0 和 c->0 一致估计均未解决或未在本稿处理. 未运行 Lean 或历史全链证书. 未重审原 run 其他独立定理或既有 H2 文稿的所有附带断言.

没有启动代理, 没有改既有文稿/工具卡/索引/AGENTS/canonical/历史 run, 没有 Git 写入或发布. 按用户明确范围, 一般 AGENTS 维护要求改由本外部作者合同和说明记录. 最终审查和发布由协调器另行安排. 作者在本提交后停止.
