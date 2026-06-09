import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk("scratch"):
    for name in files:
        if name.endswith((".py", ".txt", ".md")):
            path = os.path.join(root, name)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "mugs-templates-grid" in content:
                print(f"Found in {path}")
                # Print lines containing it
                lines = content.splitlines()
                for idx, line in enumerate(lines):
                    if "mugs-templates-grid" in line:
                        print(f"  Line {idx+1}: {line}")
