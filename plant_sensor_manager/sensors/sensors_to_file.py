import time

from real_sensors import DS18B20TemperatureSensor, BH1750LightSensor, StemmaHumiditySensor

temperature_sensor = DS18B20TemperatureSensor()
light_sensor = BH1750LightSensor()
humidity_sensor = StemmaHumiditySensor()


try:        
    light = light_sensor.read()
    time.sleep(1) 
    temp = temperature_sensor.read()
    time.sleep(1)
    moisture = humidity_sensor.read()
    time.sleep(1)
    sensor_values = {"timestamp": int(time.time()), "id": 1, "temperature": temp, "illuminance": int(light), "moisture": int(moisture)}
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
