import os

workspace_dir = r"c:\Users\anaka\Downloads\third app\third app"
keywords = ["MUG_TEMPLATES", "assets/", "template"]

for root, dirs, files in os.walk(workspace_dir):
    if any(p in root.lower() for p in ['.venv', 'node_modules', '.git', '.vscode', '.github']):
        continue
    for name in files:
        if name.endswith(('.js', '.html', '.py')):
            path = os.path.join(root, name)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                for kw in keywords:
                    if kw in content:
                        print(f"File: {os.path.relpath(path, workspace_dir)} | Contains: {kw}")
            except Exception:
                pass
