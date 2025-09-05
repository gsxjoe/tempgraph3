import spidev
import time

class MAX6675:
    def __init__(self, bus, device):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000

    def read_temp(self):
        try:
            data = self.spi.readbytes(2)
            msb = data[0]
            lsb = data[1]
            if (lsb & 0x04):
                return float("NaN") # Thermocouple disconnected
            
            temp_c = ((msb << 8) | lsb) >> 3
# added x 1.8 + 32 for fahrenheit            
            temp_c = temp_c * 0.25 * 1.8 + 32
            return temp_c
        except Exception as e:
            print(f"Error reading MAX6675: {e}")
            return float("NaN")

    def close(self):
        self.spi.close()


