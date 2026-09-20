# 比值证明作者修订报告, 2026-09-20

状态: **PROOF_SUBMITTED / 待用户独立复核**. 本报告由修订作者撰写, 不作独立 PASS 或验收结论.

## 写入范围与输入保全

- 本次只写入主项目的 `docs/SL_ratio_proof.tex`, `docs/SL_mw_lemma_reproof.tex` 和本报告.
- 未作 Git 写操作、canonical 更新、PDF 编译、AGENTS 维护或其它 gap n=1 文稿修改. PDF、AGENTS 和最终独立 review 由协调器/用户处理.
- 已读主项目及外部工作目录的 AGENTS. 用户明确限定的三个写入路径优先于一般维护要求.
- 首次写入前, 已确认 `math-baseline.json` 存在; 它的时间为 `2026-09-20T10:02:05.049645+00:00`, HEAD 为 `ee90dcc2390eed8586888c07eaaabced37e3226d`.
- 两份 TeX 的输入与该基线逐字节相同. 原始 SHA-256:
  - ratio: `450ec9354480d0163075e6322f7ffa2c8f7ffb75cab588a3c0ef0f252d6ef697`.
  - MW reproof: `3bc10b4ef854f9d9556df0055ca0d5b7d979db829211530b06dc8f8f712d7c8c`.
- 已有大量其它未提交修改与未跟踪文件; 本作者没有回滚、清理或覆盖它们. 不把其他并行作者的改动算成本次工作.
- 读取审计附件的 B05、B06, 并自行核对原稿. 附件提到的 `ratio_first_pair_repair.md` **未提供, 未读取**. 审计提出的切换函数与能量表达式是本轮的研究线索, 不能替代以下推导.
- 用户随后指出本地一手 PDF/TXT. 已读取相关正文, 逐页查看下列承重位置的 PDF 图像. 图像在内存渲染, 未另写图片或中间文件.

## 数学结论及证明义务

对象固定为有限非退化区间上的 Dirichlet 方程 $-u''=\lambda\rho u$, 有限 $R\ge1$, 可测密度 $1\le\rho\le R$ a.e. 第一、第二特征函数按 $\int\rho u_i^2=1$ 归一化. 单点密度值无谱效应.

| 义务 | 本稿给出的解析论证 | 位置/依赖 |
| --- | --- | --- |
| B05, 首对全局最优性 | 先证明极值存在, 再从任意极值密度推出唯一配置, 因而得到对全体密度的上界. 不是从候选值反推 supremum. | ratio `prop:compactness`, `thm:first-pair` |
| 平衡宽度及对称性 | 不预设两者. 由 $E=0$ 得端点斜率比, 外块的正弦匹配给两端等宽, 反射奇偶性及两条内块匹配式给平衡宽度. | ratio `eq:zero-energy`, `eq:endpoint-ratios`, `eq:interface-phases` |
| 闭式 | 对已证明是全局极值的配置作转移矩阵计算. 显式区分候选值 $C_\pm(R)$ 与定义性的 $\nu,\mu$. | ratio `sec:balanced` |
| 仿射缩放 | 若 $L(x)=cx+d$ 把新区间映到旧区间, 则 $\widetilde\lambda_j=c^2\lambda_j$. 包括 $c<0$. | MW `prop:affine` |
| 有符号胞元拼接 | $b_i=y_i'(1/2)/y_i'(-1/2)$, $b_1<0<b_2$, 第 $j$ 胞元用 $b_i^j y_i$. 检查函数与导数连续, 再按零点数识别指标. | MW `lem:cell` |
| 完整零点运动 | 对 IVP 参数求导, 用绝对连续 Wronskian 积分得到左射击 $z_j'=-\int_{-1/2}^{z_j}\rho y^2/y'(z_j)^2<0$; 右射击方向相反. 说明密度界面无遗漏项. | MW `prop:zeromotion`, `lem:count` |
| common-zero 等号分支 | 最小化分成 $z_0<z_{2k}$, $=$, $>$. 等号时右侧截断的前两特征值正好为 $\lambda_m,\lambda_{2m}$. 常密度对所有 $m\ge2$ 都落入该分支. | MW `lem:min` Case B |
| 完整截断归纳 | 以任意密度为起点, 用射击零点数与截断谱的位置关系给上下界. 修正重复的 $z_1$ 名称与归纳基底表述. | MW `lem:max`, `lem:min`, `thm:max`, `thm:min` |
| 密度类与连续性 | 有界可测盒类中的弱星谱连续性保证首对极值存在. 区间平均给保盒约束的有限阶梯 $L^1$ 逼近, 固定编号谱连续性识别三种密度类的极值. 不声称对无界指标一致收敛. | ratio `prop:compactness`; MW `prop:density`, `cor:measurable` |

