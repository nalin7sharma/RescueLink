#!/usr/bin/env python3
"""
RescueLink - Disaster Response Drone AI Navigation System with YOLOv8
CtrlAltWin - Smart India Hackathon 2025
"""

import cv2
import numpy as np
import threading
import time
import logging
from pymavlink import mavutil
from ultralytics import YOLO
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RescueLinkDrone:
    def __init__(self):
        self.vehicle = None
        self.model = None
        self.cap = None
        self.obstacle_detected = False
        self.gps_denied = False
        self.current_waypoint = 0
        self.waypoints = []
        self.running = True
        
    def initialize_camera(self):
        """Initialize camera for obstacle detection"""
        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            logger.info("Camera initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Camera initialization failed: {e}")
            return False

    def load_yolov8_model(self):
        """Load YOLOv8 model for obstacle detection"""
        try:
            # Use YOLOv8n (nano) for better performance on Raspberry Pi
            self.model = YOLO('yolov8n.pt')
            logger.info("YOLOv8 model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"YOLOv8 model loading failed: {e}")
            return False

    def connect_to_pixhawk(self):
        """Connect to Pixhawk flight controller"""
        try:
            self.vehicle = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600)
            logger.info("Connected to Pixhawk successfully")
            return True
        except Exception as e:
            logger.error(f"Pixhawk connection failed: {e}")
            return False

    def detect_obstacles(self):
        """Real-time obstacle detection using YOLOv8"""
        logger.info("Starting obstacle detection thread")
        
        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    time.sleep(0.1)
                    continue
                
                # Run YOLOv8 inference
                results = self.model(frame, conf=0.6, verbose=False)
                
                # Process results
                obstacle_detected = False
                for result in results:
                    for box in result.boxes:
                        class_id = int(box.cls[0].item())
                        conf = box.conf[0].item()
                        
                        # Check for obstacles (person, vehicle, etc.)
                        if class_id in [0, 1, 2, 3, 5, 7]:  # person, bicycle, car, motorcycle, bus, truck
                            obstacle_detected = True
                            logger.warning(f"Obstacle detected: {self.model.names[class_id]} with confidence {conf:.2f}")
                
                self.obstacle_detected = obstacle_detected
                
                # Visualize results
                annotated_frame = results[0].plot()
                cv2.imshow('RescueLink - YOLOv8 Obstacle Detection', annotated_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            except Exception as e:
                logger.error(f"Error in obstacle detection: {e}")
                time.sleep(1)
        
        self.cap.release()
        cv2.destroyAllWindows()

    def perform_avoidance_maneuver(self):
        """Perform obstacle avoidance maneuver"""
        if self.obstacle_detected:
            logger.warning("Obstacle detected! Performing avoidance maneuver.")
            try:
                # Command drone to hover and wait
                self.vehicle.mav.command_long_send(
                    self.vehicle.target_system, self.vehicle.target_component,
                    mavutil.mavlink.MAV_CMD_NAV_LOITER_UNLIM, 0, 0, 0, 0, 0, 0, 0, 0
                )
                time.sleep(3)
                # Resume mission
                self.resume_mission()
            except Exception as e:
                logger.error(f"Avoidance maneuver failed: {e}")

    def resume_mission(self):
        """Resume mission after obstacle avoidance"""
        logger.info("Resuming mission")
        # Implementation for resuming the mission
        pass

    def execute_mission(self):
        """Main mission execution loop"""
        logger.info("Starting RescueLink mission execution")
        
        try:
            while self.running:
                if not self.obstacle_detected:
                    # Follow waypoints or execute mission tasks
                    self.follow_waypoints()
                else:
                    self.perform_avoidance_maneuver()
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("Mission interrupted by user")
        except Exception as e:
            logger.error(f"Mission execution error: {e}")
        finally:
            self.cleanup()

    def follow_waypoints(self):
        """Follow pre-defined waypoints"""
        # Waypoint navigation logic
        pass

    def start_ai_processing(self):
        """Start AI processing in separate thread"""
        ai_thread = threading.Thread(target=self.detect_obstacles)
        ai_thread.daemon = True
        ai_thread.start()
        logger.info("AI processing thread started")

    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        logger.info("Resources cleaned up")

    def initialize_system(self):
        """Initialize the complete RescueLink system"""
        logger.info("Initializing RescueLink system")
        
        if not self.initialize_camera():
            return False
            
        if not self.load_yolov8_model():
            return False
            
        if not self.connect_to_pixhawk():
            return False
            
        return True

if __name__ == "__main__":
    drone = RescueLinkDrone()
    
    if drone.initialize_system():
        drone.start_ai_processing()
        drone.execute_mission()
    else:
        logger.error("RescueLink system initialization failed")
