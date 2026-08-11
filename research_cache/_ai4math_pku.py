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


for repo in [
    "frenzymath/reap",
    "frenzymath/FATE",
    "frenzymath/jixia",
    "frenzymath/LeanSearch",
]:
    print(f"===== {repo} =====")
    t = readme(repo)
    print(t[:2600])
    print()
    time.sleep(1)
