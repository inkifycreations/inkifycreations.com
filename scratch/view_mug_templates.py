with open("app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_templates = False
brace_count = 0
for idx, line in enumerate(lines):
    if "const MUG_TEMPLATES" in line or "MUG_TEMPLATES =" in line:
        in_templates = True
        print(f"Found MUG_TEMPLATES at line {idx+1}:")
    
    if in_templates:
        print(f"{idx+1}: {line.rstrip()}")
        # simple check to stop printing after 120 lines
        brace_count += line.count("{") - line.count("}")
        if idx > 300 or (brace_count == 0 and idx > 10 and ";" in line):
            break
