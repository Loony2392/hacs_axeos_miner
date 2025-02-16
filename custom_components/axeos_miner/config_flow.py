from homeassistant import config_entries
import voluptuous as vol
import aiohttp
from .const import DOMAIN

class AxeosMinerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Axeos Miner."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            host = user_input["host"]
            hostname = await self.fetch_hostname(host)
            if hostname:
                return self.async_create_entry(title=hostname, data=user_input)
            else:
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Optional("scan_interval", default=10): int,  # Scan-Intervall in Sekunden
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def fetch_hostname(self, host):
        """Fetch the hostname from the device."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{host}/api/system/info") as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data.get("hostname", host)
        except aiohttp.ClientError:
            return None