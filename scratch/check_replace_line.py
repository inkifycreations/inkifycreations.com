with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find("item.overlayHtml.replace")
if pos != -1:
    print(content[pos-100:pos+200])
else:
    print("Not found!")
