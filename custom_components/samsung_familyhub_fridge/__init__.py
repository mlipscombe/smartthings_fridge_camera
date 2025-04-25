"""The Samsung FamilyHub Fridge integration."""
from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .api import FamilyHub
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.CAMERA, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Samsung FamilyHub Fridge from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN][entry.entry_id] = entry
    hub = FamilyHub(
        hass, entry.data["token"], entry.data.get("device_id")
    )
    hass.data[DOMAIN]["hub"] = hub

    # Fetch device info on initial load
    if hub.device_id:
        device_info = await hass.async_add_executor_job(hub.get_current_device_info)
        hub.set_device_info(device_info)
        _LOGGER.debug("Fetched initial device info: %s", hub.device_name)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
