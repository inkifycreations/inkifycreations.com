import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\anaka\AppData\Local\Temp" # wait, the real path is C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs
log_dir = r"C:\Users\anaka\.gemini\antigravity\brain\ff19463d-4074-48f3-aeeb-54a1820fa937\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        # We look specifically at step 2280 or other steps that contain the full index.html file
        # step 2280 seems to contain the file view
        data = json.loads(line)
        if data.get("step_index") in [2280, 3227]:
            print(f"Step {data.get('step_index')} found!")
            content = data.get("content", "")
            # Let's search for the mugs-view section
            # It starts with <!-- 2.5 PHOTO MUGS VIEW -->
            # and ends before <!-- 3. ABOUT US VIEW -->
            start_comment = "<!-- 2.5 PHOTO MUGS VIEW -->"
            end_comment = "<!-- 3. ABOUT US VIEW -->"
            
            start_pos = content.find(start_comment)
            end_pos = content.find(end_comment)
            
            if start_pos != -1 and end_pos != -1:
                mugs_html = content[start_pos:end_pos]
                print("Extracted HTML:")
                print(mugs_html)
                
                # Save to a file
                with open("scratch/extracted_mugs_view.html", "w", encoding="utf-8") as out:
                    out.write(mugs_html)
                print("Saved to scratch/extracted_mugs_view.html")
                break
