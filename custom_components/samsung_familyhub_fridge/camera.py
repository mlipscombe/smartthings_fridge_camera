from urllib.parse import urlencode

import requests

from homeassistant.components.camera import PLATFORM_SCHEMA, Camera
from homeassistant.components.local_file.camera import LocalFile
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import HTTP_DIGEST_AUTHENTICATION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.core import callback
from .const import DOMAIN
from .api import FamilyHub, DataCoordinator
from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityFeature,
)
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from .sensor import LastUpdatedAt


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    # def setup_platform(
    #     hass: HomeAssistant,
    #     config: ConfigType,
    #     add_entities: AddEntitiesCallback,
    #     discovery_info: DiscoveryInfoType | None = None,
    # ) -> None:
    """Set up the Axis camera video stream."""
    hub = hass.data[DOMAIN]["hub"]
    # platform = entity_platform.async_get_current_platform()

    # This will call Entity.set_sleep_timer(sleep_time=VALUE)
    # platform.async_register_entity_service(
    #     "refresh",
    #     {},
    #     "refresh",
    # )
    async_add_entities(
        [
            FamilyHubCamera("family_hub_top", 0, hub),
            FamilyHubCamera("family_hub_middle", 1, hub),
            FamilyHubCamera("family_hub_bottom", 2, hub),
        ]
    )


class FamilyHubCamera(Camera):
    def __init__(self, name, index, hub):
        super().__init__()
        self.content_type = "image/jpeg"
        self.hub = hub
        self._index = index
        self._name = name
        self._image = None
        self._attr_unique_id = f"{self.hub.device_id}_{self._name}"
        
    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {("samsung_familyhub_fridge", self.hub.device_id)},
            "name": self.hub.device_name,
            "manufacturer": "Samsung",
            "model": "Family Hub Fridge",
        }

    def camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return image response."""
        return self.hub.downloaded_images[self._index]

    @property
    def name(self):
        """Return the name of this camera."""
        return self._name

    @property
    def extra_state_attributes(self):
        """Return the camera state attributes."""
        return {}
