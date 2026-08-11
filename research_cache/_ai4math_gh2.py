import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

TOKEN = os.environ["GH_TOKEN"]


def gh(url: str):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"_error": e.code}
    except Exception as e:
        return {"_error": str(e)}


def search(q):
    url = (
        "https://api.github.com/search/repositories?q="
        + urllib.parse.quote(q)
        + "&per_page=5"
    )
    d = gh(url)
    if "_error" in d:
        return [{"error": str(d["_error"])}]
    return [
        {
            "full_name": r["full_name"],
            "desc": (r.get("description") or "")[:150],
            "stars": r.get("stargazers_count"),
            "url": r["html_url"],
        }
        for r in d.get("items", [])
    ]


QUERIES = [
    "Paper2Formalization Lean",
    "FormalRx semantic autoformalization",
    "AIM natural language mathematician agent",
    "Archon formalization agent Lean",
    "Reap AlphaProof reproduction Lean",
    "NuminaMath dataset",
    "KiminaProver",
    "居浩成 automated reasoning agents",
    "Fyan formal computation human-AI",
    "MechMath agent team AMSS",
    "Erdos problems formalization Lean blueprint",
    "Quokka formalization Lean",
]

for q in QUERIES:
    print(f"### {q}")
    for r in search(q):
        if "error" in r:
            print("  ERR:", r["error"])
        else:
            print(f"  {r['full_name']} (★{r['stars']}) | {r['desc']} | {r['url']}")
    time.sleep(3)
