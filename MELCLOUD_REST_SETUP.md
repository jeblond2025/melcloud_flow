# Configurare MelCloud prin REST API (Alternativă la integrare custom)

Această metodă folosește REST commands și REST sensors din Home Assistant pentru a controla direct API-ul MelCloud, fără a avea nevoie de o integrare custom.

## Avantaje:
- ✅ Nu necesită integrare custom
- ✅ Configurare simplă în `configuration.yaml`
- ✅ Control direct prin input_number
- ✅ Senzori pentru temperaturi

## Dezavantaje:
- ⚠️ Trebuie să gestionezi manual context key (login periodic)
- ⚠️ Necesită configurare manuală a device_id și building_id
- ⚠️ Nu are funcționalități avansate ca o integrare completă

## Pașii de instalare:

### 1. Obține Device ID și Building ID

Rulează scriptul `test_melcloud.py` pentru a obține aceste valori:
```bash
python test_melcloud.py
```

Notează:
- `DeviceID`
- `BuildingID`

### 2. Adaugă configurația în Home Assistant

1. Deschide `configuration.yaml` în Home Assistant
2. Adaugă configurațiile din `HOME_ASSISTANT_REST_CONFIG.yaml`
3. **IMPORTANT:** Modifică următoarele valori:
   - `YOUR_EMAIL@example.com` → email-ul tău MelCloud
   - `YOUR_PASSWORD` → parola ta MelCloud
   - `{{ device_id }}` → DeviceID-ul tău (de ex: `12345`)
   - `{{ building_id }}` → BuildingID-ul tău (de ex: `67890`)
   - `{{ context_key }}` → va fi setat automat prin script (dar poți înlocui cu valoarea reală pentru teste)

### 3. Rulează scriptul de login

În Home Assistant:
1. Mergi la **Developer Tools** → **Services**
2. Selectează serviciul `script.melcloud_login`
3. Click pe **Call Service**
4. Verifică că `input_text.melcloud_context_key` a fost populat

### 4. Verifică senzorii

1. Mergi la **Developer Tools** → **States**
2. Caută:
   - `sensor.melcloud_temperature_tur`
   - `sensor.melcloud_temperature_retur`
   - `sensor.melcloud_temperature_exterioara`
   - `sensor.melcloud_flow_temperature_set`

### 5. Setează flow temperature

1. Mergi la **Settings** → **Devices & Services** → **Helpers**
2. Găsește `input_number.melcloud_flow_temperature`
3. Modifică valoarea (20-60°C)
4. Temperatura va fi setată automat prin automation

## Automatizare Context Key Refresh

Context key-ul expiră după un timp. Poți crea o automation pentru refresh:

```yaml
automation:
  - alias: "MelCloud Context Key Refresh"
    trigger:
      - platform: time_pattern
        hours: /6  # La fiecare 6 ore
    action:
      - service: script.melcloud_login
```

## Limitări

- Context key trebuie reîmprospătat periodic
- REST sensors pot fi mai lente decât o integrare nativă
- Nu are toate funcționalitățile unei integrări complete

## Depanare

Dacă senzorii nu funcționează:
1. Verifică că context_key este setat în `input_text.melcloud_context_key`
2. Verifică că device_id și building_id sunt corecte
3. Rulează din nou `script.melcloud_login`
4. Verifică log-urile Home Assistant pentru erori

