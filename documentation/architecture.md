# Architecture générale

```text
Caméra ──► PC / Raspberry Pi
             ├── Python + OpenCV + modèle IA
             ├── logique de décision
             ├── API Flask
             └── base SQLite
                       │ Wi-Fi / HTTP ou MQTT
                       ▼
                     ESP32
                 ┌─────┴──────┐
                 ▼            ▼
             HX711 +       PCA9685
           cellule de      servomoteurs
             charge       et pince
```

## Responsabilités
- ESP32 : lecture des capteurs, commande des actionneurs et états de sécurité.
- PC/Raspberry Pi : caméra, prédiction IA, décision, API et base de données.
- Interface web : supervision, historique et commandes de maintenance.

## Séquence
`ATTENTE → DÉTECTION → CAPTURE → CLASSIFICATION → PESÉE → DÉCISION → SAISIE → DÉPÔT → RETOUR → ENREGISTREMENT`

En cas d'incertitude, d'erreur ou de perte de communication : arrêt sûr et signalement.

## Exemple de message indicatif
```json
{"command":"SORT","object_class":"plastic","destination":"bin_plastic","request_id":"demo-001"}
```
Le protocole final et les champs seront validés par l'équipe.
