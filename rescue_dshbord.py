from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import threading
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rescue_link_secret_2025'
socketio = SocketIO(app, async_mode='threading')

class RescueDashboard:
    def __init__(self):
        self.drone_status = "Disconnected"
        self.battery_level = 100
        self.current_location = (28.6139, 77.2090)  # Default to Delhi
        self.emergency_signals = []
        self.mission_log = []
        self.connected_clients = 0
        
    def update_status(self, status):
        self.drone_status = status
        self.log_event(f"Status changed to: {status}")
        socketio.emit('status_update', {'status': status, 'timestamp': datetime.now().isoformat()})
        
    def update_battery(self, level):
        self.battery_level = level
        socketio.emit('battery_update', {'level': level, 'timestamp': datetime.now().isoformat()})
        
    def update_location(self, lat, lng):
        self.current_location = (lat, lng)
        socketio.emit('location_update', {
            'lat': lat, 
            'lng': lng, 
            'timestamp': datetime.now().isoformat()
        })
        
    def add_emergency_signal(self, signal_data):
        self.emergency_signals.append(signal_data)
        self.log_event(f"Emergency signal received: {signal_data}")
        socketio.emit('emergency_alert', {
            'type': signal_data.get('type', 'unknown'),
            'location': signal_data.get('location', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'device_id': signal_data.get('device_id', 'unknown')
        })
        
    def log_event(self, message):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'message': message
        }
        self.mission_log.append(log_entry)
        socketio.emit('log_update', log_entry)

rescue_dashboard = RescueDashboard()

@app.route('/')
def index():
    return render_template('rescue_dashboard.html')

@app.route('/api/status')
def get_status():
    return jsonify({
        'status': rescue_dashboard.drone_status,
        'battery': rescue_dashboard.battery_level,
        'location': rescue_dashboard.current_location,
        'emergencies': rescue_dashboard.emergency_signals[-10:],  # Last 10 emergencies
        'log_entries': rescue_dashboard.mission_log[-20:]  # Last 20 log entries
    })

@app.route('/api/emergency', methods=['POST'])
def handle_emergency():
    try:
        data = request.get_json()
        rescue_dashboard.add_emergency_signal(data)
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error handling emergency: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@socketio.on('connect')
def handle_connect():
    rescue_dashboard.connected_clients += 1
    logger.info(f"Client connected. Total clients: {rescue_dashboard.connected_clients}")
    rescue_dashboard.log_event("Dashboard client connected")
    
    # Send current status to newly connected client
    socketio.emit('status_update', {'status': rescue_dashboard.drone_status})
    socketio.emit('battery_update', {'level': rescue_dashboard.battery_level})
    socketio.emit('location_update', {
        'lat': rescue_dashboard.current_location[0],
        'lng': rescue_dashboard.current_location[1]
    })

@socketio.on('disconnect')
def handle_disconnect():
    rescue_dashboard.connected_clients -= 1
    logger.info(f"Client disconnected. Total clients: {rescue_dashboard.connected_clients}")
    rescue_dashboard.log_event("Dashboard client disconnected")

@socketio.on('command')
def handle_command(data):
    try:
        command = data.get('command')
        parameters = data.get('parameters', {})
        
        rescue_dashboard.log_event(f"Command received: {command}")
        
        # Process different commands
        if command == 'start_mission':
            rescue_dashboard.update_status('Mission Started')
        elif command == 'return_home':
            rescue_dashboard.update_status('Returning Home')
        elif command == 'emergency_stop':
            rescue_dashboard.update_status('Emergency Stop')
        else:
            rescue_dashboard.log_event(f"Unknown command: {command}")
            
    except Exception as e:
        logger.error(f"Error processing command: {e}")

def simulate_drone_data():
    """Simulate drone data for testing and demonstration"""
    logger.info("Starting drone data simulation")
    
    while True:
        try:
            # Simulate battery drain
            if rescue_dashboard.battery_level > 20:
                rescue_dashboard.battery_level -= 0.5
            else:
                rescue_dashboard.update_status('Low Battery - Returning Home')
                
            # Simulate location changes
            lat, lng = rescue_dashboard.current_location
            lat += 0.0001
            lng += 0.0001
            rescue_dashboard.update_location(lat, lng)
            
            # Simulate occasional emergency signals
            if int(time.time()) % 30 == 0:
                emergency_type = ['medical', 'food', 'evacuation'][int(time.time()) % 3]
                rescue_dashboard.add_emergency_signal({
                    'type': emergency_type,
                    'location': f"{lat:.6f}, {lng:.6f}",
                    'device_id': f"RL{int(time.time()) % 100:03d}"
                })
            
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error in drone simulation: {e}")
            time.sleep(5)

if __name__ == '__main__':
    # Start simulation thread for demonstration
    sim_thread = threading.Thread(target=simulate_drone_data)
    sim_thread.daemon = True
    sim_thread.start()
    
    rescue_dashboard.log_event("RescueLink Dashboard started")
    logger.info("Starting RescueLink Dashboard on http://0.0.0.0:5000")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)
