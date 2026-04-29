import smbus
import time

class PCA9685:
    def __init__(self, address=0x40, bus_num=1):
        self.bus = smbus.SMBus(bus_num)
        self.address = address
        self.set_pwm_freq(50)

    def write(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def set_pwm_freq(self, freq):
        prescale_val = int(25000000.0 / (4096 * freq) - 1)
        self.write(0x00, 0x10)
        self.write(0xFE, prescale_val)
        self.write(0x00, 0x80)

    def set_pwm(self, channel, on, off):
        reg = 0x06 + 4 * channel
        self.bus.write_byte_data(self.address, reg, on & 0xFF)
        self.bus.write_byte_data(self.address, reg + 1, on >> 8)
        self.bus.write_byte_data(self.address, reg + 2, off & 0xFF)
        self.bus.write_byte_data(self.address, reg + 3, off >> 8)