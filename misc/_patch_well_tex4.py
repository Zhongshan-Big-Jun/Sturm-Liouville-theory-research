# -*- coding: utf-8 -*-
import io
p = r"docs\SL_gap_n1_well_rigidity_R32.tex"
src = io.open(p, encoding="utf-8-sig").read()
old = "对阱族, $D(a,b)=\\lambda_2-\\lambda_1$ 沿边界参数的变分为\n\t$\\partial_a D=(R-1)f_{a,b}(a)$, $\\partial_b D=-(R-1)f_{a,b}(b)$\n\t(Feynman--Hellmann), 故 $R_1=R_2=0$ 恰为阱族内部临界点条件;\n\t$\\{f_{a,b}>0\\}$ 应等于阱 $\\{x:\\rho_{a,b}=R\\}$ (带状自洽). \\EVID{} (会话 13 数值表)\n\t与严格 FH 公式均支持此关系, 但\"极值点必为 sign-consistent good root\"的全局论证\n\t仍属开放缺口 (a), 见第 \\ref{sec:gaps} 节."
new = "对阱族, $D(a,b)=\\lambda_2-\\lambda_1$ 沿边界参数的变分为\n\t$\\partial_a D=-(R-1)f_{a,b}(a)$, $\\partial_b D=+(R-1)f_{a,b}(b)$\n\t(Feynman--Hellmann; 单特征值恒等式 $d\\lambda_k/da=-\\lambda_k(R-1)\\hat y_k(a)^2$\n\t已由 \\url{_well_fh2.py} 数值验证到 $10^{-8}$), 故 $R_1=R_2=0$ 恰为阱族内部\n\t临界点条件; $\\{f_{a,b}>0\\}$ 等于阱 $\\{x:\\rho_{a,b}=R\\}$ (带状自洽;\n\tR=4 对称 good root 处数值 $f(0.2)=+4.12$, $f(0.5)=-2.28$, $f(a)=f(b)=0$).\n\t但\"极值点必为 sign-consistent good root\"的全局论证仍属开放缺口 (d),\n\t见第 \\ref{sec:gaps} 节."
assert old in src, "rem:fh block not found"
src = src.replace(old, new)
io.open(p, "w", encoding="utf-8-sig", newline="\r\n").write(src)
print("patched")
