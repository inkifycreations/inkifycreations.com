import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

search_dirs = [
    r"c:\Users\anaka\Downloads\third app\third app",
    r"C:\Users\anaka\OneDrive\Pictures"
]

for base_dir in search_dirs:
    print(f"\nSearching in: {base_dir}")
    print("=" * 80)
    for root, dirs, files in os.walk(base_dir):
        # Skip output dirs
        if "outputs" in root.lower() or ".venv" in root or "venv" in root or "__pycache__" in root:
            continue
        for name in files:
            if "mug" in name.lower() and name.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(root, name)
                print(f"File: {os.path.relpath(path, base_dir)} | Size: {os.path.getsize(path)} bytes")
