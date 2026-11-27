/*
 ORION-Sort — squelette ESP32 non opérationnel.
 A completer apres validation des composants et du brochage.
*/
#include <Arduino.h>

enum RobotState { IDLE, WAITING_FOR_COMMAND, MOVING, ERROR_STATE, EMERGENCY_STOP };
RobotState robotState = IDLE;

void setup() {
  Serial.begin(115200);
  // TODO : initialiser I2C, PCA9685, HX711 et capteurs.
  Serial.println("ORION-Sort - firmware preparatoire");
}

void loop() {
  // TODO : lire les capteurs et valider les commandes.
  // TODO : commander les servos avec limites de securite.
  // TODO : publier la telemetrie.
  if (robotState == ERROR_STATE || robotState == EMERGENCY_STOP) {
    // TODO : appliquer l'etat sur defini par la conception.
  }
  delay(20);
}
