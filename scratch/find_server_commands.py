import os
import json

log_path = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Found transcript log.")
    with open(log_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                content = str(data.get("content", "")) + str(data.get("tool_calls", ""))
                if "runserver" in content.lower() or "manage.py" in content.lower():
                    if data.get("type") == "RUN_COMMAND" or "run_command" in str(data.get("tool_calls")):
                        print(f"Line {idx} | Source: {data.get('source')} | Type: {data.get('type')}")
                        print(f"  Content: {content[:300]}")
            except Exception as e:
                pass
else:
    print("Transcript log not found.")
