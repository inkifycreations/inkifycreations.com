import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

pos = js_content.find("renderMugsGrid() {")
if pos != -1:
    print(f"Content starting 2000 characters after renderMugsGrid start:")
    snippet = js_content[pos + 2000:pos + 4000]
    # Replace Rupee symbol just in case
    snippet = snippet.replace('\u20b9', 'Rs.')
    print(snippet)
