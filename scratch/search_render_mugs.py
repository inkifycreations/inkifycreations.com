with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if "renderMugsGrid" in line:
        print(f"Line {idx:4d}: {line.strip()}")
