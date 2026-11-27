# Intelligence Artificielle - ORION-Sort

## Responsable : Alphonse (avec assistance de Mickael)

### 1. Objectif
Reconnaître la matière des déchets (carton, métal, papier, plastique, inconnu) à partir d'une image.

### 2. Technologies utilisées
- **Python 3.9**
- **YOLOv8** (Ultralytics) pour la classification d'images.
- **OpenCV** pour la capture vidéo en temps réel.
- **Dataset** : 2026 images réparties en 5 classes.

### 3. Structure du Dataset
- `dataset/raw/` : Images brutes classées par dossiers.
- Entraînement : 80% des images (1619 images).
- Validation : 20% des images (407 images).

### 4. Entraînement
Le modèle a été entraîné avec les paramètres suivants :
- **Modèle** : YOLOv8n-cls (version nano, légère pour Raspberry Pi).
- **Epochs** : 50.
- **Augmentation** : HSV (variation de couleur), rotation, zoom.
- **Précision (Top-1 Accuracy)** : ~93% sur le jeu de validation.

### 5. Évaluation
- **Matrice de confusion** : `runs/classify/orion_classify/confusion_matrix.png`
- **Courbes d'entraînement** : `runs/classify/orion_classify/results.png`

### 6. Utilisation
- **Test sur image** : `python src/test_classify.py`
- **Test caméra temps réel** : `python src/camera_ai.py`
- **API vers serveur Web** : Le script `camera_ai.py` envoie les prédictions à `http://127.0.0.1:5000/api/detection`.