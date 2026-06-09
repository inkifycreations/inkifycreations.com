import os

search_paths = [
    r"c:\Users\anaka\Downloads\third app\third app",
    r"C:\Users\anaka\OneDrive\Pictures"
]

print("Searching for awesome dad.png:")
for path in search_paths:
    print(f"Scanning: {path}")
    for root, dirs, files in os.walk(path):
        if any(p in root.lower() for p in ['.venv', 'node_modules', '.git', '.vscode', '.github']):
            continue
        if "awesome dad.png" in files:
            full_path = os.path.join(root, "awesome dad.png")
            print(f"FOUND: {full_path}")
print("Search done.")
