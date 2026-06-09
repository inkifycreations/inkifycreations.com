import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Let's search for "renderMugsGrid() {"
start_idx = js_content.find("renderMugsGrid() {")
if start_idx == -1:
    print("Could not find renderMugsGrid")
    sys.exit(0)

# We want to find the closing brace that matches the opening brace.
# Let's count open/close braces starting from the brace of renderMugsGrid() {
brace_count = 0
found_start = False
end_idx = -1

for idx in range(start_idx, len(js_content)):
    char = js_content[idx]
    if char == '{':
        brace_count += 1
        found_start = True
    elif char == '}':
        brace_count -= 1
        if found_start and brace_count == 0:
            end_idx = idx
            break

if end_idx != -1:
    print(f"renderMugsGrid starts at {start_idx} and ends at {end_idx}")
    print("Snippet after renderMugsGrid end:")
    print(js_content[end_idx:end_idx+300].replace('\u20b9', 'Rs.'))
else:
    print("Could not find matching closing brace")
