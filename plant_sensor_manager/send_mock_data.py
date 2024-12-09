"""This test script sends a mock message to the Kafka topic."""

from connectivity.kafka_connector import KafkaConnector
from sensors.mock_sensors import (
    MockHumiditySensor,
    MockLightSensor,
    MockTemperatureSensor,
)

NUMBER_OF_MESSAGES_TO_SEND = 5

if __name__ == "__main__":
    #for first sensors device 
    token = "jGFuzDrYkEqXr7ucOlQeHTwVAAVF0wmFR9RghZiPzj7heuaFqyM4ofEi2pxJWtVi"
    #for second sensors device
    # token = "2QB9k2YHmibrLYbrgLLiUqxjWTi3JfrCIMiZtkEibW3yZAp6Xoqy8EKDyPi61RtS"

    humidity_sensor = MockHumiditySensor()
    temperature_sensor = MockTemperatureSensor()
    light_sensor = MockLightSensor()

    kafka_connector = KafkaConnector(
        "20.254.227.50:9092",
        command_callbacks={},
    )

    for i in range(NUMBER_OF_MESSAGES_TO_SEND):
        json_data = {
            "token": token,
            "humidity": humidity_sensor.read(),
            "temperature": temperature_sensor.read(),
            "light": light_sensor.read(),
        }
        kafka_connector.send_one(bytes(str(json_data), "utf-8"))
    kafka_connector.flush()
