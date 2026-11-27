from ultralytics import YOLO
import os

# 1. Charger TON modèle (remplace le nom par le tien)
# Attention au chemin : on est dans src, donc on remonte d'un cran pour aller dans models
model = YOLO('../models/orion_sort_classify_best.pt') 

# 2. Choisir une image de test (prends une image dans ton dossier test/)
image_test = '../dataset/raw/cardboard/cardboard_cardboard1.jpg' # Modifie le nom

# 3. Prédire
results = model(image_test)

# 4. Afficher le résultat
for r in results:
    # YOLO classify renvoie les probabilités pour chaque classe
    probs = r.probs
    top1 = probs.top1
    top1_conf = probs.top1conf
    class_name = model.names[top1]
    
    print(f"Image : {image_test}")
    print(f"Prédiction : {class_name} (Confiance : {top1_conf:.2f})")
    
    # Afficher toutes les probabilités (utile pour le jury)
    print("\nDétail des probabilités :")
    for i, prob in enumerate(probs.data):
        print(f"  {model.names[i]} : {prob:.4f}")