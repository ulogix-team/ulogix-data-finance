<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

# oee — Overall Equipment Effectiveness

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

Cálculo y análisis del OEE por línea y producto. Los valores del modelo financiero (`modelo_femsa_automatizacion_2026.xlsm`) definen el OEE base como **81%** con objetivo post-automatización de **86%**.

## Fórmula

```
OEE = Disponibilidad × Eficiencia × Calidad
```

## Valores del Modelo Financiero (Hoja Supuestos)

| Indicador | Valor |
|---|---|
| OEE base (hoja Supuestos) | **81,00 %** |
| OEE objetivo | **86,00 %** |
| Meta mejora throughput | +11,00 % |
| Rechazo base | 0,07 % |

## Valores Preliminares (Cálculo de Tiempos — APM)

| Indicador | Valor | Fórmula |
|---|---|---|
| Disponibilidad | **89,29 %** | T_real / T_planeado = 6.25 / 7.00 |
| Eficiencia | **88,17 %** | Vol_real × Tc / T_real |
| Calidad | **99,93 %** | 1 − (% rechazo) = 1 − 0,07% |
| **OEE calculado** | **≈ 78,67 %** | 0,8929 × 0,8817 × 0,9993 |

> Nota: el modelo financiero usa OEE base = 81% (hoja Supuestos), coherente con el promedio de las tres líneas evaluadas.

## OEE por Línea (Objetivo Post-Automatización)

| Línea | Producto | OEE base | OEE Objetivo |
|---|---|---|---|
| Línea 2 — 330 mL retornable | Bebida carbonatada vidrio | — | ≥ 86 % |
| Línea 3 — PET 1.5 L | Bebida carbonatada PET | — | ≥ 86 % |
| Línea 7 — Garrafón 25 L | Agua purificada | — | ≥ 86 % |

## Nivel de Servicio

| Indicador | Valor |
|---|---|
| Nivel de servicio base | 90,00 % |
| Nivel de servicio proyecto | 99,00 % |
| Factor monetización uplift comercial | 31,00 % |

> El salto de servicio base→proyecto (90%→99%) no se monetiza al 100%, sino en un 31%, lo que hace el caso financiero más conservador y realista.

## Contenido esperado

- `scripts/` — Scripts Python para cálculo automatizado desde datos SCADA/PLC (OPC-UA → Power BI)

## Responsables

| Rol | Nombre | GitHub |
|---|---|:---:|
| OEE / Proceso / VSM | Jorge Nicolas Garzón Acevedo | [@Nicolas-Eule](https://github.com/Nicolas-Eule) |
| **MES / Power BI / Python** | **Samuel David Sanchez Cardenas** | [@samsanchezcar](https://github.com/samsanchezcar) |
| SCADA / Datos PLC | Juan Felipe Triana Aguilera | [@jutrianaa](https://github.com/jutrianaa) |

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
