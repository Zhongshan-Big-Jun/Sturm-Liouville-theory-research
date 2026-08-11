import json
import time
import urllib.parse
import urllib.request

QUERIES = [
    "Paper2Formalization auto-formalization research papers Lean",
    "FormalRx semantic failures autoformalization",
    "LeanMarathon reliable AI co-mathematicians",
    "MechMath sorrifier formal decomposition",
    "M2F automated formalization mathematical literature",
    "FaithSieve formal evidence proof review",
    "EvE evolutionary ensemble agents mathematics",
    "KiminaProver NuminaMath",
    "Reap AlphaProof reproduction Lean",
    "Archon formalization agent Lean workspace",
    "ReasBook M2F Quokka formalization",
    "LeanAide autoformalization combinator",
    "AIM natural language mathematical research agent",
    "LeanExplain natural language explanation Lean",
    "structured natural language SNL formalization",
    "MathWeaver knowledge graph mathematics textbook",
]


def oa(search: str):
    url = (
        "https://api.openalex.org/works?search="
        + urllib.parse.quote(search)
        + "&per-page=3"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "research-agent mailto:test@example.com"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"_error": str(e)}


for q in QUERIES:
    print(f"### {q}")
    d = oa(q)
    if "_error" in d:
        print("  ERR:", d["_error"])
    else:
        for w in d.get("results", [])[:3]:
            src = (w.get("primary_location") or {}).get("source") or {}
            print(
                f"  {w.get('title')} | {w.get('publication_year')} | "
                f"{src.get('display_name')} | {w.get('doi')}"
            )
    time.sleep(1.5)
