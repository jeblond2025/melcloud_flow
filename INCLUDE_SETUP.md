# Setup MelCloud cu fișier separat (Recomandat)

## Pasul 1: Copiază fișierul

1. Copiază `melcloud.yaml` în directorul de configurare Home Assistant (același loc unde este `configuration.yaml`)
   - De obicei: `/config/melcloud.yaml`

## Pasul 2: Adaugă include în configuration.yaml

Deschide `configuration.yaml` și adaugă la sfârșit:

```yaml
# Include configurație MelCloud
!include melcloud.yaml
```

**SAU** dacă vrei să folosești structura de directoare organizată:

```yaml
# Include configurație MelCloud
!include melcloud.yaml
```

## Pasul 3: Verifică configurația

1. Mergi la **Configuration** → **Server Controls** → **Check Configuration**
2. Dacă apare eroare, verifică că fișierul `melcloud.yaml` este în același director cu `configuration.yaml`
3. Dacă totul e OK, click pe **Restart**

## Pasul 4: Completează datele

1. Mergi la **Settings** → **Devices & Services** → **Helpers**
2. Completează **DOAR** următoarele (lasă `melcloud_context_key` gol - va fi populat automat):
   - `input_text.melcloud_email` → Email-ul tău MelCloud
   - `input_text.melcloud_password` → Parola ta MelCloud
   - `input_text.melcloud_device_id` → DeviceID (obținut din `test_melcloud.py`)
   - `input_text.melcloud_building_id` → BuildingID (obținut din `test_melcloud.py`)
   - `input_text.melcloud_context_key` → **LASĂ GOL** (va fi populat automat la login)

## Pasul 5: Rulează login

1. Mergi la **Developer Tools** → **Services**
2. Selectează `script.melcloud_login`
3. Click **Call Service**
4. **IMPORTANT:** Verifică că `input_text.melcloud_context_key` a fost populat automat cu o valoare lungă (nu "ERROR" și nu gol)
   - Dacă apare "ERROR", verifică că email-ul și parola sunt corecte
   - Context key-ul este un string lung (token de autentificare) obținut de la API-ul MelCloud

## Pasul 6: Testează

1. Mergi la **Settings** → **Devices & Services** → **Helpers**
2. Găsește `input_number.melcloud_flow_temp`
3. Modifică valoarea (20-60°C)
4. Verifică în log-uri dacă request-ul a fost trimis

## Structura recomandată pentru multiple fișiere

Dacă vrei să organizezi mai bine, poți crea:

```
/config/
  configuration.yaml
  melcloud.yaml
  automations.yaml
  scripts.yaml
  ...
```

Și în `configuration.yaml`:
```yaml
automation: !include automations.yaml
script: !include scripts.yaml
!include melcloud.yaml
```

**Notă:** `melcloud.yaml` conține deja toate secțiunile necesare (input_number, input_text, rest_command, template, automation, script), deci doar adaugi `!include melcloud.yaml` în `configuration.yaml`.

## Avantaje

- ✅ Configurația este organizată separat
- ✅ Mai ușor de gestionat și editat
- ✅ Poți comenta/dezactiva ușor dacă nu o folosești
- ✅ Nu poluează `configuration.yaml` principal

