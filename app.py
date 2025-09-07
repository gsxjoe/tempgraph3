import threading
import time
from flask import Flask, render_template, jsonify
from max6675 import MAX6675


# MAX6675 sensors using SPI0 bus, with CS on CE0 (device=0) and CE1 (device=1)
sensor1 = MAX6675(bus=0, device=0)
sensor2 = MAX6675(bus=0, device=1)


# --- Application State ---
temperature_data = {"sensor1": "N/A", "sensor2": "N/A"}

# --- Background Thread for Sensor Reading and OLED Display ---
def update_sensors():
    global temperature_data
    while True:
        temp1 = sensor1.read_temp()
        temp2 = sensor2.read_temp()
# changed .2f to .1f to bring back only one decimal point and changed C to F for label        
        temperature_data["sensor1"] = f"{temp1:.1f}°F" if not isinstance(temp1, float) or not temp1 is float("NaN") else "Disconnected"
        temperature_data["sensor2"] = f"{temp2:.1f}°F" if not isinstance(temp2, float) or not temp2 is float("NaN") else "Disconnected"

        time.sleep(5)

# --- Flask Web Server ---
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')
    
@app.route('/data')
def get_data():
    return jsonify(temperature_data)

if __name__ == '__main__':
    # Start the background thread for sensor updates
    thread = threading.Thread(target=update_sensors)
    thread.daemon = True
    thread.start()
    
    # Run the Flask web server
    app.run(host='0.0.0.0', port=5050, debug=False)







