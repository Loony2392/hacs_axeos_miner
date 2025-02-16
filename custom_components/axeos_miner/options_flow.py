from homeassistant import config_entries
import voluptuous as vol


class AxeosMinerOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            self.config_entry.options.update(user_input)
            return self.async_create_entry(title="", data=self.config_entry.options)

        options_schema = vol.Schema({
            vol.Optional("scan_interval", default=self.config_entry.options.get("scan_interval", 10)): int,
        })

        return self.async_show_form(
            step_id="init", data_schema=options_schema
        )
