
from pathlib import Path
import tensorflow as tf

from prepare_dataset import (
    train_ds,
    val_ds,
    class_names
)

from model import create_model

# Dossier de sauvegarde
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "orion_sort.keras"

print("\n===== ORION-SORT : ENTRAINEMENT IA =====")

# Création du modèle
model = create_model(num_classes=len(class_names))

# Paramètres
EPOCHS = 10

# Entraînement
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)

# Sauvegarde
model.save(MODEL_PATH)

print("\n===== ENTRAINEMENT TERMINE =====")
print("Catégories :", class_names)
print("Modèle sauvegardé :", MODEL_PATH)
print("Précision finale entraînement :",
      round(history.history["accuracy"][-1] * 100, 2), "%")
print("Précision finale validation :",
      round(history.history["val_accuracy"][-1] * 100, 2), "%")
