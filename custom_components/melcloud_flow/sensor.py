"""Sensor platform for MelCloud Flow Temperature."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR_TEMPERATURE_TUR,
    SENSOR_TEMPERATURE_RETUR,
    SENSOR_TEMPERATURE_EXTERIOARA,
    SENSOR_FLOW_TEMPERATURE_SET,
)
from .coordinator import MelCloudFlowCoordinator

_LOGGER = logging.getLogger(__name__)

SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=SENSOR_TEMPERATURE_TUR,
        name="Temperature Tur",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SENSOR_TEMPERATURE_RETUR,
        name="Temperature Retur",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SENSOR_TEMPERATURE_EXTERIOARA,
        name="Temperature Exterioară",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SENSOR_FLOW_TEMPERATURE_SET,
        name="Flow Temperature Set",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the MelCloud Flow Temperature sensor platform."""
    coordinator: MelCloudFlowCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        MelCloudFlowTemperatureSensor(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class MelCloudFlowTemperatureSensor(
    CoordinatorEntity[MelCloudFlowCoordinator], SensorEntity
):
    """Representation of a MelCloud Flow Temperature Sensor."""

    def __init__(
        self,
        coordinator: MelCloudFlowCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_name = description.name

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        data = self.coordinator.data
        if not data:
            return None

        # Data is directly in response, not wrapped in "State" object
        key = self.entity_description.key

        if key == SENSOR_TEMPERATURE_TUR:
            # Flow temperature (tur) - use TankWaterTemperature or RoomTemperatureZone1
            if "TankWaterTemperature" in data:
                temp = data["TankWaterTemperature"]
                if temp is not None and temp > -30:  # Filter invalid values
                    return float(temp)
            if "RoomTemperatureZone1" in data:
                temp = data["RoomTemperatureZone1"]
                if temp is not None and temp > -30:  # Filter invalid values
                    return float(temp)

        elif key == SENSOR_TEMPERATURE_RETUR:
            # Return temperature - might be RoomTemperatureZone2 or calculated
            # For now, use RoomTemperatureZone2 if valid
            if "RoomTemperatureZone2" in data:
                temp = data["RoomTemperatureZone2"]
                if temp is not None and temp > -30:  # Filter invalid values like -39.0
                    return float(temp)
            # Alternative: could calculate from flow temp and other data

        elif key == SENSOR_TEMPERATURE_EXTERIOARA:
            # Outdoor temperature
            if "OutdoorTemperature" in data:
                temp = data["OutdoorTemperature"]
                if temp is not None:
                    return float(temp)

        elif key == SENSOR_FLOW_TEMPERATURE_SET:
            # Flow temperature setpoint - use Zone1 heat flow temp (most common)
            if "SetHeatFlowTemperatureZone1" in data:
                return float(data["SetHeatFlowTemperatureZone1"])
            if "SetCoolFlowTemperatureZone1" in data:
                return float(data["SetCoolFlowTemperatureZone1"])
            # Fallback to Zone2 if Zone1 not available
            if "SetHeatFlowTemperatureZone2" in data:
                return float(data["SetHeatFlowTemperatureZone2"])

        return None

