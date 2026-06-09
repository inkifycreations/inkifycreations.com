import os
import shutil

# Directories
pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
outputs_dir = os.path.join(pictures_dir, "outputs")
assets_dir = r"c:\Users\anaka\Downloads\third app\third app\assets"
app_js_path = r"c:\Users\anaka\Downloads\third app\third app\app.js"

# 1. Copy Composed Wraps to Assets
mappings = {
    os.path.join(outputs_dir, "birthday", "birthday.png"): os.path.join(assets_dir, "birthday_template.png"),
    os.path.join(outputs_dir, "love and annversiary", "love.png"): os.path.join(assets_dir, "love_heart_template.png"),
    os.path.join(outputs_dir, "love and annversiary", "love togther.png"): os.path.join(assets_dir, "you_me_template.png"),
    os.path.join(outputs_dir, "normal", "christmas.png"): os.path.join(assets_dir, "christmas_template.png"),
    os.path.join(outputs_dir, "Dad gesign", "awesome dad.png"): os.path.join(assets_dir, "awesome_dad.png"),
    os.path.join(outputs_dir, "Dad gesign", "best mom.png"): os.path.join(assets_dir, "best_mom.png"),
    os.path.join(outputs_dir, "normal", "motivations.png"): os.path.join(assets_dir, "motivations.png"),
}

print("Copying composed wraps to website assets:")
print("=" * 80)
for src, dst in mappings.items():
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"  Copied '{os.path.relpath(src, outputs_dir)}' -> '{os.path.basename(dst)}'")
    else:
        print(f"  Error: Source not found: '{src}'")
print("=" * 80)

