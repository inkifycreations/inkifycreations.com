import os
path = r"C:\Users\anaka\OneDrive\Pictures\mugs design\outputs"
print("Exists:", os.path.exists(path))
if os.path.exists(path):
    print("List:", os.listdir(path))
