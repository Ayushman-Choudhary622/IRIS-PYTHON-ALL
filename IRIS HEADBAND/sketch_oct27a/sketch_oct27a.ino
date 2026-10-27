
#include <NimBLEDevice.h>
#include <NimBLEHIDDevice.h>
#include <NimBLECharacteristic.h>
#include <Wire.h>

// ================= BLE MOUSE DEFINITIONS =================
#define MOUSE_LEFT 1

static const uint8_t _hidReportDescriptor[] = {
  0x05, 0x01, 0x09, 0x02, 0xa1, 0x01, 0x09, 0x01, 0xa1, 0x00,
  0x05, 0x09, 0x19, 0x01, 0x29, 0x05, 0x15, 0x00, 0x25, 0x01,
  0x75, 0x01, 0x95, 0x05, 0x81, 0x02, 0x75, 0x03, 0x95, 0x01,
  0x81, 0x03, 0x05, 0x01, 0x09, 0x30, 0x09, 0x31, 0x09, 0x38,
  0x15, 0x81, 0x25, 0x7f, 0x75, 0x08, 0x95, 0x03, 0x81, 0x06,
  0x05, 0x0c, 0x0a, 0x38, 0x02, 0x15, 0x81, 0x25, 0x7f, 0x75,
  0x08, 0x95, 0x01, 0x81, 0x06, 0xc0, 0xc0
};

class BleMouse : public NimBLEServerCallbacks {
private:
  uint8_t _buttons;
  NimBLEHIDDevice* hid;
  NimBLECharacteristic* inputMouse;
  bool connected;

public:
  BleMouse()
    : _buttons(0), hid(nullptr), inputMouse(nullptr),
      connected(false) {}

  void begin(void) {
    NimBLEDevice::init("IRIS");
    NimBLEDevice::setSecurityAuth(BLE_SM_PAIR_AUTHREQ_BOND);

    NimBLEServer* pServer = NimBLEDevice::createServer();
    pServer->setCallbacks(this);

    hid = new NimBLEHIDDevice(pServer);
    inputMouse = hid->getInputReport(0);

    hid->setManufacturer("Ayushman Choudhary");
    hid->setPnp(0x02, 0xe502, 0xa111, 0x0210);
    hid->setHidInfo(0x00, 0x02);

    hid->setReportMap(
      (uint8_t*)_hidReportDescriptor,
      sizeof(_hidReportDescriptor)
    );

    hid->startServices();

    // NEW: Battery service, currently a placeholder value.
    // This reports 100%, NOT a measured battery percentage.
    hid->setBatteryLevel(100);

    NimBLEAdvertising* pAdvertising = pServer->getAdvertising();
    pAdvertising->setAppearance(HID_MOUSE);
    pAdvertising->addServiceUUID(
      hid->getHidService()->getUUID()
    );
    pAdvertising->setName("IRIS");
    pAdvertising->start();
  }

  void move(signed char x, signed char y) {
    if (isConnected()) {
      uint8_t report[5] = {
        _buttons, (uint8_t)x, (uint8_t)y, 0, 0
      };

      inputMouse->setValue(report, 5);
      inputMouse->notify();
    }
  }

  void click(uint8_t button = MOUSE_LEFT) {
    _buttons = button;
    move(0, 0);
    delay(20);

    _buttons = 0;
    move(0, 0);
  }

  void press(uint8_t button = MOUSE_LEFT) {
    _buttons |= button;
    move(0, 0);
  }

  void release(uint8_t button = MOUSE_LEFT) {
    _buttons &= ~button;
    move(0, 0);
  }

  bool isConnected(void) const {
    return connected;
  }

  void onConnect(
    NimBLEServer* pServer,
    NimBLEConnInfo& connInfo
  ) override {
    connected = true;
  }

  void onDisconnect(
    NimBLEServer* pServer,
    NimBLEConnInfo& connInfo,
    int reason
  ) override {
    connected = false;

    // NEW: Resume advertising after disconnection,
    // so IRIS can be discovered and paired again.
    NimBLEDevice::startAdvertising();
  }
};

BleMouse bleMouse;

// ================= HARDWARE CONFIGURATION =================
#define I2C_SDA 6
#define I2C_SCL 7
#define LEFT_CLICK_PIN 2

const uint8_t MPU_ADDR = 0x68;

// ================= RGB STATUS LED =================
// Common-cathode RGB LED.
// Use a separate resistor for each colour.

#define LED_GREEN D1
#define LED_BLUE  D2
#define LED_RED   D3

void setStatusLED(bool red, bool green, bool blue) {
  digitalWrite(LED_RED, red ? HIGH : LOW);
  digitalWrite(LED_GREEN, green ? HIGH : LOW);
  digitalWrite(LED_BLUE, blue ? HIGH : LOW);
}

void showErrorLED() {
  setStatusLED(true, false, false);
}

void showStartingLED() {
  setStatusLED(false, false, true);
}

void showReadyLED() {
  setStatusLED(false, true, false);
}

// NEW: Blink blue while waiting for a Bluetooth connection.
void showSearchingLED() {
  static unsigned long lastBlink = 0;
  static bool blueOn = false;

  if (millis() - lastBlink >= 500) {
    lastBlink = millis();
    blueOn = !blueOn;
  }

  setStatusLED(false, false, blueOn);
}

// ================= MPU6050 COMMUNICATION =================
bool mpu6050Responding() {
  Wire.beginTransmission(MPU_ADDR);
  return Wire.endTransmission(true) == 0;
}

