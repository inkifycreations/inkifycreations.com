import re

path = 'index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace targets
replacements = {
    'src="assets/brand_identity.png"': 'src="{% static \'assets/brand_identity.png\' %}"',
    'src="assets/gift_box.jpg"': 'src="{% static \'assets/gift_box.jpg\' %}"',
    'src="assets/mug_photo_print.png"': 'src="{% static \'assets/mug_photo_print.png\' %}"',
    'src="assets/hero_tshirt_print.png"': 'src="{% static \'assets/hero_tshirt_print.png\' %}"'
}

replaced_count = 0
for target, replacement in replacements.items():
    occurrences = content.count(target)
    if occurrences > 0:
        content = content.replace(target, replacement)
        replaced_count += occurrences
        print(f"Replaced {occurrences} instances of: {target}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Done! Total replacements made: {replaced_count}")
