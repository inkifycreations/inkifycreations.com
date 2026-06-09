with open("index.css", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.findall(r"\.[a-zA-Z0-9_-]*overlay[^{]*\{[^}]*\}", content, re.IGNORECASE | re.DOTALL)
for m in matches[:10]:
    print(m)
    print("-" * 40)
