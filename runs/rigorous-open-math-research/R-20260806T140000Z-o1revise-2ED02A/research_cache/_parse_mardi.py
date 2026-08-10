import io, re
p = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A\research_cache\mardi4nfdi_sun2022.html"
raw = io.open(p, encoding="utf-8-sig").read()
# strip tags crudely
txt = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S)
txt = re.sub(r"<[^>]+>", " ", txt)
txt = re.sub(r"\s+", " ", txt)
print(txt[:6000])
