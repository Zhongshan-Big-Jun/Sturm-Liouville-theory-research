import json
import os
import time
import urllib.error
import urllib.request
import base64

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


def readme(repo):
    d = gh(f"https://api.github.com/repos/{repo}/readme")
    if "_error" in d:
        return f"(no readme: {d['_error']})"
    try:
        return base64.b64decode(d["content"]).decode("utf-8", errors="replace")
    except Exception as e:
        return f"(decode err: {e})"


print("===== frenzymath org =====")
d = gh("https://api.github.com/orgs/frenzymath/repos?per_page=30")
if "_error" in d:
    print("ERR:", d["_error"])
else:
    for r in d:
        print(f"  {r['name']} (★{r.get('stargazers_count')}) | {(r.get('description') or '')[:130]}")
time.sleep(1)

print()
print("===== Archon-Horizon README =====")
print(readme("frenzymath/Archon-Horizon")[:5000])
