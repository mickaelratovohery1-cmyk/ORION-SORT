# Schéma fonctionnel préliminaire
Ce n'est pas encore un schéma de câblage prêt à brancher.

```text
Alimentation adaptée servos ──► PCA9685 V+
Alimentation logique adaptée ─► ESP32
ESP32 SDA/SCL ────────────────► PCA9685
PCA9685 PWM ──────────────────► Servomoteurs
Cellule de charge ────────────► HX711 ─► ESP32
Capteur de présence ──────────► ESP32
```

À vérifier : tensions logiques, courant de pointe des servos, dimensionnement alimentation, polarité, protections, masse de référence des signaux et arrêt d'urgence. Le schéma définitif dépendra des références réelles.
