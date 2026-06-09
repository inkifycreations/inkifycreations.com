import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

backend_dir = r"c:\Users\anaka\Downloads\third app\third app\backend"
search_terms = ["index.html", "app.js", "assets", "static"]

for root, dirs, files in os.walk(backend_dir):
    if ".venv" in root or "venv" in root or "__pycache__" in root:
        continue
    for name in files:
        if name.endswith(".py"):
            path = os.path.join(root, name)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                for term in search_terms:
                    if term in content:
                        print(f"File: {os.path.relpath(path, backend_dir)} contains '{term}'")
            except Exception as e:
                pass
