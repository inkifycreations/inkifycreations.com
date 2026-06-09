with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

def search_text(anchor):
    pos = content.find(anchor)
    print(f"Anchor '{anchor[:40]}...':")
    if pos != -1:
        print(f"  Found at {pos}! Snippet:")
        print(content[pos:pos+300])
    else:
        print("  Not found!")
    print("-" * 50)

# Check route handler anchor
search_text("viewId === 'cart'")
# Check openCustomizer
search_text("openCustomizer(productId")
# Check end of productCatalog
search_text("updateTextContent(val)")
