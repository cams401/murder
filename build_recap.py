#!/usr/bin/env python3
"""Génère une feuille récap HTML privée (hors docs/, jamais poussée sur GitHub)
avec le texte de chaque page + son URL, pour préparer les QR codes."""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent

TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Récap organisateur — Murder Party</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ text-align: left; padding: 0.5rem; border-bottom: 1px solid #ddd; vertical-align: top; }}
.indice {{ background: #fff4d6; }}
.leurre {{ color: #666; }}
code {{ font-size: 0.8rem; word-break: break-all; }}
</style>
</head>
<body>
<h1>Récap organisateur (privé — ne pas partager)</h1>
<p>{count} pages. Base URL : <code>{base_url}</code></p>
<table>
<tr><th>Type</th><th>Texte</th><th>URL</th></tr>
{rows}
</table>
</body>
</html>
"""

ROW = """<tr class="{cls}"><td>{type}</td><td>{text}</td><td><code><a href="{url}">{url}</a></code></td></tr>"""


def main():
    base_url = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "BASE_URL_A_DEFINIR"
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

    rows = []
    for entry in manifest:
        url = f"{base_url}/indices/{entry['file']}"
        rows.append(
            ROW.format(
                cls=entry["type"],
                type=entry["type"],
                text=html.escape(entry["text"]).replace("\n", "<br>"),
                url=url,
            )
        )

    out = TEMPLATE.format(count=len(manifest), base_url=html.escape(base_url), rows="\n".join(rows))
    (ROOT / "recap-organisateur.html").write_text(out, encoding="utf-8")
    print("Écrit : recap-organisateur.html (privé)")


if __name__ == "__main__":
    main()
