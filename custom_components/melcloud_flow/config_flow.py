"""Config flow for MelCloud Flow Temperature integration."""
import logging
from typing import Any, Dict, Optional

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, API_BASE_URL

_LOGGER = logging.getLogger(__name__)


async def validate_auth(
    hass: HomeAssistant, username: str, password: str
) -> Dict[str, Any]:
    """Validate credentials and return device list."""
    async with aiohttp.ClientSession() as session:
        try:
            body = {
                "Email": username,
                "Password": password,
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
            
                async with session.post(
                f"{API_BASE_URL}/Login/ClientLogin",
                json=body,
                headers=headers,
            ) as response:
                _LOGGER.debug("Login response status: %s", response.status)
                
                if response.status != 200:
                    text = await response.text()
                    _LOGGER.error("Login failed with status %s: %s", response.status, text[:500])
                    raise InvalidAuth

                try:
                    data = await response.json()
                except Exception as e:
                    text = await response.text()
                    _LOGGER.error("Failed to parse login response: %s. Response: %s", e, text[:500])
                    raise InvalidAuth

                # Check for errors (ErrorId can be None on success, so check if it's not None)
                # Same logic as test_melcloud.py
                if not data:
                    _LOGGER.error("Empty response from login")
                    raise InvalidAuth
                
                if "ErrorId" in data:
                    error_id = data.get("ErrorId")
                    if error_id is not None:
                        error_msg = data.get("ErrorMessage", f"Error ID: {error_id}")
                        _LOGGER.error("Login error: %s", error_msg)
                        raise InvalidAuth
                
                login_data = data.get("LoginData")
                if not login_data:
                    _LOGGER.error("No LoginData in response. Response keys: %s", list(data.keys()))
                    raise InvalidAuth

                context_key = login_data.get("ContextKey")
                if not context_key:
                    _LOGGER.error("No ContextKey in LoginData. LoginData keys: %s", list(login_data.keys()))
                    raise InvalidAuth

                _LOGGER.debug("Authentication successful, context key obtained")

                # Get device list (same headers format as test_melcloud.py)
                headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Language": "en-US,en;q=0.5",
                    "X-MitsContextKey": context_key,
                    "X-Requested-With": "XMLHttpRequest",
                    "Cookie": "policyaccepted=true",
                }
                
                async with session.get(
                    f"{API_BASE_URL}/User/ListDevices",
                    headers=headers,
                ) as devices_response:
                    if devices_response.status != 200:
                        text = await devices_response.text()
                        _LOGGER.error("Failed to get device list (status %s): %s", devices_response.status, text[:500])
                        raise CannotConnect

                    try:
                        devices_data = await devices_response.json()
                    except Exception as e:
                        text = await devices_response.text()
                        _LOGGER.error("Failed to parse device list response: %s. Response: %s", e, text[:500])
                        raise CannotConnect
                    
                    return {
                        "context_key": context_key,
                        "devices": devices_data,
                    }
                    
        except (InvalidAuth, CannotConnect):
            # Re-raise our custom exceptions
            raise
        except aiohttp.ClientError as err:
            _LOGGER.exception("Error connecting to MelCloud API: %s", err)
            raise CannotConnect from err
        except Exception as err:
            _LOGGER.exception("Unexpected error during authentication: %s", err)
            raise InvalidAuth from err


class ConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for MelCloud Flow Temperature."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_auth(
                    self.hass,
                    user_input["username"],
                    user_input["password"],
                )

                # Find Air-to-Water devices
                devices_raw = info["devices"]
                # Handle both list and dict responses
                if isinstance(devices_raw, list):
                    devices_list = devices_raw
                elif isinstance(devices_raw, dict):
                    # If wrapped, try common keys
                    devices_list = devices_raw.get("DeviceListItems", devices_raw.get("Devices", []))
                else:
                    devices_list = []

                devices = []
                for device in devices_list:
                    if not isinstance(device, dict):
                        continue
                    # DeviceType: 0=ATA, 1=ATW (Air-to-Water), 3=ERV
                    device_type = device.get("DeviceType")
                    if device_type == 1:  # ATW (Air-to-Water)
                        devices.append(device)

                if not devices:
                    errors["base"] = "no_devices"
                else:
                    # Store devices and credentials for selection step
                    self.context["devices"] = devices
                    self.context["context_key"] = info["context_key"]
                    self.context["username"] = user_input["username"]
                    self.context["password"] = user_input["password"]
                    return await self.async_step_device()

            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_device(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle device selection step."""
        errors: Dict[str, str] = {}

        # Get devices from context (stored in previous step)
        devices = self.context.get("devices", [])

        if user_input is not None:
            device_id = user_input["device"]
            device_info = next(
                (d for d in devices if d["Device"]["DeviceID"] == int(device_id)),
                None
            )

            if device_info:
                device_name = device_info["Device"].get("DeviceName", "MelCloud Heat Pump")
                
                await self.async_set_unique_id(f"{DOMAIN}_{device_id}")
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=device_name,
                    data={
                        "username": self.context.get("username", ""),
                        "password": self.context.get("password", ""),
                        "context_key": self.context.get("context_key", ""),
                        "device_id": int(device_id),
                        "building_id": device_info["Device"]["BuildingID"],
                    },
                )

        if not devices:
            return self.async_abort(reason="no_devices")

        return self.async_show_form(
            step_id="device",
            data_schema=vol.Schema(
                {
                    vol.Required("device"): vol.In(
                        {
                            str(d["Device"]["DeviceID"]): f"{d['Device'].get('DeviceName', 'Unknown')} (ID: {d['Device']['DeviceID']})"
                            for d in devices
                        }
                    ),
                }
            ),
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

