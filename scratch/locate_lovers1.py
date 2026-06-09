import os

search_paths = [
    r"c:\Users\anaka",
    r"C:\Users\anaka\OneDrive\Pictures"
]

print("Searching for lovers1.png:")
for path in search_paths:
    print(f"Scanning: {path}")
    for root, dirs, files in os.walk(path):
        if any(p in root.lower() for p in ['.venv', 'node_modules', '.git', '.vscode', '.github', 'appdata']):
            continue
        if "lovers1.png" in files:
            full_path = os.path.join(root, "lovers1.png")
            print(f"FOUND: {full_path}")
print("Search done.")
