import os

outputs_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design\outputs"
os.makedirs(outputs_dir, exist_ok=True)
test_file = os.path.join(outputs_dir, "test.txt")

try:
    with open(test_file, 'w') as f:
        f.write("hello")
    print("File created successfully:", test_file)
    print("Exists:", os.path.exists(test_file))
    print("Folder exists:", os.path.exists(outputs_dir))
    print("Folder contents:", os.listdir(outputs_dir))
except Exception as e:
    print("Error:", e)
