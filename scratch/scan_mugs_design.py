import os

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
if not os.path.exists(pictures_dir):
    print(f"Error: Directory does not exist: {pictures_dir}")
else:
    print(f"Directory {pictures_dir} exists. Scanning contents:")
    for root, dirs, files in os.walk(pictures_dir):
        rel_path = os.path.relpath(root, pictures_dir)
        if rel_path == ".":
            rel_path = "root"
        print(f"\n[{rel_path}]")
        for d in dirs:
            print(f"  Dir: {d}")
        for f in files:
            print(f"  File: {f}")
