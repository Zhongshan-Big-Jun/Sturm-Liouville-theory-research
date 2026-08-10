# -*- coding: utf-8 -*-
p = r'docs\SL_gap_n1_symline_proof.tex'
t = open(p, encoding='utf-8').read()
a = r'\section{易区 $c\ge1/2$: \texorpdfstring{$\widetilde F_e(c)<0$}{F-e(c)<0}}\label{sec:easy}'
b = r'\section{\texorpdfstring{易区 $c\ge1/2$: $\widetilde F_e(c)<0$}{易区 c>=1/2: F_e(c)<0}}\label{sec:easy}'
c = r'\section{端点极限 $D$}\label{sec:endpoints}'
d = r'\section{\texorpdfstring{端点极限 $D$}{端点极限 D}}\label{sec:endpoints}'
assert a in t, 'a not found'
assert c in t, 'c not found'
t = t.replace(a, b).replace(c, d)
open(p, 'w', encoding='utf-8').write(t)
print('OK')
