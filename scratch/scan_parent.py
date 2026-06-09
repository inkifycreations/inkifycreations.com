import os

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures"
print(f"Scanning parent folder: {pictures_dir}")
for name in os.listdir(pictures_dir):
    path = os.path.join(pictures_dir, name)
    if os.path.isdir(path):
        print(f"Directory: {name}")
    elif name.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(f"File: {name} | Size: {os.path.getsize(path)}")
