with open("app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

import re

# Find TEMPLATES definition start
templates_match = re.search(r'(const|let|var)\s+TEMPLATES\b', js_content)
if templates_match:
    start_pos = templates_match.start()
    print(f"TEMPLATES starts at position {start_pos}")
    # print first 500 characters
    print(js_content[start_pos:start_pos+500])
else:
    print("Could not find TEMPLATES definition")

# Let's inspect the code from line 2050 to 2150
lines = js_content.splitlines()
print("\n--- app.js lines 2050 to 2150 ---")
for idx in range(2049, min(2150, len(lines))):
    print(f"{idx+1}: {lines[idx]}")
