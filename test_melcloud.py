"""Test script for MelCloud API authentication and data reading."""
import asyncio
import aiohttp
import json
from typing import Dict, Any


# Correct API base URL (from pymelcloud library)
API_BASE_URL = "https://app.melcloud.com/Mitsubishi.Wifi.Client"
API_LOGIN_URL = f"{API_BASE_URL}/Login/ClientLogin"


async def test_login(username: str, password: str) -> Dict[str, Any]:
    """Test MelCloud login and return context key."""
    print(f"🔐 Încerc să mă autentific cu utilizatorul: {username}")
    
    async with aiohttp.ClientSession() as session:
        print(f"   Endpoint: {API_LOGIN_URL}")
        try:
            # Use correct headers and body format from pymelcloud
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
                API_LOGIN_URL,
                json=body,
                headers=headers,
            ) as response:
                print(f"      Status code: {response.status}")
                
                if response.status != 200:
                    text = await response.text()
                    if len(text) > 500:
                        text = text[:500] + "..."
                    print(f"      ❌ Eroare (status {response.status}): {text}")
                    return None
                
                try:
                    data = await response.json()
                except Exception as e:
                    text = await response.text()
                    print(f"      ❌ Nu s-a putut parsa JSON: {e}")
                    print(f"      Răspuns: {text[:500]}")
                    return None
            
                # Debug: print response structure
                print(f"      📋 Chei în răspuns: {list(data.keys())}")
                
                # Check for errors (ErrorId can be None on success, so check if it's not None)
                if "ErrorId" in data:
                    error_id = data.get("ErrorId")
                    if error_id is not None:
                        error_msg = data.get("ErrorMessage", f"Error ID: {error_id}")
                        print(f"      ❌ Eroare în răspuns: {error_msg}")
                        return None
                    else:
                        print(f"      ℹ️  ErrorId este None (succes)")
                
                login_data = data.get("LoginData")
                if not login_data:
                    print(f"      ⚠️  Nu s-a găsit LoginData în răspuns")
                    print(f"      Răspuns complet: {json.dumps(data, indent=2, ensure_ascii=False)[:1000]}")
                    return None
                
                context_key = login_data.get("ContextKey")
                if not context_key:
                    print(f"      ⚠️  Nu s-a găsit ContextKey în LoginData")
                    print(f"      LoginData keys: {list(login_data.keys())}")
                    return None
                
                print(f"      ✅ Autentificare reușită!")
                print(f"      Context Key: {context_key[:30]}...")
                
                return {
                    "context_key": context_key,
                    "login_data": data,
                    "base_url": API_BASE_URL
                }
                
        except aiohttp.ClientError as e:
            print(f"      ❌ Eroare de conexiune: {e}")
            return None
        except Exception as e:
            print(f"      ❌ Excepție: {e}")
            import traceback
            traceback.print_exc()
            return None


