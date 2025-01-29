from abc import ABC, abstractmethod


class Sensor(ABC):
    # @abstractmethod
    # def start_measuring(self):
    #     pass

    @abstractmethod
    def read(self):
        pass


class HumiditySensor(Sensor):
    def __init__(self) -> None:
        super().__init__()
        self.humidity = 0

    def read(self):
        return self.humidity


class TemperatureSensor(Sensor):
    def __init__(self) -> None:
        super().__init__()
        self.temperature = 0

    def read(self):
        return self.temperature


class LightSensor(Sensor):
    def __init__(self) -> None:
        super().__init__()
        self.light = 0

    def read(self):
        return self.light
