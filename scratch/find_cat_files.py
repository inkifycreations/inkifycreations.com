import os

home_dir = r"C:\Users\anaka"
print(f"Searching home folder for 'cat' images: {home_dir}")

image_extensions = ('.png', '.jpg', '.jpeg', '.webp')
count = 0

for root, dirs, files in os.walk(home_dir):
    # Skip library and system folders
    if any(p in root.lower() for p in ['.venv', 'node_modules', '.git', '.vscode', '.github', 'appdata', 'microsoft', 'cookies', 'local settings']):
        continue
    for name in files:
        if 'cat' in name.lower() and name.lower().endswith(image_extensions):
            path = os.path.join(root, name)
            print(f"Found: {name} | Size: {os.path.getsize(path)//1024} KB | Path: {path}")
            count += 1
            if count > 50:
                break
    if count > 50:
        break
print("Search complete.")
