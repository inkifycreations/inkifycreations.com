import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

found_def = False
def_lines = []
brace_count = 0

for idx, line in enumerate(lines):
    if "const CATALOG" in line or "CATALOG =" in line:
        found_def = True
        print(f"Found CATALOG definition at line {idx+1}:")
    
    if found_def:
        def_lines.append(f"{idx+1}: {line}")
        brace_count += line.count("{") - line.count("}")
        if brace_count == 0 and len(def_lines) > 5 and (";" in line or "]" in line):
            # Print the collected lines
            for l in def_lines[:150]:
                print(l.rstrip())
            break
