import os

outputs_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design\outputs"
print("Exists:", os.path.exists(outputs_dir))
if os.path.exists(outputs_dir):
    print("Listing outputs directory contents:")
    for root, dirs, files in os.walk(outputs_dir):
        rel = os.path.relpath(root, outputs_dir)
        print(f"Folder: {rel}")
        print(f"  Dirs: {dirs}")
        print(f"  Files: {files}")
