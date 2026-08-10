# batch_e14c.py - authoritative e14 sweep over full R range, merge into e14_authoritative.json
import json, subprocess, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
py = r"C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe"
Rs = [1.02, 1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 500.0,
      600.0, 620.0, 650.0, 700.0, 750.0, 800.0, 850.0, 875.0, 880.0, 884.0,
      886.0, 888.0, 890.0, 895.0, 900.0, 950.0, 1000.0, 2000.0, 10000.0, 100000.0]
out = {}
t0 = time.time()
for R in Rs:
    f = os.path.join(HERE, "e14c_%g.json" % R)
    t1 = time.time()
    r = subprocess.run([py, os.path.join(HERE, "e14_authoritative.py"), "--R", str(R), "--out", f, "--ngrid", "200"],
                       capture_output=True, text=True, encoding="utf-8", cwd=HERE)
    line = r.stdout.strip()
    print("R=%g: %s  [%.1fs]" % (R, line, time.time()-t1), flush=True)
    if r.returncode != 0:
        print("ERR:", r.stderr[-1500:])
        continue
    with open(f, encoding="utf-8") as fh:
        out["R=%g" % R] = json.load(fh)
with open(os.path.join(HERE, "e14_authoritative.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh)
print("DONE", len(out), "total %.1fs" % (time.time()-t0))
