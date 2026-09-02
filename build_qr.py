#!/usr/bin/env python3
"""Génère les QR codes PNG manquants, une fois l'URL de base connue.

Chaque exécution qui trouve de nouveaux indices/leurres (pas encore
générés dans un lot précédent) crée un nouveau dossier qr/lot-N/ — les
lots précédents ne sont jamais modifiés, pour que l'organisateur sache
toujours quels QR codes sont déjà imprimés (lots anciens) et lesquels
restent à imprimer (dernier lot).
"""
import json
import sys
from pathlib import Path

import qrcode

ROOT = Path(__file__).parent
QR_DIR = ROOT / "qr"
SUBDIRS = {"indice": "vrais-indices", "leurre": "faux-indices"}


def existing_stems():
    stems = set()
    for lot_dir in QR_DIR.glob("lot-*"):
        for sub in SUBDIRS.values():
            for png in (lot_dir / sub).glob("*.png"):
                stems.add(png.stem)
    return stems


def next_lot_number():
    numbers = []
    for lot_dir in QR_DIR.glob("lot-*"):
        try:
            numbers.append(int(lot_dir.name.split("-")[1]))
        except (IndexError, ValueError):
            continue
    return max(numbers, default=0) + 1


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 build_qr.py https://<user>.github.io/<repo>")
        sys.exit(1)
    base_url = sys.argv[1].rstrip("/")

    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

    already_done = existing_stems()
    new_entries = [e for e in manifest if Path(e["file"]).stem not in already_done]

    if not new_entries:
        print("Aucun nouveau QR code à générer (tout est déjà dans un lot existant).")
        return

    lot_dir = QR_DIR / f"lot-{next_lot_number()}"
    for sub in SUBDIRS.values():
        (lot_dir / sub).mkdir(parents=True, exist_ok=True)

    counts = {"indice": 0, "leurre": 0}
    for entry in new_entries:
        filename = entry["file"]
        url = f"{base_url}/indices/{filename}"
        img = qrcode.make(url, border=2)
        out = lot_dir / SUBDIRS[entry["type"]] / (Path(filename).stem + ".png")
        img.save(out)
        counts[entry["type"]] += 1

    print(f"Nouveau lot : {lot_dir}")
    print(f"  {counts['indice']} vrais indices, {counts['leurre']} leurres")


if __name__ == "__main__":
    main()
