"""This test script sends a mock message to the Kafka topic."""

from connectivity.kafka_connector import KafkaConnector
from sensors.mock_sensors import (
    MockHumiditySensor,
    MockLightSensor,
    MockTemperatureSensor,
)

NUMBER_OF_MESSAGES_TO_SEND = 10

if __name__ == "__main__":
    humidity_sensor = MockHumiditySensor()
    temperature_sensor = MockTemperatureSensor()
    light_sensor = MockLightSensor()

    kafka_connector = KafkaConnector(
        "20.254.227.50:9092",
        command_callbacks={},
    )

    for i in range(NUMBER_OF_MESSAGES_TO_SEND):
        json_data = {
            "humidity": humidity_sensor.read(),
            "temperature": temperature_sensor.read(),
            "light": light_sensor.read(),
        }
        kafka_connector.send_one(bytes(str(json_data), "utf-8"))
    kafka_connector.flush()