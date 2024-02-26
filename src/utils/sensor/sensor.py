from enum import Enum
import threading


class Value():
    def __init__(self, value: float, unit: str) -> None:
        self. value: float = value
        self.unit: str = unit
    
    def __repr__(self) -> str:
        return f'{self.value} {self.unit}'
    


# Define an enumeration class called Color
class SensorType(Enum):
    SHELLY_2PM = 'SHELLY_2PM'

class Sensor():
    def __init__(self, id: int, name: str, ip: str, type: SensorType) -> None:
        self.id: int = id
        self.name: str = name
        self.ip: str = ip
        self.type: SensorType = type
        self.data = list[dict[str: Value]]

        self.thread = None
        self.stop_event = threading.Event()
        self.listeners = []
        self.event = threading.Event()

    def update(self) -> None:
        raise NotImplementedError("Subclasses must implement this function")
    
    def recording(self, log_interval: int, collection_interval: int) -> None:
        raise NotImplementedError("Subclasses must implement this function")

    def get_data(self) -> dict[str: Value]:
        self.update()
        return self.data
    
    def add_listener(self, listener):
        self.listeners.append(listener)
    
    def notify_listener(self, data: dict[str: Value]) -> None:
        for listener in self.listeners:
            listener.new_data_available(data)
    
    def start_recording(self, log_interval: int, collection_interval: int) -> None:
        self.thread = threading.Thread(target=self.recording, args=(log_interval, collection_interval))
        self.thread.start()
    
    def stop_recording(self) -> None:
        if self.thread is not None and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()

    def __repr__(self) -> str:
        return f'{self.id}. {self.name}'