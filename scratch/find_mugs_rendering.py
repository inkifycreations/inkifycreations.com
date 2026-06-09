import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("app.js", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "mugs" in line.lower() and ("view" in line.lower() or "render" in line.lower() or "page" in line.lower() or "init" in line.lower()):
            print(f"Line {idx+1:4d}: {line.strip()}")
