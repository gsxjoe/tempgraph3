import threading
import csv
import time
import os.path
from datetime import datetime
from flask import Flask, render_template, jsonify
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont
from max6675 import MAX6675

# --- Hardware Configuration ---
# GPIO setup for luma.oled, specifying CS and DC pins
oled_serial = spi(port=0, device=0, cs_high=True, reset=5, dc=6)
oled_device = sh1106(oled_serial)
# MAX6675 sensors using SPI0 bus, with CS on CE0 (device=0) and CE1 (device=1)
sensor1 = MAX6675(bus=0, device=0)
sensor2 = MAX6675(bus=0, device=1)

# Font for the OLED display
font = ImageFont.load_default()

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

        with canvas(oled_device) as draw:
            draw.text((0, 0), "Temp 1:    " + temperature_data["sensor1"], font=font, fill="white")
            draw.text((0, 20), "Temp 2:    " + temperature_data["sensor2"], font=font, fill="white")

        time.sleep(6)

def get_sensor_data()
#  global temperature_data
   while True:
        temp1 = sensor1.read_temp()
        temp2 = sensor2.read_temp()
# changed .2f to .1f to bring back only one decimal point and changed C to F for label        
#       temperature_data["sensor1"] = f"{temp1:.1f}°F" if not isinstance(temp1, float) or not temp1 is float("NaN") else "Disconnected"
#      temperature_data["sensor2"] = f"{temp2:.1f}°F" if not isinstance(temp2, float) or not temp2 is float("NaN") else "Disconnected"
    
    temperature = temp1
    humidity = temp2
    return temperature, humidity

# --- CSV logging setup ---
filename = "sensor_readings.csv"
fieldnames = ["timestamp", "temperature_c", "humidity_percent"]

# Check if the file already exists to decide whether to write headers
file_exists = os.path.isfile(filename)

# Main logging loop
print("Starting sensor data logging. Press Ctrl+C to exit.")
try:
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header row only if the file is new
        if not file_exists:
            writer.writeheader()
def get_sensor_data()

        while True:
            # Get data from your sensor
            temperature, humidity = get_sensor_data()
            
            # Create a dictionary with a timestamp and sensor data
            data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "temperature_c": temperature,
                "humidity_percent": humidity
            }
            
            # Write the data to the CSV file
            writer.writerow(data)
            csvfile.flush() # Ensure data is written immediately
            
            print(f"Logged: {data}")
            
            # Wait for 5 seconds before the next reading
            time.sleep(5)
# --- Flask Web Server ---
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify(temperature_data)

if __name__ == '__main__':
    # Start the background thread for sensor updates
    thread = threading.Thread(target=update_sensors)
    thread.daemon = True
    thread.start()
    
    # Run the Flask web server
    app.run(host='0.0.0.0', port=5000, debug=False)



