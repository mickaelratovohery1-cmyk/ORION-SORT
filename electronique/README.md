# Électronique — Responsable : Jean-Luc

Composants envisagés : ESP32, PCA9685, servomoteurs, pince, cellule de charge + HX711, capteur de présence, alimentation servo dédiée, fusible et arrêt d'urgence.

À faire :
1. Confirmer les références exactes.
2. Lire les fiches techniques.
3. Calculer courant nominal et courant de pointe.
4. Dessiner le schéma.
5. Définir le brochage après choix de la carte.
6. Tester chaque module séparément.

**Sécurité :** ne pas alimenter les servos depuis le 3,3 V de l'ESP32. Dimensionner une alimentation externe adaptée et vérifier les branchements avant mise sous tension.
