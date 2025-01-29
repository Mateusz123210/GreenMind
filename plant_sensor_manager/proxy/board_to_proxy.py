#!/usr/bin/python3
import os
import glob
import time
import board
import socket
import json
import smbus
from adafruit_seesaw.seesaw import Seesaw


def send_json(data, ip, port):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the receiver
            s.connect((ip, port))
            # Convert data to JSON and send it
            json_data = json.dumps(data)
            s.sendall(json_data.encode('utf-8'))
            print("JSON data sent successfully.")
    except Exception as e:
        print(f"Error sending JSON: {e}")

class BH1750(object):

   def __init__(self):
       # Rev 2 of Raspberry Pi and all newer use bus 1
       self.bus = smbus.SMBus(2)

   def light(self):
       data = self.bus.read_i2c_block_data(BH1750_ADDR, CMD_READ)
       result = (data[1] + (256 * data[0])) / 1.2
       return format(result,'.0f')


# initialization for temp sensor
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-*')[0]  # Folder czujnika
device_file = device_folder + '/w1_slave'

# initialization for soil sensor
i2c_bus = board.I2C()  # uses board.SCL and board.SDA
try:
    ss = Seesaw(i2c_bus, addr=0x36)
except:
    ss = None

# initialization for light sensor
BH1750_ADDR = 0x23
CMD_READ = 0x10
obj = BH1750()

def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# -------------------------------------

# -----------------
try:        
    light = obj.light()
    time.sleep(1) 
    temp = read_temp()
    time.sleep(1)
    if ss:
        moisture = ss.moisture_read()
    else:
        moisture = 0
    time.sleep(1)
    sensor_values = {"timestamp": int(time.time()), "id": 1, "temperature": temp, "illuminance": int(light), "moisture": int(moisture)}
    send_json(sensor_values, "192.168.7.1", 5000)
    msg = str(sensor_values)
except FileNotFoundError:
    msg = 'ERROR: Please enable I2C.'
except OSError:
    msg = 'ERROR: I2C device not found. Please check BH1750 wiring.'
finally:
    print(msg)
    with open("/home/debian/plant_poc/sensor_data_monstera.txt", "a") as myfile:
        myfile.write(msg)
        myfile.write("\n")