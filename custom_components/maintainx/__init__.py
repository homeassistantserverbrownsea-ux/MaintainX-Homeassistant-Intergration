import logging
import os
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
DOMAIN = "maintainx"

async def async_setup_entry(hass, entry):
    """Set up MaintainX from a config entry."""
    config_data = entry.data

    # 🚀 AUTOMATIC CARD REGISTRATION
    # This maps the internal custom_components path to a public URL route
    card_path = hass.config.path("custom_components/maintainx/dist/maintainx-card.js")
    if os.path.exists(card_path):
        hass.http.register_static_path(
            "/maintainx/maintainx-card.js",
            card_path,
            cache_headers=False
        )
        _LOGGER.info("Successfully registered MaintainX dashboard card at /maintainx/maintainx-card.js")
    else:
        _LOGGER.warning(f"Could not find card file at {card_path}")

    # SERVICE CALLS & LOGIC
    def handle_create_work_order(call):
        title = call.data.get("title")
        description = call.data.get("description", "")

        # Option 1: API Setup
        if "api_key" in config_data:
            headers = {
                "Authorization": f"Bearer {config_data['api_key']}",
                "Content-Type": "application/json"
            }
            payload = {"title": title, "description": description}
            requests.post("[https://api.getmaintainx.com/v1/workorders](https://api.getmaintainx.com/v1/workorders)", json=payload, headers=headers)

        # Option 2: URL Setup
        elif "portal_url" in config_data:
            payload = {"title": title, "details": description}
            requests.post(config_data["portal_url"], data=payload)

        # Option 3: Login Credentials Setup
        elif "username" in config_data:
            session = requests.Session()
            login_data = {"email": config_data["username"], "password": config_data["password"]}
            login_ref = session.post("[https://api.getmaintainx.com/v1/auth/login](https://api.getmaintainx.com/v1/auth/login)", json=login_data)
            if login_ref.status_code == 200:
                payload = {"title": title, "description": description}
                session.post("[https://api.getmaintainx.com/v1/workorders](https://api.getmaintainx.com/v1/workorders)", json=payload)

    hass.services.register(DOMAIN, "create_work_order", handle_create_work_order)
    return True
