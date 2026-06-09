with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find('class="nav-menu"')
if pos != -1:
    print(content[pos-100:pos+300])
