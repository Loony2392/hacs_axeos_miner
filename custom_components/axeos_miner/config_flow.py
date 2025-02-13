from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class AxeosMinerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Axeos Miner."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Axeos Miner", data=user_input)

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Optional("scan_interval", default=15): int,  # Scan-Intervall in Sekunden
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_options(self, user_input=None):
        """Handle the options step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional("scan_interval", default=15): int,  # Scan-Intervall in Sekunden
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
                vol.Optional("scan_interval", default=self.config_entry.options.get("scan_interval", 15)): int,
            })

            return self.async_show_form(
                step_id="init", data_schema=options_schema
            )