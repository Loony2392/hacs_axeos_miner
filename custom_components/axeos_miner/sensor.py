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
    "power": ["Power", UnitOfPower.WATT, "mdi:flash"],
    "voltage": ["Voltage", UnitOfElectricPotential.VOLT, "mdi:flash"],
    "current": ["Current", UnitOfElectricCurrent.AMPERE, "mdi:current-ac"],
    "temp": ["Temperature", UnitOfTemperature.CELSIUS, "mdi:thermometer"],
    "vrTemp": ["VR Temperature", UnitOfTemperature.CELSIUS, "mdi:thermometer"],
    "hashRate": ["Hash Rate", UnitOfInformation.MEGABITS, "mdi:chart-line"],
    "frequency": ["Frequency", UnitOfFrequency.HERTZ, "mdi:wave"],
    "fanspeed": ["Fan Speed", PERCENTAGE, "mdi:fan"],
    "fanrpm": ["Fan RPM", "mdi:fan"],
    "uptimeSeconds": ["Uptime", UnitOfTime.SECONDS, "mdi:clock"],
    "freeHeap": ["Free Heap", "bytes", "mdi:memory"],
    "coreVoltage": ["Core Voltage", UnitOfElectricPotential.VOLT, "mdi:flash"],
    "coreVoltageActual": ["Core Voltage Actual", UnitOfElectricPotential.VOLT, "mdi:flash"],
    "ssid": ["SSID", None, "mdi:wifi"],
    "macAddr": ["MAC Address", None, "mdi:network"],
    "hostname": ["Hostname", None, "mdi:server"],
    "wifiStatus": ["WiFi Status", None, "mdi:wifi"],
    "sharesAccepted": ["Shares Accepted", None, "mdi:check"],
    "sharesRejected": ["Shares Rejected", None, "mdi:close"],
    "asicCount": ["ASIC Count", None, "mdi:chip"],
    "smallCoreCount": ["Small Core Count", None, "mdi:chip"],
    "ASICModel": ["ASIC Model", None, "mdi:chip"],
    "stratumURL": ["Stratum URL", None, "mdi:link"],
    "fallbackStratumURL": ["Fallback Stratum URL", None, "mdi:link"],
    "stratumPort": ["Stratum Port", None, "mdi:link"],
    "fallbackStratumPort": ["Fallback Stratum Port", None, "mdi:link"],
    "stratumUser": ["Stratum User", None, "mdi:account"],
    "fallbackStratumUser": ["Fallback Stratum User", None, "mdi:account"],
    "version": ["Version", None, "mdi:information"],
    "idfVersion": ["IDF Version", None, "mdi:information"],
    "boardVersion": ["Board Version", None, "mdi:information"],
    "runningPartition": ["Running Partition", None, "mdi:information"],
    "flipscreen": ["Flip Screen", None, "mdi:rotate-3d"],
    "overheat_mode": ["Overheat Mode", None, "mdi:thermometer-alert"],
    "invertscreen": ["Invert Screen", None, "mdi:rotate-3d"],
    "invertfanpolarity": ["Invert Fan Polarity", None, "mdi:fan"],
    "autofanspeed": ["Auto Fan Speed", None, "mdi:fan"],
    "fanrpm": ["Fan RPM", "rpm", "mdi:fan"],
    # Add other sensor types as needed
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Axeos Miner sensors based on a config entry."""
    host = entry.data[CONF_HOST]
    scan_interval = entry.data.get("scan_interval", 60)  # Standard-Scan-Intervall ist 60 Sekunden
    sensors = await hass.async_add_executor_job(fetch_sensors, host, scan_interval)
    async_add_entities(sensors, True)

async def async_unload_entry(hass, entry):
    """Unload Axeos Miner sensors based on a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")

def fetch_sensors(host, scan_interval):
    """Fetch sensor data from the Axeos Miner API and create sensor entities."""
    try:
        response = requests.get(API_URL_TEMPLATE.format(host))
        response.raise_for_status()
        data = response.json()
        return [AxeosMinerSensor(host, key, value, scan_interval) for key, value in data.items() if key in SENSOR_TYPES]
    except requests.exceptions.RequestException as e:
        return [AxeosMinerSensor(host, "error", f"Error: {e}", scan_interval)]

class AxeosMinerSensor(SensorEntity):
    """Representation of an Axeos Miner sensor."""

    def __init__(self, host, key, initial_state, scan_interval):
        """Initialize the sensor."""
        self._host = host
        self._key = key
        self._name = f"Axeos Miner {SENSOR_TYPES[key][0]}"
        self._state = initial_state
        self._unit = SENSOR_TYPES[key][1]
        self._icon = SENSOR_TYPES[key][2]
        self._unique_id = f"{host}_{key}"
        self._scan_interval = scan_interval

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
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return self._unique_id

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @property
    def scan_interval(self):
        """Return the scan interval."""
        return self._scan_interval

    def update(self):
        """Fetch new state data for the sensor."""
        try:
            response = requests.get(API_URL_TEMPLATE.format(self._host))
            response.raise_for_status()
            data = response.json()
            self._state = data.get(self._key, "unknown")
        except requests.exceptions.RequestException as e:
            self._state = f"Error: {e}"