import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# 1. Remove MUG_TEMPLATES definition
start_templates = js_content.find("const MUG_TEMPLATES = [")
if start_templates != -1:
    # Find matching ending '];' for MUG_TEMPLATES array
    # We search for the first '];' after start_templates that is followed by the SPA router comment or similar.
    # To be extremely safe, we can look for the closing bracket matching the open bracket of the array.
    brace_count = 0
    found_start = False
    end_templates = -1
    for idx in range(start_templates, len(js_content)):
        char = js_content[idx]
        if char == '[':
            brace_count += 1
            found_start = True
        elif char == ']':
            brace_count -= 1
            if found_start and brace_count == 0:
                # include the semicolon if there is one
                if idx + 1 < len(js_content) and js_content[idx+1] == ';':
                    end_templates = idx + 2
                else:
                    end_templates = idx + 1
                break
    
    if end_templates != -1:
        # Let's clean it up
        js_content = js_content[:start_templates] + js_content[end_templates:]
        print("Successfully removed MUG_TEMPLATES array.")
    else:
        print("Error: Could not find end of MUG_TEMPLATES array.")
else:
    print("MUG_TEMPLATES array not found (already removed or named differently).")


# 2. Remove this.renderMugsGrid() call from init()
old_render_call = "this.renderMugsGrid();"
if old_render_call in js_content:
    js_content = js_content.replace(old_render_call, "")
    print("Removed this.renderMugsGrid() call from init().")
else:
    print("this.renderMugsGrid() call not found in init().")


# 3. Remove activeMugFilter, mugSearchQuery, filterMugs, searchMugs, and renderMugsGrid
# We look for "activeMugFilter: 'all'," and the end of renderMugsGrid()
start_filters = js_content.find("activeMugFilter: 'all',")
if start_filters != -1:
    # Find the end of renderMugsGrid()
    # We find "renderMugsGrid() {" first
    render_start = js_content.find("renderMugsGrid() {", start_filters)
    if render_start != -1:
        brace_count = 0
        found_start = False
        end_render = -1
        for idx in range(render_start, len(js_content)):
            char = js_content[idx]
            if char == '{':
                brace_count += 1
                found_start = True
            elif char == '}':
                brace_count -= 1
                if found_start and brace_count == 0:
                    end_render = idx + 1
                    # check if followed by comma and newline
                    if idx + 1 < len(js_content) and js_content[idx+1] == ',':
                        end_render = idx + 2
                    break
        
        if end_render != -1:
            # We want to remove from start_filters to end_render
            # Let's see what is immediately before start_filters to make sure we don't leave syntax errors
            # E.g. we might have:
            #   updateTextContent(val) {
            #     // Canvas preview removed
            #   },
            #   activeMugFilter: 'all',
            # We should check if we need to remove the comma after the updateTextContent method if activeMugFilter was the next key.
            # But in JS, trailing commas in objects are perfectly valid, so leaving it is fine.
            # Let's do the cut.
            js_content = js_content[:start_filters] + js_content[end_render:]
            print("Successfully removed mug filtering, search, and rendering methods from productCatalog.")
        else:
            print("Error: Could not find end of renderMugsGrid method.")
    else:
        print("Error: Could not find renderMugsGrid starting point after filters.")
else:
    print("activeMugFilter property not found (already removed).")


with open("app.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("\nApp.js cleanup completed.")