# 2. Modify app.js overlays
print("\nUpdating app.js overlays...")
with open(app_js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Dad template overlayHtml
dad_target = """    id: "mug-best-dad",
    name: "Best Dad Ever Trophy Mug",
    category: "family",
    categoryLabel: "Drinkware - Family",
    description: "Award your hero with a custom golden trophy badge and his favorite family photo. A touching Father's Day present.",
    originalPrice: 299,
    price: 219,
    overlayClass: "dad-overlay",
    overlayHtml: `
<div style="text-align: center; color: #e0f2fe; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; align-items: center;">
<span style="font-size: 0.45rem; font-weight: 900; background: #0284c7; padding: 2px 4px; border-radius: 4px; display: inline-block; letter-spacing: 0.5px;">#1 HERO</span>
<i class="fa-solid fa-trophy" style="font-size: 1.15rem; color: #fef08a; margin: 4px 0;"></i>
<span style="font-size: 0.45rem; font-weight: 600; color: #bae6fd; line-height: 1;">Best Dad</span>
</div>
`"""

dad_replacement = """    id: "mug-best-dad",
    name: "Best Dad Ever Trophy Mug",
    category: "family",
    categoryLabel: "Drinkware - Family",
    description: "Award your hero with a custom golden trophy badge and his favorite family photo. A touching Father's Day present.",
    originalPrice: 299,
    price: 219,
    overlayClass: "dad-overlay",
    overlayHtml: `
      <img src="assets/awesome_dad.png" style="width: calc(100% + 8px); height: calc(100% + 8px); margin: -4px; object-fit: cover; border-radius: 1px;" alt="Best Dad Ever Preview">
    `"""

# Replace Mom template overlayHtml
mom_target = """    id: "mug-best-mom",
    name: "Best Mom Ever Floral Mug",
    category: "family",
    categoryLabel: "Drinkware - Family",
    description: "An elegant pink-hued template with a delicate floral illustration frame and heart patterns. Show your love for mom.",
    originalPrice: 299,
    price: 219,
    overlayClass: "mom-overlay",
    overlayHtml: `
<div style="text-align: center; color: #fdf2f8; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; align-items: center;">
<span style="font-size: 0.45rem; font-weight: 900; background: #db2777; padding: 2px 4px; border-radius: 4px; display: inline-block; letter-spacing: 0.5px;">BEST MOM</span>
<i class="fa-solid fa-seedling" style="font-size: 1.15rem; color: #fbcfe8; margin: 4px 0;"></i>
<span style="font-size: 0.45rem; font-weight: 600; color: #fbcfe8; line-height: 1;">With Love</span>
</div>
`"""

mom_replacement = """    id: "mug-best-mom",
    name: "Best Mom Ever Floral Mug",
    category: "family",
    categoryLabel: "Drinkware - Family",
    description: "An elegant pink-hued template with a delicate floral illustration frame and heart patterns. Show your love for mom.",
    originalPrice: 299,
    price: 219,
    overlayClass: "mom-overlay",
    overlayHtml: `
      <img src="assets/best_mom.png" style="width: calc(100% + 8px); height: calc(100% + 8px); margin: -4px; object-fit: cover; border-radius: 1px;" alt="Best Mom Ever Preview">
    `"""

# Replace Quote template overlayHtml
quote_target = """    id: "mug-quote-minimalist",
    name: "Minimalist Motivation Quote Mug",
    category: "quotes",
    categoryLabel: "Drinkware - Quotes",
    description: "Clean typography frame with quotes designed to fuel your work ethic. Perfect for corporate desks and workspace setups.",
    originalPrice: 299,
    price: 219,
    overlayClass: "quote-overlay",
    overlayHtml: `
      <div style="text-align: center; color: #f3f4f6; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.45rem; font-weight: 900; background: #374151; padding: 2px 4px; border-radius: 4px; display: inline-block; letter-spacing: 0.5px;">FOCUS</span>
        <i class="fa-solid fa-quote-left" style="font-size: 1.1rem; color: #e5e7eb; margin: 4px 0;"></i>
        <span style="font-size: 0.45rem; font-weight: 600; color: #d1d5db; line-height: 1;">Work Hard</span>
      </div>
    `"""

quote_replacement = """    id: "mug-quote-minimalist",
    name: "Minimalist Motivation Quote Mug",
    category: "quotes",
    categoryLabel: "Drinkware - Quotes",
    description: "Clean typography frame with quotes designed to fuel your work ethic. Perfect for corporate desks and workspace setups.",
    originalPrice: 299,
    price: 219,
    overlayClass: "quote-overlay",
    overlayHtml: `
      <img src="assets/motivations.png" style="width: calc(100% + 8px); height: calc(100% + 8px); margin: -4px; object-fit: cover; border-radius: 1px;" alt="Motivation Preview">
    `"""

modified = False
if dad_target in content:
    content = content.replace(dad_target, dad_replacement)
    print("  Updated 'mug-best-dad' overlay HTML.")
    modified = True
else:
    # Try with CRLF / LF variations
    dad_target_lf = dad_target.replace('\r\n', '\n')
    if dad_target_lf in content:
        content = content.replace(dad_target_lf, dad_replacement)
        print("  Updated 'mug-best-dad' overlay HTML (LF).")
        modified = True
    else:
        print("  Warning: could not find dad_target in app.js!")

if mom_target in content:
    content = content.replace(mom_target, mom_replacement)
    print("  Updated 'mug-best-mom' overlay HTML.")
    modified = True
else:
    mom_target_lf = mom_target.replace('\r\n', '\n')
    if mom_target_lf in content:
        content = content.replace(mom_target_lf, mom_replacement)
        print("  Updated 'mug-best-mom' overlay HTML (LF).")
        modified = True
    else:
        print("  Warning: could not find mom_target in app.js!")

if quote_target in content:
    content = content.replace(quote_target, quote_replacement)
    print("  Updated 'mug-quote-minimalist' overlay HTML.")
    modified = True
else:
    quote_target_lf = quote_target.replace('\r\n', '\n')
    if quote_target_lf in content:
        content = content.replace(quote_target_lf, quote_replacement)
        print("  Updated 'mug-quote-minimalist' overlay HTML (LF).")
        modified = True
    else:
        print("  Warning: could not find quote_target in app.js!")

if modified:
    with open(app_js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("app.js updated successfully!")
else:
    print("No changes made to app.js.")
