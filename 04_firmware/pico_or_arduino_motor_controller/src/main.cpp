/*
  Segment-Polkan firmware
  Назначение:
  - низкоуровневое управление шаговыми двигателями через драйверы DM865C/TB6600 по STEP/DIR/ENABLE;
  - обработка концевиков;
  - аварийная остановка E-Stop;
  - управление сервоприводами через PCA9685 или Servo PWM;
  - обмен с Raspberry Pi по USB Serial.

  Команды по Serial, строками:
  PING
  ENABLE 1|0
  STOP
  STATUS
  HOME
  MOVE_STEPS axis steps speed_us
  MOVE_JOINT joint angle_deg speed_us
  SERVO channel angle_deg

  axis/joint: 0..4
*/

#include <Arduino.h>

// Если используется PCA9685, раскомментировать и установить библиотеку Adafruit_PWMServoDriver
// #include <Wire.h>
// #include <Adafruit_PWMServoDriver.h>
// Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

static const uint8_t AXES = 5;

// TODO: заменить на реальные пины Pico/Arduino после утверждения распиновки.
const uint8_t STEP_PINS[AXES]  = {2, 4, 6, 8, 10};
const uint8_t DIR_PINS[AXES]   = {3, 5, 7, 9, 11};
const uint8_t EN_PIN           = 12;
const uint8_t LIMIT_MIN[AXES]  = {22, 23, 24, 25, 26};
const uint8_t LIMIT_MAX[AXES]  = {27, 28, 29, 30, 31};
const uint8_t ESTOP_PIN        = 32; // NC-контакт: LOW = авария

volatile bool estop = false;
bool motorsEnabled = false;
long currentSteps[AXES] = {0, 0, 0, 0, 0};

// Примерные коэффициенты, заменить после калибровки.
float stepsPerDegree[AXES] = {88.89, 88.89, 88.89, 44.44, 44.44};

void enableMotors(bool enable) {
  motorsEnabled = enable;
  // У многих драйверов ENABLE активен LOW. Проверить по DM865C.
  digitalWrite(EN_PIN, enable ? LOW : HIGH);
}

bool isEmergency() {
  return digitalRead(ESTOP_PIN) == LOW || estop;
}

void stopAll() {
  estop = true;
  enableMotors(false);
  Serial.println("ERR ESTOP_OR_STOP_ACTIVE");
}

bool limitTriggered(uint8_t axis, int dir) {
  if (axis >= AXES) return true;
  if (dir < 0 && digitalRead(LIMIT_MIN[axis]) == LOW) return true;
  if (dir > 0 && digitalRead(LIMIT_MAX[axis]) == LOW) return true;
  return false;
}

void pulseStep(uint8_t axis, unsigned int speedUs) {
  digitalWrite(STEP_PINS[axis], HIGH);
  delayMicroseconds(speedUs);
  digitalWrite(STEP_PINS[axis], LOW);
  delayMicroseconds(speedUs);
}

bool moveSteps(uint8_t axis, long steps, unsigned int speedUs) {
  if (axis >= AXES) {
    Serial.println("ERR BAD_AXIS");
    return false;
  }
  if (!motorsEnabled) {
    Serial.println("ERR MOTORS_DISABLED");
    return false;
  }
  if (isEmergency()) {
    stopAll();
    return false;
  }

  int dir = (steps >= 0) ? 1 : -1;
  long n = labs(steps);
  digitalWrite(DIR_PINS[axis], dir > 0 ? HIGH : LOW);

  for (long i = 0; i < n; i++) {
    if (isEmergency() || limitTriggered(axis, dir)) {
      stopAll();
      return false;
    }
    pulseStep(axis, speedUs);
    currentSteps[axis] += dir;
  }
  Serial.print("OK MOVE_STEPS ");
  Serial.print(axis);
  Serial.print(" ");
  Serial.println(currentSteps[axis]);
  return true;
}

bool moveJoint(uint8_t joint, float angleDeg, unsigned int speedUs) {
  if (joint >= AXES) {
    Serial.println("ERR BAD_JOINT");
    return false;
  }
  long target = lround(angleDeg * stepsPerDegree[joint]);
  long delta = target - currentSteps[joint];
  return moveSteps(joint, delta, speedUs);
}

