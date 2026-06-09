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
            print(f"--- Step 2208 details ---")
            print("Type:", data.get("type"))
            # print keys
            print("Keys:", list(data.keys()))
            tool_calls = data.get("tool_calls", [])
            print(f"Number of tool calls: {len(tool_calls)}")
            for tc in tool_calls:
                print("Tool Name:", tc.get("name"))
                args = tc.get("arguments", {})
                print("Arg Keys:", list(args.keys()))
                # If there's content, let's dump it or see if it contains index.html
                if "TargetFile" in args:
                    print("TargetFile:", args["TargetFile"])
                # check if there's ReplacementContent or CodeContent
                content_key = "ReplacementContent" if "ReplacementContent" in args else ("CodeContent" if "CodeContent" in args else None)
                if content_key:
                    content_val = args[content_key]
                    print(f"Content length in {content_key}: {len(content_val)}")
                    # Let's save it to a file
                    with open(f"scratch/step_2208_{content_key}.txt", "w", encoding="utf-8") as out:
                        out.write(content_val)
                    print(f"Saved content to scratch/step_2208_{content_key}.txt")
            break
