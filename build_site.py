#!/usr/bin/env python3
"""Génère les pages individuelles (une par indice/leurre) pour le murder party."""
import hashlib
import html
import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent
SITE = ROOT / "docs"
INDICES = SITE / "indices"

TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <main class="card">
    <p class="eyebrow">{eyebrow}</p>
    <p class="text{small_class}">{body}</p>{signature}
  </main>
</body>
</html>
"""

def slugify_hash(key: str) -> str:
    # Le nom de fichier ne doit JAMAIS trahir si la page est un vrai indice ou
    # un leurre : le dépôt GitHub est public et sa liste de fichiers est
    # consultable par n'importe qui. On utilise donc un identifiant neutre.
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]


def make_page(kind: str, keyword: str, body: str, signature: str = "", eyebrow: str = None):
    filename = f"msg-{slugify_hash(kind + keyword + body)}.html"
    escaped_body = html.escape(body).replace("\n", "\n")
    small_class = " small" if len(body) > 70 else ""
    sig_html = f'\n    <p class="signature">{html.escape(signature)}</p>' if signature else ""
    eyebrow_text = eyebrow if eyebrow else ("Indice" if kind == "indice" else "???")
    page = TEMPLATE.format(
        title="Indice",
        eyebrow=html.escape(eyebrow_text),
        body=escaped_body,
        small_class=small_class,
        signature=sig_html,
    )
    (INDICES / filename).write_text(page, encoding="utf-8")
    return filename, body


REAL_CLUES = [
    ("mail-supprime", "Mail supprimé", ""),
    (
        "mail-alexandre",
        "Sandrine,\n\nJe refuse de continuer à cacher certains dossiers.\nNous devons parler aujourd'hui.\n\nA.",
        "",
    ),
    (
        "anomalie-filiere",
        "Toute anomalie découverte entraînera la fermeture de la filière.",
        "Alexandra",
    ),
    ("decision-direction", "Décision imposée par la direction.", ""),
    ("robin-informe", "Robin ne doit surtout pas être informé.", ""),
]

DECOYS = [
    "Raté ! Mais puisque tu es là, profite-en pour vérifier si tu as bien payé ta CVEC.",
    "Pas ici ! Par contre, si tu cherches l'amour de ta vie, il est sûrement en train de scanner un autre QR code.",
    "Désolé, ce QR code est réservé au fantôme de l'école.",
    "Rien à voir avec Sandrine… mais bravo, tu viens de perdre 10 secondes.",
    "Erreur 404 : l'indice a été mangé par Maxime.",
    "Mauvais QR, mais excellent cardio.",
    "Tu viens officiellement de scanner un mur.",
    "Continue, tu chauffes… enfin pas vraiment.",
    "Tu viens de gagner… absolument rien.",
    "Ce QR sert uniquement à tester ta patience.",
    "L'indice est en RTT.",
    "Essaie encore.",
    "Sandrine n'est pas cachée dans le distributeur de café.",
    "Le prochain indice est probablement à l'autre bout du campus.",
    "Tu n'es pas perdu, tu explores.",
    "L'indice est parti faire la Color Run.",
    "Tu pensais vraiment que ce serait aussi simple ?",
    "Encore raté… mais on croit en toi.",
    "Si tu lis ce message, c'est que tu es très motivé… ou très perdu.",
]


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def slug_keyword(text: str, n: int = 3) -> str:
    ascii_text = strip_accents(text)
    words = [w.strip(".,\"'!?…").lower() for w in ascii_text.split()]
    words = [w for w in words if w.isalpha()]
    return "-".join(words[:n]) or "leurre"


def main():
    INDICES.mkdir(parents=True, exist_ok=True)
    manifest = []

    for keyword, body, signature in REAL_CLUES:
        eyebrow = "Mail supprimé" if keyword == "mail-supprime" else "Indice"
        filename, text = make_page("indice", keyword, body, signature, eyebrow=eyebrow)
        manifest.append({"type": "indice", "file": filename, "text": text})

    for text in DECOYS:
        keyword = slug_keyword(text)
        filename, _ = make_page("leurre", keyword, text, eyebrow="???")
        manifest.append({"type": "leurre", "file": filename, "text": text})

    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"{len(manifest)} pages générées dans {INDICES}")
    print("manifest.json (privé, hors docs/) écrit à la racine du dépôt")


if __name__ == "__main__":
    main()
