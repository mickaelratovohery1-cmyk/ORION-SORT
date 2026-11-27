
from collections import deque
from pathlib import Path
import argparse

import cv2
import numpy as np
import tensorflow as tf


# ==========================================
# CONFIGURATION ORION-SORT V2
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "models" / "orion_sort_v2.keras"

CLASS_NAMES = [
    "cardboard",
    "metal",
    "paper",
    "plastic",
    "unknown"
]

IMAGE_SIZE = (160, 160)

CONFIDENCE_THRESHOLD = 0.60
ANALYSIS_INTERVAL = 10


# ==========================================
# CHARGEMENT DU MODELE
# ==========================================

print("Chargement du modele ORION-SORT V2...")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Modele introuvable : {MODEL_PATH}"
    )

model = tf.keras.models.load_model(MODEL_PATH)

print("Modele V2 charge avec succes !")


# ==========================================
# ANALYSE D'UNE IMAGE
# ==========================================

def analyze_image(image):

    # Conversion BGR vers RGB
    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    # Redimensionnement
    image = cv2.resize(
        image,
        IMAGE_SIZE
    )

    # IMPORTANT :
    # MobileNetV2 possède déjà sa normalisation
    # intégrée dans le nouveau modèle.
    # Ne pas diviser par 255 ici.

    image = image.astype("float32")

    image = np.expand_dims(
        image,
        axis=0
    )

    predictions = model.predict(
        image,
        verbose=0
    )[0]

    index = int(np.argmax(predictions))

    category = CLASS_NAMES[index]

    confidence = float(predictions[index]) * 100

    return category, confidence, predictions


# ==========================================
# ANALYSE D'UNE PHOTO
# ==========================================

def predict_photo(path):

    image = cv2.imread(str(path))

    if image is None:
        print("Impossible de lire cette image.")
        return

    category, confidence, predictions = analyze_image(image)

    print("\n===== ORION-SORT V2 : ANALYSE PHOTO =====")

    print("Image :", path.name)
    print("Categorie :", category)
    print("Confiance :", round(confidence, 2), "%")

    print("\nToutes les categories :")

    for name, score in zip(CLASS_NAMES, predictions):
        print(f"{name:12s} : {score * 100:.2f} %")

    if confidence < CONFIDENCE_THRESHOLD * 100:
        label = f"unknown - incertain ({confidence:.1f}%)"
    else:
        label = f"{category} - {confidence:.1f}%"

    cv2.putText(
        image,
        label,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 200, 0),
        2
    )

    cv2.imshow(
        "ORION-SORT V2 - Analyse photo",
        image
    )

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ==========================================
# RECONNAISSANCE PAR CAMERA
# ==========================================

def run_camera():

    print("\n===== ORION-SORT V2 : CAMERA EN DIRECT =====")
    print("Place un seul objet au centre de la camera.")
    print("Appuie sur Q pour quitter.")

    camera = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    if not camera.isOpened():
        print("ERREUR : impossible d'ouvrir la camera.")
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    prediction_history = deque(maxlen=5)

    frame_count = 0

    last_label = "Analyse en cours..."
    last_confidence = 0.0
    last_status = "Place un objet au centre"

    try:

        while True:

            success, frame = camera.read()

            if not success:
                print("Erreur de lecture de la camera.")
                break

            height, width = frame.shape[:2]

            # Zone centrale de reconnaissance
            x1 = int(width * 0.15)
            x2 = int(width * 0.85)

            y1 = int(height * 0.15)
            y2 = int(height * 0.85)

            roi = frame[y1:y2, x1:x2]

            frame_count += 1

            if frame_count % ANALYSIS_INTERVAL == 0:

                gray = cv2.cvtColor(
                    roi,
                    cv2.COLOR_BGR2GRAY
                )

                brightness = gray.mean()

                sharpness = cv2.Laplacian(
                    gray,
                    cv2.CV_64F
                ).var()

                if brightness < 35:

                    last_status = "Image trop sombre"

                    prediction_history.clear()

                elif sharpness < 30:

                    last_status = "Image trop floue"

                    prediction_history.clear()

                else:

                    try:

                        _, _, probabilities = analyze_image(roi)

                        prediction_history.append(probabilities)

                        average_probabilities = np.mean(
                            np.array(prediction_history),
                            axis=0
                        )

                        best_index = int(
                            np.argmax(average_probabilities)
                        )

                        last_confidence = float(
                            average_probabilities[best_index]
                        )

                        if last_confidence >= CONFIDENCE_THRESHOLD:

                            last_label = CLASS_NAMES[best_index]

                            last_status = "Objet reconnu"

                        else:

                            last_label = "unknown"

                            last_status = "Reconnaissance incertaine"

                    except Exception as error:

                        last_status = "Erreur de prediction"
                        print("Erreur :", error)

            # Cadre de reconnaissance
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 255),
                2
            )

            # Categorie
            cv2.putText(
                frame,
                "Objet : " + last_label,
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            # Confiance
            cv2.putText(
                frame,
                f"Confiance : {last_confidence * 100:.1f}%",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # Statut
            cv2.putText(
                frame,
                last_status,
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

            cv2.imshow(
                "ORION-SORT V2 - Reconnaissance IA",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        camera.release()
        cv2.destroyAllWindows()

        print("Camera arretee.")


# ==========================================
# PROGRAMME PRINCIPAL
# ==========================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="ORION-SORT V2 - Reconnaissance des dechets"
    )

    parser.add_argument(
        "image",
        nargs="?",
        help="Chemin de l'image a analyser"
    )

    parser.add_argument(
        "--camera",
        action="store_true",
        help="Lancer la reconnaissance par camera"
    )

    args = parser.parse_args()

    if args.camera:
        run_camera()

    elif args.image:
        predict_photo(Path(args.image))

    else:
        parser.print_help()
