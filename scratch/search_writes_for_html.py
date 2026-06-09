import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "mugs-templates-grid" in line:
            data = json.loads(line)
            # Look at write/edit tool calls
            tool_calls = data.get("tool_calls", [])
            for tc in tool_calls:
                name = tc.get("name")
                args = tc.get("arguments", {})
                # If it's write_to_file or replace_file_content and target is index.html
                target_file = args.get("TargetFile", "")
                if "index.html" in target_file:
                    print(f"Line {idx+1}: Tool {name} for {target_file}")
                    for k, v in args.items():
                        if isinstance(v, str) and "mugs-templates-grid" in v:
                            print(f"Found in arg '{k}' (length {len(v)}):")
                            print(v)
                            print("="*80)
