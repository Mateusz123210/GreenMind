"""Classes which provide interface to hardware sensors."""

import glob
import time
import board

import smbus
from adafruit_seesaw.seesaw import Seesaw

from .abc_sensors import HumiditySensor, LightSensor, TemperatureSensor


class StemmaHumiditySensor(HumiditySensor):
    """Measures humidity"""
    def __init__(self) -> None:
        super().__init__()
        i2c_bus = board.I2C()  # uses board.SCL and board.SDA
        ss = Seesaw(i2c_bus, addr=0x36)

    def read(self) -> float:
        return random.randint(5, 90)


class DS18B20TemperatureSensor(TemperatureSensor):
    """Measures temperature"""
    def __init__(self) -> None:
        super().__init__()
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28-*')[0]  # Folder czujnika
        self.device_file = device_folder + '/w1_slave'
        
    def read_temp_raw(self):
        with open(self.device_file, 'r') as f:
            lines = f.readlines()
        return lines

    def read(self) -> float:
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c


class BH1750LightSensor(LightSensor):
    """Measures light"""
    def __init__(self) -> None:
        super().__init__()
        # Beaglebone uses I2C bus 2
        self.bus = smbus.SMBus(2)
        self.BH1750_ADDR = 0x23
        self.CMD_READ = 0x10

    def read(self) -> float:
        data = self.bus.read_i2c_block_data(self.BH1750_ADDR, self.CMD_READ)
        result = (data[1] + (256 * data[0])) / 1.2
        return format(result,'.0f')
