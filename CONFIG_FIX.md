# Fix pentru configuration.yaml

Problema: `!include melcloud.yaml` la nivel root nu funcționează pentru că `melcloud.yaml` conține mai multe secțiuni.

## Soluția 1: Copiază conținutul (Recomandat)

1. **Șterge** linia `!include melcloud.yaml` din `configuration.yaml`
2. **Copiază** tot conținutul din `melcloud.yaml`
3. **Adaugă** la sfârșitul `configuration.yaml` (după linia cu `logger:`)

Configurația ta ar trebui să arate așa:

```yaml
# Text to speech
tts:
  - platform: google_translate

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
logger:
  logs:
    homeassistant.components.modbus: debug

# MelCloud Configuration (copiază aici tot conținutul din melcloud.yaml)
input_number:
  melcloud_flow_temp:
    name: "MelCloud Flow Temperature"
    initial: 45
    min: 20
    max: 60
    step: 0.5
    unit_of_measurement: "°C"

input_text:
  melcloud_email:
    name: "MelCloud Email"
    initial: ""
  # ... restul configurației
```

## Soluția 2: Include separat fiecare secțiune (Dacă vrei să păstrezi fișierul separat)

Dacă vrei să păstrezi fișierul separat, trebuie să rescrii `melcloud.yaml` în fișiere separate și să le incluzi separat. Dar asta este mai complicat și nu recomand.

**Recomandarea mea: Folosește Soluția 1 - copiază conținutul direct.**

