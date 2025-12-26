# MelCloud Flow Temperature

Integrare custom pentru Home Assistant care permite controlul temperaturii de curgere (flow temperature) pentru pompele de căldură Mitsubishi Electric Air-to-Water controlate prin MelCloud.

## Funcționalități

- ✅ **Setare flow temperature** - Controlează temperatura de curgere prin entitate Number
- ✅ **Senzori de temperatură**:
  - Temperatură pe tur
  - Temperatură retur
  - Temperatură exterioară
  - Flow temperature set (valoarea setată)

## Instalare

### Opțiunea 1: Instalare manuală

1. Copiază directorul `custom_components/melcloud_flow` în directorul `custom_components` al Home Assistant
2. Repornește Home Assistant
3. Adaugă integrarea prin Settings → Devices & Services → Add Integration → Caută "MelCloud Flow Temperature"

### Opțiunea 2: Instalare prin HACS

1. Asigură-te că ai [HACS](https://hacs.xyz/) instalat
2. În HACS, mergi la Integrations
3. Click pe "..." (meniul din colț) → "Custom repositories"
4. Adaugă repository-ul acestui proiect:
   - Repository: `jeblond2025/melcloud_flow`
   - Category: Integration
5. Click pe "MelCloud Flow Temperature" → "Download"
6. Repornește Home Assistant
7. Adaugă integrarea prin Settings → Devices & Services → Add Integration

## Configurare

1. În Home Assistant, mergi la **Settings** → **Devices & Services**
2. Click pe **Add Integration** (colțul din dreapta jos)
3. Caută și selectează **MelCloud Flow Temperature**
4. Introduceți credențialele MelCloud (email/username și password)
5. Selectează dispozitivul dorit (pompa de căldură Air-to-Water)
6. Finalizează configurarea

## Entități create

După configurare, veți avea următoarele entități:

### Number
- `number.flow_temperature` - Pentru setarea temperaturii de curgere (20-60°C)

### Sensors
- `sensor.temperature_tur` - Temperatura pe tur
- `sensor.temperature_retur` - Temperatura retur
- `sensor.temperature_exterioara` - Temperatura exterioară
- `sensor.flow_temperature_set` - Temperatura de curgere setată

## Utilizare

### Setare flow temperature

Poți seta temperatura de curgere în mai multe moduri:

1. **Prin UI**: Mergi la entitatea `number.flow_temperature` și ajustează valoarea
2. **Prin automatizări**: Folosește acțiunea `number.set_value`
   ```yaml
   service: number.set_value
   target:
     entity_id: number.flow_temperature
   data:
     value: 45.0
   ```

### Utilizare în automatizări

Poți folosi senzorii în automatizări pentru a monitoriza și controla pompa de căldură:

```yaml
automation:
  - alias: "Ajustează flow temperature bazat pe temperatură exterioară"
    trigger:
      - platform: numeric_state
        entity_id: sensor.temperature_exterioara
        above: -5
    action:
      - service: number.set_value
        target:
          entity_id: number.flow_temperature
        data:
          value: 50
```

## Limitări

- Integrarea suportă doar dispozitive Air-to-Water (DeviceType=1)
- Flow temperature este setată pentru Zone1 (pentru sisteme cu mai multe zone)
- Actualizarea datelor se face la fiecare 60 de secunde

## Dezvoltare

Pentru testare locală, vezi `test_melcloud.py` pentru script de test al API-ului MelCloud.

## Contribuții

Contribuțiile sunt binevenite! Te rog să creezi un issue sau pull request.

## Licență

MIT License

## Disclaimer

Această integrare nu este oficială și nu este asociată cu Mitsubishi Electric sau MelCloud. Este dezvoltată de comunitate pentru comunitate.

