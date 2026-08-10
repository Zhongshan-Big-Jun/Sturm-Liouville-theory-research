# -*- coding: utf-8 -*-
import io
p = r'F:\LaTeX\BVE research\docs\SL_inf_ratio_proof.tex'
s = io.open(p, encoding='utf-8-sig').read()

# 1) remove leftover old proof block after the lemma
start = s.find('\\begin{proof}\n\t在 $\\rho$ 常数段上令')
assert start >= 0, 'leftover proof start not found'
end = s.find('\\end{proof}', start) + len('\\end{proof}')
s = s[:start] + s[end:]

# 2) replace the messy theta sketch in the theorem proof by a pointer to the lemma
old_sketch = r"""	经典计算 (见 \cite[p.~21]{ls} 或引理 \ref{lem:prufer}):
	\[
		\theta'(x) = \sqrt{\lambda\rho(x)} + \sqrt\lambda\,\frac{y}{y'}
		\cdot \frac{d}{dx}\Bigl(\frac{y'}{\sqrt\lambda y}\Bigr)
		= \sqrt{\lambda\rho(x)} + o(1),
	\]
	其中 $o(1)$ 对 $\lambda \to \infty$ 在 $x$ 的每个连续段上一致成立,
	在跳点处 $\theta$ 连续 (方程以 $y, y'$ 连续解释). 更精确地,
	对逐段常数 $\rho$ 可写出每段的显式解
	$y = c_1\cos(\sqrt{\lambda\rho_i}\,x) + c_2\sin(\sqrt{\lambda\rho_i}\,x)$,
	直接得到相角沿第 $i$ 段增长
	\[
		\theta(x_i) - \theta(x_{i-1})
		= \sqrt{\lambda\rho_i}\,(x_i - x_{i-1}) + O(1),
	\]
	余项 $O(1)$ 与 $\lambda$ 无关 (仅依赖 $\rho_i$ 与跳的位置; 转移矩阵
	乘性因子吸收于常数). 求和得
	\[
		\theta(L) = \sqrt\lambda \sum_i \sqrt{\rho_i}\,(x_i - x_{i-1}) + O(1)
		= \sqrt\lambda\, L_\rho + O(1).
	\]
"""
new_sketch = r"""	用引理 \ref{lem:prufer} 的 Prufer 相角: 定义
	$y = r\sin\varphi$, $y' = \sqrt{\lambda\rho}\,r\cos\varphi$,
	$\varphi(0) = 0$. 在每个常数段内 $\varphi' = \sqrt{\lambda\rho}$
	精确成立, 在至多 $m$ 个跳点处 $\varphi$ 跳跃有界 ($|\Delta\varphi| \le \pi$,
	与 $\lambda$ 无关). 求和得
	\[
		\varphi(L) = \sqrt\lambda \sum_i \sqrt{\rho_i}\,(x_i - x_{i-1}) + O(1)
		= \sqrt\lambda\, L_\rho + O(1).
	\]
"""
assert old_sketch in s, 'sketch not found'
s = s.replace(old_sketch, new_sketch)

io.open(p, 'w', encoding='utf-8-sig', newline='\n').write(s)
print('patched ok')
