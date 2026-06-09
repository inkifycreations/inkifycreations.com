import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("app.js", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "openCustomizer" in line:
            print(f"Line {idx+1:4d}: {line.strip()}")