本次写出的首对论证同时覆盖最大和最小 **比值**. 没有用它替代或重审任何特征值 **间距** 证明.

首对全局论证的关键步骤如下, 每步的推导已放入 TeX:

1. 以 $H_0^1$ 的能量内积定义紧正自伴算子 $(T_\rho u,v)=\int\rho uv$. 单位球乘积族在 $L^1$ 中相对紧, 故有界盒内的弱星密度收敛导致算子范数收敛. 谱极小极大原理给固定编号谱连续性, 弱星紧性保证最大、最小比值均达到.
2. 首变分为 $\delta\log(\lambda_2/\lambda_1)=\int hF$, $F=u_1^2-u_2^2$. 盒约束给相应的 bang-bang 切换规则.
3. 对 $r=u_2/u_1$, 双端积分 Wronskian 给 $r'<0$ 于整个开区间. 因此 $F=0$ 至多发生在两点, 没有正测度的奇异切换集.
4. 用分段线性 Lipschitz 函数 $g$ 表示 $\rho F$: 最大时 $g(t)=Rt$ 对 $t\ge0$, $g(t)=t$ 对 $t\le0$, 最小时反置. 于是 $E=u_1'^2/\lambda_1-u_2'^2/\lambda_2+g(F)$ 绝对连续且 $E'=0$ a.e. 归一化给 $\int E=0$, 从而 $E\equiv0$. 界面处 $F=0$ 保证能量连续.
5. 设 $q=\sqrt{\lambda_2/\lambda_1}>1$. $E(0)=E(1)=0$ 给 $r(0+)=q$, $r(1-)=-q$. 两个切换点必存在, 两侧外密度相同.
6. 外块密度 $d_o$、内块密度 $d_m$ 尚未预设宽度. 在左接口 $\alpha$, 等幅正弦与无零点分支给 $(\sqrt{\lambda_1d_o}+\sqrt{\lambda_2d_o})\alpha=\pi$. 右端得到同一外块宽度, 从而对称.
7. 设 $h=1/2-\alpha$, $X=\sqrt{\lambda_1d_o}\alpha$, $Y=\sqrt{\lambda_1d_m}h$, $Z=\sqrt{\lambda_2d_m}h$. 证明 $0<X,Y<\pi/2$, $0<Z<\pi$, 再从 $\cot X=\sqrt{d_m/d_o}\tan Y=\sqrt{d_m/d_o}\cot Z$ 推出 $Z<\pi/2$ 和 $Y+Z=\pi/2$. 因此 $\sqrt{d_o}\alpha=2\sqrt{d_m}h$.
8. 所以最大配置为 $[1,R,1]$, 宽 $(s,1,s)/(2s+1)$; 最小配置为 $[R,1,R]$, 宽 $(1,s,1)/(s+2)$, $s=\sqrt R$. 这描述的是每一个已经存在的全局极值, 足以给全局上、下界. $R=1$ 单独用常密度谱处理.

两稿的依赖是按命题而非按文件区分的有向无环链:

