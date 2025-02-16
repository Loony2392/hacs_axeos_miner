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
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity, UpdateFailed
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
    """Set up AxeOS Miner sensors based on a config entry."""
    host = entry.data[CONF_HOST]
    scan_interval = entry.options.get("scan_interval", 60)  # Standard-Scan-Intervall ist 60 Sekunden

    coordinator = AxeOSMinerDataUpdateCoordinator(hass, host, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    sensors = [AxeOSMinerSensor(coordinator, key) for key in SENSOR_TYPES]
    async_add_entities(sensors, True)

async def async_unload_entry(hass, entry):
    """Unload AxeOS Miner sensors based on a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")


class AxeOSMinerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching AxeOS Miner data."""

    def __init__(self, hass, host, scan_interval):
        """Initialize."""
        self.host = host
        self.api_url = API_URL_TEMPLATE.format(host)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=scan_interval)

    async def _async_update_data(self):
        """Fetch data from AxeOS Miner."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            raise UpdateFailed(f"Error fetching data: {e}")


class AxeOSMinerSensor(CoordinatorEntity, SensorEntity):
    """Representation of an AxeOS Miner sensor."""

    def __init__(self, coordinator, key):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._name = f"{coordinator.data.get('hostname', coordinator.host)} {SENSOR_TYPES[key][0]}"
        self._unit = SENSOR_TYPES[key][1]
        self._icon = SENSOR_TYPES[key][2]
        self._device_class = SENSOR_TYPES[key][3]
        self._unique_id = f"{coordinator.host}_{key}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key)

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
        value = self.coordinator.data.get(self._key)
        if isinstance(value, (int, float)):
            return round(value, 2)  # Runde auf 2 Nachkommastellen
        if isinstance(value, str) and len(value) > 255:
            return value[:255]  # Begrenze die Länge des Zustands auf 255 Zeichen
        return value
