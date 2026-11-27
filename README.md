# ORION TECH V2 — ORION-Sort
Projet ORION UNIVERSITY, thème B : bras robotique intelligent de tri des déchets.

## Objectif
Reconnaître, peser, saisir et trier des objets dans les bacs Plastique, Métal, Papier, Carton ou Inconnu.

## Équipe
- Mickael : chef de projet, coordination, intégration et web
- Jean-Luc : électronique et ESP32
- Faneva : mécanique, robotique et cinématique
- Alphonse : intelligence artificielle et dataset

## Architecture prévue
- ESP32 : capteurs et actionneurs
- PCA9685 : commande PWM des servomoteurs
- Cellule de charge + HX711 : mesure du poids
- Caméra + Python/OpenCV/TensorFlow : reconnaissance
- Flask + SQLite : tableau de bord et historique

## Dossiers
`documentation/`, `electronique/`, `robotique/`, `intelligence_artificielle/`, `web/`, `tests/`.

## Important
Ce dépôt est un dossier préparatoire. Aucun branchement ou test physique n'a été effectué. Les références, broches, dimensions, limites et calibrations doivent être confirmées avec le matériel réel. Les données affichées par l'application web sont des données de démonstration.
