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
- `build_qr.py` — génère les QR codes PNG **manquants** une fois l'URL connue
  (nécessite le module Python `qrcode`, voir `.venv-qr`). Ne touche jamais un
  PNG déjà généré : chaque exécution qui trouve de nouveaux indices/leurres
  crée un nouveau dossier `qr/lot-N/` (avec `vrais-indices/` et
  `faux-indices/`), en plus des lots précédents déjà imprimés. Comme ça, on
  sait toujours quels QR codes sont déjà imprimés (`lot-1`, `lot-2`, ...) et
  lesquels restent à imprimer (dernier lot en date).
- `build_recap.py` — génère `recap-vrais-indices.html` et
  `recap-faux-indices.html` (privés, jamais poussés sur GitHub) listant
  chaque texte + son URL, pour préparer l'impression.
- `manifest.json`, `qr/`, `recap-*.html` — **jamais commités**
  (voir `.gitignore`) : ils révèlent quelles pages sont de vrais indices.

## Régénérer après ajout de nouveaux indices/leurres

```bash
python3 build_site.py
python3 build_recap.py https://cams401.github.io/murder
python3 -m venv .venv-qr && .venv-qr/bin/pip install "qrcode[pil]"  # une fois
.venv-qr/bin/python build_qr.py https://cams401.github.io/murder
```

Le dernier `qr/lot-N/` créé contient uniquement les QR codes des indices
ajoutés depuis la dernière impression — c'est celui-là qu'il faut imprimer.

## Déploiement GitHub Pages

1. Créer un dépôt GitHub vide nommé `murder` sous le compte `cams401`.
2. Pousser ce dépôt (voir commandes fournies).
3. Dans Settings → Pages : source = branche `main`, dossier `/docs`.
4. Le site sera disponible sur `https://cams401.github.io/murder/`.
5. Imprimer les QR codes du dernier `qr/lot-N/` (correspondance dans
   `recap-vrais-indices.html` / `recap-faux-indices.html`, à garder pour toi).
