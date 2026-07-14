# Arquitectura del modelo técnico-financiero

## Capas

1. **Evidencia:** históricos KOF, pronóstico por SKU, BOM, cotizaciones, referencias de mercado, roster y levantamientos de tiempos.
2. **Ingeniería:** estados antes/después, OEE bottom-up, MLT, capacidad, selección de máquinas, CAPEX por línea y APU.
3. **Planeación:** escenarios de demanda, MRP, inventario, cronograma, depreciación, resultados y flujo de caja.
4. **Ejecución:** ERP Streamlit, Odoo, UNS MQTT, SCADA/MES y stock en vivo.
5. **Publicación:** Google Sheets como fuente viva y este repositorio como snapshot auditable.

## Fronteras que no deben mezclarse

- `Tiempos` documenta supuestos y estados de ingeniería; no reemplaza el OEE medido por MQTT.
- `CAPEX` y `Licencias` gobiernan el motor financiero; el código Python solo aporta defaults cuando Sheets no está disponible.
- `Demanda` y `DemandaEscenario` usan rangos fijos consumidos por fórmulas. No se deben reordenar o reemplazar con `clear+append`.
- `data/maestro_productos.csv` gobierna el maestro físico de Odoo/MRP y es independiente del maestro de unit economics.

## Flujo de cálculo

```text
Pronóstico ─► demanda activa ─► capacidad / inventario / MRP
                                  │
CAPEX + APU + Licencias + RRHH ───┼─► depreciación / OPEX
                                  │
Precios + costos por SKU ─────────┼─► ER incremental
                                  ▼
                             Flujo de caja
                                  ▼
                         VPN · TIR · ROI · payback
```
