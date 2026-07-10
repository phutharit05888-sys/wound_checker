from PIL import Image
import os

# Folder to scan
folder = "Train_Data"

corrupted = []

# Scan all files
for root, dirs, files in os.walk(folder):

    for file in files:

        path = os.path.join(root, file)

        try:
            img = Image.open(path)
            img.verify()

        except Exception:
            corrupted.append(path)

# Print results
print("\nCorrupted Images:\n")

for img in corrupted:
    print(img)

print(f"\nTotal corrupted images: {len(corrupted)}")