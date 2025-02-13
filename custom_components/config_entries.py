from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
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
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
