import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "mug_photo_print.png" in line:
            print(f"Line {idx+1}: {line.strip()}")
