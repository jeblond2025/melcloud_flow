"""Number platform for MelCloud Flow Temperature."""
from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    NUMBER_FLOW_TEMPERATURE,
    FLOW_TEMPERATURE_MIN,
    FLOW_TEMPERATURE_MAX,
    FLOW_TEMPERATURE_STEP,
)
from .coordinator import MelCloudFlowCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the MelCloud Flow Temperature number platform."""
    coordinator: MelCloudFlowCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([MelCloudFlowTemperatureNumber(coordinator, entry)])


class MelCloudFlowTemperatureNumber(
    CoordinatorEntity[MelCloudFlowCoordinator], NumberEntity
):
    """Representation of a MelCloud Flow Temperature Number."""

    def __init__(
        self,
        coordinator: MelCloudFlowCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_{NUMBER_FLOW_TEMPERATURE}"
        self._attr_name = "Flow Temperature"
        self._attr_native_min_value = FLOW_TEMPERATURE_MIN
        self._attr_native_max_value = FLOW_TEMPERATURE_MAX
        self._attr_native_step = FLOW_TEMPERATURE_STEP
        self._attr_native_unit_of_measurement = "°C"

    @property
    def native_value(self) -> float | None:
        """Return the current flow temperature setpoint."""
        data = self.coordinator.data
        if not data:
            return None

        # Data is directly in response, not wrapped in "State" object
        # Use Zone1 heat flow temperature (most common for single zone systems)
        if "SetHeatFlowTemperatureZone1" in data:
            return float(data["SetHeatFlowTemperatureZone1"])
        if "SetCoolFlowTemperatureZone1" in data:
            return float(data["SetCoolFlowTemperatureZone1"])
        # Fallback to Zone2 if Zone1 not available
        if "SetHeatFlowTemperatureZone2" in data:
            return float(data["SetHeatFlowTemperatureZone2"])

        return None

    async def async_set_native_value(self, value: float) -> None:
        """Update the flow temperature."""
        success = await self.coordinator.async_set_flow_temperature(value)
        if success:
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set flow temperature to %s", value)

