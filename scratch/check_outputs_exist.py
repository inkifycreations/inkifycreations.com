import os

output_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design\outputs"
print(f"Checking outputs directory: {output_dir}")

for root, dirs, files in os.walk(output_dir):
    for name in files:
        path = os.path.join(root, name)
        print(f"File: {name} | RelPath: {os.path.relpath(path, output_dir)} | Exist: {os.path.exists(path)}")
