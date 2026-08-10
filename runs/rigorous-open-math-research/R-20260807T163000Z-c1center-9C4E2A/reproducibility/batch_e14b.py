# patch e14_authoritative.py: threshold 0.0012 -> 0.002 (keeps fp-arm, stops at its fold)
$p = Get-Content e14_authoritative.py -Raw
$p = $p.Replace('r - a > 0.0012', 'r - a > 0.002')
Set-Content -Encoding UTF8 e14_authoritative.py $p
@'
# batch_e14b.py - rerun transition band + spot checks with corrected filter
import json, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
py = r"C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe"
Rs = [4.0, 10.0, 100.0, 500.0, 880.0, 884.0, 886.0, 888.0, 890.0, 895.0, 900.0, 950.0, 1000.0, 2000.0, 10000.0]
out = {}
for R in Rs:
    f = os.path.join(HERE, f"e14b_R{R:g}.json")
    r = subprocess.run([py, "e14_authoritative.py", "--R", str(R), "--out", f, "--ngrid", "180"],
                       capture_output=True, text=True, encoding="utf-8")
    line = r.stdout.strip()
    print(f"R={R:g}: {line}", flush=True)
    if r.returncode != 0:
        print("ERR:", r.stderr[-1500:])
        continue
    with open(f, encoding="utf-8") as fh:
        out[f"R={R:g}"] = json.load(fh)
with open(os.path.join(HERE, "e14b_authoritative.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh)
print("DONE", len(out))
