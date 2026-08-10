import io, os, hashlib
root = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A"
for dirpath, dirs, files in os.walk(root):
    for fn in files:
        p = os.path.join(dirpath, fn)
        with open(p, "rb") as f:
            b = f.read()
        if b.startswith(b"\xef\xbb\xbf"):
            with open(p, "wb") as f:
                f.write(b[3:])
            print("BOM stripped:", os.path.relpath(p, root))
print("done")
