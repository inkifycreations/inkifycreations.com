import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
log_path = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\tasks\task-3259.log"

if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print("LOG CONTENT:")
    print("=" * 80)
    print(content)
    print("=" * 80)
else:
    print(f"Log not found at: {log_path}")
