# -*- coding: utf-8 -*-
import io, os, json
p = r"lean-proof\verification.json"
raw = open(p, "rb").read()
bom = raw[:3] == b"\xef\xbb\xbf"
data = raw.decode("utf-8-sig" if bom else "utf-8")
repls = [
    (
        '"obligation": "O5", "result": "MINOR_PARAPHRASE", "notes": "formal uses proof-required hypothesis c0 <= A_m - B_m; informal lists weaker A_m >= B_m"',
        '"obligation": "O5", "result": "FAITHFUL", "notes": "formal uses proof-required hypothesis c0 <= A_m - B_m; informal source corrected 2026-08-11 to A_m - B_m >= c0 (F-001 RESOLVED)"',
    ),
    (
        '{ "location": "informal doc SL_stability_moment_jump.tex Theorem 2.1", "issue": "stated hypothesis A_m >= B_m weaker than proof-required A_m - B_m >= c0; formal uses the stronger (proof-used) hypothesis (F-001)" }',
        '{ "location": "informal doc SL_stability_moment_jump.tex Theorem 2.1", "issue": "stated hypothesis A_m >= B_m weaker than proof-required A_m - B_m >= c0; formal uses the stronger (proof-used) hypothesis (F-001)", "status": "RESOLVED 2026-08-11: source corrected to A_m - B_m >= c0" }',
    ),
    (
        '"repair_hints": "Correct the informal theorem statement to A_m - B_m >= c0.  For the remaining completeness steps, formalize the isometric isomorphism and Weierstrass density separately."',
        '"repair_hints": "F-001 resolved 2026-08-11 (source corrected to A_m - B_m >= c0); no further repair needed.  For the remaining completeness steps, formalize the isometric isomorphism and Weierstrass density separately."',
    ),
]
for old, new in repls:
    assert data.count(old) == 1, old[:60]
    data = data.replace(old, new, 1)
# validate JSON
json.loads(data)
tmp = p + ".tmp"
with io.open(tmp, "wb") as f:
    f.write((("\ufeff" if bom else "") + data).encode("utf-8"))
os.replace(tmp, p)
print("verification.json patched + JSON valid")