# Instrucțiuni Test MelCloud API

## Creare environment virtual (recomandat)

```bash
python -m venv venv
```

## Activare environment virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

## Instalare dependențe

După activarea environment-ului virtual:

```bash
pip install -r requirements_test.txt
```

## Rulare test

```bash
python test_melcloud.py
```

Scriptul va solicita:
1. Email/Username MelCloud
2. Password MelCloud

Apoi va testa:
- ✅ Autentificarea
- ✅ Listarea dispozitivelor
- ✅ Citirea datelor dispozitivului (Air-to-Water)

## Ce va afișa

Scriptul va afișa:
- Structura completă a răspunsului API
- Toate câmpurile disponibile în obiectul `State`
- Valorile de temperatură găsite

Acest lucru ne va ajuta să identificăm exact numele câmpurilor pentru:
- Flow temperature (set)
- Temperature tur
- Temperature retur  
- Temperature exterioară

