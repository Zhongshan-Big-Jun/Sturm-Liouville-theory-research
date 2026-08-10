# -*- coding: utf-8 -*-
import io
p = r'F:\LaTeX\BVE research\docs\SL_inf_ratio_proof.tex'
s = io.open(p, encoding='utf-8-sig').read()
old = '\\begin{lemma}[Prufer'
i = s.find(old)
print('found lemma at', i)
if i >= 0:
    print(s[i:i+200])
