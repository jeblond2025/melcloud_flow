# Instrucțiuni pentru publicare pe GitHub și HACS

## Pasul 1: Creează repository-ul pe GitHub

1. Mergi pe [GitHub](https://github.com) și loghează-te
2. Click pe **"+"** din colțul din dreapta sus → **"New repository"**
3. Completează:
   - **Repository name**: `melcloud_flow` (sau alt nume)
   - **Description**: "Home Assistant custom integration for MelCloud Flow Temperature control"
   - **Visibility**: Public (obligatoriu pentru HACS)
   - **NU** adăuga README, .gitignore sau licență (le avem deja)
4. Click **"Create repository"**

## Pasul 2: Actualizează manifest.json

Înainte de a publica, actualizează URL-urile din `custom_components/melcloud_flow/manifest.json`:

1. Deschide `custom_components/melcloud_flow/manifest.json`
2. Înlocuiește `yourusername` cu numele tău de utilizator GitHub real:
   ```json
   "documentation": "https://github.com/YOUR_USERNAME/melcloud_flow",
   "issue_tracker": "https://github.com/YOUR_USERNAME/melcloud_flow/issues",
   "codeowners": ["@YOUR_USERNAME"],
   ```

## Pasul 3: Publică codul pe GitHub

În terminal, rulează următoarele comenzi:

```bash
# Inițializează git (dacă nu e deja făcut)
git init

# Adaugă toate fișierele
git add .

# Fă primul commit
git commit -m "Initial commit: MelCloud Flow Temperature integration"

# Adaugă remote-ul GitHub (înlocuiește YOUR_USERNAME cu numele tău)
git remote add origin https://github.com/YOUR_USERNAME/melcloud_flow.git

# Publică pe GitHub
git branch -M main
git push -u origin main
```

## Pasul 4: Instalare prin HACS

După ce ai publicat repository-ul:

1. Deschide Home Assistant
2. Mergi la **HACS** → **Integrations**
3. Click pe **"..."** (meniul din colțul din dreapta sus) → **"Custom repositories"**
4. Adaugă repository-ul:
   - **Repository**: `YOUR_USERNAME/melcloud_flow` (fără https://github.com/)
   - **Category**: Selectează **"Integration"**
5. Click **"Add"** apoi **"Save"**
6. Înapoi la **HACS** → **Integrations**, ar trebui să vezi **"MelCloud Flow Temperature"**
7. Click pe el → **"Download"**
8. Repornește Home Assistant
9. Adaugă integrarea prin **Settings** → **Devices & Services** → **Add Integration** → Caută **"MelCloud Flow Temperature"**

## Pasul 5: Actualizări viitoare

Când vrei să faci actualizări:

```bash
# Adaugă modificările
git add .

# Fă commit
git commit -m "Descriere modificări"

# Publică
git push
```

Utilizatorii vor putea actualiza prin HACS (vor primi notificare când apare o nouă versiune).

## Notă importantă

Pentru ca HACS să recunoască automat noile versiuni:
- Asigură-te că versiunea din `manifest.json` crește la fiecare release
- Opțional: creează releases pe GitHub (Tags) pentru o gestionare mai bună a versiunilor

