import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "mugs" in line.lower() and ("nav" in line.lower() or "href" in line.lower() or "link" in line.lower() or "menu" in line.lower() or "anchor" in line.lower() or "onclick" in line.lower()):
            print(f"Line {idx+1:4d}: {line.strip()}")
