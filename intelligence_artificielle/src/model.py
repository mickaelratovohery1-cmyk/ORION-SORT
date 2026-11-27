
import tensorflow as tf
from tensorflow.keras import layers, models

def create_model(num_classes=5):

    model = models.Sequential([
        layers.Input(shape=(160, 160, 3)),

        # Première extraction de caractéristiques
        layers.Conv2D(32, (3, 3), activation="relu"),
        layers.MaxPooling2D((2, 2)),

        # Deuxième extraction
        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.MaxPooling2D((2, 2)),

        # Troisième extraction
        layers.Conv2D(128, (3, 3), activation="relu"),
        layers.MaxPooling2D((2, 2)),

        # Classification
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    model = create_model()

    print("\n===== ORION-SORT : ARCHITECTURE IA =====")
    model.summary()
