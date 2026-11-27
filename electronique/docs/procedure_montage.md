# Procédure de montage — Jean-Luc

## Phase 0 — préparation
1. Relever la référence exacte de chaque composant.
2. Photographier chaque composant.
3. Vérifier les tensions indiquées sur les cartes.
4. Préparer le multimètre.
5. Ne pas connecter les servos au premier test.

## Phase 1 — ESP32
1. Connecter l'ESP32 au PC par USB.
2. Téléverser `micrologiciel/test_esp32_i2c.ino`.
3. Ouvrir le moniteur série à 115200 bauds.

## Phase 2 — PCA9685
1. ESP32 GPIO21 → SDA.
2. ESP32 GPIO22 → SCL.
3. GND ESP32 → GND logique PCA9685.
4. VCC logique → tension conforme au module.
5. Alimenter la partie servo avec la source prévue.
6. Lancer le scanner I²C.
7. Vérifier l'adresse détectée.

## Phase 3 — un seul servo
1. Couper l'alimentation.
2. Brancher un seul servo sur CH0.
3. Vérifier signal, +V et GND.
4. Remettre sous tension.
5. Tester un mouvement très faible.
6. Arrêter immédiatement en cas de bruit anormal, échauffement ou chute de tension.

## Phase 4 — quatre servos
Ajouter les servos un par un et mesurer le comportement de l'alimentation.

## Phase 5 — HX711
1. Brancher le HX711.
2. Vérifier la détection.
3. Lire la valeur brute.
4. Faire la tare.
5. Calibrer avec un poids connu.
6. Refaire la mesure avec au moins un autre poids.

## Phase 6 — capteurs
Tester séparément IR puis HC-SR04.

## Phase 7 — signaux
Tester LED, buzzer et bouton STOP logiciel.

## Phase 8 — intégration
Assembler les sous-systèmes uniquement après validation individuelle.
