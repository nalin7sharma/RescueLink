# RescueLink Hardware Setup Guide

## Required Components
1. F550 Hexacopter Frame
2. Pixhawk Flight Controller
3. Raspberry Pi 4 (4GB+ recommended)
4. GPS Module (U-blox NEO-M8N recommended)
5. LoRa Transceiver Module (SX1276 based)
6. Raspberry Pi Camera Module v2
7. Optical Flow Sensor (PX4Flow)
8. ESP32 Development Board
9. Micro Servo Motors (SG90)
10. 4S LiPo Battery (10,000mAh+)
11. Electronic Speed Controllers (30A BLHeli)
12. BLDC Motors (920KV)
13. 10-inch Propellers (CW and CCW)

## Assembly Instructions

### Step 1: Frame Assembly
1. Assemble the F550 frame according to manufacturer instructions
2. Mount the six BLDC motors to the frame arms
3. Attach ESCs to the frame and connect to motors
4. Secure the power distribution board to the frame center

### Step 2: Flight Controller Setup
1. Mount Pixhawk flight controller to the frame using vibration dampeners
2. Connect ESCs to Pixhawk output ports (MAIN 1-6)
3. Connect GPS module to Pixhawk GPS port
4. Connect optical flow sensor to Pixhawk I2C port
5. Connect telemetry radio to Pixhawk TELEM port

### Step 3: Companion Computer Setup
1. Mount Raspberry Pi 4 to the frame using standoffs
2. Connect camera module to Raspberry Pi CSI port
3. Connect Raspberry Pi to Pixhawk via USB
4. Connect optical flow sensor to Raspberry Pi GPIO (optional)
5. Connect LoRa module to Raspberry Pi SPI pins

### Step 4: Communication System
1. Solder antenna to LoRa module
2. Connect LoRa module to Raspberry Pi:
   - VCC to 3.3V
   - GND to GND
   - SCK to SCLK
   - MISO to MISO
   - MOSI to MOSI
   - NSS to GPIO8 (CE0)
   - RST to GPIO25
   - DIO0 to GPIO24

3. Connect second LoRa module to ESP32 for emergency device

### Step 5: Power System
1. Connect battery to power distribution board
2. Connect ESCs to power distribution board
3. Connect Pixhawk to power distribution board (5V BEC)
4. Connect Raspberry Pi to power distribution board (5V regulator)
5. Add power filter for clean power to Raspberry Pi

### Step 6: Payload Mechanism
1. Mount servo motor to the frame bottom
2. Connect servo to ESP32 GPIO pins
3. Design and attach payload release mechanism
4. Test payload release functionality

## Wiring Diagram
Pixhawk <--> USB <--> Raspberry Pi <--> Camera
Pixhawk <--> I2C <--> Optical Flow Sensor
Raspberry Pi <--> SPI <--> LoRa Module
ESP32 <--> GPIO <--> LoRa Module + Servo
Battery <--> PDB <--> ESCs + Power Systems


## Calibration Procedure

1. **ESC Calibration**: 
   - Use Mission Planner to calibrate all ESCs
   - Ensure proper motor rotation directions

2. **Sensor Calibration**:
   - Calibrate accelerometer and gyroscope
   - Calibrate compass in interference-free area
   - Calibrate optical flow sensor

3. **PID Tuning**:
   - Start with default Pixhawk parameters
   - Tune for stable flight with payload

4. **Camera Calibration**:
   - Calibrate camera for proper distortion correction
   - Test YOLOv8 object detection range

## Software Configuration

1. **Pixhawk Firmware**:
   - Install ArduCopter firmware
   - Configure flight modes
   - Set up fail-safes

2. **Raspberry Pi Setup**:
   - Install Raspberry Pi OS
   - Enable camera interface
   - Configure SPI for LoRa

3. **Emergency Device**:
   - Program ESP32 with provided code
   - Test LoRa communication range

## Safety Precautions

- Always disconnect battery when working on electronics
- Test motors without props first
- Perform initial flights in open areas
- Follow local drone regulations
- Use LiPo battery safety bags for charging
- Implement geofencing for safe operation areas
- Test fail-safe procedures thoroughly

## Testing Procedure

1. **Bench Testing**:
   - Test all components without props
   - Verify communication systems
   - Test payload release mechanism

2. **Ground Testing**:
   - Test object detection while walking
   - Verify GPS and optical flow operation
   - Test emergency signal transmission

3. **Flight Testing**:
   - Initial hover test without payload
   - Gradually increase payload weight
   - Test obstacle avoidance in controlled environment
   - Test emergency scenarios

## Troubleshooting

**Common Issues:**
1. **Vibration problems**: Ensure proper balancing and vibration dampening
2. **GPS issues**: Check antenna placement away from electronics
3. **LoRa range issues**: Check antenna orientation and obstacles
4. **Object detection failures**: Adjust camera focus and lighting conditions

**Solutions:**
- Check all connections and wiring
- Verify power supply stability
- Update all software components
- Calibrate sensors regularly
