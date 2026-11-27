# Partie électronique — rapport

## 1. Mission
Jean-Luc est responsable de l'étude et de l'intégration électronique du système ORION-SORT.

## 2. Choix d'architecture
L'ESP32 constitue le contrôleur temps réel. Le PCA9685 permet de commander les servomoteurs via I²C. Les mesures de poids utilisent une cellule de charge associée au HX711. La présence et la distance sont mesurées par des capteurs dédiés.

## 3. Alimentation
La puissance des servomoteurs est séparée de la logique. Le dimensionnement final doit être justifié à partir des fiches techniques des servos réellement utilisés.

## 4. Validation
Chaque sous-système est testé séparément avant intégration : ESP32, I²C, servos, HX711, présence, distance, LED, buzzer et STOP.

## 5. Preuves
Ajouter ici les photos réelles du montage, les mesures au multimètre, les captures du moniteur série et le schéma KiCad/Fritzing final.
