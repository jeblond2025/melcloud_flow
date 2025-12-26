# Fix pentru Include în configuration.yaml

Există două moduri de a include fișierul `melcloud.yaml`:

## Opțiunea 1: Include direct (Simplu - Recomandat)

În `configuration.yaml`, adaugă la **sfârșitul** fișierului (pe o linie nouă, fără indentare):

```yaml
!include melcloud.yaml
```

**IMPORTANT:** 
- Trebuie să fie la nivel de root (fără indentare)
- Nu trebuie să fie sub nicio altă cheie
- Trebuie să fie pe o linie separată

## Opțiunea 2: Include sub secțiuni (Dacă Opțiunea 1 nu funcționează)

Dacă ai deja secțiuni definite în `configuration.yaml`, trebuie să le mergi manual.

**NU poți folosi:**
```yaml
input_number: !include melcloud.yaml  # ❌ NU FUNCȚIONEAZĂ
```

Pentru că `melcloud.yaml` conține mai multe secțiuni (input_number, input_text, rest_command, etc.)

**Soluție:** Trebuie să incluzi fiecare secțiune separat sau să le copiezi manual în `configuration.yaml`.

## Opțiunea 3: Folosește include_dir (Avansat)

Creează un director `config/melcloud/` și mută fișierul acolo, apoi în `configuration.yaml`:

```yaml
!include_dir_merge_list melcloud/
```

Dar asta necesită să rescrii `melcloud.yaml` în format listă.

## Recomandarea mea:

Folosește **Opțiunea 1** - adaugă `!include melcloud.yaml` la sfârșitul fișierului `configuration.yaml`, fără indentare, pe o linie separată.

