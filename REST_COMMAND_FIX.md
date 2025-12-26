# Fix pentru rest_command - response_template nu este suportat

## Problema:

`rest_command` în Home Assistant **NU suportă** `response_template`. Trebuie să procesăm răspunsul diferit.

## Soluția Simplă (Recomandat):

Folosește un **Python Script Helper** pentru login, care poate procesa răspunsul corect.

### Pașii:

1. **Creează directorul** (dacă nu există):
   ```
   /config/python_scripts/
   ```

2. **Creează fișierul** `/config/python_scripts/melcloud_login.py` cu conținutul din `melcloud_login_alternative.py`

3. **Modifică script-ul** în `scripts.yaml`:
   ```yaml
   melcloud_login:
     alias: "MelCloud Login"
     sequence:
       - service: python_script.melcloud_login
   ```

4. **Activează Python Scripts** în `configuration.yaml`:
   ```yaml
   python_script:
   ```

### Alternativă: Folosește HTTP Request direct în automation

Poți folosi `http.request` în loc de `rest_command` pentru a obține răspunsul direct.

### Soluția Rapidă (Fără Python Scripts):

Dacă nu vrei să folosești Python Scripts, poți seta context key-ul manual:
1. Rulează `test_melcloud.py` pentru a obține context key-ul
2. Setează-l manual în `input_text.melcloud_context_key` prin UI

Context key-ul expiră după câteva ore, deci va trebui să-l reînnoiești periodic.
