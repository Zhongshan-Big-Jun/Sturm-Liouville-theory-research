import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

TOKEN = os.environ["GH_TOKEN"]

REPOS = [
    "YuanheZ/LeanMarathon",
    "siddhartha-gadgil/LeanAide",
    "optpku/ReasBook",
    "TropicalFatFish/anonymous-faithsieve",
    "chenyili0818/OptProver",
    "SJTU-AI4Math/LeanExplain",
    "scaling-group/eve",
    "MechMath/IMO2026",
]

ORGS = ["SJTU-AI4Math", "scaling-group", "ProjectNumina", "MechMath"]


def gh(url: str):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_url": url}
    except Exception as e:
        return {"_error": str(e), "_url": url}


for repo in REPOS:
    d = gh(f"https://api.github.com/repos/{repo}")
    print(f"===== {repo} =====")
    if "_error" in d:
        print("  ERR:", d["_error"], d["_url"])
        continue
    print("  desc:", d.get("description"))
    print("  topics:", d.get("topics"))
    print("  stars:", d.get("stargazers_count"), "| forks:", d.get("forks_count"))
    print("  homepage:", d.get("homepage"))
    print("  created:", d.get("created_at"), "| pushed:", d.get("pushed_at"))
    print("  default_branch:", d.get("default_branch"))
    time.sleep(1)

for org in ORGS:
    d = gh(f"https://api.github.com/orgs/{org}/repos?per_page=30")
    print(f"===== ORG {org} =====")
    if "_error" in d:
        print("  ERR:", d["_error"], d["_url"])
        continue
    for r in d:
        print(f"  {r['name']} (★{r.get('stargazers_count')}) | {(r.get('description') or '')[:120]}")
    time.sleep(1)