- 首对紧性与变分结构 -> 候选的闭式计算 -> 首对全局极值.
- 有符号胞元拼接 + Wronskian 零点运动 + 截断归纳 -> 倍指标极值等于定义性的首对极值.
- 上述两支 + $\lambda_{n+1}\le\lambda_{2n}$ -> 全序列相邻比值上确界.
- MW 文稿最后的闭式推论可引用 ratio 的首对结构定理, 但 MW 的倍指标证明不引用这个闭式推论, ratio 主定理也不反向进入首对证明.
- MW 的归一化是 $[a,1]$, 与 ratio 的 $[1,R]$ 通过 $a=1/R$ 对应; 已消除把 MW 的 $\nu(a)$ 写成同一自变量 $\nu(R)$ 的混淆.

## 一手文献定位、原始范围与实际读取边界

| 来源 | 本次核对的 PDF 原页 | 内容和边界 |
| --- | --- | --- |
| Mahar--Willner, *An extremal eigenvalue problem*, CPAM 29 (1976), 517--529, DOI 10.1002/cpa.3160290505 | 印刷 517--519 / PDF 1--3 | 原始范围为跳点数有界的分段连续密度 $0<a\le\rho\le1$; p.518 Theorems 1--2 是两跳及对称结构. 同页明确没有证明跳点唯一性. p.519 (4.1)--(4.5) 是最大情形的界面和归一化系统. |
| 同上 | 印刷 521--524 / PDF 5--8 | Lemma 1 及 (5.3) 原页确为第一函数用 $(-s)^j$, 第二函数用 $t^j$. Lemma 2 原文只详写最大情形, 最小情形以类似论证带过. |
| 同上 | 印刷 526--529 / PDF 10--13 | Lemma 4 及 (5.21)--(5.23) 的商函数/Wronskian机制, Lemma 5 和 Theorem 2 的对称性论证, p.529 Theorem 3 的倍指标极值传递. |
| Keller, *The minimum ratio of two eigenvalues*, SIAM J. Appl. Math. 31(3) (1976), 485--491, DOI 10.1137/0131042 | 印刷 485--489 / PDF 1--5 | (1.1)--(2.1) 的原始分段连续盒类; (3.1)--(3.9) 的归一化、变分和切换条件; p.488 明确把两跳对称结果归于 Mahar--Willner; (4.1)--(4.8) 的最小配置、界面和归一化系统. |

