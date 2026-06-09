with open("app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

def print_context(line_num, context_size=10):
    start = max(0, line_num - context_size)
    end = min(len(lines), line_num + context_size)
    print(f"\n--- Context around line {line_num+1} ---")
    for i in range(start, end):
        prefix = "-> " if i == line_num else "   "
        print(f"{prefix}{i+1}: {lines[i].rstrip()}")

for idx, line in enumerate(lines):
    if "renderMugsGrid" in line:
        print_context(idx, 5)
    if "searchMugs" in line:
        print_context(idx, 5)
