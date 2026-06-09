import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

def remove_cat_illustration(input_path, output_path):
    img = Image.open(input_path)
    w, h = img.size
    img_rgb = img.convert('RGB')
    pixels = img_rgb.load()
    
    # Bounding box of the mug body (excluding the handle which is on the right)
    mug_body_left = 450
    mug_body_right = 1050
    mug_body_top = 150
    mug_body_bottom = 900
    
    # Threshold for dark ink pixels
    dark_threshold = 120
    
    # Make a copy of pixels to modify
    new_img = img_rgb.copy()
    new_pixels = new_img.load()
    
    for y in range(mug_body_top, mug_body_bottom + 1):
        # Scan across the row to find dark pixels and interpolate them
        x = mug_body_left
        while x <= mug_body_right:
            r, g, b = pixels[x, y]
            # Check if this pixel is dark
            if r < dark_threshold and g < dark_threshold and b < dark_threshold:
                # Find the start of the dark run
                start_x = x
                # Scan to find the end of the dark run
                end_x = x
                while end_x <= mug_body_right:
                    nr, ng, nb = pixels[end_x, y]
                    if nr < dark_threshold and ng < dark_threshold and nb < dark_threshold:
                        end_x += 1
                    else:
                        break
                
                # end_x is now the first non-dark pixel to the right, or mug_body_right + 1
                # We interpolate between (start_x - 1) and end_x
                left_x = start_x - 1
                right_x = end_x
                
                # Boundary conditions
                if left_x < mug_body_left:
                    left_x = mug_body_left
                if right_x > mug_body_right:
                    right_x = mug_body_right
                
                left_color = pixels[left_x, y]
                right_color = pixels[right_x, y]
                
                # Fill in the run
                run_length = right_x - left_x
                if run_length > 0:
                    for ix in range(start_x, right_x):
                        # Linear interpolation factor
                        t = (ix - left_x) / run_length
                        ir = int(left_color[0] * (1 - t) + right_color[0] * t)
                        ig = int(left_color[1] * (1 - t) + right_color[1] * t)
                        ib = int(left_color[2] * (1 - t) + right_color[2] * t)
                        new_pixels[ix, y] = (ir, ig, ib)
                
                # Advance x to the end of the run
                x = end_x
            else:
                x += 1
                
    # Save the modified image
    new_img.save(output_path, "PNG")
    print(f"Cleaned image saved to: {output_path}")

remove_cat_illustration("assets/mug.png", "assets/mug_blank_test.png")
