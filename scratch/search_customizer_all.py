import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
for i in range(740, 804):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}")
