import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

if not os.path.exists(transcript_path):
    print(f"Log path does not exist: {transcript_path}")
    sys.exit(1)

print("Reading log...")
with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "id=\"mugs-view\"" in line or "<!-- 2.5 PHOTO MUGS VIEW -->" in line:
            print(f"Found match on line {idx+1}!")
            try:
                data = json.loads(line)
                # We search for tool_calls or replacement text
                print("Step Index:", data.get("step_index"))
                print("Type:", data.get("type"))
                
                # Check if this contains the HTML code
                content = str(data.get("content", ""))
                if "id=\"mugs-view\"" in content:
                    print("Found in content! Length:", len(content))
                    # Print context
                    start = content.find("id=\"mugs-view\"")
                    print(content[max(0, start-100):min(len(content), start+2000)])
                    print("-" * 50)
                
                # Check tool calls
                tool_calls = data.get("tool_calls", [])
                for tc in tool_calls:
                    args = tc.get("arguments", {})
                    # check targetContent or replacementContent or codeContent
                    for k, v in args.items():
                        if isinstance(v, str) and "id=\"mugs-view\"" in v:
                            print(f"Found in tool call argument '{k}'! Length: {len(v)}")
                            start = v.find("id=\"mugs-view\"")
                            print(v[max(0, start-100):min(len(v), start+3000)])
                            print("=" * 80)
            except Exception as e:
                print(f"Error parsing line {idx+1}: {e}")
