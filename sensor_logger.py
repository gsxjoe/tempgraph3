import csv
import time
from datetime import datetime
import os.path

# --- Replace with your sensor's library and reading function ---
def get_sensor_data():
    """
    This function simulates reading data from a sensor.
    Replace this with your actual code to get readings from your sensor.
    
    For example, with a DHT11 sensor, you might have:
    import adafruit_dht
    import board
    dht_device = adafruit_dht.DHT11(board.D4)
    temperature = dht_device.temperature
    humidity = dht_device.humidity
    return temperature, humidity
    """
    # Simulated data for demonstration
    temperature = 22.5 + (time.time() % 10)
    humidity = 60.1 + (time.time() % 5)
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
            
except KeyboardInterrupt:
    print("\nLogging stopped by user. CSV file is saved.")
except Exception as e:
    print(f"An error occurred: {e}")
