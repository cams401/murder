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
    {
        "keyword": "mail-supprime",
        "body": "Mail supprimé",
        "eyebrow": "Mail supprimé",
    },
    {
        "keyword": "mail-alexandre",
        "body": "Sandrine,\n\nJe refuse de continuer à cacher certains dossiers.\nNous devons parler aujourd'hui.\n\nA.",
    },
    {
        "keyword": "anomalie-filiere",
        "body": "Toute anomalie découverte entraînera la fermeture de la filière.",
        "signature": "Alexandra",
    },
    {
        "keyword": "decision-direction",
        "body": "Décision imposée par la direction.",
    },
    {
        "keyword": "robin-informe",
        "body": "Robin ne doit surtout pas être informé.",
    },
    {
        "keyword": "note-audit",
        "body": "Audit – 14h00",
        "eyebrow": "Note",
    },
    {
        "keyword": "ticket-impression",
        "body": "Heure : 11h08\nUtilisateur : ADMIN-ALEX",
        "eyebrow": "Ticket d'impression",
    },
    {
        "keyword": "rapport-etudiants",
        "body": "Personne ne doit évoquer ces dossiers devant les étudiants.",
        "eyebrow": "Rapport",
    },
    {
        "keyword": "carte-identite-axelle",
        "body": "Axelle\n\nNée le 11/03/1998",
        "eyebrow": "Carte d'identité",
    },
    {
        "keyword": "badges-alexandra",
        "body": "Badge : ALEXANDRA\n\n11h11 — Ascenseur\n11h15 — Ascenseur\n11h27 — Ascenseur",
        "eyebrow": "Historique des badges",
    },
    {
        "keyword": "liste-etudiants",
        "body": (
            "LISTE DES ÉTUDIANTS — L3\n\n"
            "...rie Lambert\n"
            "Julien R...\n"
            "...andre Petit\n"
            "Camille Do...\n"
            "...na Novak\n"
            "Thomas Ber...\n"
            "...abelle Roy\n"
            "Yanis Kh..."
        ),
        "eyebrow": "Liste des étudiants (incomplète)",
    },
    {
        "keyword": "prenom-andrea",
        "body": "Andréa",
    },
    {
        "keyword": "sms-sandrine-andrea",
        "body": (
            "Sandrine : « Pourquoi veux-tu les clés ? »\n\n"
            "Andréa : « Alexandra me l'a demandé. »\n\n"
            "Sandrine : « Je trouve ça étrange... »\n\n"
            "Alexandra : « Ne discute pas. Fais-le. »"
        ),
        "eyebrow": "SMS",
    },
    {
        "keyword": "sms-axelle-sandrine",
        "body": (
            "Axelle : « Tu comptes vraiment tout dire ? »\n\n"
            "Sandrine : « Il le faut, Axelle. »\n\n"
            "Axelle : « S'il te plaît, ne dis rien. Ça détruirait tout pour moi. »\n\n"
            "Sandrine : « Je suis désolée. »"
        ),
        "eyebrow": "SMS",
    },
    {
        "keyword": "mails-sandrine-robin",
        "body": (
            "Sandrine : « Robin, il faut que tu voies ces dossiers avant l'audit. »\n\n"
            "Robin : « Je sais déjà. Ce n'est plus mon problème. »"
        ),
        "eyebrow": "Mails",
    },
    {
        "keyword": "sms-andrea-alexandra",
        "body": (
            "Andréa : « Les clés sont où tu voulais. »\n\n"
            "Alexandra : « Bien. Oublie tout ça. »"
        ),
        "eyebrow": "SMS",
    },
    {
        "keyword": "sms-alexandra-robin",
        "body": (
            "Alexandra : « On peut arranger ça avant l'audit ? »\n\n"
            "Robin : « Fais ce que tu as à faire. Je ne veux rien savoir. »"
        ),
        "eyebrow": "SMS",
    },
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
    "Ce QR code a demandé l'asile politique dans un autre indice.",
    "Bravo, tu as trouvé... un QR code.",
    "Sandrine te remercie de ta visite, mais n'a rien à te dire ici.",
    "Indice non trouvé. As-tu essayé de le chercher avec les yeux ouverts ?",
    "Ce n'est pas un indice, c'est un test de curiosité. Tu l'as réussi.",
    "L'enquête continue, mais pas ici.",
    "Ce QR code participe activement à ton échec.",
    "Un indice sur deux se trouve ailleurs. Celui-ci fait partie de l'autre moitié.",
    "Robin n'est pas caché derrière ce QR code non plus.",
    "Alexandra ne validera pas ce chemin d'enquête.",
    "Ce message s'autodétruira... non, en fait, pas du tout.",
    "Tu progresses à une vitesse remarquablement lente.",
    "Ce QR code a été placé ici uniquement pour le suspense.",
    "Toujours pas d'indice, mais toujours de l'espoir.",
    "Ce n'est pas la case départ, mais ça y ressemble beaucoup.",
    "Un faux indice de plus dans ta collection.",
    "Les vrais indices ne se scannent pas par hasard.",
    "Ce QR code préfère garder ses secrets.",
    "Si la victoire était facile, ce ne serait pas un murder party.",
    "Tu chauffes… au sens propre, avec ton téléphone en plein soleil.",
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

    for clue in REAL_CLUES:
        filename, text = make_page(
            "indice",
            clue["keyword"],
            clue["body"],
            clue.get("signature", ""),
            eyebrow=clue.get("eyebrow", "Indice"),
        )
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
