with open("app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

import re
print("Searching for renderMugsGrid references:")
matches = [m.start() for m in re.finditer(r'renderMugsGrid', js_content)]
for m in matches:
    print(f"  Found renderMugsGrid reference at pos {m}: {js_content[max(0, m-50):min(len(js_content), m+100)]}\n")

print("Searching for TEMPLATES references:")
matches = [m.start() for m in re.finditer(r'\bTEMPLATES\b', js_content)]
for m in matches:
    print(f"  Found TEMPLATES reference at pos {m}: {js_content[max(0, m-50):min(len(js_content), m+100)]}\n")
