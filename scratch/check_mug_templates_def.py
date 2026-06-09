import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Find MUG_TEMPLATES definition
match = re.search(r'(const|let|var)\s+MUG_TEMPLATES\b', js_content)
if match:
    start_pos = match.start()
    print(f"MUG_TEMPLATES starts at position {start_pos}")
    # print first 300 characters
    print(js_content[start_pos:start_pos+300])
    
    # find where it ends (it should end at the closing array bracket before spa router or next section)
    # let's search for the end of the array, e.g. "];" or similar close to it
    end_match = re.search(r'\];\s*//\s*---\s*1\.\s*SPA\s*ROUTER', js_content)
    if end_match:
        end_pos = end_match.end()
        print(f"MUG_TEMPLATES array ends at position {end_pos}")
    else:
        print("Could not find exact end of MUG_TEMPLATES array")
else:
    print("Could not find MUG_TEMPLATES definition")
