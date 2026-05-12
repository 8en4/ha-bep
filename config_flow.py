"""Config flow for BEP Collectes."""
from __future__ import annotations

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, LOCALITIES_URL


async def fetch_localities(hass) -> list[dict]:
    """Fetch all localities from BEP API."""
    session = async_get_clientsession(hass)

    async with session.get(
        LOCALITIES_URL,
        timeout=aiohttp.ClientTimeout(total=10),
    ) as response:
        response.raise_for_status()
        return await response.json(content_type=None)


class BepCollectesConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Config flow for BEP Collectes."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize config flow."""
        self._localities: list[dict] = []
        self._filtered: list[dict] = []

    async def async_step_user(self, user_input=None):
        """Search locality step."""
        errors = {}

        if not self._localities:
            try:
                self._localities = await fetch_localities(self.hass)
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"

        if user_input is not None and not errors:
            search = user_input["search"].strip().lower()

            self._filtered = [
                loc
                for loc in self._localities
                if (
                    search in loc["name"].lower()
                    or search in str(loc["zipCode"])
                )
            ]

            if not self._filtered:
                errors["base"] = "invalid_locality"
            else:
                return await self.async_step_select()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("search"): selector.TextSelector(),
                }
            ),
            errors=errors,
        )

    async def async_step_select(self, user_input=None):
        """Select locality step."""
        errors = {}

        options = {
            loc["name"]: loc
            for loc in self._filtered
        }

        if user_input is not None:
            selected = options.get(user_input["locality"])

            if selected:
                await self.async_set_unique_id(
                    str(selected["id"])
                )

                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=selected["name"],
                    data={
                        "locality_id": selected["id"],
                        "slug": selected["slug"],
                        "name": selected["name"],
                    },
                )

            errors["base"] = "invalid_locality"

        return self.async_show_form(
            step_id="select",
            data_schema=vol.Schema(
                {
                    vol.Required("locality"): (
                        selector.SelectSelector(
                            selector.SelectSelectorConfig(
                                options=list(options.keys()),
                                mode=selector.SelectSelectorMode.DROPDOWN,
                            )
                        )
                    ),
                }
            ),
            errors=errors,
        )

