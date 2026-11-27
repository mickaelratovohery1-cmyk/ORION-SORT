
from pathlib import Path
import tensorflow as tf

# Configuration du dataset
BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = BASE_DIR / "dataset" / "raw"

IMAGE_SIZE = (160, 160)
BATCH_SIZE = 16
SEED = 42

print("\n===== ORION-SORT : PRÉPARATION DES IMAGES =====")

# Vérifier le dossier
if not DATASET_DIR.exists():
    raise FileNotFoundError(
        f"Dataset introuvable : {DATASET_DIR}"
    )

# Charger les images d'entraînement (80 %)
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

# Charger les images de validation (20 %)
val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

# Récupérer les noms des catégories
class_names = train_ds.class_names

# Normaliser les pixels entre 0 et 1
normalization = lambda images, labels: (
    tf.cast(images, tf.float32) / 255.0,
    labels
)

train_ds = train_ds.map(normalization)
val_ds = val_ds.map(normalization)

# Préparer les chargements
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)

# Afficher le résultat
print("\n===== RÉSULTAT =====")
print("Catégories :", class_names)
print("Taille des images :", IMAGE_SIZE)
print("Taille des lots :", BATCH_SIZE)
print("Entraînement : 80 %")
print("Validation : 20 %")

for images, labels in train_ds.take(1):
    print("Forme des images :", images.shape)
    print("Forme des étiquettes :", labels.shape)
    print("Valeur minimale des pixels :", float(tf.reduce_min(images)))
    print("Valeur maximale des pixels :", float(tf.reduce_max(images)))

print("\nPréparation terminée !")