async def test_list_devices(context_key: str, base_url: str = None) -> Dict[str, Any]:
    """Test listing devices from MelCloud."""
    print(f"\n📱 Listez dispozitivele...")
    
    if base_url is None:
        base_url = API_BASE_URL
    
    async with aiohttp.ClientSession() as session:
        try:
            # Use correct headers from pymelcloud
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "X-MitsContextKey": context_key,
                "X-Requested-With": "XMLHttpRequest",
                "Cookie": "policyaccepted=true",
            }
            
            endpoint = f"{base_url}/User/ListDevices"
            print(f"   Endpoint: {endpoint}")
            async with session.get(endpoint, headers=headers) as response:
                print(f"      Status code: {response.status}")
                
                if response.status != 200:
                    text = await response.text()
                    if len(text) > 500:
                        text = text[:500] + "..."
                    print(f"      ❌ Eroare (status {response.status}): {text}")
                    return None
                
                try:
                    entries = await response.json()
                except Exception as e:
                    text = await response.text()
                    print(f"      ❌ Nu s-a putut parsa JSON: {e}")
                    print(f"      Răspuns: {text[:500]}")
                    return None
                
                # Parse device structure (from pymelcloud client.py)
                # entries is a list of structures, each containing Devices, Areas, Floors
                devices_list = []
                for entry in entries:
                    if "Structure" in entry:
                        structure = entry["Structure"]
                        # Add devices from root level
                        if "Devices" in structure:
                            devices_list.extend(structure["Devices"])
                        # Add devices from Areas
                        if "Areas" in structure:
                            for area in structure["Areas"]:
                                if "Devices" in area:
                                    devices_list.extend(area["Devices"])
                        # Add devices from Floors and their Areas
                        if "Floors" in structure:
                            for floor in structure["Floors"]:
                                if "Devices" in floor:
                                    devices_list.extend(floor["Devices"])
                                if "Areas" in floor:
                                    for area in floor["Areas"]:
                                        if "Devices" in area:
                                            devices_list.extend(area["Devices"])
                    else:
                        # If no Structure, try direct list
                        devices_list.append(entry)
                
                print(f"   ✅ Găsite {len(devices_list)} dispozitive")
                
                # Remove duplicates by DeviceID
                visited = set()
                unique_devices = [
                    d for d in devices_list
                    if isinstance(d, dict) and d.get("DeviceID") not in visited and not visited.add(d.get("DeviceID"))
                ]
                
                print(f"      ✅ {len(unique_devices)} dispozitive unice după eliminarea duplicatelor")
                
                air_to_water_devices = []
                for device in unique_devices:
                    # Debug: print full device structure
                    print(f"\n   🔍 Structura completă a dispozitivului:")
                    print(json.dumps(device, indent=4, ensure_ascii=False)[:1500])
                    
                    # Try different ways to get device type (from pymelcloud: conf.get("Device", {}).get("DeviceType"))
                    device_obj = device.get("Device", device)
                    device_type = device_obj.get("DeviceType") if isinstance(device_obj, dict) else device.get("DeviceType")
                    
                    device_id = device.get("DeviceID") or device_obj.get("DeviceID") if isinstance(device_obj, dict) else None
                    device_name = device.get("DeviceName") or device_obj.get("DeviceName") if isinstance(device_obj, dict) else "Unknown"
                    building_id = device.get("BuildingID") or device_obj.get("BuildingID") if isinstance(device_obj, dict) else None
                    
                    print(f"\n   📋 Extras:")
                    print(f"      ID: {device_id}")
                    print(f"      Nume: {device_name}")
                    print(f"      Device Type: {device_type} (0=ATA, 1=ATW/Air-to-Water, 3=ERV)")
                    print(f"      Building ID: {building_id}")
                    
                    # DeviceType: 0=ATA, 1=ATW (Air-to-Water), 3=ERV
                    if device_type == 1:  # ATW (Air-to-Water)
                        air_to_water_devices.append({
                            "device": device,
                            "device_id": device_id,
                            "building_id": building_id,
                            "device_name": device_name
                        })
                    elif device_type is None:
                        print(f"      ⚠️  DeviceType este None - va fi inclus pentru testare oricum")
                        # Include it anyway for testing
                        air_to_water_devices.append({
                            "device": device,
                            "device_id": device_id,
                            "building_id": building_id,
                            "device_name": device_name
                        })
                
                print(f"\n      ✅ Găsite {len(air_to_water_devices)} dispozitive Air-to-Water (ATW)")
                return {
                    "all_devices": entries,
                    "air_to_water_devices": air_to_water_devices
                }
                
        except Exception as e:
            print(f"   ❌ Excepție la listarea dispozitivelor: {e}")
            import traceback
            traceback.print_exc()
            return None