// ================= GYROSCOPE OFFSETS =================
long gyroOffsetX = 0;
long gyroOffsetY = 0;
long gyroOffsetZ = 0;

// ================= CLICK / DRAG VARIABLES =================
bool dragging = false;
bool lastLeftState = HIGH;

unsigned long leftPressTime = 0;

// ================= SETUP =================
void setup() {
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  pinMode(LED_RED, OUTPUT);

  showStartingLED();

  // Keep the headband still during startup calibration.
  delay(3000);

  pinMode(LEFT_CLICK_PIN, INPUT_PULLUP);

  Wire.begin(I2C_SDA, I2C_SCL);
  Wire.setClock(400000);

  delay(100);

  // Wait for MPU6050.
  while (!mpu6050Responding()) {
    showErrorLED();
    delay(500);
  }

  showStartingLED();

  // Wake up MPU6050.
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0x00);
  Wire.endTransmission(true);

  // Gyroscope range: +/- 500 degrees/second.
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x1B);
  Wire.write(0x08);
  Wire.endTransmission(true);

  delay(100);

  // ================= CALIBRATE ALL THREE AXES =================
  long sumX = 0;
  long sumY = 0;
  long sumZ = 0;

  for (int i = 0; i < 500; i++) {
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x43);

    if (Wire.endTransmission(false) != 0) {
      showErrorLED();
      ESP.restart();
    }

    uint8_t bytesReceived = Wire.requestFrom(
      MPU_ADDR,
      (uint8_t)6,
      (uint8_t)true
    );

    if (bytesReceived != 6) {
      showErrorLED();
      ESP.restart();
    }

    int16_t gx = (int16_t)(
      ((uint16_t)Wire.read() << 8) | Wire.read()
    );

    int16_t gy = (int16_t)(
      ((uint16_t)Wire.read() << 8) | Wire.read()
    );

    int16_t gz = (int16_t)(
      ((uint16_t)Wire.read() << 8) | Wire.read()
    );

    sumX += gx;
    sumY += gy;
    sumZ += gz;

    delay(3);
  }

  gyroOffsetX = sumX / 500;
  gyroOffsetY = sumY / 500;
  gyroOffsetZ = sumZ / 500;

  // Start Bluetooth HID mouse.
  bleMouse.begin();

  showStartingLED();
}

// ================= MAIN LOOP =================
void loop() {
  // Check MPU6050 communication every 250 ms.
  static unsigned long lastMPUCheck = 0;
  static bool mpuOK = true;

  if (millis() - lastMPUCheck >= 250) {
    lastMPUCheck = millis();
    mpuOK = mpu6050Responding();
  }

  if (!mpuOK) {
    showErrorLED();
    delay(12);
    return;
  }

  // NEW: Blink blue while disconnected; green while connected.
  if (bleMouse.isConnected()) {
    showReadyLED();
  } else {
    showSearchingLED();
    delay(12);
    return;
  }

  // ================= READ ALL THREE GYROSCOPE AXES =================
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x43);

  if (Wire.endTransmission(false) != 0) {
    showErrorLED();
    delay(12);
    return;
  }

  uint8_t bytesReceived = Wire.requestFrom(
    MPU_ADDR,
    (uint8_t)6,
    (uint8_t)true
  );

  if (bytesReceived != 6) {
    showErrorLED();
    delay(12);
    return;
  }

  int16_t gx = (int16_t)(
    ((uint16_t)Wire.read() << 8) | Wire.read()
  );

  int16_t gy = (int16_t)(
    ((uint16_t)Wire.read() << 8) | Wire.read()
  );

  int16_t gz = (int16_t)(
    ((uint16_t)Wire.read() << 8) | Wire.read()
  );

  // ================= CALCULATE DELTAS =================
  long deltaX = (long)gx - gyroOffsetX;
  long deltaY = (long)gy - gyroOffsetY;
  long deltaZ = (long)gz - gyroOffsetZ;

  // ================= DEADZONE =================
  const int deadzoneThreshold = 180;

  if (abs(deltaX) < deadzoneThreshold) deltaX = 0;
  if (abs(deltaY) < deadzoneThreshold) deltaY = 0;
  if (abs(deltaZ) < deadzoneThreshold) deltaZ = 0;

  // ================= IRIS CURSOR MAPPING =================
  const int sensitivity = 150;

  // Original tested mapping preserved.
  int moveX = -(int)(deltaX / sensitivity);
  int moveY = -(int)(deltaZ / sensitivity);

  moveX = constrain(moveX, -127, 127);
  moveY = constrain(moveY, -127, 127);

  if (moveX != 0 || moveY != 0) {
    bleMouse.move(
      (signed char)moveX,
      (signed char)moveY
    );
  }

  // ================= CLICK / DRAG =================
  bool leftPressed =
    (digitalRead(LEFT_CLICK_PIN) == LOW);

  bool isMoving =
    (moveX != 0 || moveY != 0);

  // Detect button press.
  if (leftPressed && lastLeftState == HIGH) {
    leftPressTime = millis();
  }

  // Start dragging if held while moving.
  if (leftPressed &&
      !dragging &&
      isMoving &&
      (millis() - leftPressTime > 150)) {

    bleMouse.press(MOUSE_LEFT);
    dragging = true;
  }

  // Detect button release.
  if (!leftPressed && lastLeftState == LOW) {
    if (dragging) {
      bleMouse.release(MOUSE_LEFT);
      dragging = false;
    } else if (millis() - leftPressTime < 300) {
      bleMouse.click(MOUSE_LEFT);
    }
  }

  lastLeftState = leftPressed;

  delay(12);
}
