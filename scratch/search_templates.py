import re

with open('app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's parse all templates in MUG_TEMPLATES array
# We can find the MUG_TEMPLATES block
match = re.search(r'const MUG_TEMPLATES = \[(.*?)\];', content, re.DOTALL)
if match:
    block = match.group(1)
    # Find all objects in the array
    objs = re.findall(r'\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*category:\s*"([^"]+)"', block)
    for oid, name, cat in objs:
        if cat in ('birthday', 'love'):
            print(f"ID: {oid} | Name: {name} | Category: {cat}")
else:
    print("MUG_TEMPLATES array not found")