async def test_get_device_data(context_key: str, device_id: int, building_id: int, base_url: str = None):
    """Test reading device data."""
    print(f"\n📊 Citesc datele pentru dispozitivul {device_id}...")
    
    if base_url is None:
        base_url = API_BASE_URL
    
    async with aiohttp.ClientSession() as session:
        try:
            # Use correct headers from pymelcloud
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "X-MitsContextKey": context_key,
                "X-Requested-With": "XMLHttpRequest",
                "Cookie": "policyaccepted=true",
            }
            
            # Device Get endpoint format (from pymelcloud): /Device/Get?id={device_id}&buildingID={building_id}
            url = f"{base_url}/Device/Get?id={device_id}&buildingID={building_id}"
            print(f"   Endpoint: {url}")
            
            async with session.get(url, headers=headers) as response:
                print(f"      Status code: {response.status}")
                
                if response.status == 401:
                    print(f"      ⚠️  Context key expirat (401), ar trebui să re-autentific")
                    return None
                
                if response.status != 200:
                    text = await response.text()
                    if len(text) > 500:
                        text = text[:500] + "..."
                    print(f"      ❌ Eroare (status {response.status}): {text}")
                    return None
                
                try:
                    data = await response.json()
                except Exception as e:
                    text = await response.text()
                    print(f"      ❌ Nu s-a putut parsa JSON: {e}")
                    print(f"      Răspuns: {text[:500]}")
                    return None
                
                print(f"      ✅ Date citite cu succes!")
                print(f"\n   Structura datelor (primele 2000 caractere):")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
                
                # Try to extract relevant temperature data
                print(f"\n   📍 Căutând date de temperatură...")
                state = data.get("State", {})
                if state:
                    print(f"   State object găsit cu {len(state)} câmpuri")
                    print(f"\n   Câmpuri de temperatură găsite în State:")
                    for key in sorted(state.keys()):
                        value = state[key]
                        if isinstance(value, (int, float)) and ("temp" in key.lower() or "set" in key.lower() or "flow" in key.lower()):
                            print(f"      {key}: {value}°C")
                    
                    print(f"\n   Toate câmpurile din State (tipuri):")
                    for key in sorted(state.keys())[:30]:  # Primele 30
                        print(f"      - {key}: {type(state[key]).__name__} = {state[key]}")
                else:
                    print(f"   ⚠️  Nu s-a găsit obiectul 'State' în răspuns")
                    print(f"   Câmpuri disponibile în răspuns:")
                    for key in sorted(data.keys()):
                        print(f"      - {key}: {type(data[key]).__name__}")
                
                return data
                
        except Exception as e:
            print(f"   ❌ Excepție la citirea datelor: {e}")
            import traceback
            traceback.print_exc()
            return None


async def main():
    """Main test function."""
    print("=" * 60)
    print("🧪 Test MelCloud API")
    print("=" * 60)
    
    # Get credentials from user
    username = input("\n📧 Email/Username MelCloud: ").strip()
    password = input("🔑 Password MelCloud: ").strip()
    
    if not username or not password:
        print("❌ Username și password sunt obligatorii!")
        return
    
    # Test login
    login_result = await test_login(username, password)
    if not login_result:
        print("\n❌ Test eșuat la autentificare")
        return
    
    context_key = login_result["context_key"]
    
    base_url = login_result.get("base_url", API_BASE_URL)
    
    # Test list devices
    devices_result = await test_list_devices(context_key, base_url)
    if not devices_result:
        print("\n❌ Test eșuat la listarea dispozitivelor")
        return
    
    air_to_water_devices = devices_result["air_to_water_devices"]
    if not air_to_water_devices:
        print("\n⚠️  Nu s-au găsit dispozitive (sau DeviceType este None)")
        print("    Continuăm cu testarea citirii datelor pentru primul dispozitiv găsit...")
        # Try with first device anyway for testing
        all_devices = devices_result.get("all_devices", [])
        if all_devices:
            # Extract first device from structure
            first_entry = all_devices[0] if isinstance(all_devices, list) else all_devices
            if isinstance(first_entry, dict) and "Structure" in first_entry:
                structure = first_entry["Structure"]
                devices_in_structure = []
                if "Devices" in structure:
                    devices_in_structure.extend(structure["Devices"])
                if devices_in_structure:
                    first_device_raw = devices_in_structure[0]
                    device_id = first_device_raw.get("DeviceID")
                    building_id = first_device_raw.get("BuildingID")
                    if device_id and building_id:
                        print(f"\n   🔧 Testăm cu dispozitivul ID: {device_id}, Building: {building_id}")
                        device_data = await test_get_device_data(
                            context_key,
                            device_id,
                            building_id,
                            base_url
                        )
                        if device_data:
                            print("\n" + "=" * 60)
                            print("✅ Testul de citire date a trecut!")
                            print("=" * 60)
                        return
        print("    Nu s-a putut continua testarea")
        return
    
    # Test get device data for first Air-to-Water device
    first_device = air_to_water_devices[0]
    device_data = await test_get_device_data(
        context_key,
        first_device["device_id"],
        first_device["building_id"],
        base_url
    )
    
    if device_data:
        print("\n" + "=" * 60)
        print("✅ Toate testele au trecut cu succes!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("⚠️  Testul de citire date a eșuat")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

