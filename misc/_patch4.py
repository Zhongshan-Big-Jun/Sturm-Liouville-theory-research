# -*- coding: utf-8 -*-
p = r'docs\SL_gap_n1_symline_proof.tex'
t = open(p, encoding='utf-8').read()
a1 = r'该区密度从 $R$ 变 $1$'
b1 = r'该条带从中间区 ($\rho=1$) 变为阱区 ($\rho=R$)'
a2 = r'$\partial_a\lambda_k=+\lambda_k(R-1)\hat y_k(a)^2$'
b2 = r'$\partial_a\lambda_k=-\lambda_k(R-1)\hat y_k(a)^2$ (密度点态增大, 特征值减小)'
assert a1 in t and a2 in t, 'target missing'
t = t.replace(a1, b1).replace(a2, b2)
open(p, 'w', encoding='utf-8').write(t)
print('OK')
