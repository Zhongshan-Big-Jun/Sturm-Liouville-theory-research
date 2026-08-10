# batch_e14.py - run e14 for the intermediate band, merge into one json
import json, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
py = r"C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe"
Rs = [600.0, 620.0, 650.0, 700.0, 750.0, 800.0, 850.0, 875.0, 880.0, 884.0, 886.0, 888.0, 890.0, 895.0, 900.0]
out = {}
for R in Rs:
    f = os.path.join(HERE, f"e14_R{R:g}.json")
    if os.path.exists(f):
        with open(f, encoding="utf-8") as fh:
            out[f"R={R:g}"] = json.load(fh)
        continue
    r = subprocess.run([py, "e14_authoritative.py", "--R", str(R), "--out", f, "--ngrid", "180"],
                       capture_output=True, text=True, encoding="utf-8")
    print(r.stdout.strip())
    if r.returncode != 0:
        print("ERR:", r.stderr[-2000:])
        continue
    with open(f, encoding="utf-8") as fh:
        out[f"R={R:g}"] = json.load(fh)
with open(os.path.join(HERE, "e14_authoritative.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh)
print("DONE", len(out))
