# Troubleshooting "Invalid handler specified" Error

Dacă apare eroarea "Invalid handler specified", încearcă următorii pași:

## 1. Verifică structura directoarelor

Asigură-te că structura este corectă:
```
custom_components/
  melcloud_flow/
    __init__.py
    config_flow.py
    const.py
    manifest.json
    ...
```

## 2. Șterge cache-ul Home Assistant

1. Oprește Home Assistant
2. Șterge directorul `__pycache__` din `custom_components/melcloud_flow/` (dacă există)
3. Șterge directorul `.homeassistant/__pycache__` (dacă există)
4. Repornește Home Assistant

## 3. Verifică fișierele instalate

Dacă ai instalat prin HACS, verifică că toate fișierele sunt prezente în:
`config/custom_components/melcloud_flow/`

## 4. Reinstalează complet

1. Șterge integrarea din Home Assistant (Settings → Devices & Services)
2. Șterge din HACS
3. Șterge manual directorul `config/custom_components/melcloud_flow/` (dacă există)
4. Repornește Home Assistant
5. Reinstalează din HACS
6. Repornește din nou
7. Adaugă integrarea

## 5. Verifică log-urile

În log-urile Home Assistant, caută:
- ImportError
- ModuleNotFoundError
- SyntaxError
- Traceback complet

Trimite mesajul complet de eroare pentru diagnosticare.

