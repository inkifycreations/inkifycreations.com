import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

app_js_path = "app.js"
index_html_path = "index.html"

# 1. Edit index.html
print("Editing index.html...")
with open(index_html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Replace Slide 3 button
old_button = """                  <button class="btn-primary" onclick="appRouter.navigate('mugs')">
                    Explore Mug Studio <i class="fa-solid fa-mug-saucer"></i>
                  </button>"""

new_button = """                  <button class="btn-primary" onclick="productCatalog.openCustomizer(4)">
                    Customize Mug <i class="fa-solid fa-mug-hot"></i>
                  </button>"""

if old_button in html_content:
    html_content = html_content.replace(old_button, new_button)
    print("  Slide 3 button updated to open customizer directly.")
else:
    # Try LF version
    old_button_lf = old_button.replace('\r\n', '\n')
    new_button_lf = new_button.replace('\r\n', '\n')
    if old_button_lf in html_content:
        html_content = html_content.replace(old_button_lf, new_button_lf)
        print("  Slide 3 button updated to open customizer directly (LF).")
    else:
        print("  Warning: Could not find Slide 3 button in index.html!")

# Remove mugs-view section
# It goes from <section id="mugs-view" ...> to the next </section>
mugs_section_regex = r"<!-- 2\.5 PHOTO MUGS VIEW -->\s*<section id=\"mugs-view\" class=\"view-section\">.*?<\/section>"
if re.search(mugs_section_regex, html_content, re.DOTALL):
    html_content = re.sub(mugs_section_regex, "", html_content, flags=re.DOTALL)
    print("  Removed mugs-view section successfully.")
else:
    # Try without the comment in case it's different
    mugs_section_regex_alt = r"<section id=\"mugs-view\" class=\"view-section\">.*?<\/section>"
    if re.search(mugs_section_regex_alt, html_content, re.DOTALL):
        html_content = re.sub(mugs_section_regex_alt, "", html_content, flags=re.DOTALL)
        print("  Removed mugs-view section successfully (no comment match).")
    else:
        print("  Warning: Could not find mugs-view section in index.html!")

with open(index_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)


# 2. Edit app.js
print("\nEditing app.js...")
with open(app_js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Remove 'mugs' from routing segments
old_router_check = "['home', 'products', 'mugs', 'about', 'cart', 'orders', 'success', 'tracking']"
new_router_check = "['home', 'products', 'about', 'cart', 'orders', 'success', 'tracking']"

if old_router_check in js_content:
    js_content = js_content.replace(old_router_check, new_router_check)
    print("  Removed 'mugs' from router checks.")
else:
    print("  Warning: Could not find routing checks in app.js!")

# Remove mugs handler inside navigate()
old_mugs_handler = """    } else if (viewId === 'mugs') {
      productCatalog.renderMugsGrid();"""

if old_mugs_handler in js_content:
    js_content = js_content.replace(old_mugs_handler, "")
    print("  Removed mugs routing handler.")
else:
    # Try LF / formatting variant
    old_mugs_handler_lf = old_mugs_handler.replace('\r\n', '\n')
    if old_mugs_handler_lf in js_content:
        js_content = js_content.replace(old_mugs_handler_lf, "")
        print("  Removed mugs routing handler (LF).")
    else:
        print("  Warning: Could not find mugs routing handler in app.js!")

# Remove openCustomizer redirect
old_customizer_redirect = """    if (productId === 4 && !templateName) {
      appRouter.navigate('mugs');
      return;
    }"""

if old_customizer_redirect in js_content:
    js_content = js_content.replace(old_customizer_redirect, "")
    print("  Removed mugs redirect in openCustomizer.")
else:
    # Try LF version
    old_customizer_redirect_lf = old_customizer_redirect.replace('\r\n', '\n')
    if old_customizer_redirect_lf in js_content:
        js_content = js_content.replace(old_customizer_redirect_lf, "")
        print("  Removed mugs redirect in openCustomizer (LF).")
    else:
        print("  Warning: Could not find mugs redirect in openCustomizer!")

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("\nMugs page removal completed successfully!")
