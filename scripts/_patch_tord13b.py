# -*- coding: utf-8 -*-
import io
p = r'docs\SL_third_order_recurrence_theory.tex'
s = io.open(p, encoding='utf-8').read()

# abstract: add item 5
old = r"""	\item \emph{第三解与最小解 (定理 \ref{thm:minimal})}: 变差常数 (离散 Wronskian)
		给出第三基解的和式构造; 向后迭代收敛到最小解 $h^*$ ($h^*_0 \neq 0$),
		且 $h^*_{j+1}/h^*_j = \frac{c}{4j^2}(1+O(1/j))$,
		$h^*_j = K(c/4)^j/(j!)^2 \cdot j^{-3}(1+o(1))$ (数值验证, 常数 $K$ 未闭式化).
\end{enumerate}
未闭合问题如实登记 (盒式归纳的退化配置排除与最小解的闭式), 见第 6 节."""
new = r"""	\item \emph{第三解与最小解 (定理 \ref{thm:minimal})}: 变差常数 (离散 Wronskian)
		给出第三基解的和式构造; 向后迭代收敛到最小解 $h^*$ ($h^*_0 \neq 0$),
		且 $h^*_{j+1}/h^*_j = \frac{c}{4j^2}(1+O(1/j))$,
		$h^*_j = K(c/4)^j/(j!)^2 \cdot j^{-3}(1+o(1))$ (数值验证, 常数 $K$ 未闭式化).
	\item \emph{完整分类 (2026-08-05 补充, 定理 \ref{thm:full})}: 一切
		有理比值积分解恰为 $E^{(\tau)}$ 族加刚性支 $E^-$; 三支柱
		(渐近分类 + 刚性 + 4-参数归约) 全符号/精确验证; 最小解比值
		非有理 (数值排除 + 逐阶唯一性). 最小解渐近展开到 $O(j^{-7})$
		(eq:rhos), 常数表 $K(c)$ 含锚点 $K(0)=\tfrac34$, $K(1)=e/4$
		(25 位数值); 盒式归纳齐次部分封闭 (退化配置精确排除).
\end{enumerate}
未闭合问题如实登记 (源项控制与最小解闭式), 见第 8 节."""
assert old in s, "abstract not found"
s = s.replace(old, new, 1)

# open problems section: rewrite
old2 = r"""\section{未闭合问题 (如实登记)}

\begin{description}
	\item[盒式归纳的退化配置] 路线 A 的核心缺口: 比值偏差 $d_j = \rho_j - e_j
		\geq 0$ 的归纳需要排除``$d_{j-1} = 0$ 而 $d_{j-2} > 0$''这类盒内
		退化配置 (单边归纳条件不足). 定理 \ref{thm:reduction} 的降阶把
		三阶问题化为二阶 $s$-递推, 或可为 $d_j$ 提供新的归纳量, 但完整的
		封闭论证未完成.
	\item[最小解的闭式] $h^*_j$ 的和式表达 (定理 \ref{thm:minimal}) 已给出,
		但其超几何求和未化简; 渐近常数 $K$ 未闭式化.
	\item[一般系数族的分类] 定理 \ref{thm:beta} 只处理 $E_j = \prod(1+\beta/(2k))$
		型积分解; 更一般 (如 $\prod(1+\beta/(k+\gamma))$) 的积分解存在性
		未分类.
	\item[与完备性证明的关系] 路线 A 的完整化仍不必要: $H^1$-矩路线 (会话 10)
		已闭合证明. 本文的价值在于 (i) 结构定理本身, (ii) 对旧脚本公式的更正.
\end{description}"""
new2 = r"""\section{未闭合问题 (如实登记)}

\begin{description}
	\item[源项控制 (残余缺口)] 盒式归纳的齐次部分已封闭 (第 \ref{sec:box} 节),
		但非齐次源项 $T_j D$ (最小解分量的贡献) 的 $D$-控制未闭合:
		一般解 $E = c_1E^+ + c_2E^- + c_3 z^{\mathrm{ind}}$ 的比值偏差
		由齐次部分 (定理 \ref{thm:full}) 与 $c_3$-源的叠加决定, 源项的
		前向不变性缺证明.
	\item[最小解的闭式] $K(c)$ 无闭式; 锚点 $K(0) = \tfrac34$,
		$K(1) = e/4$ 为数值级 ($K(1)$ 至 25 位). (eq:rhos) 是形式展开,
		Birkhoff--Trjitzinsky 型严格化未完成.
	\item[高次有理函数排除] 自由支次数 $> 2$ 的有理比值未穷尽排除
		(4-参数归约只列举次数 $\leq 2$); 最小解非有理为数值排除 +
		逐阶唯一性, 非完整证明.
	\item[两参数族分类] 定理 \ref{thm:beta} 的 $(1+\beta/(2k))$ 族与
		一般 $(1+\alpha/(k+\gamma))$ 族 (\path{op13_general_product_classify.py}:
		偶次恰给 $(\alpha,\gamma) \in \{(-\tfrac12,0),(\tfrac12,-1),(\tfrac12,0)\}$,
		奇次 $\{(\tfrac12,0),(\tfrac32,-1),(\tfrac32,0)\}$) 均已分类;
		$\gamma = -1$ 对应 $E^+ \pm E^-$ 组合的尾部表示
		(\path{op13_tail_check.py}: $T/E^- = 2j$ 型).
	\item[与完备性证明的关系] 路线 A 的完整化仍不必要: $H^1$-矩路线 (会话 10)
		已闭合证明. 本文的价值在于 (i) 结构定理本身, (ii) 对旧脚本公式的更正,
		(iii) 分类工具 (定理 \ref{thm:full}) 对一般三阶递推的可迁移性.
\end{description}"""
assert old2 in s, "open problems not found"
s = s.replace(old2, new2, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print("patched abstract + open problems")
