import logging
import os
import requests
from homeassistant.components.http import StaticPathConfig
from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)
DOMAIN = "maintainx"

PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass, entry):
    """Set up MaintainX from a config entry."""
    config_data = entry.data
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = config_data

    # ? SECURE ASYNC CARD REGISTRATION (HA 2024.7+ Compliant)
    card_path = hass.config.path("custom_components/maintainx/dist/maintainx-card.js")
    
    if os.path.exists(card_path):
        try:
            await hass.http.async_register_static_paths([
                StaticPathConfig("/maintainx/maintainx-card.js", card_path, False)
            ])
            _LOGGER.info("Successfully registered MaintainX dashboard card")
        except RuntimeError as e:
            if "already registered" in str(e):
                _LOGGER.debug("MaintainX dashboard card route already registered")
            else:
                raise
    
    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # SERVICE CALLS & LOGIC
    def handle_create_work_order(call):
        title = call.data.get("title")
        description = call.data.get("description", "")

        if "api_key" in config_data:
            headers = {
                "Authorization": f"Bearer {config_data['api_key']}",
                "Content-Type": "application/json"
            }
            payload = {"title": title, "description": description}
            requests.post("https://api.getmaintainx.com/v1/workorders", json=payload, headers=headers)
        elif "portal_url" in config_data:
            payload = {"title": title, "details": description}
            requests.post(config_data["portal_url"], data=payload)
        elif "username" in config_data:
            session = requests.Session()
            login_data = {"email": config_data["username"], "password": config_data["password"]}
            login_ref = session.post("https://api.getmaintainx.com/v1/auth/login", json=login_data)
            if login_ref.status_code == 200:
                payload = {"title": title, "description": description}
                session.post("https://api.getmaintainx.com/v1/workorders", json=payload)

    hass.loop.call_soon_threadsafe(
        hass.services.register, DOMAIN, "create_work_order", handle_create_work_order
    )
    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
