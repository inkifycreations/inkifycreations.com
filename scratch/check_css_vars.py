with open("index.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(25, 45):
    print(f"{i+1}: {lines[i].strip()}")
