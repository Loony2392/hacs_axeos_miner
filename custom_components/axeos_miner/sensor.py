import requests
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_HOST
from .const import DOMAIN

API_URL_TEMPLATE = "http://{}/api/system/info"

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Axeos Miner sensor based on a config entry."""
    host = entry.data[CONF_HOST]
    async_add_entities([AxeosMinerSensor(host)], True)

class AxeosMinerSensor(SensorEntity):
    """Representation of an Axeos Miner sensor."""

    def __init__(self, host):
        """Initialize the sensor."""
        self._host = host
        self._state = None
        self._name = "Axeos Miner Sensor"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor."""
        try:
            response = requests.get(API_URL_TEMPLATE.format(self._host))
            response.raise_for_status()
            data = response.json()
            self._state = data.get("state", "unknown")
        except requests.exceptions.RequestException as e:
            self._state = f"Error: {e}"