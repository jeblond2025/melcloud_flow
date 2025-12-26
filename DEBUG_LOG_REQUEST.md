# Cerere pentru Debug Log-uri

Pentru a diagnostica problema "Invalid handler specified", am nevoie de log-urile complete din Home Assistant.

## Pașii pentru a obține log-urile:

1. **Activează logging-ul detaliat:**
   - Settings → System → Logs
   - Click pe "Download Full Log"
   - Sau copiază log-urile din ultimele 5-10 minute

2. **Încearcă să adaugi integrarea:**
   - Settings → Devices & Services → Add Integration
   - Caută "MelCloud Flow Temperature"
   - Notează exact ce eroare apare

3. **Filtrează log-urile:**
   - Caută: `melcloud_flow`
   - Sau caută: `config_flow`
   - Sau caută: `Invalid handler`
   - Sau caută: `Traceback`
   - Sau caută: `ImportError`, `ModuleNotFoundError`, `SyntaxError`

4. **Trimite următoarele:**
   - Ultimele 100-200 linii de log după ce apare eroarea
   - Orice mesaj care conține "melcloud_flow"
   - Orice traceback complet

**Exemplu de ce să cauți:**
```
2025-12-26 18:21:33.028 ERROR (SyncWorker_0) [homeassistant.loader] ...
2025-12-26 18:21:33.029 ERROR (MainThread) [homeassistant.config_entries] ...
Traceback (most recent call last):
  File "...", line X, in ...
    ...
```

Sau poți rula în terminalul Home Assistant (SSH/Console):
```bash
tail -n 200 /config/home-assistant.log | grep -i melcloud
```

