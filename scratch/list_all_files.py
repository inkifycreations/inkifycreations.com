import os

root_dir = r"C:\Users\anaka\OneDrive\Pictures"
print(f"Walking root directory: {root_dir}")

for root, dirs, files in os.walk(root_dir):
    if "outputs" in root.lower() or "outputs" in dirs:
        print(f"Found outputs directory: {root}")
        print(f"Files inside: {files[:10]}")
