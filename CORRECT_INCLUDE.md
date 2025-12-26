# Corectare Include în configuration.yaml

Problema: `!include melcloud.yaml` la nivel root nu funcționează când fișierul conține multiple secțiuni.

## Soluție Corectă:

În `configuration.yaml`, **NU** folosi `!include melcloud.yaml` direct.

În schimb, **copiază conținutul** din `melcloud.yaml` direct în `configuration.yaml` sau folosește una dintre opțiunile de mai jos.

## Opțiunea 1: Copiază conținutul (Cel mai simplu)

1. Deschide `melcloud.yaml`
2. Copiază tot conținutul
3. Adaugă-l la sfârșitul `configuration.yaml`
4. Sau înlocuiește secțiunile respective (input_number, input_text, etc.)

## Opțiunea 2: Include sub secțiuni separate (Dacă ai deja secțiuni)

Dacă ai deja `input_number:`, `automation:`, etc. în `configuration.yaml`, trebuie să le mergi manual sau să folosești `!include_dir_merge_list`.

## Opțiunea 3: Include manual fiecare secțiune (Recomandat dacă vrei include)

Rescrie `melcloud.yaml` astfel încât fiecare secțiune să fie într-un fișier separat:
- `melcloud_input_number.yaml`
- `melcloud_automation.yaml`
- etc.

Și apoi în `configuration.yaml`:
```yaml
input_number: !include melcloud_input_number.yaml
automation: !include melcloud_automation.yaml
```

## Recomandarea mea:

**Folosește Opțiunea 1** - copiază conținutul din `melcloud.yaml` direct în `configuration.yaml`. Este cea mai simplă și funcționează garantat.

