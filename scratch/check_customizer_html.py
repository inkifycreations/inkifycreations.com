with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find('id="customizer-view"')
if pos != -1:
    print(content[pos-100:pos+3000])
else:
    print("customizer-view not found!")
