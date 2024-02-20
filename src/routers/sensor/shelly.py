import requests
import threading
import time
import numpy as np
from enum import Enum

class Type(Enum):
    VALUE1 = "1PM"
    VALUE2 = "2PM"

class Data():
    def __init__(self) -> None:
        self.sensor_id: int
        self.channel: int
        self.status: bool
        self.power: float
        self.voltage: float
        self.current: float
        self.frequency: float
        self.pf: float
        self.temperature: float

class Shelly:
    def __init__(self, id: int, ip: str, type:Type) -> None:
        self.id = id
        self.ip = ip
        self.type = type

        if self.type == 'SHELLY_1PM': self.number_of_channels = 1
        if self.type == 'SHELLY_2PM': self.number_of_channels = 2

        self.dataset: list[Data] = []
        self.average_dataset = []

        self.thread = None
        self.stop_event = threading.Event()

        self.listeners = []
        self.event = threading.Event()

    def get_raw_data(self):
        url = f'http://{self.ip}/rpc'
        data = {"id":0, "method":"Shelly.GetStatus"}

        response = requests.post(url, json=data)

        return response.json()

    def update_data(self) -> None:
        data = self.get_raw_data()

        dataset = []
        for i in range(self.number_of_channels):
            channel_name = f'switch:{i}'
            channel = Data()
            channel.sensor_id = -1
            channel.channel = i
            channel.status = data['result'][channel_name]['output']
            channel.power = data['result'][channel_name]['apower']
            channel.voltage = data['result'][channel_name]['voltage']
            channel.current = data['result'][channel_name]['current']
            channel.frequency = data['result'][channel_name]['freq']
            channel.pf = data['result'][channel_name]['pf']
            channel.temperature = data['result'][channel_name]['temperature']['tC']
            dataset.append(channel)
        
        self.dataset = dataset

    def get_data(self) -> list[Data]:
        self.update_data()
        return self.dataset

    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify_listeners(self, dataset: list[Data]):
        for listener in self.listeners:
            listener.new_data_available(dataset)

    def recording(self, log_interval: int, collection_interval: int):
        while not self.stop_event.is_set():
            power_avg = [[] for _ in range(self.number_of_channels)]
            voltage_avg = [[] for _ in range(self.number_of_channels)]
            current_avg = [[] for _ in range(self.number_of_channels)]
            frequency_avg = [[] for _ in range(self.number_of_channels)]
            pf_avg = [[] for _ in range(self.number_of_channels)]
            temperature_avg = [[] for _ in range(self.number_of_channels)]

            for _ in range(int(log_interval/collection_interval)):
                self.update_data()
                
                for channel_index in range(self.number_of_channels):
                    power_avg[channel_index].append(self.dataset[channel_index].power)
                    voltage_avg[channel_index].append(self.dataset[channel_index].voltage)
                    current_avg[channel_index].append(self.dataset[channel_index].current)
                    frequency_avg[channel_index].append(self.dataset[channel_index].frequency)
                    pf_avg[channel_index].append(self.dataset[channel_index].pf)
                    temperature_avg[channel_index].append(self.dataset[channel_index].temperature)

                time.sleep(collection_interval)

            mean_dataset: list[Data] = []

            for index in range(self.number_of_channels):
                mean_data = Data()

                mean_data.sensor_id = self.id
                mean_data.channel = index
                mean_data.power = np.round(np.mean(power_avg[index]),1)
                mean_data.voltage = np.round(np.mean(voltage_avg[index]),2)
                mean_data.current = np.round(np.mean(current_avg[index]),3)
                mean_data.frequency = np.round(np.mean(frequency_avg[index]),2)
                mean_data.pf = np.round(np.mean(pf_avg[index]),2)
                mean_data.temperature = np.round(np.mean(temperature_avg[index]),1)
                
                mean_dataset.append(mean_data)

            self.notify_listeners(mean_dataset)

    def start_recording(self, log_interval: int, collection_interval: int) -> None:
        self.thread = threading.Thread(target=self.recording, args=(log_interval, collection_interval))
        self.thread.start()

    def stop_recording(self) -> None:
        if self.thread is not None and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()
