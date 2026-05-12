"""DataUpdateCoordinator for BEP Collectes."""
from __future__ import annotations

import logging

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    BASE_URL,
    DOMAIN,
    SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class BepCollectesCoordinator(
    DataUpdateCoordinator,
):
    """Coordinator to fetch BEP collectes data."""

    def __init__(
        self,
        hass: HomeAssistant,
        locality_id: int,
        slug: str,
        name: str,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

        self.locality_id = locality_id
        self.slug = slug
        self.locality_name = name

    async def _async_update_data(self) -> list[dict]:
        """Fetch data from BEP API."""
        url = (
            f"{BASE_URL}"
            f"?id={self.locality_id}"
            f"&name={self.locality_name}"
            f"&format=json"
            f"&slug={self.slug}"
        )

        session = async_get_clientsession(self.hass)

        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                response.raise_for_status()

                data = await response.json(
                    content_type=None
                )

                return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(
                f"Erreur récupération BEP: {err}"
            ) from err
