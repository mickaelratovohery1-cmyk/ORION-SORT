#include <Wire.h>

#define SDA_PIN 21
#define SCL_PIN 22

void setup() {
  Serial.begin(115200);
  delay(500);

  Wire.begin(SDA_PIN, SCL_PIN);

  Serial.println();
  Serial.println("=== ORION-SORT | TEST I2C ===");

  uint8_t count = 0;

  for (uint8_t address = 1; address < 127; address++) {
    Wire.beginTransmission(address);

    if (Wire.endTransmission() == 0) {
      Serial.printf("Peripherique I2C detecte : 0x%02X\n", address);
      count++;
    }
  }

  if (count == 0) {
    Serial.println("Aucun peripherique I2C detecte.");
    Serial.println("Verifier SDA, SCL, GND et alimentation.");
  } else {
    Serial.printf("Nombre de peripheriques : %u\n", count);
  }
}

void loop() {
  delay(2000);
}
