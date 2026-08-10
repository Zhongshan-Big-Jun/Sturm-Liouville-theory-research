import os, hashlib
root = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A"
skip = {"research_cache"}  # handle separately at end
for group in ["root", "reproducibility", "research_cache"]:
    print("="*30, group)
    base = root if group == "root" else os.path.join(root, group)
    names = sorted(os.listdir(base))
    for fn in names:
        p = os.path.join(base, fn)
        if not os.path.isfile(p):
            continue
        h = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()
        print(h, os.path.join(group, fn) if group != "root" else fn)
