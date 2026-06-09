import os

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures"
for folder in ["Camera Roll", "Screenshots"]:
    path = os.path.join(pictures_dir, folder)
    if os.path.exists(path):
        print(f"\nScanning folder: {path}")
        files = os.listdir(path)
        for name in sorted(files)[:30]: # Limit to first 30 files
            fpath = os.path.join(path, name)
            if os.path.isfile(fpath) and name.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"  - {name} | Size: {os.path.getsize(fpath)} bytes")
