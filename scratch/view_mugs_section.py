import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_section = False
start_idx = 0
for idx, line in enumerate(lines):
    if 'id="mugs-view"' in line:
        in_section = True
        start_idx = idx
        print(f"Section starts at line {idx+1}")
    if in_section and '</section>' in line:
        print(f"Section ends at line {idx+1}")
        # print the section
        for j in range(start_idx, idx + 1):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
