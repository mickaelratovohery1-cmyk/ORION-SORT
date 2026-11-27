
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = BASE_DIR / "dataset" / "raw"

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

invalid_images = []
valid_count = 0

print("\n===== ORION-SORT : VERIFICATION DES IMAGES =====")

for category in sorted(DATASET_DIR.iterdir()):
    if not category.is_dir():
        continue

    for image_path in category.iterdir():
        if image_path.suffix.lower() not in EXTENSIONS:
            continue

        try:
            with Image.open(image_path) as img:
                img.load()
            valid_count += 1

        except Exception as error:
            invalid_images.append(image_path)
            print("\nIMAGE INVALIDE :", image_path)
            print("Erreur :", error)

print("\n========== RESULTAT ==========")
print("Images valides :", valid_count)
print("Images invalides :", len(invalid_images))

if not invalid_images:
    print("Toutes les images sont lisibles !")
