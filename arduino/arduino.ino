#include <Servo.h>

#define PULSE_MIN (200)
#define PULSE_MAX (577)

#define SERVO0_PIN (5)
#define SERVO1_PIN (6)
#define SERVO2_PIN (9)

Servo servo0;
Servo servo1;
Servo servo2;

void setup() {
  servo0.attach(SERVO0_PIN, PULSE_MIN, PULSE_MAX);
  servo1.attach(SERVO1_PIN, PULSE_MIN, PULSE_MAX);
  servo2.attach(SERVO2_PIN, PULSE_MIN, PULSE_MAX);
  Serial.begin(9600);

  servo0.write(90);
  servo1.write(90);
  servo2.write(90);
}

uint8_t s;
uint8_t v;

void loop() {
  if(Serial.available() > 1) {
    Serial.readBytes(&s, 1);
    Serial.readBytes(&v, 1);

    switch(s) {
    case 0:
      servo0.write(v);
      break;
    case 1:
      servo1.write(v);
      break;
    case 2:
      servo2.write(v);
      break;
    default:
      break;
    }

    delay(15);
  }
}
