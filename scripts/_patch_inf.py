# -*- coding: utf-8 -*-
import io
p = r'F:\LaTeX\BVE research\docs\SL_inf_ratio_proof.tex'
s = io.open(p, encoding='utf-8-sig').read()

start = s.find('\\begin{lemma}[Prufer')
end = s.find('\\end{lemma}', start) + len('\\end{lemma}')

new_lemma = """\\begin{lemma}[Prufer 相角方程]\\label{lem:prufer}
	设 $\\rho$ 在 $(0,L)$ 上逐段常数 (至多 $m$ 个跳). 对 (1) 的解 $y$,
	定义相角 $\\varphi$ 与振幅 $r$ 为
	\\[
		y(x) = r(x)\\sin\\varphi(x), \\qquad
		y'(x) = \\sqrt{\\lambda\\rho(x)}\\, r(x)\\cos\\varphi(x),
	\\]
	并在 $x = 0$ 取 $\\varphi(0) = 0$. 则在每个常数段内
	\\[
		r'(x) = 0, \\qquad \\varphi'(x) = \\sqrt{\\lambda\\rho(x)}
	\\]
	精确成立; 在 $\\rho$ 的跳点处 $r, \\varphi$ 因 $y, y'$ 连续而跳跃,
	但每次跳跃的量 $|\\Delta\\varphi| \\le \\pi$ 与 $\\lambda$ 无关.
	因此
	\\[
		\\varphi(L) = \\sqrt\\lambda \\int_0^L \\sqrt{\\rho(x)}\\,dx + O(1),
	\\]
	余项 $O(1)$ 仅依赖 $\\rho$ 的跳点集合 (至多 $m\\pi$).
\\end{lemma}

\\begin{proof}
	在每个常数段内 $\\rho \\equiv \\rho_i$, 微分定义给出
	$y' = r'\\sin\\varphi + r\\varphi'\\cos\\varphi$ 与
	$y' = \\sqrt{\\lambda\\rho_i}\\, r\\cos\\varphi$, 且 $y'' = -\\lambda\\rho_i y$
	给出 $\\sqrt{\\lambda\\rho_i}\\,r'\\cos\\varphi
	- \\sqrt{\\lambda\\rho_i}\\,r\\varphi'\\sin\\varphi
	= -\\lambda\\rho_i r\\sin\\varphi$. 消去 $\\sqrt{\\lambda\\rho_i}$
	得线性方程组
	\\[
		r'\\sin\\varphi + r\\varphi'\\cos\\varphi
		= \\sqrt{\\lambda\\rho_i}\\,r\\cos\\varphi,
		\\qquad
		r'\\cos\\varphi - r\\varphi'\\sin\\varphi
		= -\\sqrt{\\lambda\\rho_i}\\,r\\sin\\varphi.
	\\]
	分别乘以 $\\sin\\varphi, \\cos\\varphi$ 并相加: $r' = 0$;
	乘以 $\\cos\\varphi, -\\sin\\varphi$ 并相加: $\\varphi' = \\sqrt{\\lambda\\rho_i}$.
	在跳点 $x_j$ 处 $y, y'$ 连续, 由 $\\tan\\varphi = y\\sqrt{\\lambda\\rho}/y'$
	知 $\\varphi$ 跳变满足 $|\\Delta\\varphi| < \\pi$ (因 $\\sqrt\\rho$
	界于 $[\\sqrt a, \\sqrt A]$, $\\varphi$ 与 $y'/(\\sqrt\\lambda y)$ 同象限,
	至多相差一个象限), 与 $\\lambda$ 无关. 积分并对至多 $m$ 个跳求和
	即得所求. \\qed
\\end{proof}"""

s = s[:start] + new_lemma + s[end:]
s = s.replace('特征值条件 $y(L) = 0$ 等价于 $\\theta(L) = k\\pi$ ($k \\in \\mathbb N$),',
              '特征值条件 $y(L) = 0$ 等价于 $\\varphi(L) = k\\pi$ ($k \\in \\mathbb N$),')
s = s.replace('N(\\lambda) = \\Bigl\\lfloor \\frac{\\theta(L)}{\\pi}\\Bigr\\rfloor',
              'N(\\lambda) = \\Bigl\\lfloor \\frac{\\varphi(L)}{\\pi}\\Bigr\\rfloor')
io.open(p, 'w', encoding='utf-8-sig', newline='\n').write(s)
print('patched ok')
