with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r'data-view="home"', content)
for idx, m in enumerate(matches):
    print(f"Match {idx+1} at position {m.start()}:")
    print(content[m.start()-100:m.start()+200])
