import os

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
print(f"Walking mugs design: {pictures_dir}")

for root, dirs, files in os.walk(pictures_dir):
    rel = os.path.relpath(root, pictures_dir)
    print(f"Folder: {rel}")
    print(f"  Dirs: {dirs}")
    print(f"  Files count: {len(files)}")
