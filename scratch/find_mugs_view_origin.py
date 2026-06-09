import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

earliest_step = None
earliest_type = None
earliest_snippet = ""
earliest_line = 0

with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "mugs-view" in line:
            try:
                data = json.loads(line)
                step_idx = data.get("step_index")
                content = str(data.get("content", ""))
                
                # Check if this contains the HTML code
                if "id=\"mugs-view\"" in content or "id='mugs-view'" in content:
                    earliest_step = step_idx
                    earliest_type = data.get("type")
                    earliest_line = idx + 1
                    
                    # Get snippet
                    pos = content.find("mugs-view")
                    earliest_snippet = content[max(0, pos-200):min(len(content), pos+4000)]
                    break
            except Exception as e:
                pass

if earliest_step is not None:
    print(f"Earliest match found at Line {earliest_line}, Step {earliest_step} (Type: {earliest_type}):")
    print(earliest_snippet)
else:
    print("No matches found in logs.")
