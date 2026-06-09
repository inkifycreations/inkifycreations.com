import os
from PIL import Image

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
output_dir = os.path.join(pictures_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)

print("Pictures dir:", pictures_dir)
print("Output dir:", output_dir)
print("Output dir exists:", os.path.exists(output_dir))

# Try saving a test image
test_img = Image.new('RGB', (100, 100), (255, 0, 0))
target_path = os.path.join(output_dir, "test_img.png")
test_img.save(target_path)
print("Saved test_img.png:", target_path)
print("Exists:", os.path.exists(target_path))
print("Outputs contents:", os.listdir(output_dir))
