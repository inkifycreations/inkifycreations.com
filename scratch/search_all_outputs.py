import os

home_dir = r"C:\Users\anaka"
print(f"Searching for 'outputs' directory in home folder: {home_dir}")

for root, dirs, files in os.walk(home_dir):
    # Skip library and system folders to avoid lag
    if any(p in root.lower() for p in ['.venv', 'node_modules', '.git', '.vscode', '.github', 'appdata', 'microsoft', 'cookies', 'local settings']):
        continue
    for d in dirs:
        if d.lower() == "outputs":
            path = os.path.join(root, d)
            print(f"FOUND outputs folder: {path}")
            print(f"  Files inside: {os.listdir(path)}")
print("Search done.")
