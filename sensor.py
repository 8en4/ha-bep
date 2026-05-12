"""Sensor platform for BEP Collectes."""
from __future__ import annotations

from datetime import datetime, timezone
import logging

from homeassistant.components.sensor import (
    SensorEntity,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN
from .coordinator import BepCollectesCoordinator

_LOGGER = logging.getLogger(__name__)

COLLECT_TYPES = [
    {
        "key": "isOrga",
        "name": "Organique",
        "icon": "mdi:leaf",
    },
    {
        "key": "isPmc",
        "name": "PMC",
        "icon": "mdi:recycle",
    },
    {
        "key": "isCartons",
        "name": "Cartons",
        "icon": "mdi:package-variant",
    },
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    coordinator: BepCollectesCoordinator = (
        hass.data[DOMAIN][entry.entry_id]
    )

    entities = []

    for collect_type in COLLECT_TYPES:
        entities.append(
            BepNextCollecteSensor(
                coordinator,
                entry,
                collect_type,
            )
        )

        entities.append(
            BepDaysUntilCollecteSensor(
                coordinator,
                entry,
                collect_type,
            )
        )

    async_add_entities(entities)


def _find_next_collecte(
    data: list[dict],
    key: str,
) -> dict | None:
    """Find next collecte."""
    today = datetime.now(
        timezone.utc
    ).date()

    for item in data:
        if item.get(key):
            date = datetime.fromisoformat(
                item["date"].replace(
                    "Z",
                    "+00:00",
                )
            ).date()

            if date >= today:
                return item

    return None


class BepBaseSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """Base BEP sensor."""

    def __init__(
        self,
        coordinator: BepCollectesCoordinator,
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {
                (
                    DOMAIN,
                    self.coordinator.locality_id,
                )
            },
            "name": (
                f"BEP "
                f"{self.coordinator.locality_name}"
            ),
            "manufacturer": "BEP",
        }


class BepNextCollecteSensor(
    BepBaseSensor,
):
    """Next collecte sensor."""

    def __init__(
        self,
        coordinator: BepCollectesCoordinator,
        entry: ConfigEntry,
        collect_type: dict,
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)

        self._collect_type = collect_type

        self._attr_name = (
            f"Prochaine collecte "
            f"{collect_type['name']}"
        )

        self._attr_unique_id = (
            f"{entry.entry_id}_"
            f"{collect_type['key']}_date"
        )

        self._attr_icon = collect_type["icon"]

    @property
    def native_value(self):
        """Return next collecte date."""
        if not self.coordinator.data:
            return None

        item = _find_next_collecte(
            self.coordinator.data,
            self._collect_type["key"],
        )

        if item:
            return datetime.fromisoformat(
                item["date"].replace(
                    "Z",
                    "+00:00",
                )
            ).date()

        return None


class BepDaysUntilCollecteSensor(
    BepBaseSensor,
):
    """Days until collecte sensor."""

    def __init__(
        self,
        coordinator: BepCollectesCoordinator,
        entry: ConfigEntry,
        collect_type: dict,
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)

        self._collect_type = collect_type

        self._attr_name = (
            f"Jours avant collecte "
            f"{collect_type['name']}"
        )

        self._attr_unique_id = (
            f"{entry.entry_id}_"
            f"{collect_type['key']}_days"
        )

        self._attr_icon = collect_type["icon"]

        self._attr_native_unit_of_measurement = "j"

    @property
    def native_value(self):
        """Return remaining days."""
        if not self.coordinator.data:
            return None

        item = _find_next_collecte(
            self.coordinator.data,
            self._collect_type["key"],
        )

        if item:
            today = datetime.now(
                timezone.utc
            ).date()

            date = datetime.fromisoformat(
                item["date"].replace(
                    "Z",
                    "+00:00",
                )
            ).date()

            return (date - today).days

        return None
