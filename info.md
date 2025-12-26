# MelCloud Flow Temperature

Integrare custom pentru Home Assistant care permite controlul temperaturii de curgere (flow temperature) pentru pompele de căldură Mitsubishi Electric Air-to-Water controlate prin MelCloud.

## Funcționalități

- ✅ Setare flow temperature prin entitate Number
- ✅ Senzori pentru temperatură pe tur, retur și exterioară
- ✅ Senzor pentru flow temperature set

## Configurare

1. Adaugă integrarea prin Settings → Devices & Services → Add Integration
2. Introdu credențialele MelCloud
3. Selectează dispozitivul (pompa de căldură Air-to-Water)

## Entități

- `number.flow_temperature` - Setare temperatura curgere
- `sensor.temperature_tur` - Temperatură pe tur
- `sensor.temperature_retur` - Temperatură retur  
- `sensor.temperature_exterioara` - Temperatură exterioară
- `sensor.flow_temperature_set` - Flow temperature setată

