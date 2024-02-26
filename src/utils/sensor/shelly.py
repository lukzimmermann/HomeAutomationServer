import requests
from src.utils.sensor.sensor import Sensor, SensorType, Value


class Shelly(Sensor):
    def __init__(self, id: int, name: str, ip: str) -> None:
        super().__init__(id, name, ip, SensorType.SHELLY_2PM)

    def update(self) -> None:

        self.data: dict[str, Value] = []

        url = f'http://{self.ip}/rpc'
        data = {"id":0, "method":"Shelly.GetStatus"}

        response = requests.post(url, json=data)

        data = response.json()

        for i in range(2):
            channel_name = f'switch:{i}'
            dataset: dict[str, Value] = {}

            dataset['power'] = Value(data['result'][channel_name]['apower'], 'W')
            dataset['voltage'] = Value(data['result'][channel_name]['voltage'], 'V')
            dataset['current'] = Value(data['result'][channel_name]['current'], 'A')
            dataset['frequency'] = Value(data['result'][channel_name]['freq'], 'Hz')
            dataset['pf'] = Value(data['result'][channel_name]['pf'], '-')
            dataset['temperature'] = Value(data['result'][channel_name]['temperature']['tC'], '°C')

            self.data.append(dataset)
        


