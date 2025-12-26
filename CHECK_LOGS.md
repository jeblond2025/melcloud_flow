# Verificare Erori Home Assistant

Pentru a diagnostica eroarea "Invalid handler specified", te rog să verifici log-urile Home Assistant:

1. Mergi la **Settings** → **System** → **Logs**
2. Caută erori care conțin:
   - `melcloud_flow`
   - `config_flow`
   - `Invalid handler`
   - Traceback/Exception messages

3. Poți filtra log-urile cu:
   - `melcloud` în căutare
   - Sau caută erori din ultimele 10-15 minute

**Ce să cauți:**
- Import errors (ModuleNotFoundError, ImportError)
- Syntax errors în config_flow.py
- Probleme cu DOMAIN sau const.py
- Probleme cu definirea clasei ConfigFlow

**După ce găsești eroarea, trimite-mi mesajul complet de eroare pentru a putea remedia problema.**

