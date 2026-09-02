#!/usr/bin/env python3
"""Génère deux feuilles récap HTML privées (hors docs/, jamais poussées sur
GitHub) : une pour les vrais indices, une pour les leurres, avec le texte de
chaque page + son URL, pour préparer l'impression des QR codes."""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent

TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>{page_title} — Murder Party</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ text-align: left; padding: 0.5rem; border-bottom: 1px solid #ddd; vertical-align: top; }}
code {{ font-size: 0.8rem; word-break: break-all; }}
</style>
</head>
<body>
<h1>{page_title} (privé — ne pas partager)</h1>
<p>{count} pages. Base URL : <code>{base_url}</code></p>
<table>
<tr><th>Texte</th><th>URL</th></tr>
{rows}
</table>
</body>
</html>
"""

ROW = """<tr><td>{text}</td><td><code><a href="{url}">{url}</a></code></td></tr>"""

FILES_BY_TYPE = {
    "indice": ("recap-vrais-indices.html", "Récap — vrais indices"),
    "leurre": ("recap-faux-indices.html", "Récap — faux indices"),
}


def main():
    base_url = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "BASE_URL_A_DEFINIR"
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

    for kind, (out_filename, page_title) in FILES_BY_TYPE.items():
        rows = []
        for entry in manifest:
            if entry["type"] != kind:
                continue
            url = f"{base_url}/indices/{entry['file']}"
            rows.append(
                ROW.format(
                    text=html.escape(entry["text"]).replace("\n", "<br>"),
                    url=url,
                )
            )

        out = TEMPLATE.format(
            page_title=page_title,
            count=len(rows),
            base_url=html.escape(base_url),
            rows="\n".join(rows),
        )
        (ROOT / out_filename).write_text(out, encoding="utf-8")
        print(f"Écrit : {out_filename} (privé, {len(rows)} pages)")


if __name__ == "__main__":
    main()
