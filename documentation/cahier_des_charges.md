# Cahier des charges — ORION-Sort
**ORION TECH V2 — ORION UNIVERSITY | Thème B | Version préparatoire 0.1**

## 1. Présentation
ORION-Sort est un système de tri qui utilise un bras robotique à quatre axes, une caméra, une intelligence artificielle et une mesure de poids pour classer et déplacer des déchets.

## 2. Objectif général
Réaliser un prototype capable de reconnaître un objet, mesurer sa masse, le saisir et le déposer dans le bac correspondant.

## 3. Classes à reconnaître
- Plastique
- Métal
- Papier
- Carton
- Inconnu / absence d'objet

Le système doit rejeter une prédiction lorsque la confiance est insuffisante. Le seuil sera fixé après les essais.

## 4. Fonctionnement
1. L'objet est placé dans la zone de détection.
2. Le capteur détecte sa présence.
3. La caméra capture une image.
4. Le modèle IA prédit la catégorie et la confiance.
5. La balance mesure la masse après stabilisation.
6. Le programme choisit la destination.
7. Le bras approche et saisit l'objet.
8. Le bras le dépose dans le bac choisi.
9. Le bras revient en position d'attente.
10. L'opération est enregistrée et affichée sur le tableau de bord.

## 5. Matériel envisagé
- ESP32
- PCA9685
- Servomoteurs pour les articulations et la pince
- Cellule de charge et HX711
- Capteur de présence IR ou ultrasonique
- Caméra USB ou caméra compatible avec l'ordinateur hôte
- Alimentation externe adaptée aux servomoteurs
- Arrêt d'urgence et protections mécaniques

Le nombre exact, les modèles et les dimensions doivent être confirmés. Le sujet prévoit un bras 4 axes ; vérifier la configuration réelle des actionneurs avant achat ou câblage.

## 6. Logiciels envisagés
- C/C++ pour le firmware ESP32
- Python et OpenCV pour le traitement d'image
- TensorFlow/Keras pour le modèle IA
- Flask pour l'application web
- SQLite pour l'historique du prototype
- Communication locale Wi-Fi via HTTP ou MQTT, à décider avec l'équipe

## 7. Fonctions web attendues
- État de connexion du contrôleur
- Image analysée, classe prédite et confiance
- Poids mesuré et destination
- Historique des opérations
- Statistiques par matière et masse cumulée
- Commande manuelle des articulations en mode maintenance
- Arrêt d'urgence logique, en complément d'un arrêt matériel

## 8. Sécurité
- Ne jamais alimenter les servos depuis la sortie 3,3 V de l'ESP32.
- Dimensionner l'alimentation selon le courant de pointe des servos.
- Vérifier les tensions, polarités et masses avant branchement.
- Tester d'abord sans charge et à vitesse réduite.
- Protéger les zones de pincement et dégager la zone de mouvement.
- En cas de perte de communication ou d'erreur, passer à un état sûr.
- Ne jamais laisser le bras fonctionner sans surveillance.
- L'arrêt logiciel ne remplace pas un arrêt d'urgence physique.

## 9. Critères de validation
- Reconnaissance des quatre catégories et rejet des objets incertains.
- Mesure de poids calibrée avec des masses de référence.
- Saisie et dépôt sans chute ni collision.
- Enregistrement de chaque opération.
- Tableau de bord affichant les informations attendues.
- Tests documentés avec résultats réels.

## 10. Livrables
Cahier des charges, architecture, schéma électronique, firmware ESP32, calculs de cinématique, dataset original, rapport d'évaluation IA, application web, protocole de test et rapport final.

## 11. Points à confirmer
Dimensions du bras, références des servos, caméra, ordinateur hôte, protocole de communication, position des bacs, seuil IA, charge utile et calendrier final.
