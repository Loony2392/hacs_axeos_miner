# This file initializes the package and contains the basic setup logic for the integration.
# It registers the integration and implements the main logic for communication with the Axeos Miner API.

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
import logging
import aiohttp
from .const import DOMAIN

VERSION = "1.0.0"  # Aktuelle Version der Integration
UPDATE_URL = "https://api.github.com/repos/Loony2392/hacs_axeos_miner/releases/latest"

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Axeos Miner component."""
    hass.data.setdefault(DOMAIN, {})
    await check_for_updates(hass)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Axeos Miner from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def check_for_updates(hass: HomeAssistant):
    """Check if there is a new version of the integration available."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(UPDATE_URL) as response:
                response.raise_for_status()
                latest_release = await response.json()
                latest_version = latest_release["tag_name"]

                if VERSION < latest_version:
                    _LOGGER.warning(
                        "A new version of Axeos Miner integration is available: %s. You are currently using version: %s",
                        latest_version,
                        VERSION,
                    )
        except aiohttp.ClientError as e:
            _LOGGER.error("Error checking for updates: %s", e)