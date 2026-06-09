import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("backend/inkify_backend/settings.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "TEMPLATES = [" in line or "STATIC_URL" in line or "STATICFILES_DIRS" in line or "STATIC_ROOT" in line:
        print(f"Line {idx+1}:")
        # print next 15 lines
        for j in range(idx, min(len(lines), idx + 20)):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print("-" * 50)
