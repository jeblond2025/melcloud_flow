# Setup Simplu MelCloud prin REST API

## Pașii de configurare:

### 1. Obține Device ID și Building ID

Rulează scriptul `test_melcloud.py`:
```bash
python test_melcloud.py
```

Notează: `DeviceID` și `BuildingID`

### 2. Adaugă configurația în Home Assistant

1. Deschide **File Editor** sau editează `configuration.yaml`
2. Adaugă conținutul din `MELCLOUD_SIMPLE_SETUP.yaml`
3. Verifică configurația (Configuration → Check Configuration)
4. Repornește Home Assistant

### 3. Completează datele

1. Mergi la **Settings** → **Devices & Services** → **Helpers**
2. Completează:
   - `input_text.melcloud_email` → Email-ul tău MelCloud
   - `input_text.melcloud_password` → Parola ta MelCloud
   - `input_text.melcloud_device_id` → DeviceID (de ex: `12345`)
   - `input_text.melcloud_building_id` → BuildingID (de ex: `67890`)

### 4. Rulează login

1. Mergi la **Developer Tools** → **Services**
2. Selectează `script.melcloud_login`
3. Click **Call Service**
4. Verifică că `input_text.melcloud_context_key` are o valoare (nu "ERROR")

### 5. Testează setarea temperaturii

1. Mergi la **Settings** → **Devices & Services** → **Helpers**
2. Găsește `input_number.melcloud_flow_temp`
3. Modifică valoarea (20-60°C)
4. Verifică în log-uri dacă request-ul a fost trimis

### 6. Verifică senzorii

După câteva minute, ar trebui să apară:
- `sensor.melcloud_temperature_tur`
- `sensor.melcloud_temperature_retur`
- `sensor.melcloud_temperature_exterioara`
- `sensor.melcloud_flow_temperature_set`

## Refresh Context Key

Context key-ul expiră. Adaugă o automation pentru refresh:

```yaml
automation:
  - alias: "MelCloud Context Key Refresh"
    trigger:
      - platform: time_pattern
        hours: /6  # La fiecare 6 ore
    action:
      - service: script.melcloud_login
```

## Utilizare

1. **Setare flow temperature:** Modifică `input_number.melcloud_flow_temp`
2. **Vizualizare temperaturi:** Vezi senzori în Dashboard
3. **Refresh context key:** Rulează `script.melcloud_login` periodic

## Notă importantă

Această metodă folosește `sensor.set_state` pentru a stoca datele din API. Acest senzor nu este vizibil în UI, dar este folosit de template sensors pentru a extrage valorile.

