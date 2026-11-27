from ultralytics import YOLO

# 1. Charger un modèle pré-entraîné (YOLOv8 nano est rapide, 's' est plus précis)
model = YOLO('yolov8n.pt') 

# 2. Lancer l'entraînement avec AUGMENTATION FORTE
# C'est ici que la magie opère pour ne pas confondre les couleurs
results = model.train(
    data='data.yaml',      # Le fichier qu'on vient de créer
    epochs=100,            # 100 epochs pour bien apprendre (tu peux réduire si ça prend trop de temps)
    imgsz=640,             # Taille standard
    batch=16,              # Réduis à 8 si tu as une petite carte graphique
    
    # --- PARAMÈTRES D'AUGMENTATION (Le secret) ---
    hsv_h=0.015,           # Variation de la teinte (couleur) -> Aide à ignorer la couleur
    hsv_s=0.7,             # Variation de la saturation -> Crucial pour ne pas confondre blanc/gris
    hsv_v=0.4,             # Variation de la luminosité (clair/sombre)
    degrees=15.0,          # Rotation aléatoire (l'objet peut être penché)
    translate=0.1,         # Décalage (l'objet n'est pas toujours au centre)
    scale=0.5,             # Zoom avant/arrière
    fliplr=0.5,            # Miroir horizontal (50% de chance)
    mosaic=1.0,            # Mélange 4 images en une -> Apprend le contexte
    mixup=0.1,             # Superposition d'images -> Apprend la texture
    # ----------------------------------------------
    
    name='orion_sort_v3_augmented'  # Le nom de ton nouveau modèle
)

print("Entraînement terminé ! Le modèle est dans runs/detect/orion_sort_v3_augmented/weights/best.pt")