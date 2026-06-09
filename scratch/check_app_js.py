import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Let's count occurrences of "id: \"mug-"
import re
matches = re.findall(r"id:\s*\"mug-[^\"]*\"", content)
print(f"Total templates in app.js: {len(matches)}")
print("First 5 template ids:")
for m in matches[:5]:
    print(f"  {m}")
print("Last 5 template ids:")
for m in matches[-5:]:
    print(f"  {m}")
