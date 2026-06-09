import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk("scratch"):
    for name in files:
        if name.endswith(".py"):
            path = os.path.join(root, name)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "mugs-view" in content:
                print(f"Found 'mugs-view' in {path}")
                # Print lines around it
                lines = content.splitlines()
                for idx, line in enumerate(lines):
                    if "mugs-view" in line:
                        print(f"  Line {idx+1}: {line}")
