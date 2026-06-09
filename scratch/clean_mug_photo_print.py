import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

def clean_photo_print(input_path, output_path):
    img = Image.open(input_path)
    w, h = img.size
    img_rgb = img.convert('RGB')
    pixels = img_rgb.load()
    
    # Bounding box for the main front-facing body of the mug
    # Based on the X range 0 to 1023, we clean from X=150 to X=800 (excluding handle and edges)
    # and Y=200 to Y=800
    mug_body_left = 150
    mug_body_right = 800
    mug_body_top = 200
    mug_body_bottom = 800
    
    dark_threshold = 120
    
    new_img = img_rgb.copy()
    new_pixels = new_img.load()
    
    for y in range(mug_body_top, mug_body_bottom + 1):
        x = mug_body_left
        while x <= mug_body_right:
            r, g, b = pixels[x, y]
            if r < dark_threshold and g < dark_threshold and b < dark_threshold:
                start_x = x
                end_x = x
                while end_x <= mug_body_right:
                    nr, ng, nb = pixels[end_x, y]
                    if nr < dark_threshold and ng < dark_threshold and nb < dark_threshold:
                        end_x += 1
                    else:
                        break
                
                left_x = start_x - 1
                right_x = end_x
                
                if left_x < mug_body_left:
                    left_x = mug_body_left
                if right_x > mug_body_right:
                    right_x = mug_body_right
                
                left_color = pixels[left_x, y]
                right_color = pixels[right_x, y]
                
                run_length = right_x - left_x
                if run_length > 0:
                    for ix in range(start_x, right_x):
                        t = (ix - left_x) / run_length
                        ir = int(left_color[0] * (1 - t) + right_color[0] * t)
                        ig = int(left_color[1] * (1 - t) + right_color[1] * t)
                        ib = int(left_color[2] * (1 - t) + right_color[2] * t)
                        new_pixels[ix, y] = (ir, ig, ib)
                
                x = end_x
            else:
                x += 1
                
    new_img.save(output_path, "PNG")
    print(f"Cleaned square mug saved to: {output_path}")

clean_photo_print("assets/mug_photo_print.png", "assets/mug_photo_print_clean.png")
