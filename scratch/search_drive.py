import os
import time

home_dir = r"C:\Users\anaka"
print(f"Searching for files created today in: {home_dir}")

today_start = time.time() - 3600 * 2  # files modified in the last 2 hours
count = 0

for root, dirs, files in os.walk(home_dir):
    # Skip library and system folders to avoid lag
    if any(p in root.lower() for p in ['.venv', 'node_modules', '.git', '.vscode', '.github', 'appdata', 'microsoft', 'cookies', 'local settings']):
        continue
    for name in files:
        if name.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(root, name)
            try:
                mtime = os.path.getmtime(path)
                if mtime > today_start:
                    print(f"Modified recently: {name} | Size: {os.path.getsize(path)//1024} KB | Path: {path}")
                    count += 1
                    if count > 50:
                        break
            except Exception:
                pass
    if count > 50:
        break
print("Search done.")
