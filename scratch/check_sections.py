with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r'<section\s+id="([^"]+)"', content)
for m in matches:
    print(f"Section ID: {m.group(1)} at position {m.start()}")
