"""The MelCloud Flow Temperature integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import MelCloudFlowCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.NUMBER, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MelCloud Flow Temperature from a config entry."""
    coordinator = MelCloudFlowCoordinator(
        hass,
        username=entry.data["username"],
        password=entry.data["password"],
        context_key=entry.data.get("context_key", ""),
        device_id=entry.data["device_id"],
        building_id=entry.data["building_id"],
    )

    # Fetch initial data so we have data when entities are added
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator: MelCloudFlowCoordinator = hass.data[DOMAIN][entry.entry_id]
        await coordinator.async_close()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

