import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "mugs-templates-grid" in line or "mugs-view" in line:
            try:
                data = json.loads(line)
                print(f"Line {idx+1} | Step {data.get('step_index')} | Type: {data.get('type')} | Source: {data.get('source')} | Status: {data.get('status')}")
            except Exception as e:
                print(f"Error parsing line {idx+1}: {e}")
