import os

designs_dir = "assets/mug_designs"
if os.path.exists(designs_dir):
    files = os.listdir(designs_dir)
    print(f"Directory {designs_dir} exists and contains {len(files)} files.")
    print("Sample files:", files[:10])
else:
    print(f"Directory {designs_dir} does not exist!")
