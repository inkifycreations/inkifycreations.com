import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\anaka\Downloads\third app\third app"
for root, dirs, files in os.walk(workspace_dir):
    if ".venv" in root or "venv" in root or "__pycache__" in root:
        continue
    for name in files:
        if name.endswith(('.html', '.js', '.css')):
            path = os.path.join(root, name)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "mug_photo_print.png" in content:
                    print(f"File: {os.path.relpath(path, workspace_dir)} contains 'mug_photo_print.png'")
            except Exception as e:
                pass
