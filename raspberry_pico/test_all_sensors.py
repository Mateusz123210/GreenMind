import machine, onewire, ds18x20, time, utime

ds_pin = machine.Pin(15)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
# Analog input pin for the TEMT6000 sensor
temt6000_pin = machine.ADC(26)
humidity_pin = machine.ADC(27)

def read_light_intensity():
    light_value = temt6000_pin.read_u16()
    light_percentage = (light_value / 65535.0) * 1000
    return light_percentage

def read_humidity():
    value = humidity_pin.read_u16()
    #light_percentage = ((value / 65535.0)-((1/3.3)/65535.0))*2.3/2 * 100
    light_percentage =(value / 65535.0)
    return light_percentage

roms = ds_sensor.scan()
print('Found DS devices: ', roms)

while True:
  ds_sensor.convert_temp()
  time.sleep_ms(750)
  for rom in roms:
    print(rom)
    tempC = ds_sensor.read_temp(rom)
    tempF = tempC * (9/5) +32
    print('temperature (ºC):', "{:.2f}".format(tempC))
    print('temperature (ºF):', "{:.2f}".format(tempF))
    print()
    light = read_light_intensity()
    humidity= read_humidity()
    print("Light Intensity: {:.0f} lux".format(light))
    print("Hum: {:.2f}".format(humidity))
  time.sleep(0.1)
