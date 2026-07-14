"""Valida integridad, estructura y manifiesto del snapshot financiero."""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

RAIZ = Path(__file__).resolve().parents[1]
MODELO = RAIZ / "financiero" / "modelo" / "Modelo_FEMSA_Ulogix_2026.xlsx"
MANIFIESTO = MODELO.with_name("modelo.manifest.json")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def main() -> None:
    errores: list[str] = []
    if not MODELO.is_file() or not MANIFIESTO.is_file():
        raise SystemExit("Faltan el XLSX publicado o su manifiesto.")

    meta = json.loads(MANIFIESTO.read_text(encoding="utf-8"))
    contenido = MODELO.read_bytes()
    digest = hashlib.sha256(contenido).hexdigest()
    if digest != meta.get("sha256"):
        errores.append("El SHA-256 del XLSX no coincide con el manifiesto.")
    if len(contenido) != meta.get("bytes"):
        errores.append("El tamaño del XLSX no coincide con el manifiesto.")

    formulas = 0
    celdas_error = 0
    with zipfile.ZipFile(MODELO) as libro:
        requeridos = {"[Content_Types].xml", "xl/workbook.xml"}
        faltantes = requeridos.difference(libro.namelist())
        if faltantes:
            errores.append(f"Estructura XLSX incompleta: {sorted(faltantes)}")
        raiz = ET.fromstring(libro.read("xl/workbook.xml"))
        hojas = len(raiz.findall(".//m:sheet", NS))
        for nombre in libro.namelist():
            if not nombre.startswith("xl/worksheets/sheet") or not nombre.endswith(".xml"):
                continue
            xml = ET.fromstring(libro.read(nombre))
            formulas += len(xml.findall(".//m:f", NS))
            celdas_error += len(xml.findall('.//m:c[@t="e"]', NS))

    if hojas < 30:
        errores.append(f"Se esperaban al menos 30 hojas y se encontraron {hojas}.")
    if formulas < 1000:
        errores.append(f"El libro parece estático: solo contiene {formulas} fórmulas.")
    if celdas_error:
        errores.append(f"El XML contiene {celdas_error} celdas de error.")

    print(f"Hojas: {hojas}")
    print(f"Fórmulas serializadas: {formulas}")
    print(f"Celdas de error: {celdas_error}")
    print(f"SHA-256: {digest}")
    if errores:
        for error in errores:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Publicación válida.")


if __name__ == "__main__":
    main()
