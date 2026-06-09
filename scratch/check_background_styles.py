with open("index.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "background" in line or "body" in line:
        if idx > 0 and "body" in lines[idx-1] or "body" in line or "view-section" in line:
            print(f"Line {idx+1}: {line.strip()}")
