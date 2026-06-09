import sys
sys.stdout.reconfigure(encoding='utf-8')

files = ["index.html", "app.js"]
for name in files:
    print(f"\nSearching in: {name}")
    print("=" * 80)
    with open(name, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if "mug.png" in line:
                print(f"Line {idx+1:4d}: {line.strip()}")
