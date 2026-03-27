<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

# power-bi — MES Analytics (Manufacturing Execution System)

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

Dashboards de Manufacturing Execution System (MES) con Power BI, conectados a datos del PLC/SCADA. Módulo Valor Agregado del proyecto integrador APM 2026-1.

## Indicadores a Visualizar

| Dashboard | KPIs | Fuente de datos |
|---|---|---|
| OEE por línea | Disponibilidad, Eficiencia, Calidad | PLC / Logix Emulate vía OPC-UA |
| Producción en tiempo real | Unidades/h, rechazos, paros | SCADA Ignition |
| Comparativo antes/después | OEE base 81% → objetivo 86% | Histórico + simulación |
| Análisis de paros | Tiempo inactividad planeada vs no planeada | PLC / SCADA |
| Financiero ejecutivo | VPN COP 2.18B · TIR 23.16% · Payback 39m | modelo_femsa_automatizacion_2026.xlsm |

## OEE Base (Modelo Financiero — Hoja Supuestos)

```
OEE base:     81,00 %  → objetivo post-automatización: 86,00 %
Throughput:   +11,00 % meta de mejora
Nivel servicio base:    90 %  → proyecto: 99 %
Factor monetización uplift:  31 %
```

## Licencias Software (del Modelo)

| Software | Modalidad | CAPEX inicial | OPEX mensual |
|---|---|---|---|
| Studio 5000 Logix Designer | Perpetua | COP 34.650.000 | — |
| ABB RobotStudio Premium | Anual | — | COP 770.000 |
| Microsoft Azure IoT + storage | Mensual | — | COP 6.000.000 |
| NI LabVIEW Full | Anual | — | COP 555.362,50 |
| Siemens NX Manufacturing | Mensual | — | COP 1.694.000 |
| Siemens Plant Simulation X | Anual | — | COP 4.038.457,50 |
| Ignition / SCADA runtime | Anual | — | COP 1.122.916,67 |
| **Total OPEX mensual licencias** | | | **COP 14.180.736,67** |

## Contenido esperado

- `reportes/` — Archivos `.pbix` con dashboards de producción, calidad y eficiencia
- `datasets/` — Fuentes de datos (`.csv`, `.xlsx`, conectores OPC/SQL desde Ignition)

## Responsables

| Rol | Nombre | GitHub |
|---|---|:---:|
| **MES / Power BI (Responsable principal)** | **Samuel David Sanchez Cardenas** | [@samsanchezcar](https://github.com/samsanchezcar) |
| SCADA / Datos fuente | Juan Felipe Triana Aguilera | [@jutrianaa](https://github.com/jutrianaa) |
| Supervisor de par | Jorge Nicolas Garzón Acevedo | [@Nicolas-Eule](https://github.com/Nicolas-Eule) |

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
