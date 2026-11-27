import cv2
from ultralytics import YOLO
import requests
import time
import random

# --- CONFIGURATION ---
# Chemin vers ton modèle (adapte selon où tu es)
MODEL_PATH = '../runs/classify/orion_classify/weights/best.pt' 

# URL de ton serveur Flask
API_URL = "http://127.0.0.1:5000/api/detection"

# Charger le modèle
model = YOLO(MODEL_PATH)

# Ouvrir la caméra
cap = cv2.VideoCapture(0)

print("Démarrage de la caméra IA. Appuie sur 'q' pour quitter.")

# Variable pour éviter d'envoyer 30 requêtes par seconde au serveur
last_sent_time = 0
SEND_INTERVAL = 2.0  # Envoyer une détection toutes les 2 secondes max

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Prédiction
    results = model(frame, verbose=False)
    
    if results[0].probs is not None:
        top1 = results[0].probs.top1
        conf = results[0].probs.top1conf.item()
        classe = model.names[top1]
        
        # 2. Simulation du poids (à remplacer par la vraie lecture de l'ESP32)
        # Pour tester, on met un poids aléatoire
        poids_simule = random.uniform(5, 400)
        
        # 3. Affichage sur l'image (pour toi, en local)
        texte = f"{classe} ({conf:.2f}) - {poids_simule:.0f}g"
        cv2.putText(frame, texte, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 4. Envoi au serveur web (toutes les 2 secondes)
        current_time = time.time()
        if current_time - last_sent_time > SEND_INTERVAL:
            # On n'envoie que si la confiance est suffisante (ex: > 60%)
            if conf > 0.60: 
                payload = {
                    "category": classe,
                    "weight_g": round(poids_simule, 1),
                    "confidence": round(conf, 2)
                }
                
                try:
                    response = requests.post(API_URL, json=payload)
                    if response.status_code == 201:
                        print(f"✅ Envoyé : {classe} | {poids_simule:.0f}g | Confiance: {conf:.2f}")
                    else:
                        print(f"⚠️ Erreur serveur : {response.status_code}")
                except requests.exceptions.ConnectionError:
                    print("❌ Impossible de joindre le serveur Flask. Est-il lancé ?")
                
                last_sent_time = current_time

    # Afficher la vidéo
    cv2.imshow('ORION-Sort - IA Camera', frame)

    # Quitter avec 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()