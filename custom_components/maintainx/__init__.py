import logging
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
DOMAIN = "maintainx"

async def async_setup_entry(hass, entry):
    """Set up MaintainX from a config entry."""
    config_data = entry.data

    def handle_create_work_order(call):
        title = call.data.get("title")
        description = call.data.get("description", "")

        # OPTION 1: API Setup
        if "api_key" in config_data:
            headers = {
                "Authorization": f"Bearer {config_data['api_key']}",
                "Content-Type": "application/json"
            }
            payload = {"title": title, "description": description}
            requests.post("https://api.getmaintainx.com/v1/workorders", json=payload, headers=headers)

        # OPTION 2: URL Setup
        elif "portal_url" in config_data:
            payload = {"title": title, "details": description}
            requests.post(config_data["portal_url"], data=payload)

        # OPTION 3: Login Credentials Setup
        elif "username" in config_data:
            session = requests.Session()
            # Dynamic login handling
            login_data = {"email": config_data["username"], "password": config_data["password"]}
            login_ref = session.post("https://api.getmaintainx.com/v1/auth/login", json=login_data)
            if login_ref.status_code == 200:
                payload = {"title": title, "description": description}
                session.post("https://api.getmaintainx.com/v1/workorders", json=payload)

    hass.services.register(DOMAIN, "create_work_order", handle_create_work_order)
    return True
