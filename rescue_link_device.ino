#include <LoRa.h>
#include <ESP32Servo.h>

// Pin definitions
#define BUTTON_PIN 2
#define LED_PIN 13
#define SERVO_PIN 4
#define LORA_CS 5
#define LORA_RST 14
#define LORA_DIO0 2

// Device configuration
#define RESCUE_DEVICE_ID "RL001"
#define LORA_FREQUENCY 433E6
#define DEBOUNCE_DELAY 300

Servo releaseServo;
int buttonPressCount = 0;
long lastPressTime = 0;
bool emergencySignalSent = false;

void setup() {
  Serial.begin(115200);
  Serial.println("RescueLink Emergency Device Initializing...");
  
  // Initialize pins
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  
  // Initialize servo
  releaseServo.attach(SERVO_PIN);
  releaseServo.write(0); // Initial position
  
  // Initialize LoRa
  LoRa.setPins(LORA_CS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(LORA_FREQUENCY)) {
    Serial.println("RescueLink LoRa initialization failed!");
    while (1);
  }
  
  Serial.println("RescueLink LoRa initialization successful!");
  Serial.println("Device Ready - Press button for emergency signals");
  blinkLED(3, 200); // Ready signal
}

void loop() {
  // Check for button presses
  checkButton();
  
  // Send emergency signal after button presses
  if (buttonPressCount > 0 && millis() - lastPressTime > 3000 && !emergencySignalSent) {
    sendEmergencySignal();
    emergencySignalSent = true;
    buttonPressCount = 0;
  }
  
  // Reset emergency signal flag if no button pressed for a while
  if (emergencySignalSent && millis() - lastPressTime > 10000) {
    emergencySignalSent = false;
  }
  
  // Check for incoming messages
  receiveLoRaMessage();
  
  delay(50); // Small delay to reduce CPU usage
}

void checkButton() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    long currentTime = millis();
    if (currentTime - lastPressTime > DEBOUNCE_DELAY) {
      buttonPressCount++;
      lastPressTime = currentTime;
      blinkLED(1, 100); // Visual feedback
      
      Serial.print("RescueLink Button presses: ");
      Serial.println(buttonPressCount);
      
      // Reset emergency signal flag when new button press occurs
      emergencySignalSent = false;
    }
  }
}

void sendEmergencySignal() {
  LoRa.beginPacket();
  LoRa.print("RESCUE_EMERGENCY:");
  LoRa.print(RESCUE_DEVICE_ID);
  LoRa.print(":");
  LoRa.print(buttonPressCount);
  LoRa.print(":");
  LoRa.print(millis());
  LoRa.endPacket();
  
  Serial.print("RescueLink Emergency signal sent: ");
  Serial.print(buttonPressCount);
  Serial.println(" presses");
  
  // Visual confirmation
  blinkLED(5, 100);
}

void receiveLoRaMessage() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String message = "";
    while (LoRa.available()) {
      message += (char)LoRa.read();
    }
    
    Serial.print("RescueLink Received: ");
    Serial.println(message);
    
    if (message == "RESCUE_RELEASE") {
      releasePayload();
    } else if (message.startsWith("RESCUE_ACK")) {
      // Acknowledgment received
      blinkLED(2, 500);
    }
  }
}

void releasePayload() {
  Serial.println("RescueLink Releasing payload...");
  
  // Release payload
  releaseServo.write(90);
  delay(1000);
  releaseServo.write(0);
  
  Serial.println("RescueLink Payload released successfully!");
  
  // Visual confirmation
  blinkLED(3, 300);
}

void blinkLED(int count, int delayTime) {
  for (int i = 0; i < count; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(delayTime);
    digitalWrite(LED_PIN, LOW);
    if (i < count - 1) delay(delayTime);
  }
}
