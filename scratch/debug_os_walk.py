import os
path = r"C:\Users\anaka\OneDrive\Pictures\mugs design\outputs"
print("walk:")
for root, dirs, files in os.walk(path):
    print(root, dirs, len(files))
