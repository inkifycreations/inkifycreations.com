with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Searching app.js for templates:")
print("=" * 80)
in_templates = False
count = 0
for idx, line in enumerate(lines, 1):
    if "MUG_TEMPLATES" in line or "mug_templates" in line.lower():
        in_templates = True
        count = 0
    if in_templates:
        print(f"Line {idx:4d}: {line.strip()}")
        count += 1
        if count > 80: # Print up to 80 lines of MUG_TEMPLATES array
            print("... (truncated)")
            break
print("=" * 80)
