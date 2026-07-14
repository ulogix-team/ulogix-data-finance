<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

# Modelo financiero · FEMSA Fontibón

Evaluación demand-driven a 60 meses del retrofit de L1, L2 y L3. El libro de Google Sheets es el modelo vivo; el [XLSX publicado](modelo/Modelo_FEMSA_Ulogix_2026.xlsx) es una copia auditable del estado indicado en su manifiesto.

## Indicadores vigentes

| Indicador | Valor |
|---|---:|
| TMAR anual | 18,00 % |
| VPN | **COP 11.032.069.063** |
| TIR anual efectiva | **78,2 %** |
| ROI | **226,7 %** |
| Payback simple / descontado | **22 / 25 meses** |
| CAPEX total con contingencia | **COP 9.165.554.245** |
| CAPEX de software | COP 112.086.015 |
| OPEX licencias y hosting | COP 8.262.150/mes |

## De dónde sale cada cifra

| Bloque | Fuente viva | Regla |
|---|---|---|
| CAPEX | `CAPEX` | 85 activos en bloques L1, L2, L1-L2 compartido, L3 y común; pie y subtotales con fórmulas |
| Ingeniería | `APU_Ingenieria` | Cantidades y tarifas editables; AIU como referencia de mercado; totales enlazados a CAPEX |
| Licencias | `Licencias` | CAPEX perpetuo separado de OPEX recurrente |
| Nómina | `RRHH` | Roster individual → resumen por rol → costo empleador |
| Operación | `Tiempos` | Estado antes/después, OEE +5 % relativo, MLT, máquinas y capacidad |
| Demanda | `Demanda` y `DemandaEscenario` | Rangos posicionales escritos por el ERP; no se reordenan |
| Valoración | `Flujo_Caja`, `Sensibilidad`, `Reportes` | Fórmulas enlazadas, horizonte de 60 meses |

## Alcance del CAPEX

- L1: llenadora KRONES usada, encajonadora custom y conexión a la celda compartida.
- L2: llenadora KRONES usada, Variopac usada y conexión a la celda compartida.
- L1-L2: GANTRY ABB común, alternado entre las dos líneas, con BOM de ingeniería detallada.
- L3: robot ABB cotizado por EUROBOTS a GBP 13.500 con envío/logística; se conserva la llenadora existente.
- Controlador ABB IRC5: cotización IGAM de USD 6.500 con envío/logística.
- Común: Ignition SCADA, MES, ERP/Odoo, Coreflux/UNS, Tecnomatix Plant Simulation, Siemens NX y RobotStudio según modalidad de licencia.
- Fuera de alcance: lavadoras nuevas e inspección de línea; las alternativas evaluadas permanecen con cantidad cero para conservar trazabilidad.

## Archivos

| Ruta | Estado | Uso |
|---|---|---|
| `modelo/Modelo_FEMSA_Ulogix_2026.xlsx` | **Vigente** | Snapshot reproducible del libro vivo |
| `modelo/modelo.manifest.json` | **Vigente** | Fecha, hash y procedencia de la publicación |
| `flujo-caja/modelo_femsa_automatizacion_2026.xlsm` | Legado | Modelo inicial; no usar para decisiones actuales |
| `presupuesto/Memorias_calculo_consumo.xlsx` | Memoria técnica | Evidencia auxiliar de consumo |

La metodología y las pruebas de consistencia están en [`../docs/METODOLOGIA_VIABILIDAD.md`](../docs/METODOLOGIA_VIABILIDAD.md).

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
