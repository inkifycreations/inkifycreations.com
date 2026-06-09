with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find('id="about-view"')
if pos != -1:
    print(content[pos-300:pos+300])
