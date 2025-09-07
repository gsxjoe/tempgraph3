import csv
import time
from datetime import datetime
import os.path
from max6675 import MAX6675

# --- Replace with your sensor's library and reading function ---
def get_sensor_data():
    sensor1=MAX6675(bus=0, device=0)
    sensor2=MAX6675(bus=0, device=1)
    # Simulated data for demonstration
    grill = round(sensor1.read_temp(),2)
    meat = round(sensor2.read_temp(),2)
    return grill, meat

# --- CSV logging setup ---
filename = "./static/sensor_readings.csv"
fieldnames = ["timestamp", "Grill", "Meat"]

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
            grill, meat = get_sensor_data()
            
            # Create a dictionary with a timestamp and sensor data
            data = {
                "timestamp": datetime.now().strftime("%m-%d %H:%M"),
                "Grill": grill,
                "Meat": meat
            }
            
            # Write the data to the CSV file
            writer.writerow(data)
            csvfile.flush() # Ensure data is written immediately
            
            print(f"Logged: {data}")
            
            # Wait for 60 seconds before the next reading
            time.sleep(60)
            
except KeyboardInterrupt:
    print("\nLogging stopped by user. CSV file is saved.")
except Exception as e:
    print(f"An error occurred: {e}")
