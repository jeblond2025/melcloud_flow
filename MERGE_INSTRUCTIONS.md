# Cum să unifici configurația cu cea existentă

Dacă ai deja secțiuni în `configuration.yaml`, trebuie să le unifici, nu să le duplici.

## Dacă ai deja `rest_command:` în configuration.yaml

**NU** adăuga:
```yaml
rest_command:  # ❌ EROARE - duplicat
  melcloud_login:
    ...
```

**În schimb**, adaugă sub secțiunea existentă:
```yaml
rest_command:  # Secțiunea ta existentă
  existing_command:
    ...
  # Adaugă aici comenzile MelCloud (fără a scrie din nou "rest_command:")
  melcloud_login:
    url: "https://app.melcloud.com/Mitsubishi.Wifi.Client/Login/ClientLogin"
    method: POST
    # ... restul configurării
  melcloud_set_temp:
    ...
  melcloud_get_data:
    ...
```

## Același lucru pentru toate secțiunile

Dacă ai deja:
- `input_number:` → adaugă `melcloud_flow_temp:` sub secțiunea existentă
- `input_text:` → adaugă input-urile MelCloud sub secțiunea existentă
- `template:` → adaugă template-urile MelCloud sub secțiunea existentă
- `automation:` → adaugă automation-urile în `automations.yaml` (dacă folosești `!include automations.yaml`)
- `script:` → adaugă script-urile în `scripts.yaml` (dacă folosești `!include scripts.yaml`)

## Exemplu complet:

Dacă `configuration.yaml` arată așa:
```yaml
rest_command:
  my_existing_command:
    url: "http://example.com"
    method: GET
```

Adaugă sub el:
```yaml
rest_command:
  my_existing_command:
    url: "http://example.com"
    method: GET
  
  # MelCloud commands
  melcloud_login:
    url: "https://app.melcloud.com/Mitsubishi.Wifi.Client/Login/ClientLogin"
    method: POST
    # ... restul
```

**IMPORTANT:** Nu scrie `rest_command:` de două ori!

