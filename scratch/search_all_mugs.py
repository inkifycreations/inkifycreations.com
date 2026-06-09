import re

def search_leftovers(filepath):
    print(f"\n--- Leftovers in {filepath} ---")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # We want to find occurrences of the word 'mugs' as a route or navigation target
    matches = [m.start() for m in re.finditer(r'\bmugs?\b', content, re.IGNORECASE)]
    print(f"Found {len(matches)} occurrences of 'mug'/'mugs'")
    for idx, pos in enumerate(matches):
        start = max(0, pos - 50)
        end = min(len(content), pos + 50)
        snippet = content[start:end].replace('\n', ' ')
        print(f"  Match {idx+1} at {pos}: ...{snippet}...")

search_leftovers("index.html")
search_leftovers("app.js")
