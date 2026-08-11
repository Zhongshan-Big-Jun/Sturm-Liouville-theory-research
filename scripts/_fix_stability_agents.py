# -*- coding: utf-8 -*-
import io, os, json
p = r"state\activity.jsonl"
raw = open(p, "rb").read()
bom = raw[:3] == b"\xef\xbb\xbf"
data = raw.decode("utf-8-sig" if bom else "utf-8")
if data and not data.endswith("\n"):
    data += "\n"
entry = {
    "activity_id": "ACT-20260811-023",
    "started_at": "2026-08-11T08:00:00Z",
    "ended_at": "2026-08-11T08:40:00Z",
    "effective_minutes": 40,
    "category": "maintenance",
    "related_ids": ["MRP-20260731-BVE-SL"],
    "artifacts_created_or_updated": [
        "docs/SL_stability_moment_jump.tex",
        "docs/SL_stability_moment_jump.pdf",
        "docs/build/SL_stability_moment_jump.*",
        "tools/jump-stability.md",
        "tools/README.md",
        "lean-proof/STATUS.md",
        "lean-proof/audit_report.md",
        "lean-proof/verification.json",
        "AGENTS.md",
        "scripts/_fix_stability_f001.py",
        "scripts/_fix_stability_tools.py",
        "scripts/_fix_stability_agents.py",
    ],
    "summary": "F-001 statement correction (session 67): SL_stability_moment_jump.tex Theorem 2.1/2.2 hypothesis corrected from A_m >= B_m to B_m >= 0 and A_m - B_m >= c_0 (matches proof + Lean formalization). Counterexamples verified (A_m=B_m=1 oscillates; A_m-B_m=1/2<c0 breaks product bound); 2000 random-coefficient Fraction checks pass under corrected hypothesis. tex recompiled 7 pp zero warnings; tools + lean-proof records synced (F-001 RESOLVED, O5 FAITHFUL); lake build re-run 8564 jobs exit 0; AGENTS.md session 67 recorded. STRICT text fix, no new numerical claims.",
    "evidence": ["scripts/_fix_stability_f001.py", "scripts/_fix_stability_tools.py", "lean-proof/audit_report.md addendum"],
    "recorded_by": "coordinator",
    "notes": "estimate; no git commit (not requested); run-manifest.json kept as session-66 record (Lean input hashes unchanged)."
}
data += json.dumps(entry, ensure_ascii=False) + "\n"
tmp = p + ".tmp"
with io.open(tmp, "wb") as f:
    f.write((("\ufeff" if bom else "") + data).encode("utf-8"))
os.replace(tmp, p)
# validate: every line parses
for ln in data.splitlines():
    json.loads(ln)
print("activity.jsonl appended + validated,", len(data.splitlines()), "entries")