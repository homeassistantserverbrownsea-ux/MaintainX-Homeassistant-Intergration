import logging
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import CONF_API_KEY
from .const import DOMAIN
import requests

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up MaintainX sensor from a config entry."""
    config_data = config_entry.data
    
    entities = []
    
    # Add work order count sensor if API key exists
    if "api_key" in config_data:
        entities.append(MaintainXWorkOrderCountSensor(hass, config_data))
    
    async_add_entities(entities)


class MaintainXWorkOrderCountSensor(SensorEntity):
    """Sensor for MaintainX work order count."""
    
    def __init__(self, hass, config_data):
        self.hass = hass
        self.config_data = config_data
        self._attr_name = "MaintainX Work Order Count"
        self._attr_unique_id = f"maintainx_workorder_count"
        self._attr_device_class = SensorDeviceClass.NUMBER
        self._state = 0
    
    @property
    def state(self):
        return self._state
    
    async def async_update(self):
        """Fetch work order count from API."""
        try:
            headers = {"Authorization": f"Bearer {self.config_data['api_key']}"}
            response = requests.get("https://api.getmaintainx.com/v1/workorders", headers=headers)
            if response.status_code == 200:
                self._state = len(response.json().get("data", []))
        except Exception as e:
            _LOGGER.error(f"Error fetching work orders: {e}")
