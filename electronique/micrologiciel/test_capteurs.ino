#include <Wire.h>

#define PRESENCE 27
#define TRIG 5
#define ECHO 34
#define LED_R 25
#define LED_G 26
#define LED_B 33
#define BUZZER 23
#define ESTOP 4

void setup() {
  Serial.begin(115200);

  Wire.begin(21, 22);

  pinMode(PRESENCE, INPUT);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);

  pinMode(BUZZER, OUTPUT);
  pinMode(ESTOP, INPUT_PULLUP);

  Serial.println("ORION-SORT - TEST CAPTEURS");
}

void loop() {
  int presence = digitalRead(PRESENCE);
  int stopState = digitalRead(ESTOP);

  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  unsigned long duration = pulseIn(ECHO, HIGH, 30000);

  Serial.printf("Presence=%d | STOP=%d | ", presence, stopState);

  if (duration > 0) {
    float distance = duration * 0.0343f / 2.0f;
    Serial.printf("Distance=%.1f cm\n", distance);
  } else {
    Serial.println("Distance=timeout");
  }

  if (stopState == LOW) {
    digitalWrite(LED_R, HIGH);
    digitalWrite(LED_G, LOW);
    digitalWrite(LED_B, LOW);
    tone(BUZZER, 2000);
  } else {
    noTone(BUZZER);
    digitalWrite(LED_R, LOW);
    digitalWrite(LED_G, HIGH);
    digitalWrite(LED_B, LOW);
  }

  delay(500);
}