在线检索首先核对了 [Keller 出版社页面](https://epubs.siam.org/doi/10.1137/0131042) 和 [MW 出版社目录](https://onlinelibrary.wiley.com/toc/10970312/1976/29/5). 网页全文访问没有成功; 用户随后提供的本地来源解决了本轮相关正文的获取问题. 上述 PDF 原页核对替代了只看网页摘要的初始状态. 没有声称全部 OCR 正确, 没有逐页验收两篇论文的所有结论, 也没有把当前闭式或能量证明宣称为原创成果.

**依赖区分:** 第一变分和商函数方法有上述一手来源对应. 本稿仍自行证明所需实例, 特别是可测盒类紧性、零能量、对称性和平衡宽度. 首对全局上界不以文献未核实的完整极值定理为黑箱, 也不由 MW 的结构定理加一个平衡候选直接跳出. 背景依赖为弱星紧性、紧自伴谱极小极大原理、经典 Sturm 振荡/比较和常微分方程唯一性/参数依赖.

## 作者检查及其限制

- 10 项 SymPy 精确恒等式: 两个三块转移矩阵式, 仿射 $c^2$, 常密度共同零点及比值, 第二特征函数两端同号斜率, 参数 Wronskian 恒等式, 分块能量导数恒等式.
- 14 组有限数值配置: $R=1,1.5,2,3,4,10,100$ 的最大/最小候选; 根的编号另用零点数核对. 闭式比值最大相对误差 $3.74\times10^{-14}$, 零能量残差最大 $3.78\times10^{-12}$, 接口切换残差最大 $4.20\times10^{-14}$.
- 非对称三块密度 $[1.2,3.4,2.1]$, 宽 $[0.13,0.52,0.35]$, 实际有符号因子约为 $(-0.89825884,0.98066003)$, 不等幅. $n=2,3$ 胞元重复的指标和平方律最大相对误差 $1.20\times10^{-14}$.
- 同一密度在 $\lambda=80$ 的四个内部零点, 参数 Wronskian 导数与中心差分的最大绝对差 $1.29\times10^{-12}$; 一阶变分与中心差分的绝对差 $6.92\times10^{-12}$.
- 截断检查使用固定随机种子 20260920, 十个非对称四块密度, 各检查 $k=1,2,3$. 30 个样例覆盖最大分支 A/B 各 14/16 个, 最小严格分支 A/C 各 14/16 个, 并核对左右截断的谱指标. 等号分支由常密度的符号恒等式和正文解析论证承担, 不靠随机采样碰到它.
- 另用一维有界优化对 $R=2,4,10,100$ 的对称三块族进行发现阶段核对, 最优宽度与平衡宽度吻合. 这只是对称子族有限数值观察, 不进入全体密度的证明链.
- 两份 TeX 的 label 唯一性、交叉引用、环境栈、花括号和美元符号基本结构检查无异常; 精确路径的 `git diff --check` 无输出. 这些是静态检查, **不是编译成功或数学验收**.
- 未运行历史 `op05_*` 脚本, 未复验旧文全部数值结论. 两份文稿中历史记录已与本轮作者检查区别. 未生成 PDF, 未进行 Lean 形式化.

本次作者提交为 B05/B06 所需步骤提供了逐步解析证明, 没有把其中任何承重步骤留作未证明的额外假设. 这是一项**作者主张**, 仍需用户独立 review. 本稿没有解决固定 $n\ge2$ 的相邻比值精确极值及全序列下确界问题, 没有重做其它 gap n=1 结论; 这些不由本轮数值样例或倍指标等式推出.

## 最终文件绑定

以下哈希绑定本次提交及本地来源. 报告自身不作自引用哈希; 它是作者说明, 不是独立验收证书.

```json
{
  "runtime": {
    "python": "3.14.4",
    "numpy": "2.5.2",
    "scipy": "1.18.1",
    "sympy": "1.14.0"
  },
  "files": {
    "docs/SL_ratio_proof.tex": {
      "sha256": "1c633c7cd3772d473435ea6cc66255946393ed4998f4c25128a547607da58f29",
      "bytes": 26978,
      "locators": {
        "prop:compactness": 70,
        "sec:first-pair": 124,
        "thm:first-pair": 129,
        "eq:first-variation": 149,
        "eq:switch-rule": 164,
        "eq:zero-energy": 187,
        "eq:endpoint-ratios": 203,
        "eq:interface-phases": 237,
        "sec:balanced": 327,
        "eq:balanced-secular": 346,
        "sec:open": 482
      }
    },
    "docs/SL_mw_lemma_reproof.tex": {
      "sha256": "f27885888e1e300316676fcff18268785bff4c528195ce48b26a2f9d2578182a",
      "bytes": 22493,
      "locators": {
        "eq:main": 52,
        "prop:density": 72,
        "prop:affine": 99,
        "prop:osc": 113,
        "prop:interl": 118,
        "prop:zeromotion": 127,
        "eq:zero-motion": 155,
        "cor:crossing": 176,
        "lem:count": 186,
        "sec:lemma1": 210,
        "lem:cell": 212,
        "eq:cellidentity": 224,
        "cor:lemma1": 267,
        "sec:lemma2": 279,
        "eq:restriction-indices": 292,
        "lem:max": 300,
        "thm:max": 335,
        "lem:min": 349,
        "thm:min": 399,
        "cor:measurable": 410,
        "thm:theorem3": 423,
        "cor:sup": 441,
        "cor:closed": 458
      }
    },
    "papers/mw1976.pdf": {
      "sha256": "360843524a6156bcdac94ffbcb398f66936a8ed2cd66448afd089b05996e37a1",
      "bytes": 446924
    },
    "papers/keller1976.pdf": {
      "sha256": "761cee5186f0946c8746a5ac3d8de7a7bb30356a70c96763c657073549455201",
      "bytes": 567078
    },
    "papers/mw1976.txt": {
      "sha256": "2c9bf0d79c69b3378624521e0e74aa9ae60dc74488c380b331b71ae704b2e27b",
      "bytes": 23364
    },
    "papers/keller1976.txt": {
      "sha256": "e6ada3e7d7875fc20e4cf7c6b70a4c30cdd845eaa30137178db659295ba47758",
      "bytes": 53092
    }
  }
}
```

## 可复现的局部检查

以下代码块是本轮实际执行的独立临时检查内容, 保存于本报告以遵守只有三个文件可写的限制. 它们只读/计算/输出, 不写项目文件. 在主项目工作根用 `python3 -B` 执行各代码块即可复现; 两个程序分别完整, 不依赖工程本地 Python 工具. 静态检查不代替协调器后续 PDF 编译.

### 程序 1: 精确恒等式、首对候选、有符号胞元及零点运动

```python
import json, math
import numpy as np
import sympy as sp
from scipy.optimize import brentq, minimize_scalar

results = {}
a,b,k,s = sp.symbols("a b k s", nonzero=True)
M1 = sp.Matrix([[a,b/k],[-k*b,a]])
M2 = sp.Matrix([[a,b/(k*s)],[-k*s*b,a]])
assert sp.simplify((M1*M2*M1)[0,1]-b/(k*s)*((2*s+1)*a*a-s*s*b*b)) == 0
assert sp.simplify((M2*M1*M2)[0,1]-b/(k*s*s)*(s*(s+2)*a*a-b*b)) == 0
x,c,d = sp.symbols("x c d", real=True)
v = sp.sin(sp.pi*(c*x+d))
assert sp.simplify(-sp.diff(v,x,2)-c*c*sp.pi**2*v) == 0
m = sp.symbols("m", integer=True, positive=True)
assert sp.simplify(sp.sin(m*sp.pi*(1-1/m))) == 0
assert sp.simplify(sp.sin(2*m*sp.pi*(1-1/m))) == 0
assert sp.simplify((2*sp.pi/(1/m))**2/(sp.pi/(1/m))**2) == 4
assert sp.diff(sp.sin(2*sp.pi*(x+sp.Rational(1,2))),x).subs(x,-sp.Rational(1,2)) == 2*sp.pi
assert sp.diff(sp.sin(2*sp.pi*(x+sp.Rational(1,2))),x).subs(x,sp.Rational(1,2)) == 2*sp.pi
u,w = sp.Function("u")(x), sp.Function("w")(x)
rho,lam,lam1,lam2 = sp.symbols("rho lam lam1 lam2", positive=True)
W = sp.diff(u,x)*w-u*sp.diff(w,x)
assert sp.expand(sp.diff(W,x).subs({sp.diff(u,x,2):-lam*rho*u,
    sp.diff(w,x,2):-lam*rho*w-rho*u})-rho*u*u) == 0
K = sp.diff(u,x)**2/lam1-sp.diff(w,x)**2/lam2
assert sp.expand((sp.diff(K,x)+rho*sp.diff(u*u-w*w,x)).subs({
    sp.diff(u,x,2):-lam1*rho*u,sp.diff(w,x,2):-lam2*rho*w})) == 0
results["exact_identities"] = 10

def propagate(k, vals, widths, stop=1.0):
    y,v,total,pos = 0.,1.,0.,0.
    for rho,width in zip(vals,widths):
        width = min(width,max(0.,stop-pos))
        if width <= 0: break
        q = k*math.sqrt(rho); phase = q*width
        A,B = y,v/q
        total += rho*(A*A*(width/2+math.sin(2*phase)/(4*q))
            +B*B*(width/2-math.sin(2*phase)/(4*q))
            +A*B*math.sin(phase)**2/q)
        y,v = A*math.cos(phase)+B*math.sin(phase), q*(-A*math.sin(phase)+B*math.cos(phase))
        pos += width
    return y,v,total

def zeros(k, vals, widths):
    y,v,pos = 0.,1.,0.; out = []
    for rho,width in zip(vals,widths):
        q = k*math.sqrt(rho); theta = math.atan2(q*y,v)
        for j in range(math.floor(theta/math.pi)-1,math.ceil((theta+q*width)/math.pi)+2):
            t = (j*math.pi-theta)/q
            if 1e-9 < t <= width+1e-9 and pos+t < 1-1e-8:
                z = pos+t
                if not out or abs(z-out[-1]) > 1e-8: out.append(z)
        co,si = math.cos(q*width),math.sin(q*width)
        y,v = co*y+si*v/q,-q*si*y+co*v
        pos += width
    return out

def eigenvalues(vals,widths,count):
    step = .045/math.sqrt(max(vals)); roots = []
    lo = 1e-7; flo = propagate(lo,vals,widths)[0]
    upper = (count+1)*math.pi/math.sqrt(min(vals))
    for hi in np.arange(lo+step,upper+step,step):
        fhi = propagate(hi,vals,widths)[0]
        if flo*fhi < 0:
            root = brentq(lambda q:propagate(q,vals,widths)[0],lo,hi,xtol=2e-13)
            assert len(zeros(root,vals,widths)) == len(roots), ("index",root)
            roots.append(root*root)
            if len(roots)==count: return np.array(roots)
        lo,flo = hi,fhi
    raise AssertionError("missing roots")

candidates = []; max_energy = max_switch = max_formula = 0.
for R in [1.,1.5,2.,3.,4.,10.,100.]:
    s = math.sqrt(R)
    for maximum in [True,False]:
        outer = s/(2*s+1) if maximum else 1/(s+2)
        vals = [1.,R,1.] if maximum else [R,1.,R]
        widths = [outer,1-2*outer,outer]
        angle = math.acos(s/(s+1) if maximum else 1/(s+1))
        target = ((math.pi-angle)/angle)**2
        eig = eigenvalues(vals,widths,2); waves = np.sqrt(eig)
        norms = np.array([propagate(q,vals,widths)[2] for q in waves])
        residual = abs(eig[1]/eig[0]-target)/target
        max_formula = max(max_formula,residual)
        for z in [outer,.5,1-outer,.07,.91]:
            state = [propagate(q,vals,widths,z) for q in waves]
            F = state[0][0]**2/norms[0]-state[1][0]**2/norms[1]
            r = vals[1] if outer < z < 1-outer else vals[0]
            E = state[0][1]**2/(eig[0]*norms[0])-state[1][1]**2/(eig[1]*norms[1])+r*F
            max_energy = max(max_energy,abs(E))
            if abs(z-outer)<1e-10 or abs(z-(1-outer))<1e-10:
                max_switch = max(max_switch,abs(F))
        candidates.append([R,"max" if maximum else "min",float(eig[1]/eig[0])])
assert max_formula < 1e-10 and max_energy < 1e-9 and max_switch < 1e-9
results["candidate_cases"] = candidates
results["max_relative_formula_error"] = max_formula
results["max_zero_energy_residual"] = max_energy
results["max_switch_residual"] = max_switch

vals,widths = [1.2,3.4,2.1],[.13,.52,.35]
eig = eigenvalues(vals,widths,2); slopes = [propagate(math.sqrt(e),vals,widths)[1] for e in eig]
assert slopes[0] < 0 < slopes[1]
cell_errors = []
for n in [2,3]:
    ext = eigenvalues(vals*n,[w/n for w in widths]*n,2*n)
    error = max(abs(ext[n-1]/(n*n*eig[0])-1),abs(ext[2*n-1]/(n*n*eig[1])-1))
    assert error < 1e-10
    cell_errors.append([n,float(error)])
    for factor in slopes:
        for j in range(n-1):
            assert abs(n*factor**j*factor-n*factor**(j+1)) < 1e-11
results["signed_cell_factors"] = slopes
results["cell_relative_errors"] = cell_errors

base = 80.; eps = 1e-4
zs = zeros(math.sqrt(base),vals,widths)
zp,zm = zeros(math.sqrt(base+eps),vals,widths),zeros(math.sqrt(base-eps),vals,widths)
assert len(zs)==len(zp)==len(zm)
errors = []
for z,zplus,zminus in zip(zs,zp,zm):
    _,deriv,integral = propagate(math.sqrt(base),vals,widths,z)
    exact = -integral/(deriv*deriv); finite = (zplus-zminus)/(2*eps)
    assert exact < 0
    errors.append(abs(exact-finite))
assert max(errors) < 1e-8
results["zero_motion_checks"] = len(errors)
results["zero_motion_max_absolute_error"] = max(errors)

h = np.array([.2,-.3,.1]); eps = 1e-5
def log_ratio(v):
    es=eigenvalues(v,widths,2); return math.log(es[1]/es[0])
finite = (log_ratio(np.array(vals)+eps*h)-log_ratio(np.array(vals)-eps*h))/(2*eps)
nodes,weights = np.polynomial.legendre.leggauss(24); derivative = 0.; left = 0.
norms = [propagate(math.sqrt(e),vals,widths)[2] for e in eig]
for j,width in enumerate(widths):
    for z,wgt in zip(left+width*(nodes+1)/2,weights*width/2):
        y1=propagate(math.sqrt(eig[0]),vals,widths,z)[0]
        y2=propagate(math.sqrt(eig[1]),vals,widths,z)[0]
        derivative += h[j]*wgt*(y1*y1/norms[0]-y2*y2/norms[1])
    left += width
assert abs(finite-derivative) < 1e-7
results["first_variation_absolute_error"] = abs(finite-derivative)
print(json.dumps(results,ensure_ascii=False,indent=2))

```

执行输出:

```json
{
  "exact_identities": 10,
  "candidate_cases": [
    [
      1.0,
      "max",
      3.99999999999997
    ],
    [
      1.0,
      "min",
      3.99999999999997
    ],
    [
      1.5,
      "max",
      4.753820778554825
    ],
    [
      1.5,
      "min",
      3.4006824319599698
    ],
    [
      2.0,
      "max",
      5.403884872479626
    ],
    [
      2.0,
      "min",
      3.051398103912691
    ],
    [
      3.0,
      "max",
      6.51973822859612
    ],
    [
      3.0,
      "min",
      2.645872391598372
    ],
    [
      4.0,
      "max",
      7.481533386207036
    ],
    [
      4.0,
      "min",
      2.4091685548064627
    ],
    [
      10.0,
      "max",
      11.820372828909482
    ],
    [
      10.0,
      "min",
      1.8641935279288893
    ],
    [
      100.0,
      "max",
      39.83043629457489
    ],
    [
      100.0,
      "min",
      1.261218378826444
    ]
  ],
  "max_relative_formula_error": 3.732379501788298e-14,
  "max_zero_energy_residual": 3.777145263228476e-12,
  "max_switch_residual": 4.196643033083092e-14,
  "signed_cell_factors": [
    -0.8982588377444526,
    0.9806600325762017
  ],
  "cell_relative_errors": [
    [
      2,
      1.199040866595169e-14
    ],
    [
      3,
      1.099120794378905e-14
    ]
  ],
  "zero_motion_checks": 4,
  "zero_motion_max_absolute_error": 1.2853281806946004e-12,
  "first_variation_absolute_error": 6.910527705628056e-12
}
```

### 程序 2: 截断分支与谱指标

```python
import json,math
import numpy as np
from scipy.optimize import brentq

def propagate(k, vals, widths, stop=1.0):
    y,v,total,pos = 0.,1.,0.,0.
    for rho,width in zip(vals,widths):
        width = min(width,max(0.,stop-pos))
        if width <= 0: break
        q = k*math.sqrt(rho); phase = q*width
        A,B = y,v/q
        total += rho*(A*A*(width/2+math.sin(2*phase)/(4*q))
            +B*B*(width/2-math.sin(2*phase)/(4*q))
            +A*B*math.sin(phase)**2/q)
        y,v = A*math.cos(phase)+B*math.sin(phase), q*(-A*math.sin(phase)+B*math.cos(phase))
        pos += width
    return y,v,total

def zeros(k, vals, widths):
    y,v,pos = 0.,1.,0.; out = []
    for rho,width in zip(vals,widths):
        q = k*math.sqrt(rho); theta = math.atan2(q*y,v)
        for j in range(math.floor(theta/math.pi)-1,math.ceil((theta+q*width)/math.pi)+2):
            t = (j*math.pi-theta)/q
            if 1e-9 < t <= width+1e-9 and pos+t < 1-1e-8:
                z = pos+t
                if not out or abs(z-out[-1]) > 1e-8: out.append(z)
        co,si = math.cos(q*width),math.sin(q*width)
        y,v = co*y+si*v/q,-q*si*y+co*v
        pos += width
    return out

def eigenvalues(vals,widths,count):
    step = .045/math.sqrt(max(vals)); roots = []
    lo = 1e-7; flo = propagate(lo,vals,widths)[0]
    upper = (count+1)*math.pi/math.sqrt(min(vals))
    for hi in np.arange(lo+step,upper+step,step):
        fhi = propagate(hi,vals,widths)[0]
        if flo*fhi < 0:
            root = brentq(lambda q:propagate(q,vals,widths)[0],lo,hi,xtol=2e-13)
            assert len(zeros(root,vals,widths)) == len(roots), ("index",root)
            roots.append(root*root)
            if len(roots)==count: return np.array(roots)
        lo,flo = hi,fhi
    raise AssertionError("missing roots")

rng=np.random.default_rng(20260920)
cases=[]; counts={"max_A":0,"max_B":0,"min_A":0,"min_C":0}
def restrict(vals,widths,start,end):
    v=[]; w=[]; pos=0.
    for rho,width in zip(vals,widths):
        overlap=max(0.,min(pos+width,end)-max(pos,start))
        if overlap>1e-13: v.append(rho); w.append(overlap/(end-start))
        pos+=width
    return v,w
for sample in range(10):
    vals=list(1+3*rng.random(4))
    widths=list(rng.dirichlet(np.ones(4)*2))
    eig=eigenvalues(vals,widths,8)
    for k in [1,2,3]:
        m=k+1; z0=zeros(math.sqrt(eig[m-1]),vals,widths)[-1]
        z=zeros(math.sqrt(eig[2*m-1]),vals,widths)
        z2k=z[2*k-1]; leftvals,leftwidths=restrict(vals,widths,0,z0)
        rightvals,rightwidths=restrict(vals,widths,z0,1)
        el=eigenvalues(leftvals,leftwidths,2*k)/(z0*z0)
        er=eigenvalues(rightvals,rightwidths,2)/((1-z0)**2)
        assert abs(el[k-1]/eig[m-1]-1)<1e-9 and abs(er[0]/eig[m-1]-1)<1e-9
        if z0 < z2k:
            counts["max_A"]+=1; counts["min_A"]+=1
            assert eig[2*m-1] <= el[2*k-1]*(1+1e-9)
            assert eig[2*m-1] >= er[1]*(1-1e-9)
        else:
            counts["max_B"]+=1; counts["min_C"]+=1
            assert eig[2*m-1] <= er[1]*(1+1e-9)
            assert eig[2*m-1] >= el[2*k-1]*(1-1e-9)
        cases.append([sample,k,float(z0-z2k)])
assert all(v>0 for v in counts.values())
print(json.dumps({"random_seed":20260920,"density_samples":10,"truncation_cases":30,
    "branch_counts":counts,"common_zero":"symbolic constant-density identity in main check",
    "scope":"finite floating-point restriction/index checks, not a universal proof"},indent=2))

```

执行结果: 十个密度, 三十个截断样例, 分支计数 `max_A=14,max_B=16,min_A=14,min_C=16`. 全部断言未触发. 这不构成独立 PASS, 也不是对无限维全局极值的数值证明.
