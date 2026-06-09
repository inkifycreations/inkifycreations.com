import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
# Find sections containing mugs page content or grid
matches = list(re.finditer(r"id=\"mugs-templates-grid\"|view-mugs|mugs-view", content))
for m in matches[:3]:
    start = max(0, m.start() - 200)
    end = min(len(content), m.end() + 1000)
    print(f"Match context around index {m.start()}:")
    print(content[start:end])
    print("=" * 80)
