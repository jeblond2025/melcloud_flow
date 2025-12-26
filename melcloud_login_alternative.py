# Python Script Helper pentru MelCloud Login
# Creează acest fișier în /config/python_scripts/melcloud_login.py
# Apoi folosește-l în script: service: python_script.melcloud_login

import aiohttp
import json

# Obține credențialele
email = data.get('email', hass.states.get('input_text.melcloud_email').state)
password = data.get('password', hass.states.get('input_text.melcloud_password').state)

if not email or not password:
    logger.error("Email sau parolă lipsă")
    return

# Face login
url = "https://app.melcloud.com/Mitsubishi.Wifi.Client/Login/ClientLogin"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
}
payload = {
    "Email": email,
    "Password": password,
    "Language": 0,
    "AppVersion": "1.19.1.1",
    "Persist": True,
    "CaptchaResponse": None,
}

async def do_login():
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("ErrorId") is None:
                    context_key = data.get("LoginData", {}).get("ContextKey")
                    if context_key:
                        hass.services.call("input_text", "set_value", {
                            "entity_id": "input_text.melcloud_context_key",
                            "value": context_key
                        })
                        logger.info("Login reușit, context key salvat")
                        return
            logger.error("Login eșuat")
    
await do_login()

