# -*- coding: utf-8 -*-
p = r'docs\SL_gap_n1_symline_proof.tex'
t = open(p, encoding='utf-8').read()
a = r'\section{\texorpdfstring{易区 $c\ge1/2$: $\widetilde F_e(c)<0$}{易区 c>=1/2: F_e(c)<0}}\label{sec:easy}'
b = r'\section{易区 (c>=1/2): F_e(c)<0}\label{sec:easy}'
assert a in t
open(p, 'w', encoding='utf-8').write(t.replace(a, b))
print('replaced for test')
