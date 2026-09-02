#!/usr/bin/env python3
"""Génère les QR codes PNG pour chaque page, une fois l'URL de base connue.

Les QR codes des vrais indices et des leurres sont rangés dans deux
dossiers séparés pour que l'organisateur ne les mélange pas à l'impression.
"""
import json
import sys
from pathlib import Path

import qrcode

ROOT = Path(__file__).parent
QR_DIR = ROOT / "qr"

DEST_BY_TYPE = {
    "indice": QR_DIR / "vrais-indices",
    "leurre": QR_DIR / "faux-indices",
}


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 build_qr.py https://<user>.github.io/<repo>")
        sys.exit(1)
    base_url = sys.argv[1].rstrip("/")

    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

    for d in DEST_BY_TYPE.values():
        d.mkdir(parents=True, exist_ok=True)

    counts = {"indice": 0, "leurre": 0}
    for entry in manifest:
        filename = entry["file"]
        url = f"{base_url}/indices/{filename}"
        img = qrcode.make(url, border=2)
        out = DEST_BY_TYPE[entry["type"]] / (Path(filename).stem + ".png")
        img.save(out)
        counts[entry["type"]] += 1

    print(f"{counts['indice']} QR codes (vrais indices) dans {DEST_BY_TYPE['indice']}")
    print(f"{counts['leurre']} QR codes (faux indices) dans {DEST_BY_TYPE['leurre']}")


if __name__ == "__main__":
    main()
