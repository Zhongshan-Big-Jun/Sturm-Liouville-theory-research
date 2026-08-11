import json
import os
import time
import urllib.error
import urllib.request

TOKEN = os.environ["GH_TOKEN"]

REPOS = [
    "YuanheZ/LeanMarathon",
    "siddhartha-gadgil/LeanAide",
    "optpku/ReasBook",
    "TropicalFatFish/anonymous-faithsieve",
    "chenyili0818/OptProver",
    "SJTU-AI4Math/LeanExplain",
    "SJTU-AI4Math/SNL-Basics",
    "SJTU-AI4Math/Fulcrum-Template",
    "SJTU-AI4Math/MathWeaver",
    "scaling-group/eve",
    "MechMath/MechMath-v1",
    "MechMath/MechMath-agent-team",
]


def gh(url: str):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"_error": e.code}
    except Exception as e:
        return {"_error": str(e)}


for repo in REPOS:
    d = gh(f"https://api.github.com/repos/{repo}/readme")
    print(f"===== {repo} =====")
    if "_error" in d:
        print("  ERR:", d["_error"])
        continue
    import base64

    try:
        text = base64.b64decode(d["content"]).decode("utf-8", errors="replace")
    except Exception as e:
        print("  decode err:", e)
        continue
    print(text[:3000])
    print()
    time.sleep(1)
