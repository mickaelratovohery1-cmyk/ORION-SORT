
from pathlib import Path
import numpy as np
import tensorflow as tf
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import confusion_matrix, classification_report

# ==========================================
# CONFIGURATION ORION-SORT V2
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = BASE_DIR / "dataset" / "raw"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "orion_sort_v2.keras"

IMAGE_SIZE = (160, 160)
BATCH_SIZE = 16
SEED = 42

print("\n===== ORION-SORT : ENTRAINEMENT AMELIORE =====")

# ==========================================
# 1. CHARGEMENT DU DATASET
# ==========================================

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

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

class_names = train_ds.class_names
number_classes = len(class_names)

print("\nClasses :", class_names)
print("Nombre de classes :", number_classes)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)

# ==========================================
# 2. EQUILIBRAGE DES CLASSES
# ==========================================

all_labels = np.concatenate([
    labels.numpy() for _, labels in train_ds
])

weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(all_labels),
    y=all_labels
)

class_weights = {
    int(class_id): float(weight)
    for class_id, weight in zip(np.unique(all_labels), weights)
}

print("\nPoids des classes :", class_weights)

# ==========================================
# 3. AUGMENTATION DES IMAGES
# ==========================================

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.10),
    tf.keras.layers.RandomZoom(0.15),
    tf.keras.layers.RandomContrast(0.15)
], name="augmentation")

# ==========================================
# 4. MOBILE NET V2 PRE-ENTRAINE
# ==========================================

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(160, 160, 3),
    include_top=False,
    weights="imagenet"
)

# Première phase : on conserve les poids pré-entraînés.
base_model.trainable = False

inputs = tf.keras.Input(shape=(160, 160, 3))

x = data_augmentation(inputs)

# Les images passent de [0, 255] à [-1, 1],
# format attendu par MobileNetV2.
x = tf.keras.layers.Rescaling(
    scale=1.0 / 127.5,
    offset=-1
)(x)

x = base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.35)(x)
outputs = tf.keras.layers.Dense(
    number_classes,
    activation="softmax"
)(x)

model = tf.keras.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ==========================================
# 5. SAUVEGARDE DU MEILLEUR MODELE
# ==========================================

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath=MODEL_PATH,
    monitor="val_accuracy",
    save_best_only=True,
    mode="max",
    verbose=1
)

early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)

# ==========================================
# 6. PREMIER ENTRAINEMENT
# ==========================================

print("\n===== PHASE 1 : APPRENTISSAGE =====")

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10,
    class_weight=class_weights,
    callbacks=[checkpoint, early_stop]
)

# ==========================================
# 7. AFFINAGE DU MODELE
# ==========================================

print("\n===== PHASE 2 : AFFINAGE =====")

base_model.trainable = True

# On ne débloque que les 30 dernières couches.
for layer in base_model.layers[:-30]:
    layer.trainable = False

# On garde les couches BatchNormalization gelées.
for layer in base_model.layers:
    if isinstance(layer, tf.keras.layers.BatchNormalization):
        layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

checkpoint_finetune = tf.keras.callbacks.ModelCheckpoint(
    filepath=MODEL_PATH,
    monitor="val_accuracy",
    save_best_only=True,
    mode="max",
    verbose=1
)

early_stop_finetune = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=5,
    class_weight=class_weights,
    callbacks=[checkpoint_finetune, early_stop_finetune]
)

# ==========================================
# 8. EVALUATION FINALE
# ==========================================

print("\n===== EVALUATION DU MODELE =====")

best_model = tf.keras.models.load_model(MODEL_PATH)

loss, accuracy = best_model.evaluate(val_ds, verbose=1)

print(f"\nPrécision validation : {accuracy * 100:.2f}%")
print(f"Perte validation : {loss:.4f}")

# Prédictions sur les images de validation.
y_true = np.concatenate([
    labels.numpy() for _, labels in val_ds
])

predictions = best_model.predict(val_ds, verbose=1)
y_pred = np.argmax(predictions, axis=1)

print("\n===== MATRICE DE CONFUSION =====")
print(confusion_matrix(y_true, y_pred))

print("\n===== RAPPORT DE CLASSIFICATION =====")
print(classification_report(
    y_true,
    y_pred,
    target_names=class_names,
    zero_division=0
))

print("\n===== ENTRAINEMENT TERMINE =====")
print("Nouveau modèle :", MODEL_PATH)
print(f"Taille du modèle : {MODEL_PATH.stat().st_size / (1024 * 1024):.2f} Mo")
