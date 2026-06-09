with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r"overlayHtml|overlayClass", content)
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 200)
    print(f"Match context around index {m.start()}:")
    print(content[start:end])
    print("=" * 80)
