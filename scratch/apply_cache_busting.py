import sys
sys.stdout.reconfigure(encoding='utf-8')

# Replacements in app.js
app_js_path = "app.js"
with open(app_js_path, "r", encoding="utf-8") as f:
    app_js_content = f.read()

app_js_replacements = {
    'assets/birthday_template.png': 'assets/birthday_template.png?v=2',
    'assets/love_heart_template.png': 'assets/love_heart_template.png?v=2',
    'assets/awesome_dad.png': 'assets/awesome_dad.png?v=2',
    'assets/best_mom.png': 'assets/best_mom.png?v=2',
    'assets/motivations.png': 'assets/motivations.png?v=2',
    'assets/christmas_template.png': 'assets/christmas_template.png?v=2',
    'assets/you_me_template.png': 'assets/you_me_template.png?v=2',
    'assets/mug.png': 'assets/mug.png?v=2',
}

modified_app_js = app_js_content
for src, dst in app_js_replacements.items():
    # Only replace if not already cache-busted
    if src in modified_app_js and src + "?v=" not in modified_app_js:
        modified_app_js = modified_app_js.replace(src, dst)
        print(f"app.js: Replaced '{src}' -> '{dst}'")

if modified_app_js != app_js_content:
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(modified_app_js)
    print("app.js updated successfully with cache busting!")
else:
    print("No changes needed in app.js.")

# Replacements in index.html
index_html_path = "index.html"
with open(index_html_path, "r", encoding="utf-8") as f:
    index_html_content = f.read()

index_html_replacements = {
    'assets/mug_photo_print.png': 'assets/mug_photo_print.png?v=2',
}

modified_index_html = index_html_content
for src, dst in index_html_replacements.items():
    if src in modified_index_html and src + "?v=" not in modified_index_html:
        modified_index_html = modified_index_html.replace(src, dst)
        print(f"index.html: Replaced '{src}' -> '{dst}'")

if modified_index_html != index_html_content:
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(modified_index_html)
    print("index.html updated successfully with cache busting!")
else:
    print("No changes needed in index.html.")
