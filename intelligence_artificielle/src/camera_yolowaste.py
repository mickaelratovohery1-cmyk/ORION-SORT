import cv2
from ultralytics import YOLO

# Charger TON modèle entraîné (pas le pré-entraîné yolov8n.pt)
model = YOLO('models/yolowaste_best.pt')  # ou le chemin de ton nouveau best.pt

# Simulation de la lecture de la balance (à remplacer par la lecture série de l'ESP32)
def lire_poids():
    # Ici tu mettras ton code pour lire le HX711 via l'ESP32
    # Exemple : return 25.5 (grammes)
    return 50.0 

def analyser_objet(image_path):
    # 1. Prédiction YOLO
    results = model(image_path)
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Récupérer la classe et la confiance
            cls_id = int(box.cls[0])
            confiance = float(box.conf[0])
            classe_nom = model.names[cls_id]
            
            # Récupérer le poids
            poids = lire_poids()
            
            # --- LOGIQUE DE DECISION (Cahier des charges) ---
            decision_finale = classe_nom
            
            # Règle 1 : Confiance faible -> On demande à l'utilisateur
            if confiance < 0.60:
                decision_finale = "Incertain"
            
            # Règle 2 : Combinaison Image + Poids
            elif classe_nom == "plastic":
                # Une bouteille plastique vide pèse < 30g
                # Si c'est plus lourd, c'est une bouteille pleine (à rejeter)
                if poids > 100: 
                    decision_finale = "Rejet (Bouteille pleine)"
            
            elif classe_nom == "metal":
                # Une canette vide pèse ~15g, une boîte de conserve ~400g
                # L'IA peut confondre l'alu avec du papier, le poids aide
                if poids < 5: 
                    decision_finale = "Incertain"
            
            print(f"Objet: {classe_nom} | Confiance: {confiance:.2f} | Poids: {poids}g | Décision: {decision_finale}")
            
            # Ici, tu envoies 'decision_finale' à ton serveur Flask/ESP32 pour bouger le bras

# Test avec une image
analyser_objet('test/cardboard/cardboard1.jpg')