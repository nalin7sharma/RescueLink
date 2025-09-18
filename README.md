# RescueLink - Disaster Response Drone System with YOLOv8

## Project Overview
**RescueLink** is an AI-powered drone system designed to deliver medical supplies and communication devices to remote areas during natural disasters.  
The system features:
- Real-time obstacle avoidance using **YOLOv8**
- **GPS-denied navigation**
- **Long-range communication** capabilities

---

## Key Features
- 🚁 AI-powered obstacle detection and avoidance using **YOLOv8**  
- 📡 GPS-denied navigation with **optical flow sensors**  
- 📶 Long-range **LoRa communication** for emergency signaling  
- 🌐 Web-based dashboard for mission monitoring  
- 🎯 Secure payload delivery mechanism  
- 📦 Scalable design with **5kg+ payload capacity**  

---

## Hardware Requirements
- F550 Hexacopter Frame  
- Pixhawk Flight Controller  
- Raspberry Pi 4 (**4GB+ recommended**)  
- GPS Module  
- LoRa Transceiver  
- Raspberry Pi compatible Camera Module  
- Optical Flow Sensor  
- ESP32 Microcontroller  
- Servo Motors for payload release  
- **4S LiPo Battery (10,000mAh+)**  

---

## Software Requirements
- Python 3.8+  
- Arduino IDE (for ESP32 programming)  
- OpenCV 4.7+  
- Ultralytics YOLOv8  
- Flask Web Framework  
- ArduPilot Firmware  

---

## Installation Instructions

### 1. Clone the repository
```bash
git clone https://github.com/nalin7sharma/RescueLink.git
cd RescueLink
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Upload ESP32 code
- Open **rescue_link_device.ino** in Arduino IDE  
- Install required libraries (`LoRa`, `ESP32Servo`)  
- Select **ESP32 board** and upload code  

---

## Usage Instructions

### Start the AI navigation system
```bash
python rescue_link.py
```

### Start the web dashboard
```bash
python rescue_dashboard.py
```

### Access the dashboard at
```
http://your-raspberry-pi-ip:5000
```

### Emergency device operation
- Press button **once** → Food supplies  
- Press button **twice** → Medical supplies  
- Press button **three times** → Emergency evacuation  

✅ LED will confirm signal transmission  


---

## System Architecture
The RescueLink system consists of:
- Drone platform with **Pixhawk flight controller**  
- **Raspberry Pi 4** for AI processing with YOLOv8  
- **ESP32-based emergency communication devices**  
- Web-based control dashboard  
- **LoRa long-range communication** network  

---

## Testing and Validation
The system has been tested for:
- ✅ Autonomous GPS-waypoint navigation  
- ✅ AI obstacle avoidance using YOLOv8 in controlled environments  
- ✅ Emergency signal transmission and reception  
- ✅ Payload delivery mechanism reliability  
- ✅ GPS-denied navigation capabilities  



