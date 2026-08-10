# -*- coding: utf-8 -*-
import subprocess
patch = open("misc/_patch1.txt", encoding="utf-8").read()
exe = r"C:\Program Files\WindowsApps\OpenAI.Codex_26.803.5235.0_x64__2p2nqsd0c76g0\app\resources\codex.exe"
r = subprocess.run([exe, "--codex-run-as-apply-patch", patch], capture_output=True, text=True, encoding="utf-8")
print("RC:", r.returncode)
print(r.stdout[-1500:] if r.stdout else "")
print(r.stderr[-1500:] if r.stderr else "")
