import os
import time

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"

for root, dirs, files in os.walk(pictures_dir):
    folder = os.path.relpath(root, pictures_dir)
    if folder == ".":
        continue
    print(f"\nFolder: {folder}")
    for name in sorted(files):
        if name.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(root, name)
            mtime = os.path.getmtime(path)
            size = os.path.getsize(path)
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
            print(f"  - {name:40s} | Size: {size:8d} | Modified: {time_str}")
