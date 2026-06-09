import os
import json

log_path = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs\transcript.jsonl"
if os.path.exists(log_path):
    print("Found transcript log.")
    keywords = ["mugs design", "Cat mug Design", "birthday 1.png", "ChatGPT Image"]
    matches = {kw: [] for kw in keywords}
    
    with open(log_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                content = str(data.get("content", "")) + str(data.get("tool_calls", ""))
                for kw in keywords:
                    if kw.lower() in content.lower():
                        matches[kw].append((line_num, data.get("type"), data.get("source")))
            except Exception as e:
                pass
                
    for kw, occurrences in matches.items():
        print(f"\nKeyword: '{kw}' - {len(occurrences)} occurrences")
        for occ in occurrences[:10]: # Print first 10 occurrences
            print(f"  Line {occ[0]} | Type: {occ[1]} | Source: {occ[2]}")
else:
    print("Transcript log not found.")
