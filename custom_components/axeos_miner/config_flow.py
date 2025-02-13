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
            # Hier kannst du eine Funktion hinzufügen, um den Hostnamen vom Gerät abzurufen
            hostname = await self.fetch_hostname(host)
            return self.async_create_entry(title=hostname, data=user_input)

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Optional("scan_interval", default=60): int,  # Scan-Intervall in Sekunden
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
            return host

    async def async_step_options(self, user_input=None):
        """Handle the options step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional("scan_interval", default=60): int,  # Scan-Intervall in Sekunden
        })

        return self.async_show_form(
            step_id="options", data_schema=options_schema
        )

    @staticmethod
    @config_entries.HANDLERS.register(DOMAIN)
    class AxeosMinerOptionsFlowHandler(config_entries.OptionsFlow):
        """Handle Axeos Miner options."""

        def __init__(self, config_entry):
            """Initialize options flow."""
            self.config_entry = config_entry

        async def async_step_init(self, user_input=None):
            """Manage the options."""
            if user_input is not None:
                self.config_entry.options.update(user_input)
                return self.async_create_entry(title="", data=self.config_entry.options)

            options_schema = vol.Schema({
                vol.Optional("scan_interval", default=self.config_entry.options.get("scan_interval", 60)): int,
            })

            return self.async_show_form(
                step_id="init", data_schema=options_schema
            )