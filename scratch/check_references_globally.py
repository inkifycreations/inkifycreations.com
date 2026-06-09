import re

def search_in_file(filepath, word):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    matches = [m.start() for m in re.finditer(r'\b' + re.escape(word) + r'\b', content)]
    print(f"File {filepath}: Found {len(matches)} occurrences of '{word}'")

search_in_file("index.html", "MUG_TEMPLATES")
search_in_file("app.js", "MUG_TEMPLATES")
