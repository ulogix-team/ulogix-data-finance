<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

# oee — Overall Equipment Effectiveness

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

Cálculo y análisis del OEE por línea y producto. Los valores preliminares provienen del archivo Excel del equipo (taller Módulo 2 — Gestión de Producción).

## Fórmula

```
OEE = Disponibilidad × Eficiencia × Calidad
```

## Valores Preliminares (Modelo del Equipo)

| Indicador | Valor | Fórmula |
|---|---|---|
| Disponibilidad | **89.29 %** | T_real / T_planeado = 6.25 / 7.00 |
| Eficiencia | **88.17 %** | Vol_real × Tc / T_real |
| Calidad | **99.93 %** | 1 − (% rechazo) = 1 − 0.07% |
| **OEE** | **≈ 78.67 %** | 0.8929 × 0.8817 × 0.9993 |

> Referencia de clase mundial: OEE ≥ 85%. La línea de base del 78.67% es el punto de partida para la mejora mediante automatización.

## OEE por Línea (Objetivo Post-Automatización)

| Línea | Producto | OEE Objetivo |
|---|---|---|
| Línea 2 — 330 mL retornable | Bebida carbonatada vidrio | ≥ 85 % |
| Línea 3 — PET 1 L–2 L | Bebida carbonatada PET | ≥ 80 % |
| Línea 7 — Garrafón 20 L | Agua purificada | ≥ 75 % |

## Contenido esperado

- `calculo-oee.xlsx` — Hoja consolidada con OEE por producto y línea
- `scripts/` — Scripts Python para cálculo automatizado desde datos SCADA/PLC

## Responsables

| Rol | Nombre | GitHub |
|---|---|:---:|
| OEE / Proceso / VSM | Jorge Nicolas Garzón Acevedo | [@Nicolas-Eule](https://github.com/Nicolas-Eule) |
| **MES / Power BI / Python** | **Samuel David Sanchez Cardenas** | [@samsanchezcar](https://github.com/samsanchezcar) |
| SCADA / Datos PLC | Juan Felipe Triana Aguilera | [@jutrianaa](https://github.com/jutrianaa) |

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
