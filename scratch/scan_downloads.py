import os

downloads_dir = r"C:\Users\anaka\Downloads"
print(f"Scanning downloads folder: {downloads_dir}")

image_extensions = ('.png', '.jpg', '.jpeg', '.webp')
count = 0

for root, dirs, files in os.walk(downloads_dir):
    # Exclude venv and node_modules to avoid scanning thousands of library files
    if any(p in root.lower() for p in ['.venv', 'node_modules', '.git', '.vscode', '.github']):
        continue
    for name in files:
        if name.lower().endswith(image_extensions):
            path = os.path.join(root, name)
            size_kb = os.path.getsize(path) // 1024
            # We look for images that are not inside the project's frontend/backend/assets folders
            if "third app" not in root.lower() or "assets" in root.lower():
                print(f"File: {name} | Size: {size_kb} KB | Path: {os.path.relpath(path, downloads_dir)}")
                count += 1
                if count > 50:
                    print("Too many images, stopping list.")
                    break
    if count > 50:
        break
