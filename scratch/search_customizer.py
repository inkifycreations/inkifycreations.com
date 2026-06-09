with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = list(re.finditer(r'customizer', content, re.IGNORECASE))
print(f"Found {len(matches)} occurrences of 'customizer'")
for idx, m in enumerate(matches[:10]):
    print(f"Match {idx+1} at {m.start()}:")
    print(content[m.start()-100:m.start()+200])
    print("=" * 50)
