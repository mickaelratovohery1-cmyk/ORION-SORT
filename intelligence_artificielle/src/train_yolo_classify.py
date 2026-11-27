from ultralytics import YOLO

# On charge un modèle de classification (pas de détection)
model = YOLO('yolov8n-cls.pt') 

# On pointe directement vers le dossier raw (qui contient les dossiers par classe)
results = model.train(
    data='../dataset/raw',  # YOLO va lire les sous-dossiers comme des classes
    epochs=50,
    imgsz=224,
    batch=16,
    name='orion_classify'
)