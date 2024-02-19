from sensor_handler import SensorHandler


sensor_handler = SensorHandler()

for sensor in sensor_handler.sensor_list:
    for channel in sensor.channels:
        print(channel)
