import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

img = Image.open("assets/mug_photo_print.png")
w, h = img.size
img_rgb = img.convert('RGB')

# Let's check some pixels in the middle to see if it has the cat drawing.
# Since it's 1024x1024, let's check bounding box of white/light pixels.
min_x, min_y, max_x, max_y = w, h, 0, 0
for y in range(h):
    for x in range(w):
        r, g, b = img_rgb.getpixel((x, y))
        if r > 120 and g > 120 and b > 120:
            if x < min_x: min_x = x
            if y < min_y: min_y = y
            if x > max_x: max_x = x
            if y > max_y: max_y = y

print(f"Mug body bounding box: X: {min_x} to {max_x}, Y: {min_y} to {max_y}")
print(f"Mug body size: {max_x - min_x}x{max_y - min_y}")

# Slice at Y = 512
slice_y = h // 2
print(f"\nAnalyzing horizontal slice at Y = {slice_y}:")
for x in range(min_x, max_x + 1, 10):
    r, g, b = img_rgb.getpixel((x, slice_y))
    # Print only if it's dark
    if r < 120 and g < 120 and b < 120:
        print(f"  X={x:4d}: RGB=({r:3d}, {g:3d}, {b:3d}) - DARK!")
