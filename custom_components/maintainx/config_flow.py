import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

DOMAIN = "maintainx"

class MaintainXConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MaintainX."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """First step: choose connection type."""
        if user_input is not None:
            self.connection_type = user_input["connection_type"]
            if self.connection_type == "api":
                return await self.async_step_api()
            elif self.connection_type == "url":
                return await self.async_step_url()
            elif self.connection_type == "auth":
                return await self.async_step_auth()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("connection_type", default="api"): vol.In({
                    "api": "API Key (Admin Access)",
                    "url": "Public Request Portal URL",
                    "auth": "Username & Password"
                })
            })
        )

    async def async_step_api(self, user_input=None):
        """Form for API Key."""
        if user_input is not None:
            return self.async_create_entry(title="MaintainX (API)", data=user_input)
        return self.async_show_form(
            step_id="api",
            data_schema=vol.Schema({vol.Required("api_key"): str})
        )

    async def async_step_url(self, user_input=None):
        """Form for Public Request Portal URL."""
        if user_input is not None:
            return self.async_create_entry(title="MaintainX (Portal)", data=user_input)
        return self.async_show_form(
            step_id="url",
            data_schema=vol.Schema({vol.Required("portal_url"): str})
        )

    async def async_step_auth(self, user_input=None):
        """Form for Username and Password."""
        if user_input is not None:
            return self.async_create_entry(title="MaintainX (User Login)", data=user_input)
        return self.async_show_form(
            step_id="auth",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str
            })
        )
