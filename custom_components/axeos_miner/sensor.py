import aiohttp
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    CONF_HOST,
    UnitOfPower,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfTemperature,
    UnitOfFrequency,
    PERCENTAGE,
    UnitOfTime,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, UPDATE_URL, VERSION

_LOGGER = logging.getLogger(__name__)

API_URL_TEMPLATE = "http://{}/api/system/info"

SENSOR_TYPES = {
    "power": ["Power", UnitOfPower.WATT, "mdi:flash", "power"],
    "voltage": ["Voltage", "mV", "mdi:flash", "voltage"],
    "current": ["Current", "mA", "mdi:current-ac", "current"],
    "temp": ["Temperature", UnitOfTemperature.CELSIUS, "mdi:thermometer", "temperature"],
    "vrTemp": ["VR Temperature", UnitOfTemperature.CELSIUS, "mdi:thermometer", "temperature"],
    "hashRate": ["Hash Rate", "MH/s", "mdi:chart-line", None],
    "frequency": ["Frequency", UnitOfFrequency.HERTZ, "mdi:wave", None],
    "fanspeed": ["Fan Speed", PERCENTAGE, "mdi:fan", None],
    "fanrpm": ["Fan RPM", "rpm", "mdi:fan", None],
    "uptimeSeconds": ["Uptime", UnitOfTime.SECONDS, "mdi:clock", None],
    "freeHeap": ["Free Heap", "bytes", "mdi:memory", None],
    "coreVoltage": ["Core Voltage", UnitOfElectricPotential.VOLT, "mdi:flash", "voltage"],
    "coreVoltageActual": ["Core Voltage Actual", UnitOfElectricPotential.VOLT, "mdi:flash", "voltage"],
    "ssid": ["SSID", None, "mdi:wifi", None],
    "macAddr": ["MAC Address", None, "mdi:network", None],
    "hostname": ["Hostname", None, "mdi:server", None],
    "wifiStatus": ["WiFi Status", None, "mdi:wifi", None],
    "sharesAccepted": ["Shares Accepted", None, "mdi:check", None],
    "sharesRejected": ["Shares Rejected", None, "mdi:close", None],
    "asicCount": ["ASIC Count", None, "mdi:chip", None],
    "smallCoreCount": ["Small Core Count", None, "mdi:chip", None],
    "ASICModel": ["ASIC Model", None, "mdi:chip", None],
    "stratumURL": ["Stratum URL", None, "mdi:link", None],
    "fallbackStratumURL": ["Fallback Stratum URL", None, "mdi:link", None],
    "stratumPort": ["Stratum Port", None, "mdi:link", None],
    "fallbackStratumPort": ["Fallback Stratum Port", None, "mdi:link", None],
    "stratumUser": ["Stratum User", None, "mdi:account", None],
    "fallbackStratumUser": ["Fallback Stratum User", None, "mdi:account", None],
    "version": ["Version", None, "mdi:information", None],
    "idfVersion": ["IDF Version", None, "mdi:information", None],
    "boardVersion": ["Board Version", None, "mdi:information", None],
    "runningPartition": ["Running Partition", None, "mdi:information", None],
    "flipscreen": ["Flip Screen", None, "mdi:rotate-3d", None],
    "overheat_mode": ["Overheat Mode", None, "mdi:thermometer-alert", None],
    "invertscreen": ["Invert Screen", None, "mdi:rotate-3d", None],
    "invertfanpolarity": ["Invert Fan Polarity", None, "mdi:fan", None],
    "autofanspeed": ["Auto Fan Speed", None, "mdi:fan", None],
    "changelog": ["Changelog", None, "mdi:information", None],
    # Add other sensor types as needed
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Axeos Miner sensors based on a config entry."""
    host = entry.data[CONF_HOST]
    scan_interval = entry.options.get("scan_interval", 60)  # Standard-Scan-Intervall ist 60 Sekunden
    sensors = await fetch_sensors(hass, host, scan_interval)
    async_add_entities(sensors, True)

async def async_unload_entry(hass, entry):
    """Unload Axeos Miner sensors based on a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")

async def fetch_sensors(hass, host, scan_interval):
    """Fetch sensor data from the Axeos Miner API and create sensor entities."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL_TEMPLATE.format(host)) as response:
                response.raise_for_status()
                data = await response.json()
                hostname = data.get("hostname", host)  # Verwende den Hostnamen aus den Daten oder den Hostnamen aus der Konfiguration
                _LOGGER.debug("Fetched data: %s", data)
                sensors = [AxeosMinerSensor(hostname, key, value, scan_interval) for key, value in data.items() if key in SENSOR_TYPES]
                
                # Füge die Versions- und Changelog-Sensoren hinzu
                sensors.append(AxeosMinerVersionSensor())
                sensors.append(AxeosMinerChangelogSensor())
                
                return sensors
    except aiohttp.ClientError as e:
        _LOGGER.error("Error fetching data from %s: %s", host, e)
        return [AxeosMinerSensor(host, "error", f"Error: {e}", scan_interval)]

class AxeosMinerSensor(SensorEntity):
    """Representation of an Axeos Miner sensor."""

    def __init__(self, hostname, key, initial_state, scan_interval):
        """Initialize the sensor."""
        self._hostname = hostname
        self._key = key
        self._name = f"{hostname} {SENSOR_TYPES[key][0]}"
        self._state = initial_state
        self._unit = SENSOR_TYPES[key][1]
        self._icon = SENSOR_TYPES[key][2]
        self._device_class = SENSOR_TYPES[key][3]
        self._unique_id = f"{hostname}_{key}"
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

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        return "measurement"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if isinstance(self._state, (int, float)):
            return round(self._state, 2)  # Runde auf 2 Nachkommastellen
        if isinstance(self._state, str) and len(self._state) > 255:
            return self._state[:255]  # Begrenze die Länge des Zustands auf 255 Zeichen
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL_TEMPLATE.format(self._hostname)) as response:
                    response.raise_for_status()
                    data = await response.json()
                    _LOGGER.debug("Fetched data for %s: %s", self._key, data)
                    self._state = data.get(self._key, "unknown")
                    if self._state is None:
                        self._state = "unknown"
                    if isinstance(self._state, str) and len(self._state) > 255:
                        self._state = self._state[:255]  # Begrenze die Länge des Zustands auf 255 Zeichen
        except aiohttp.ClientError as e:
            _LOGGER.error("Error updating sensor %s: %s", self._name, e)
            self._state = f"Error: {e}"

class AxeosMinerVersionSensor(SensorEntity):
    """Representation of the Axeos Miner version sensor."""

    def __init__(self):
        """Initialize the version sensor."""
        self._name = "Axeos Miner Version"
        self._state = VERSION
        self._icon = "mdi:information"
        self._unique_id = "axeos_miner_version"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return self._unique_id

class AxeosMinerChangelogSensor(SensorEntity):
    """Representation of the Axeos Miner changelog sensor."""

    def __init__(self):
        """Initialize the changelog sensor."""
        self._name = "Axeos Miner Changelog"
        self._state = None
        self._icon = "mdi:information"
        self._unique_id = "axeos_miner_changelog"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return self._unique_id

    async def async_update(self):
        """Fetch new changelog data."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(UPDATE_URL) as response:
                    response.raise_for_status()
                    latest_release = await response.json()
                    changelog = latest_release.get("body", "No changelog available")
                    self._state = changelog
        except aiohttp.ClientError as e:
            _LOGGER.error("Error fetching changelog: %s", e)
            self._state = f"Error: {e}"