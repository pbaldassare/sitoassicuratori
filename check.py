#!/usr/bin/env python3
"""Controllo prima di andare online: python3 check.py. Esce con errore se trova un problema."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
html = (ROOT / "index.html").read_text(encoding="utf-8")
privacy = (ROOT / "privacy.html").read_text(encoding="utf-8")
ids = re.findall(r'\bid="([^"]+)"', html)
errors = []

for name in sorted({i for i in ids if ids.count(i) > 1}):
    errors.append(f"id duplicato: {name}")
for target in sorted(set(re.findall(r'href="#([^"]+)"', html))):
    if target not in ids:
        errors.append(f"link interno rotto: #{target}")
for path in sorted(set(re.findall(r'(?:url\("|href=")(fonts/[^"]+)"', html))):
    if not (ROOT / path).is_file():
        errors.append(f"file mancante: {path}")
for url in sorted(set(re.findall(r'(?:src|href)="(https?://[^"]+)"|url\("?(https?://[^")]+)', html))):
    errors.append(f"risorsa esterna, passa i dati dei visitatori a terzi: {url[0] or url[1]}")
for placeholder in ("example.com", "DA COMPLETARE"):
    if placeholder in html + privacy:
        errors.append(f"segnaposto ancora presente: {placeholder}")

print("\n".join(errors) or "OK")
sys.exit(bool(errors))
