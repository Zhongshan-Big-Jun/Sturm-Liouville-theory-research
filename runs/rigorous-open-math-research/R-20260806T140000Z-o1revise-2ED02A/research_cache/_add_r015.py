import io, os, json, hashlib
root = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A"
p = os.path.join(root, "research_ledger.md")
s = io.open(p, encoding="utf-8").read()
entry = """
## R-015 (2026-08-06 continuation): failure routes and tooling lessons

- Failure route: Sun 2022 S1/S2 exact class definitions.  All public routes
  failed or were empty: ScienceDirect page + r.jina.ai proxy (connection
  closed/failed), Peeref (login wall), Semantic Scholar Graph API (HTTP 429
  twice), OpenAlex (200, no abstract, closed), Crossref (200, no abstract),
  MaRDI portal (200, empty metadata page), zbMATH PDF (403), web search
  (snippet only).  Outcome: NOT_VERIFIABLE, honestly recorded in
  status_and_literature.md N3.  Lesson: for closed-access articles, an
  unresolved bibliographic detail must be reported as NOT_VERIFIABLE, not
  inferred.
- Tooling failure: apply_patch.bat mangles multi-line patch arguments on
  Windows (%* newline handling), repeatedly returning "Invalid patch: The
  last line of the patch must be '*** End Patch'".  Workaround that works:
  invoke codex.exe --codex-run-as-apply-patch directly from PowerShell with
  the patch as a single argument.  Lesson recorded for future runs.
- Tooling limitation: Remove-Item in shell commands was policy-blocked this
  session; scratch files were left in place and recorded as scratch in
  repro_manifest.md instead of deleted.
- Encoding lesson: Windows PowerShell -Encoding utf8 writes a UTF-8 BOM;
  several artifacts carried BOMs and were stripped at closure (all run
  hashes re-verified after stripping).  For ASCII-only artifacts, verify with
  an explicit BOM/non-ASCII scan before closing.
- Process lesson: ledger R-010 claimed audit_report.md was written while the
  file was lost; this session delivered it and recorded the correction as new
  entries (R-011..R-015) rather than retro-editing R-010.  Rule: before
  claiming an artifact is delivered, verify the file exists and hash it.
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(s.rstrip("\n") + "\n" + entry)
h = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()
print("new research_ledger hash:", h)
# update manifest
mp = os.path.join(root, "run-manifest.json")
d = json.loads(io.open(mp, encoding="utf-8").read())
for art in d["artifacts"]:
    if art["path"] == "research_ledger.md":
        art["sha256"] = h
io.open(mp, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
# final verification of all manifest hashes
ok = True
for art in d["artifacts"]:
    if art["sha256"] and not art["sha256"].startswith("REFRESH"):
        cur = hashlib.sha256(open(os.path.join(root, art["path"]), "rb").read()).hexdigest().upper()
        if cur != art["sha256"]:
            ok = False
            print("MISMATCH", art["path"])
print("ALL MANIFEST HASHES MATCH:", ok)
print("run-manifest final hash:", hashlib.sha256(open(mp, "rb").read()).hexdigest().upper())
