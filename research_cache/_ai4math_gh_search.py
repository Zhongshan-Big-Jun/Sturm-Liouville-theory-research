import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

TOKEN = os.environ["GH_TOKEN"]

QUERIES = [
    "LeanMarathon",
    "Paper2Formalization",
    "FormalRx autoformalization",
    "MechMath",
    "LeanAide",
    "reaptactic",
    "Reap AlphaProof Lean",
    "Evolutionary Ensemble eve math",
    "Archon formal math Lean",
    "ReasBook",
    "FaithSieve",
    "OptProver",
    "CAM-Bench",
    "ReasLab",
    "NuminaMath",
    "KiminaProver",
    "MathWeaver 数学",
    "LeanExplain",
    "Fyan formal math",
    "autoformalization agent Lean research paper",
]


def gh_search(query: str):
    url = (
        "https://api.github.com/search/repositories?q="
        + urllib.parse.quote(query)
        + "&per_page=5"
    )
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode())
            out = []
            for it in d.get("items", []):
                out.append(
                    {
                        "full_name": it["full_name"],
                        "desc": (it.get("description") or "")[:160],
                        "stars": it.get("stargazers_count"),
                        "url": it["html_url"],
                    }
                )
            return out
    except Exception as e:
        return [{"error": str(e)}]


for q in QUERIES:
    res = gh_search(q)
    print(f"### {q}")
    for r in res:
        if "error" in r:
            print("  ERR:", r["error"])
        else:
            print(
                f"  {r['full_name']} (★{r['stars']}) | {r['desc']} | {r['url']}"
            )
    time.sleep(3)
