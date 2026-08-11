import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

QUERIES = [
    ("Paper2Formalization", "ti:%22Paper2Formalization%22"),
    ("FormalRx", "ti:%22FormalRx%22"),
    ("LeanMarathon", "ti:%22LeanMarathon%22"),
    ("MechMath", "ti:%22MechMath%22"),
    ("KiminaProver", "all:%22KiminaProver%22"),
    ("M2F formalization", "ti:%22M2F%22+AND+abs:%22formalization%22"),
    ("FaithSieve", "all:%22FaithSieve%22"),
    ("AIM mathematician", "ti:%22AI%20mathematician%22"),
    ("autoformalization survey", "ti:%22autoformalization%22+AND+abs:%22survey%22"),
]


def arxiv(query: str):
    url = "https://export.arxiv.org/api/query?search_query=" + query + "&max_results=5"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode()
        except Exception as e:
            print(f"    (retry {attempt+1}: {e})")
            time.sleep(8 + attempt * 6)
    return None


def parse(xml_text: str):
    if not xml_text:
        return []
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_text)
    out = []
    for e in root.findall("a:entry", ns):
        title = "".join(e.find("a:title", ns).itertext()).strip()
        ident = e.find("a:id", ns).text
        pub = e.find("a:published", ns).text
        out.append((title, ident, pub))
    return out


for label, q in QUERIES:
    print(f"### {label}")
    xml_text = arxiv(q)
    for title, ident, pub in parse(xml_text):
        print(f"  {title} | {ident} | {pub}")
    time.sleep(5)
