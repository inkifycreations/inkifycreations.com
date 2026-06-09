import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\anaka\Downloads\third app\third app"
for name in os.listdir(workspace_dir):
    path = os.path.join(workspace_dir, name)
    if os.path.isfile(path) and name.endswith(('.html', '.js', '.css')):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if "some days are hard" in content.lower():
                print(f"Found in file: {name}")
                # print matching line numbers
                f.seek(0)
                for idx, line in enumerate(f):
                    if "some days are hard" in line.lower():
                        print(f"  Line {idx+1}: {line.strip()}")
        except Exception as e:
            print(f"Error reading {name}: {e}")
