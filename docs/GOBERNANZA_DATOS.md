# Gobierno y fuentes de datos

| Dominio | Fuente primaria | Consumidor | Control |
|---|---|---|---|
| Pronóstico | Pipeline `pronostico-demanda` + hojas de forecast | ERP, escenarios, MRP | Backtest, MAPE y bandas Monte Carlo |
| CAPEX | Hoja `CAPEX` | Motor financiero | Fórmulas por moneda, subtotales por bloque y contingencia |
| Licencias | Hoja `Licencias` | CAPEX software y OPEX mensual | Modalidad perpetua/anual/mensual separada |
| APU | Hoja `APU_Ingenieria` | Tres servicios de CAPEX | Mano de obra + terceros + materiales + logística + AIU |
| RRHH | Hoja `RRHH` | Nómina de operación e implementación | Roster → resumen por rol → reconciliación |
| Tiempos/OEE de diseño | Hoja `Tiempos` | Capacidad y factibilidad | Comparación antes/después por L1/L2/L3 |
| OEE real | UNS MQTT | MES y base `kpi_uns` | Nunca se toma del ERP financiero |
| Finanzas | Hojas enlazadas del libro | Dashboard y ERP | Barrido de errores de fórmula y reconciliación |

## Jerarquía

1. Google Sheets vivo.
2. Datos transaccionales de ERP/Odoo/MQTT para sus dominios operativos.
3. Snapshot XLSX de este repositorio.
4. Constantes fallback en código.
5. Modelos y reportes históricos, solo como evidencia.

## Seguridad

No se versionan `.env`, cuentas de servicio, tokens, API keys ni credenciales. El script de publicación recibe una ruta de entorno y solo guarda el XLSX más su hash.
