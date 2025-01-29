"""Classes which provide mock sensor data for testing purposes."""

import random

from .abc_sensors import HumiditySensor, LightSensor, TemperatureSensor


class MockHumiditySensor(HumiditySensor):
    """A mock humidity sensor, provides random values."""

    def __init__(self) -> None:
        super().__init__()

    def read(self) -> float:
        return random.randint(5, 90)


class MockTemperatureSensor(TemperatureSensor):
    """A mock temperature sensor, provides random values."""

    def __init__(self) -> None:
        super().__init__()

    def read(self) -> float:
        return random.randint(15, 35)


class MockLightSensor(LightSensor):
    """A mock light sensor, provides random values."""

    def __init__(self) -> None:
        super().__init__()

    def read(self) -> float:
        return random.randint(0, 1000)
