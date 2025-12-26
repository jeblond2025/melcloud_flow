# ⚠️ URGENT: SECURITATE COMPROMISĂ

## IMPORTANT - ACȚIUNE IMEDIATĂ NECESARĂ:

**Fișierele cu configurație care conțin date sensibile au fost adăugate în git și publicate pe GitHub!**

### Fișiere afectate (deja șterse):
- ✅ `CONFIGURATION_FIXED.yaml` - ȘTERS din git
- ✅ `melcloud_to_copy.yaml` - ȘTERS din git
- ⚠️ **DAR** sunt încă în istoricul git (comituri anterioare)

### Date care au fost expuse:
- Email: `bogdan.sandulache@gmail.com`
- Parolă: `Network_14`
- Device ID: `77001175`
- Building ID: `591400`

### ACȚIUNI URGENTE NECESARE:

1. **SCHIMBĂ PAROLA MELCLOUD ACUM:**
   - Mergi pe https://www.melcloud.com/
   - Login cu contul tău
   - **Schimbă parola IMEDIAT**
   - Parola veche (`Network_14`) a fost expusă în repository-ul public

2. **CURĂȚĂ GIT HISTORY (Recomandat):**
   
   Opțiunea 1 - Simplă (dacă repository-ul este nou și nu ai multe colaboratori):
   ```bash
   # Creează un repository nou
   # Copiază doar fișierele fără date sensibile
   # Șterge repository-ul vechi
   ```

   Opțiunea 2 - Avansată (folosind git-filter-repo):
   ```bash
   # Instalează git-filter-repo
   pip install git-filter-repo
   
   # Șterge fișierele din întreg istoricul
   git filter-repo --path CONFIGURATION_FIXED.yaml --invert-paths
   git filter-repo --path melcloud_to_copy.yaml --invert-paths
   
   # Force push (ATENȚIE: va rescrie istoricul!)
   git push --force
   ```

3. **VERIFICĂ DACA MAI EXISTĂ DATE SENSIBILE:**
   ```bash
   # Caută în tot repository-ul
   git log -p | grep -i "bogdan\|Network_14\|77001175\|591400"
   ```

### MĂSURI PREVENTIVE:

✅ Am actualizat `.gitignore` pentru a exclude fișierele cu configurație
✅ Am creat `melcloud_template.yaml` ca template fără date sensibile
✅ Am creat `SECURITY_WARNING.md` cu instrucțiuni

### PENTRU VIITOR:

- **NICIODATĂ** nu adăuga parole, API keys, sau date sensibile în git
- Folosește doar template-uri fără date reale
- Completează datele sensibile direct în Home Assistant UI, nu în fișiere YAML
- Review cod înainte de commit
- Folosește `git secrets` pentru a detecta automat date sensibile

### STATUS:

- ✅ Fișierele au fost șterse din staging
- ✅ `.gitignore` a fost actualizat
- ⚠️ Fișierele sunt încă în istoricul git (comituri vechi)
- ⚠️ **SCHIMBĂ PAROLA ACUM**

