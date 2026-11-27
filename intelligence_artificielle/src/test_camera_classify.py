import cv2
from ultralytics import YOLO

# 1. Charger ton modèle (attention au chemin, on est dans src)
# Si tu utilises le modèle de l'entraînement local :
model = YOLO('../runs/classify/orion_classify/weights/best.pt') 
# Si tu as téléchargé le modèle de Colab, remplace par :
# model = YOLO('../models/orion_sort_classify_best.pt')

# 2. Ouvrir la webcam (0 = webcam par défaut)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la caméra.")
    exit()

print("Appuie sur 'q' pour quitter.")

while True:
    # Lire une image de la caméra
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Faire la prédiction sur l'image
    # verbose=False évite d'afficher du texte dans le terminal à chaque frame
    results = model(frame, verbose=False)

    # 4. Récupérer le résultat
    if results[0].probs is not None:
        top1 = results[0].probs.top1
        conf = results[0].probs.top1conf.item()
        classe = model.names[top1]

        # 5. Dessiner le texte sur l'image
        texte = f"{classe} ({conf:.2f})"
        
        # Changer la couleur selon la classe (pour faire joli sur la vidéo)
        couleur = (0, 255, 0) # Vert par défaut
        if conf < 0.60:
            couleur = (0, 0, 255) # Rouge si l'IA n'est pas sûre

        cv2.putText(frame, texte, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, couleur, 2)
        
        # Optionnel : Afficher toutes les probabilités en petit
        probs = results[0].probs.data
        for i, p in enumerate(probs):
            nom = model.names[i]
            cv2.putText(frame, f"{nom}: {p:.2f}", (20, 90 + i*30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # 6. Afficher l'image
    cv2.imshow('ORION-Sort - Test Camera', frame)

    # 7. Quitter avec 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra
cap.release()
cv2.destroyAllWindows()