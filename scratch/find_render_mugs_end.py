with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for "renderMugsGrid() {" and then find the matching closing bracket
# Or search for the next method after renderMugsGrid, like "openCustomizer" or whatever is next
start_pos = content.find("renderMugsGrid() {")
if start_pos != -1:
    print(f"renderMugsGrid starts at position {start_pos}")
    # Let's print 1200 characters from start_pos
    print(content[start_pos:start_pos+1200])
    
    # Let's search for the next method, e.g. "openCustomizer(productId"
    next_method_pos = content.find("openCustomizer(productId", start_pos)
    if next_method_pos != -1:
        print(f"\nNext method starts at {next_method_pos}:")
        print(content[next_method_pos-100:next_method_pos+300])
    else:
        print("Could not find openCustomizer after renderMugsGrid")
else:
    print("Could not find renderMugsGrid")
