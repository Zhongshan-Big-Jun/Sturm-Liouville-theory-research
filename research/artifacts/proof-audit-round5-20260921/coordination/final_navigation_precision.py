from pathlib import Path
R=Path('/mnt/f/LaTeX/BVE research')
P=R/'research_map.md';B=P.read_bytes();A=b"General non-cofinite O1'LD and s=3 remain OPEN.";assert B.count(A)==1;P.write_bytes(B.replace(A,b"General non-cofinite O1'LD and the cofinite classification at s=3 remain OPEN."))
P=R/'tools/README.md';T=P.read_text();A="一般非余有限O1'LD与s=3仍开放.";assert T.count(A)==1;T=T.replace(A,"一般非余有限O1'LD与s=3的对应分类仍开放.");A='37个局部Lean定理及四份隔离检验';assert T.count(A)==1;T=T.replace(A,'37个局部Lean定理、四份隔离审查回执与额外的独立编译检查');P.write_text(T)
print('Navigation now explicitly limits the open s=3 statement to the corresponding classification.')
