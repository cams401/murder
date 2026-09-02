# Murder Party — indices QR code

Site statique : chaque page sous `docs/indices/` affiche **uniquement** un
texte (indice réel ou leurre), sans navigation ni lien — pensé pour être
ouvert via un QR code scanné par les joueurs.

## Structure

- `docs/` — le site déployé sur GitHub Pages (root = ce dossier).
  - `index.html` — page neutre si quelqu'un tombe sur la racine du site.
  - `indices/*.html` — une page par indice/leurre. Noms de fichiers
    volontairement neutres (`msg-<hash>.html`) pour qu'on ne puisse pas
    deviner depuis le dépôt GitHub quelles pages sont de vrais indices.
  - `assets/style.css` — le style commun.
- `build_site.py` — régénère les pages à partir des textes définis dans le
  script (`REAL_CLUES` et `DECOYS`).
- `build_qr.py` — génère un QR code PNG par page une fois l'URL connue
  (nécessite le module Python `qrcode`, voir `.venv-qr`).
- `build_recap.py` — génère `recap-organisateur.html` (privé, jamais poussé
  sur GitHub) listant chaque texte + son URL, pour préparer l'impression.
- `manifest.json`, `qr/`, `recap-organisateur.html` — **jamais commités**
  (voir `.gitignore`) : ils révèlent quelles pages sont de vrais indices.

## Régénérer après modification des textes

```bash
python3 build_site.py
python3 build_recap.py https://cams401.github.io/murder
python3 -m venv .venv-qr && .venv-qr/bin/pip install "qrcode[pil]"  # une fois
.venv-qr/bin/python build_qr.py https://cams401.github.io/murder
```

## Déploiement GitHub Pages

1. Créer un dépôt GitHub vide nommé `murder` sous le compte `cams401`.
2. Pousser ce dépôt (voir commandes fournies).
3. Dans Settings → Pages : source = branche `main`, dossier `/docs`.
4. Le site sera disponible sur `https://cams401.github.io/murder/`.
5. Imprimer les QR codes du dossier `qr/` (correspondance dans
   `recap-organisateur.html`, à garder pour toi).
