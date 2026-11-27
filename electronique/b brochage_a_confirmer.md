# Brochage à confirmer avant câblage final

Ce fichier est volontairement une fiche de validation. Les GPIO proposés ci-dessous sont ceux retenus pour le prototype.

| Fonction | Composant | Broche ESP32 | Validation |
|---|---|---:|---|
| SDA | PCA9685 | GPIO21 | À tester |
| SCL | PCA9685 | GPIO22 | À tester |
| DT | HX711 | GPIO19 | À tester |
| SCK | HX711 | GPIO18 | À tester |
| Présence | IR | GPIO27 | À tester |
| TRIG | HC-SR04 | GPIO5 | À tester |
| ECHO | HC-SR04 | GPIO34 | À tester + diviseur si nécessaire |
| LED R | RGB | GPIO25 | À tester |
| LED G | RGB | GPIO26 | À tester |
| LED B | RGB | GPIO33 | À tester |
| Buzzer | Buzzer | GPIO23 | À tester |
| STOP logiciel | Bouton | GPIO4 | À tester |

## PCA9685
- CH0 : Base
- CH1 : Épaule
- CH2 : Coude
- CH3 : Pince
- Adresse I²C attendue par défaut : 0x40, à confirmer par scanner I²C.

## Important
Avant de valider le tableau, relever les références exactes des cartes et servomoteurs réellement disponibles.
