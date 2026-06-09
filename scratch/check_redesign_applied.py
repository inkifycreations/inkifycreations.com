import sys
sys.stdout.reconfigure(encoding='utf-8')

# Check index.html filter pills
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

has_friends = "filterMugs('friends'" in html
has_classic = "filterMugs('classic'" in html
print(f"index.html has 'friends' filter: {has_friends}")
print(f"index.html has 'classic' filter: {has_classic}")

# Check app.js templates count
with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
matches = re.findall(r"id:\s*\"mug-[^\"]*\"", js)
print(f"Total templates in app.js: {len(matches)}")
