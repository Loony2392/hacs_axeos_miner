# This file initializes the package and contains the basic setup logic for the integration.
# It registers the integration and implements the main logic for communication with the Axeos Miner API.

from homeassistant import ConfigEntry, HomeAssistant
from homeassistant.helpers import discovery

DOMAIN = "axeos_miner"

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Axeos Miner integration."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry for Axeos Miner."""
    hass.data[DOMAIN][entry.entry_id] = entry.data
    await discovery.async_load_platform(hass, "sensor", DOMAIN, {}, entry)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await discovery.async_unload_platform(hass, "sensor", entry)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok