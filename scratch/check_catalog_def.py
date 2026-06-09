with open("app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

pos = js_content.find("const CATALOG = [")
if pos != -1:
    print(js_content[pos:pos+1500])
else:
    print("CATALOG not found!")
