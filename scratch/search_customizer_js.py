with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

import re
# Find mentions of selection, design, gallery, customizer
search_terms = ["customizer", "design", "gallery", "photo", "upload"]
for term in search_terms:
    matches = list(re.finditer(term, content, re.IGNORECASE))
    print(f"Term '{term}': found {len(matches)} matches.")
    # Show the first 3 match contexts
    for m in matches[:3]:
        start = max(0, m.start() - 50)
        end = min(len(content), m.end() + 100)
        print(f"  [{m.start()}]: ...{content[start:end].strip()}...")
    print("-" * 50)
