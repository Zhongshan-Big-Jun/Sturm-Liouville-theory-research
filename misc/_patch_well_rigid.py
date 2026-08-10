# -*- coding: utf-8 -*-
"""Move the demo/main code of _well_rigid_verify.py under __main__ guard so it is importable."""
import re
p = r"scripts\_well_rigid_verify.py"
src = open(p, encoding="utf-8").read()
marker = 'print("=" * 70)\nprint("PART A: exact symbolic identities")'
if marker not in src:
    print("marker not found")
else:
    # indent everything from the PART A print onward by 4 spaces and wrap in if __name__ block
    idx = src.index(marker)
    head, body = src[:idx], src[idx:]
    indented = "\n".join(("    " + ln if ln.strip() else ln) for ln in body.splitlines())
    new = head + "if __name__ == '__main__':\n" + indented + "\n"
    open(p, "w", encoding="utf-8", newline="\n").write(new)
    print("patched OK")
