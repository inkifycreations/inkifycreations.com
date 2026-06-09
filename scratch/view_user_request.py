import os
import json

log_path = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs\transcript.jsonl"
start_line = 2530
end_line = 2555

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            if start_line <= idx <= end_line:
                try:
                    data = json.loads(line)
                    print(f"Line {idx} | Source: {data.get('source')} | Type: {data.get('type')}")
                    content = data.get("content", "")
                    if content:
                        print(f"  Content: {content[:400]}...")
                except Exception as e:
                    print(f"Error line {idx}: {e}")
else:
    print("Transcript log not found.")
