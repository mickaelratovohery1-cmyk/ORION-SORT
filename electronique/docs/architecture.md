# Architecture électronique

## Architecture globale

```text
PC/Raspberry Pi
  IA + Web + Base de données
          |
        Wi-Fi
          |
        ESP32
   _______|________________________
  |       |       |       |       |
 PCA9685 HX711    IR    HC-SR04  I/O
  |
  +-- Servo Base
  +-- Servo Épaule
  +-- Servo Coude
  +-- Servo Pince

HX711 --> Cellule de charge
ESP32 --> LED / Buzzer / STOP
```

Le cahier des charges précise que l'ESP32 gère les capteurs et actionneurs en temps réel tandis que l'ordinateur ou Raspberry Pi héberge l'IA, le serveur web et la base de données. La communication se fait sur le réseau Wi-Fi local.
