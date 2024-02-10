import math
import requests
import os
import ast
from dotenv import load_dotenv
from enum import Enum
import threading
import time
import urllib3
import uuid
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colormath.color_objects import xyYColor, sRGBColor
from colormath.color_conversions import convert_color


urllib3.disable_warnings(InsecureRequestWarning)

class HueEndPointTyp(Enum):
    ROOM = 'room'
    LIGHT = 'light'
    GROUP = 'grouped_light'


class Light:
    def __init__(self, rid:str, name = '', on=False) -> None:
        self.id = -1
        self.rid = rid
        self.name = name
        self.on = on
        self.brightness = 100
        self.color = [255, 255, 200]
        self.coordinate = [0,0,0]

    def __str__(self) -> str:
        return f'{self.id}\t{self.name}'

class Room():
    def __init__(self, id: str, name: str, on: bool, lights: [Light]) -> None:
        self.id = id
        self.name = name
        self.on = on
        self.lights = lights

    def __str__(self) -> str:
        return f'{self.id}\t{self.name}'

load_dotenv()

class Hue:
    rooms: [Room] = []
    threads = {}

    def __init__(self) -> None:
        rooms = self.get_api_call_hue(HueEndPointTyp.ROOM)

        for room in rooms:
            if(room['type'] == 'room'):
                id = room['services'][0]['rid']
                name = room['metadata']['name']
                lights: [Light] = []
                for light in room["children"]:
                    lights.append(Light(light['rid']))
                self.rooms.append(Room(id, name, False, lights))
        
        self.update_rooms()
        coordinates = self.read_coordinate_file()

        for room in self.rooms:
            for light in room.lights:
                for coor in coordinates:
                    if coor == light.id:
                        light.coordinate = coordinates[light.id]

    def update_rooms(self):
        lights = self.get_api_call_hue(HueEndPointTyp.LIGHT)

        for light in lights:
            for room in self.rooms:
                for room_light in room.lights:
                    if light['owner']['rid'] == room_light.rid:
                        room_light.id = light['id']
                        room_light.name = light['metadata']['name']
                        room_light.on = light['on']['on']
                        if 'dimming' in light:
                            room_light.brightness = light['dimming']['brightness']
                        if 'color' in light and 'xy' in light['color']:
                            room_light.color = self.convert_xy_to_rgb(light['color']['xy']['x'], light['color']['xy']['y'])
                        if room_light.on: room.on = True
                        else: room.on = False
                            
    def read_coordinate_file(self):
        coordinates = {}
        with open('light_position.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                element = line.split(':')
                coordinates[element[0]] = ast.literal_eval(element[1])
        
        return coordinates

    def get_rooms_from_hue(self):
        self.update_rooms()
        return self.rooms
    
    def set_room(self, room_id):
        self.update_rooms()
        set_state = False

        for room in self.rooms:
            if room.id == room_id:
                set_state = room.on

        body = {
            "on": {
                "on": not set_state
            },
            "dimming": {
                "brightness": 100
            }
        }

        return self.put_api_call_hue(HueEndPointTyp.GROUP, room_id, body)
    
    def cinema_mode(self):
        room_id = ''

        for room in self.rooms:
            if room.name == 'Wohnzimmer':
                room_id = room.id
        
        body = {
            "on": {
                "on": True
            },
            "dimming": {
                "brightness": 25
            }
        }

        if room_id != '':
            return self.put_api_call_hue(HueEndPointTyp.GROUP, room_id, body)

    def dimm_light(self, light_id, duration, brightness):
        unique_id = str(uuid.uuid4())
        print(unique_id)
        exit_flag = threading.Event()
        thread = threading.Thread(target=self.dimm_light_thread, name=unique_id,
                                  args=(light_id, duration, brightness, exit_flag))
        self.threads[unique_id] = (thread, exit_flag)
        thread.start()
        return {"automation_id": unique_id}
        
    def dimm_light_thread(self, light_id, duration, brightness, exit_flag):
        MIN_INTERVAL_TIME =  1
        interval_time = -1
        step_size = 1

        if brightness == -1:
            light_state = self.get_light_state(light_id)
            brightness = light_state.brightness

        if brightness <= 0:
            print('Cant dimm if brightness less than 1!')
            return 

        while not exit_flag.is_set():
            while True:
                interval_time = duration / (brightness / step_size)
                if interval_time > MIN_INTERVAL_TIME:
                    break
                else:
                    step_size += 1

            self.set_light(light_id, True, brightness)

            has_changed = False

            while brightness >= 0 and not exit_flag.is_set():
                self.set_light(light_id, True, brightness)

                time.sleep(interval_time)

                light_state = self.get_light_state(light_id)
                brightness_difference = math.fabs(light_state.brightness - brightness)
                if brightness_difference > 5 or not light_state.on:
                    print('stop automation, state has changed...')
                    has_changed = True
                    break

                brightness -= step_size

            if not has_changed and brightness <= 0 and not exit_flag.is_set():
                self.set_light(light_id, False, 0)
                self.set_light(light_id, False, 100)

            exit_flag.set()

    def set_light(self, id:str, state: bool, brightness:int = -1):
        body = {}

        if brightness == -1:
            body = {
                    "on": {
                        "on": state
                    }
                }
        else:
            body = {
                "on": {
                    "on": state
                },
                "dimming": {
                    "brightness": brightness
                }
            }

        self.put_api_call_hue(HueEndPointTyp.LIGHT, id, body)

    def get_automation_state(self, automation_id=0):
        alive_threads = {}

        # Remove terminated threads from the dictionary
        for thread_name, thread_info in list(self.threads.items()):
            thread, exit_flag = thread_info
            if thread.is_alive():
                alive_threads[thread_name] = thread_info

        self.threads = alive_threads  # Update the threads dictionary

        if not self.threads:
            return {"status": "no automation running"}

        if automation_id == 0:
            # Check the state of all threads
            response_json_array = [{"id": thread_name, "is_alive": thread_info[0].is_alive()} for thread_name, thread_info in self.threads.items()]
        else:
            # Check the state of a specific thread
            response_json_array = {"status": "alive"} if str(automation_id) in self.threads else [{"status": "not found"}]

        return response_json_array
    
    def stop_automation(self, automation_id):
        print(f"Attempting to stop automation: {automation_id}")
        print(f"Current threads: {self.threads}")

        if automation_id in self.threads:
            thread, exit_flag = self.threads[automation_id]
            exit_flag.set()  # Set the flag to signal the thread to exit
            thread.join()  # Wait for the thread to finish
            del self.threads[automation_id]
            print(f"Thread {automation_id} killed.")
            return {"status": "stopped"}

        print(f"Automation {automation_id} not found in threads.")
        return {"status": "not found"}

    def convert_xy_to_rgb(self, x: int, y: int):
        cie_color = xyYColor(x, y, 1.0)
        rgb_color = convert_color(cie_color, sRGBColor)
        r = int(max(0, min(255, rgb_color.rgb_r * 255)))
        g = int(max(0, min(255, rgb_color.rgb_g * 255)))
        b = int(max(0, min(255, rgb_color.rgb_b * 255)))
        return [r, g, b]
    
    def convert_rgb_to_xy(self, r: int, g: int, b: int):
        rgb_color = sRGBColor(r, g, b)
        cie_color = convert_color(rgb_color, xyYColor)
        x=cie_color.xyy_x
        y=cie_color.xyy_y
        return [x, y]

    def get_api_call_hue(self, endPoint: HueEndPointTyp):
        ip = os.getenv("HUE_BRIDGE_IP")
        user = os.getenv("HUE_BRIDGE_USER")
        url = f'https://{ip}/clip/v2/resource/{endPoint.value}'

        headers = {
            'hue-application-key': user
        }
        data = []
        try:
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                data = response.json()
            else:
                print(f'Request failed with status: {response.status_code}')
        except requests.exceptions.RequestException as e:
            # Handle any errors that occurred during the request
            print('Requests error:', e)

        return data['data']
    
    def put_api_call_hue(self, endPoint: HueEndPointTyp, parameter, body):
        ip = os.getenv("HUE_BRIDGE_IP")
        user = os.getenv("HUE_BRIDGE_USER")
        url = f'https://{ip}/clip/v2/resource/{endPoint.value}/{parameter}'

        headers = {
            'hue-application-key': user
        }

        print(url)

        try:
            response = requests.put(url, headers=headers, json=body, verify=False)
            print(response.json())
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f'Request failed with status: {response.status_code}')
        except requests.exceptions.RequestException as e:
            # Handle any errors that occurred during the request
            print('Requests error:', e)

    def get_light_state(self, id):
        ip = os.getenv("HUE_BRIDGE_IP")
        user = os.getenv("HUE_BRIDGE_USER")
        url = f'https://{ip}/clip/v2/resource/light/{id}'

        headers = {
            'hue-application-key': user
        }
        data = []
        try:
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                data = response.json()
            else:
                print(f'Request failed with status: {response.status_code}')
        except requests.exceptions.RequestException as e:
            # Handle any errors that occurred during the request
            print('Requests error:', e)


        light = Light(-1)
        light.id = id
        light.name = data['data'][0]['metadata']['name']
        light.on = data['data'][0]['on']['on']
        light.color = data['data'][0]
        if 'dimming' in data['data'][0]:
            light.brightness = int(data['data'][0]['dimming']['brightness'])

        return light


