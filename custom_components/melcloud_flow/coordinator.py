"""Data update coordinator for MelCloud Flow Temperature."""
import logging
from datetime import timedelta
from typing import Any, Dict, Optional

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, API_BASE_URL, API_DEVICE_GET_URL, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class MelCloudFlowCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from MelCloud API."""

    def __init__(
        self,
        hass: HomeAssistant,
        username: str,
        password: str,
        context_key: str,
        device_id: int,
        building_id: int,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self._username = username
        self._password = password
        self._context_key = context_key
        self._device_id = device_id
        self._building_id = building_id
        self._session: Optional[aiohttp.ClientSession] = None

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from MelCloud API."""
        try:
            if not self._session:
                self._session = aiohttp.ClientSession()

            # Refresh context key if needed (it expires)
            context_key = await self._get_context_key()

            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "X-MitsContextKey": context_key,
                "X-Requested-With": "XMLHttpRequest",
                "Cookie": "policyaccepted=true",
            }

            # Get device data (using query parameters, not path)
            url = f"{API_DEVICE_GET_URL}?id={self._device_id}&buildingID={self._building_id}"
            async with self._session.get(url, headers=headers) as response:
                if response.status == 401:
                    # Context key expired, refresh it
                    context_key = await self._get_context_key()
                    headers["X-MitsContextKey"] = context_key
                    self._context_key = context_key

                    async with self._session.get(url, headers=headers) as retry_response:
                        if retry_response.status != 200:
                            raise UpdateFailed(
                                f"Error fetching device data: {retry_response.status}"
                            )
                        data = await retry_response.json()
                elif response.status != 200:
                    raise UpdateFailed(f"Error fetching device data: {response.status}")
                else:
                    data = await response.json()

            return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with MelCloud API: {err}") from err

    async def _get_context_key(self) -> str:
        """Get or refresh context key."""
        if not self._session:
            self._session = aiohttp.ClientSession()

        try:
            body = {
                "Email": self._username,
                "Password": self._password,
                "Language": 0,
                "AppVersion": "1.19.1.1",
                "Persist": True,
                "CaptchaResponse": None,
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            }
            
            async with self._session.post(
                f"{API_BASE_URL}/Login/ClientLogin",
                json=body,
                headers=headers,
            ) as response:
                if response.status != 200:
                    raise UpdateFailed("Failed to authenticate with MelCloud")

                data = await response.json()
                context_key = data.get("LoginData", {}).get("ContextKey")
                if not context_key:
                    raise UpdateFailed("Invalid response from MelCloud")

                self._context_key = context_key
                return context_key

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error authenticating with MelCloud: {err}") from err

    async def _fetch_device_data(self) -> Dict[str, Any]:
        """Fetch current device data (helper method to avoid recursion)."""
        if not self._session:
            self._session = aiohttp.ClientSession()

        context_key = await self._get_context_key()
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "X-MitsContextKey": context_key,
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": "policyaccepted=true",
        }

        url = f"{API_DEVICE_GET_URL}?id={self._device_id}&buildingID={self._building_id}"
        async with self._session.get(url, headers=headers) as response:
            if response.status == 401:
                # Context key expired, refresh it
                context_key = await self._get_context_key()
                headers["X-MitsContextKey"] = context_key
                self._context_key = context_key

                async with self._session.get(url, headers=headers) as retry_response:
                    if retry_response.status != 200:
                        raise UpdateFailed(
                            f"Error fetching device data: {retry_response.status}"
                        )
                    return await retry_response.json()
            elif response.status != 200:
                raise UpdateFailed(f"Error fetching device data: {response.status}")
            else:
                return await response.json()

    async def async_set_flow_temperature(self, temperature: float) -> bool:
        """Set flow temperature on device."""
        if not self._session:
            self._session = aiohttp.ClientSession()

        try:
            context_key = await self._get_context_key()
            
            # Get current device state
            current_data = await self._fetch_device_data()
            if not current_data:
                _LOGGER.error("Failed to fetch current device data")
                return False
            
            # Data is directly in response, not wrapped in "State" object
            # Update the flow temperature field
            # Use SetHeatFlowTemperatureZone1 (most common for single zone systems)
            atw_data = current_data.copy()
            
            # Determine which zone to update based on operation mode
            operation_mode_zone1 = atw_data.get("OperationModeZone1", 1)
            
            # OperationModeZone1: 1=Heat, 2=Cool, etc.
            # Set the appropriate flow temperature based on mode
            if operation_mode_zone1 == 1:  # Heat mode
                atw_data["SetHeatFlowTemperatureZone1"] = temperature
                _LOGGER.debug("Setting heat flow temperature Zone1 to %s", temperature)
            elif operation_mode_zone1 == 2:  # Cool mode
                atw_data["SetCoolFlowTemperatureZone1"] = temperature
                _LOGGER.debug("Setting cool flow temperature Zone1 to %s", temperature)
            else:
                # Default to heat flow temperature
                atw_data["SetHeatFlowTemperatureZone1"] = temperature
                _LOGGER.debug("Setting heat flow temperature Zone1 to %s (default)", temperature)

            # For ATW devices, use SetAtw endpoint
            url = f"{API_BASE_URL}/Device/SetAtw"
            
            # Headers with correct format from pymelcloud
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "X-MitsContextKey": context_key,
                "X-Requested-With": "XMLHttpRequest",
                "Cookie": "policyaccepted=true",
                "Content-Type": "application/json",
            }
            
            async with self._session.post(
                url,
                json=atw_data,  # Send the ATW data directly
                headers=headers,
            ) as response:
                if response.status == 200:
                    # Refresh coordinator data
                    await self.async_request_refresh()
                    return True
                else:
                    error_text = await response.text()
                    _LOGGER.error(
                        "Failed to set flow temperature (status %s): %s",
                        response.status,
                        error_text,
                    )
                    return False

        except Exception as err:
            _LOGGER.exception("Error setting flow temperature: %s", err)
            return False

    async def async_close(self) -> None:
        """Close the session."""
        if self._session:
            await self._session.close()
            self._session = None

