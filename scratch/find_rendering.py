with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_render = False
count = 0
for idx, line in enumerate(lines, 1):
    if "renderMugsGrid" in line:
        in_render = True
        count = 0
    if in_render:
        print(f"Line {idx:4d}: {line.rstrip()}")
        count += 1
        if count > 80:
            break
