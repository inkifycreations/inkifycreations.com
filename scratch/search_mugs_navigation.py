import sys
sys.stdout.reconfigure(encoding='utf-8')

files = ["index.html", "app.js"]
for name in files:
    print(f"\nSearching in: {name}")
    print("=" * 80)
    with open(name, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if "mugs" in line.lower() and ("navigate" in line.lower() or "activeview" in line.lower() or "router" in line.lower() or "viewid" in line.lower()):
                print(f"Line {idx+1:4d}: {line.strip()}")
