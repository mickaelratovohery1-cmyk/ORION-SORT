from ultralytics import YOLO

# 1. Charger un modèle pré-entraîné (YOLOv8n est rapide, YOLOv8s est plus précis)
# On utilise le modèle "nano" pour que ça tourne vite sur Raspberry Pi
model = YOLO('yolov8n.pt') 

# 2. Entraîner le modèle
results = model.train(
    data='data.yaml',      # Le fichier de configuration
    epochs=50,             # 50 epochs suffisent généralement (regarde si la loss stagne)
    imgsz=640,             # Taille des images (standard pour YOLO)
    batch=16,              # Réduis à 8 si tu as une petite carte graphique
    name='orion_sort_v3',  # Le nom de ton nouveau modèle
    patience=10            # Arrête si pas d'amélioration pendant 10 epochs
)

# 3. Sauvegarder le meilleur modèle
# Il sera dans runs/detect/orion_sort_v3/weights/best.pt