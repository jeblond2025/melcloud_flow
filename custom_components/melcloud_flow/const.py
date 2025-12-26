"""Constants for MelCloud Flow Temperature integration."""

DOMAIN = "melcloud_flow"

# API endpoints (from pymelcloud library)
API_BASE_URL = "https://app.melcloud.com/Mitsubishi.Wifi.Client"
API_LOGIN_URL = f"{API_BASE_URL}/Login/ClientLogin"
API_DEVICE_GET_URL = f"{API_BASE_URL}/Device/Get"
API_SET_ATA_URL = f"{API_BASE_URL}/Device/SetAta"
API_SET_ATW_URL = f"{API_BASE_URL}/Device/SetAtw"

# Update intervals
UPDATE_INTERVAL = 60  # seconds

# Sensor names
SENSOR_TEMPERATURE_TUR = "temperature_tur"
SENSOR_TEMPERATURE_RETUR = "temperature_retur"
SENSOR_TEMPERATURE_EXTERIOARA = "temperature_exterioara"
SENSOR_FLOW_TEMPERATURE_SET = "flow_temperature_set"

# Number entity
NUMBER_FLOW_TEMPERATURE = "flow_temperature"

# Flow temperature limits (typical for heat pumps)
FLOW_TEMPERATURE_MIN = 20.0
FLOW_TEMPERATURE_MAX = 60.0
FLOW_TEMPERATURE_STEP = 0.5

