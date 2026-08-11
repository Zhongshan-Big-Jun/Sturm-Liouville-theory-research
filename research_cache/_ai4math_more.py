import json
import os
import time
import urllib.error
import urllib.request
import base64

TOKEN = os.environ["GH_TOKEN"]

REPOS = [
    "optsuite/M2F",
    "MechMath/MechMath-agent-team/nl-prover",
    "MechMath/MechMath-agent-team/kb-manager",
    "MechMath/MechMath-agent-team/fl-prover",
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


def readme(repo, sub=""):
    url = f"https://api.github.com/repos/{repo}/readme"
    if sub:
        url += f"/{sub}"
    d = gh(url)
    if "_error" in d:
        return f"(no readme at {sub}: {d['_error']})"
    try:
        return base64.b64decode(d["content"]).decode("utf-8", errors="replace")
    except Exception as e:
        return f"(decode err: {e})"


for repo in REPOS:
    print(f"===== {repo} =====")
    if "/" in repo and repo.count("/") > 1:
        parts = repo.split("/", 2)
        root = f"{parts[0]}/{parts[1]}"
        sub = parts[2]
        # 尝试子目录 readme 或目录列表
        d = gh(f"https://api.github.com/repos/{root}/contents/{sub}")
        if isinstance(d, list):
            names = [x["name"] for x in d]
            print("  dir:", names)
            for n in names:
                if n.lower().startswith("readme"):
                    t = gh(f"https://api.github.com/repos/{root}/contents/{sub}/{n}")
                    if "_error" not in t:
                        txt = base64.b64decode(t["content"]).decode("utf-8", errors="replace")
                        print(f"  --- {n} ---")
                        print(txt[:3500])
                        break
        else:
            print("  ERR:", d.get("_error"))
        continue
    print(readme(repo)[:3500])
    print()
    time.sleep(1)
