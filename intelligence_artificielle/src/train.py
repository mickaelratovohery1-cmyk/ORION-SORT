
from pathlib import Path

DATASET = Path(__file__).resolve().parents[1] / "dataset" / "raw"

CLASSES = ["plastic", "metal", "paper", "cardboard", "unknown"]

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def main():
    missing = [
        name for name in CLASSES
        if not (DATASET / name).is_dir()
    ]

    if missing:
        raise SystemExit(f"Dossiers manquants : {missing}")

    print("\n===== ORION-SORT : CONTRÔLE DU DATASET =====\n")

    total = 0

    for name in CLASSES:
        folder = DATASET / name

        images = [
            file for file in folder.iterdir()
            if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
        ]

        count = len(images)
        total += count

        print(f"{name:<12} : {count} image(s)")

    print("\n-------------------------------------------")
    print(f"TOTAL        : {total} image(s)")
    print("-------------------------------------------")

    if total == 0:
        print("Aucune image trouvée. Ajoutez des images au dataset.")
    else:
        print("Dataset détecté. Prochaine étape : préparer les images.")


if __name__ == "__main__":
    main()
