#include <Servo.h>

#define PULSE_MIN (200)
#define PULSE_MAX (577)

#define SERVO0_PIN (5)
#define SERVO1_PIN (6)

Servo servo0;
Servo servo1;

void setup() {
  servo0.attach(SERVO0_PIN, PULSE_MIN, PULSE_MAX);
  servo1.attach(SERVO1_PIN, PULSE_MIN, PULSE_MAX);
  Serial.begin(9600);

  servo0.write(90);
  servo1.write(90);
}

uint8_t s;
uint8_t v;

void loop() {
  if(Serial.available() > 1) {
    Serial.readBytes(&s, 1);
    Serial.readBytes(&v, 1);
    if(s == 0) {
      servo0.write(v);
    } else {
      servo1.write(v);
    }
    delay(15);
  }
}
