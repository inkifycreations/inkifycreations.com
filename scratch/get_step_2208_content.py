import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        data = json.loads(line)
        if data.get("step_index") == 2208:
            content = data.get("content", "")
            with open("scratch/step_2208_content.txt", "w", encoding="utf-8") as out:
                out.write(content)
            print("Successfully saved Step 2208 content to scratch/step_2208_content.txt")
            break
