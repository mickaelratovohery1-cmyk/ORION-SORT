
from pathlib import Path
import argparse

from ultralytics import YOLO

# Chemins du projet
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "yolowaste_best.pt"
DATASET_DIR = BASE_DIR / "dataset" / "raw"
RESULTS_DIR = BASE_DIR / "results"

# Extensions d'images acceptées
EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def main():
    parser = argparse.ArgumentParser(
        description="Tester YOLOWaste sur une image"
    )
    parser.add_argument(
        "--image",
        type=str,
        help="Chemin de l'image à analyser"
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Seuil de confiance (défaut : 0.25)"
    )
    args = parser.parse_args()

    # Vérifier le modèle
    if not MODEL_PATH.exists():
        print("ERREUR : modèle introuvable :", MODEL_PATH)
        return

    # Choisir l'image
    if args.image:
        image_path = Path(args.image)
    else:
        images = [
            p for p in DATASET_DIR.rglob("*")
            if p.is_file() and p.suffix.lower() in EXTENSIONS
        ]

        if not images:
            print("Aucune image trouvée dans le dataset.")
            return

        image_path = images[0]
        print("Image choisie automatiquement :", image_path)

    if not image_path.is_file():
        print("ERREUR : image introuvable :", image_path)
        return

    # Charger le modèle
    print("\nChargement de YOLOWaste...")
    model = YOLO(str(MODEL_PATH))

    print("Modèle chargé :", model.names)
    print("\nAnalyse de l'image...")

    # Effectuer la détection
    results = model.predict(
        source=str(image_path),
        imgsz=640,
        conf=args.conf,
        device="cpu",
        save=True,
        project=str(RESULTS_DIR),
        name="test_yolowaste",
        exist_ok=True,
        verbose=False
    )

    # Afficher les résultats
    for result in results:
        if result.boxes is None or len(result.boxes) == 0:
            print("\nAucun objet détecté.")
            continue

        print("\n===== RESULTATS YOLOWASTE =====")

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())

            class_name = model.names[class_id]

            print(
                f"Objet : {class_name} | "
                f"Confiance : {confidence * 100:.2f}%"
            )

        print("\nImage annotée enregistrée.")

    print("Dossier des résultats :", RESULTS_DIR / "test_yolowaste")


if __name__ == "__main__":
    main()
