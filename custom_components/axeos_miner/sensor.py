import requests
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    CONF_HOST,
    UnitOfPower,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfTemperature,
    UnitOfFrequency,
    PERCENTAGE,
    UnitOfInformation,
    UnitOfTime,
)
from .const import DOMAIN

API_URL_TEMPLATE = "http://{}/api/system/info"

SENSOR_TYPES = {
    "power": ["Power", UnitOfPower.WATT],
    "voltage": ["Voltage", UnitOfElectricPotential.VOLT],
    "current": ["Current", UnitOfElectricCurrent.AMPERE],
    "temp": ["Temperature", UnitOfTemperature.CELSIUS],
    "vrTemp": ["VR Temperature", UnitOfTemperature.CELSIUS],
    "hashRate": ["Hash Rate", UnitOfInformation.MEGABITS],
    "frequency": ["Frequency", UnitOfFrequency.HERTZ],
    "fanspeed": ["Fan Speed", PERCENTAGE],
    "fanrpm": ["Fan RPM", "rpm"],
    "uptimeSeconds": ["Uptime", UnitOfTime.SECONDS],
    # Add other sensor types as needed
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Axeos Miner sensors based on a config entry."""
    host = entry.data[CONF_HOST]
    sensors = await hass.async_add_executor_job(fetch_sensors, host)
    async_add_entities(sensors, True)

async def async_unload_entry(hass, entry):
    """Unload Axeos Miner sensors based on a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")

def fetch_sensors(host):
    """Fetch sensor data from the Axeos Miner API and create sensor entities."""
    try:
        response = requests.get(API_URL_TEMPLATE.format(host))
        response.raise_for_status()
        data = response.json()
        return [AxeosMinerSensor(host, key, value) for key, value in data.items() if key in SENSOR_TYPES]
    except requests.exceptions.RequestException as e:
        return [AxeosMinerSensor(host, "error", f"Error: {e}")]

class AxeosMinerSensor(SensorEntity):
    """Representation of an Axeos Miner sensor."""

    def __init__(self, host, key, initial_state):
        """Initialize the sensor."""
        self._host = host
        self._key = key
        self._name = f"Axeos Miner {SENSOR_TYPES[key][0]}"
        self._state = initial_state
        self._unit = SENSOR_TYPES[key][1]
        self._unique_id = f"{host}_{key}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of the sensor."""
        return self._unit

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return self._unique_id

    def update(self):
        """Fetch new state data for the sensor."""
        try:
            response = requests.get(API_URL_TEMPLATE.format(self._host))
            response.raise_for_status()
            data = response.json()
            self._state = data.get(self._key, "unknown")
        except requests.exceptions.RequestException as e:
            self._state = f"Error: {e}"