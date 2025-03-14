"""This test script sends a mock message to the Kafka topic."""

import time
from connectivity.kafka_connector import KafkaConnector
from sensors.mock_sensors import (
    MockHumiditySensor,
    MockLightSensor,
    MockTemperatureSensor,
)

NUMBER_OF_MESSAGES_TO_SEND = 5

if __name__ == "__main__":
    #for first sensors device 
    token = "1735684275820034ZWNFZGNXTlg2Vzl2T0xuUFNPa3JZZk9OcHpQUVlRb3JYOEpTa0RDeUJka1VsUDZ3"
    #for second sensors device
    # token = "2QB9k2YHmibrLYbrgLLiUqxjWTi3JfrCIMiZtkEibW3yZAp6Xoqy8EKDyPi61RtS"

    humidity_sensor = MockHumiditySensor()
    temperature_sensor = MockTemperatureSensor()
    light_sensor = MockLightSensor()

    kafka_connector = KafkaConnector(
        "50.85.212.131:9092",
        command_callbacks={},
    )

    for i in range(NUMBER_OF_MESSAGES_TO_SEND):
        json_data = {
            "token": token,
            "timestamp": time.time(),
            "temperature": temperature_sensor.read(),
            "illuminance": light_sensor.read(),
            "moisture": humidity_sensor.read()      
        }
        kafka_connector.send_one(bytes(str(json_data), "utf-8"))
    kafka_connector.flush()
