#!/usr/bin/env python3
"""Génère les QR codes PNG pour chaque page, une fois l'URL de base connue."""
import json
import sys
from pathlib import Path

import qrcode

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
QR_DIR = ROOT / "qr"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 build_qr.py https://<user>.github.io/<repo>")
        sys.exit(1)
    base_url = sys.argv[1].rstrip("/")

    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

    QR_DIR.mkdir(exist_ok=True)
    for entry in manifest:
        filename = entry["file"]
        url = f"{base_url}/indices/{filename}"
        img = qrcode.make(url, border=2)
        out = QR_DIR / (Path(filename).stem + ".png")
        img.save(out)

    print(f"{len(manifest)} QR codes générés dans {QR_DIR}")


if __name__ == "__main__":
    main()
