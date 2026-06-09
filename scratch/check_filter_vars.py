import re

with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

for word in ["activeMugFilter", "mugSearchQuery"]:
    matches = [m.start() for m in re.finditer(r'\b' + re.escape(word) + r'\b', content)]
    print(f"Word '{word}': Found {len(matches)} occurrences")
    for idx, pos in enumerate(matches):
        print(f"  Match {idx+1} at {pos}: {content[max(0, pos-40):min(len(content), pos+80)].replace('\n', ' ')}")
