# -*- coding: utf-8 -*-
import io
p = r'docs\SL_third_order_recurrence_theory.tex'
s = io.open(p, encoding='utf-8').read()
print("len before:", len(s))
anchor = r"\section{数值验证}"
print("anchor present:", anchor in s)