void setServoAngle(uint8_t channel, int angleDeg) {
  angleDeg = constrain(angleDeg, 0, 180);
  // PCA9685 вариант:
  // int pulseMin = 150;
  // int pulseMax = 600;
  // int pulse = map(angleDeg, 0, 180, pulseMin, pulseMax);
  // pwm.setPWM(channel, 0, pulse);

  Serial.print("OK SERVO ");
  Serial.print(channel);
  Serial.print(" ");
  Serial.println(angleDeg);
}

void homeAxis(uint8_t axis) {
  if (axis >= AXES) return;
  enableMotors(true);
  digitalWrite(DIR_PINS[axis], LOW);
  while (digitalRead(LIMIT_MIN[axis]) != LOW) {
    if (isEmergency()) {
      stopAll();
      return;
    }
    pulseStep(axis, 800);
  }
  currentSteps[axis] = 0;
  Serial.print("OK HOME_AXIS ");
  Serial.println(axis);
}

void homeAll() {
  for (uint8_t i = 0; i < AXES; i++) homeAxis(i);
  Serial.println("OK HOME");
}

void printStatus() {
  Serial.print("STATUS enabled=");
  Serial.print(motorsEnabled ? 1 : 0);
  Serial.print(" estop=");
  Serial.print(isEmergency() ? 1 : 0);
  Serial.print(" steps=");
  for (uint8_t i = 0; i < AXES; i++) {
    Serial.print(currentSteps[i]);
    if (i < AXES - 1) Serial.print(',');
  }
  Serial.println();
}

void handleCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;

  if (cmd == "PING") { Serial.println("PONG"); return; }
  if (cmd == "STATUS") { printStatus(); return; }
  if (cmd == "STOP") { stopAll(); return; }
  if (cmd == "HOME") { estop = false; homeAll(); return; }

  int value = 0;
  if (sscanf(cmd.c_str(), "ENABLE %d", &value) == 1) {
    if (value == 1) estop = false;
    enableMotors(value == 1);
    Serial.println(value == 1 ? "OK ENABLED" : "OK DISABLED");
    return;
  }

  int axis = 0;
  long steps = 0;
  int speedUs = 700;
  if (sscanf(cmd.c_str(), "MOVE_STEPS %d %ld %d", &axis, &steps, &speedUs) == 3) {
    moveSteps((uint8_t)axis, steps, (unsigned int)speedUs);
    return;
  }

  int joint = 0;
  float angle = 0;
  if (sscanf(cmd.c_str(), "MOVE_JOINT %d %f %d", &joint, &angle, &speedUs) == 3) {
    moveJoint((uint8_t)joint, angle, (unsigned int)speedUs);
    return;
  }

  int channel = 0;
  int servoAngle = 0;
  if (sscanf(cmd.c_str(), "SERVO %d %d", &channel, &servoAngle) == 2) {
    setServoAngle((uint8_t)channel, servoAngle);
    return;
  }

  Serial.print("ERR UNKNOWN_CMD ");
  Serial.println(cmd);
}

void setup() {
  Serial.begin(115200);
  for (uint8_t i = 0; i < AXES; i++) {
    pinMode(STEP_PINS[i], OUTPUT);
    pinMode(DIR_PINS[i], OUTPUT);
    pinMode(LIMIT_MIN[i], INPUT_PULLUP);
    pinMode(LIMIT_MAX[i], INPUT_PULLUP);
  }
  pinMode(EN_PIN, OUTPUT);
  pinMode(ESTOP_PIN, INPUT_PULLUP);
  enableMotors(false);

  // PCA9685 init:
  // Wire.begin();
  // pwm.begin();
  // pwm.setPWMFreq(50);

  Serial.println("READY SEGMENT_POLKAN_FIRMWARE");
}

void loop() {
  if (digitalRead(ESTOP_PIN) == LOW) stopAll();
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    handleCommand(cmd);
  }
}
