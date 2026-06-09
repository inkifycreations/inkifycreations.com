import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = list(re.finditer(r"<header|</header>|<nav|</nav>|class=\"nav-|class=\"menu-", content))
for m in matches[:5]:
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 500)
    print(f"Match context around index {m.start()}:")
    print(content[start:end])
    print("=" * 80)
