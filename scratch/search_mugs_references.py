import re

def search_file(filepath, patterns):
    print(f"\n--- Searching {filepath} ---")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    for pat in patterns:
        matches = [m.start() for m in re.finditer(pat, content)]
        print(f"Pattern '{pat}': Found {len(matches)} matches")
        for idx, pos in enumerate(matches[:5]):
            # Get surrounding lines
            start = max(0, pos - 100)
            end = min(len(content), pos + 200)
            snippet = content[start:end]
            print(f"  Match {idx+1} near position {pos}:\n{snippet}\n")

search_file("index.html", ["Explore Mug Studio", "id=\"mugs-view\"", "mugs-view"])
search_file("app.js", [
    r"\['home', 'products', 'mugs'",
    r"viewId === 'mugs'",
    r"productId === 4 && !templateName"
])
