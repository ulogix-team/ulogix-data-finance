# Reglas de trabajo de ulogix-data-finance

- Responder y documentar en español.
- El Google Sheet conectado al ERP es la fuente viva de CAPEX, licencias, APU, RRHH, parámetros y resultados. Los XLSX versionados son snapshots de publicación.
- No sustituir cifras vivas por las constantes fallback de `ulogix-fontibon-suite/core/finanzas_negocio.py`.
- Mantener las líneas como L1 (Coca-Cola 350 ml vidrio), L2 (QuAtro 1.5 L PET) y L3 (garrafón 25 L).
- No volver al esquema histórico de líneas 2/3/7 ni al OEE plano 81%→86%.
- La mejora fase 1 de OEE es exactamente +5% relativo por línea; ≥86% es una meta aspiracional separada.
- El OEE vivo procede del UNS MQTT; `Tiempos` y los libros de ingeniería son documentales.
- Conservar el modelo `.xlsm` inicial como legado identificado; no presentarlo como vigente.
- No versionar `.env`, cuentas de servicio, API keys ni IDs privados.
- Usar los assets visuales de `ulogix-team/assets` en documentación principal.
- La asistencia de IA se declara en README, pero ninguna herramienta de IA debe figurar como autora, coautora o colaboradora de commits.
