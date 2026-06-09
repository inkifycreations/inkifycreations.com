import os
from PIL import Image

cat_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design\Cat mug Design"
base_name = "CAT WALLSEE.png"
other_names = ["cat sleep.png", "cat nap.png", "cat come out.png"]

base_path = os.path.join(cat_dir, base_name)
with Image.open(base_path) as base_img:
    base_rgb = base_img.convert('RGB')
    w_base, h_base = base_rgb.size
    print(f"Base image: {base_name} ({w_base}x{h_base})")
    
    for other_name in other_names:
        other_path = os.path.join(cat_dir, other_name)
        with Image.open(other_path) as other_img:
            other_rgb = other_img.convert('RGB')
            w_other, h_other = other_rgb.size
            print(f"\nOther image: {other_name} ({w_other}x{h_other})")
            
            # Let's count how many pixels are different in the overlapping area
            # We resize other to base size for simple comparison, or just compare corners
            # Let's print colors of the non-grey areas
            # For example, let's look at the top-left 100x100 corner
            corners_match = True
            diff_count = 0
            total_checked = 0
            for y in range(min(h_base, h_other)):
                for x in range(min(w_base, w_other)):
                    r1, g1, b1 = base_rgb.getpixel((x, y))
                    r2, g2, b2 = other_rgb.getpixel((x, y))
                    
                    # If neither pixel is neutral grey
                    is_grey1 = abs(r1-g1) <= 2 and abs(g1-b1) <= 2 and 120 <= r1 <= 200
                    is_grey2 = abs(r2-g2) <= 2 and abs(g2-b2) <= 2 and 120 <= r2 <= 200
                    
                    if not is_grey1 and not is_grey2:
                        total_checked += 1
                        if abs(r1-r2) > 10 or abs(g1-g2) > 10 or abs(b1-b2) > 10:
                            diff_count += 1
            print(f"  Non-grey pixels compared: {total_checked}")
            print(f"  Different non-grey pixels: {diff_count} ({diff_count / total_checked * 100:.2f}% different)")
