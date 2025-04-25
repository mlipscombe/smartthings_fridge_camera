from urllib.parse import urlencode

import requests

from homeassistant.components.camera import PLATFORM_SCHEMA, Camera
from homeassistant.components.local_file.camera import LocalFile
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import HTTP_DIGEST_AUTHENTICATION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.core import callback
from .const import DOMAIN
from .api import FamilyHub, DataCoordinator

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    hub = hass.data[DOMAIN]["hub"]
    coordinator = DataCoordinator(hass, hub)
    async_add_entities([LastUpdatedAt(coordinator)])


class LastUpdatedAt(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        self._last_updated_at = None
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.api.device_id}_last_updated"
        self._attr_name = "Last Updated"
        
    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {("samsung_familyhub_fridge", self.coordinator.api.device_id)},
            "name": "Samsung Family Hub Fridge",
            "manufacturer": "Samsung",
            "model": "Family Hub Fridge",
        }

    @property
    def last_updated_at(self) -> str | None:
        return self._last_updated_at

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._last_updated_at = self.coordinator.last_updated_at
        if self._last_updated_at:
            self.async_write_ha_state()
