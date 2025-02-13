from homeassistant.helpers.entity import Entity
import requests
from .const import API_URL

class AxeosMinerSensor(Entity):
    def __init__(self, name, sensor_type):
        self._name = name
        self._sensor_type = sensor_type
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._name}_{self._sensor_type}"

    def update(self):
        try:
            response = requests.get(f"{API_URL}/system/info")
            data = response.json()
            self._state = data.get(self._sensor_type)
        except Exception as e:
            self._state = None
            # Log the error if needed

def setup_platform(hass, config, add_entities, discovery_info=None):
    response = requests.get(f"{API_URL}/system/info")
    data = response.json()
    
    sensors = []
    for key in data.keys():
        sensors.append(AxeosMinerSensor(f"Axeos Miner {key.replace('_', ' ').title()}", key))
    
    add_entities(sensors, True)