# -*- coding: utf-8 -*-
import io
p = r"docs\SL_gap_n1_well_rigidity_R32.tex"
src = io.open(p, encoding="utf-8-sig").read()
old = r"\begin{itemize}\setlength{\itemsep}{0pt}"
new = r"\begin{itemize}\setlength{\itemsep}{0pt}\raggedright"
assert old in src
src = src.replace(old, new)
io.open(p, "w", encoding="utf-8-sig", newline="\r\n").write(src)
print("patched")
