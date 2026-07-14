"""Publica el Google Sheet financiero como XLSX sin versionar credenciales."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]


def _argumentos() -> argparse.Namespace:
    raiz = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=raiz / ".env")
    parser.add_argument(
        "--output",
        type=Path,
        default=raiz / "financiero" / "modelo" / "Modelo_FEMSA_Ulogix_2026.xlsx",
    )
    return parser.parse_args()


def _resolver_credencial(valor: str, env_file: Path) -> Path:
    ruta = Path(valor).expanduser()
    if ruta.is_absolute():
        return ruta
    return (env_file.resolve().parent / ruta).resolve()


def main() -> None:
    args = _argumentos()
    load_dotenv(args.env_file, override=False)
    spreadsheet_id = os.getenv("SHEETS_SPREADSHEET_ID", "").strip()
    credencial = os.getenv("GOOGLE_SA_JSON", "").strip()
    if not spreadsheet_id or not credencial:
        raise SystemExit("Faltan SHEETS_SPREADSHEET_ID o GOOGLE_SA_JSON en el entorno.")

    cred_path = _resolver_credencial(credencial, args.env_file)
    if not cred_path.is_file():
        raise SystemExit(f"No existe la cuenta de servicio configurada: {cred_path}")

    credentials = service_account.Credentials.from_service_account_file(
        cred_path, scopes=SCOPES
    )
    session = AuthorizedSession(credentials)
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export"
    respuesta = session.get(url, params={"format": "xlsx"}, timeout=120)
    respuesta.raise_for_status()

    salida = args.output.resolve()
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_bytes(respuesta.content)
    digest = hashlib.sha256(respuesta.content).hexdigest()
    manifiesto = {
        "archivo": salida.name,
        "publicado_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": digest,
        "bytes": len(respuesta.content),
        "fuente": "Google Sheets vivo conectado a ulogix-fontibon-suite",
        "regla": "El XLSX es un snapshot; Google Sheets conserva la autoridad operativa.",
    }
    salida.with_name("modelo.manifest.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Publicado: {salida}")
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()
