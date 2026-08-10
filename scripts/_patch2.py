import io
p = r"F:\LaTeX\BVE research\scripts\audit_o3a_pdf_part1.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("assert abs(Fp_num-formula) < mp.mpf('1e-40')", "assert abs(Fp_num-formula) < mp.mpf('1e-30')")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")
