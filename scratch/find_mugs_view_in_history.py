import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "mugs-templates-grid" in line:
            try:
                data = json.loads(line)
                step_idx = data.get("step_index")
                # print(f"Found on line {idx+1}, Step {step_idx}")
                
                # Check if there are tool calls in this line
                tool_calls = data.get("tool_calls", [])
                for tc_idx, tc in enumerate(tool_calls):
                    name = tc.get("name")
                    args = tc.get("arguments", {})
                    # Print if it has code/replacement content
                    for k, v in args.items():
                        if isinstance(v, str) and "mugs-templates-grid" in v:
                            print(f"Step {step_idx} | Tool: {name} | Arg: {k} (length {len(v)})")
                            # Save this argument content
                            filename = f"scratch/extracted_arg_step_{step_idx}_{k}.html"
                            with open(filename, "w", encoding="utf-8") as out:
                                out.write(v)
                            print(f"  Saved to {filename}")
            except Exception as e:
                pass
