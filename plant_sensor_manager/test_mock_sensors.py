import pytest
import random
from unittest.mock import patch
from sensors.mock_sensors import MockHumiditySensor, MockTemperatureSensor, MockLightSensor


@pytest.mark.parametrize("sensor_class, min_val, max_val", [
    (MockHumiditySensor, 5, 90),
    (MockTemperatureSensor, 15, 35),
    (MockLightSensor, 0, 1000),
])
def test_mock_sensors_range(sensor_class, min_val, max_val):
    """Test if the sensor values are within the expected range."""
    sensor = sensor_class()
    for _ in range(100):
        value = sensor.read()
        assert min_val <= value <= max_val, f"{sensor_class.__name__} value {value} out of range"


@pytest.mark.parametrize("sensor_class, mock_value", [
    (MockHumiditySensor, 50),
    (MockTemperatureSensor, 25),
    (MockLightSensor, 500),
])
def test_mock_sensors_fixed_value(sensor_class, mock_value):
    """Test if the sensors return the mocked value when patched."""
    with patch("random.randint", return_value=mock_value):
        sensor = sensor_class()
        assert sensor.read() == mock_value, f"{sensor_class.__name__} did not return the expected mocked value"


if __name__ == "__main__":
    pytest.main()
