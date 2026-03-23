<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

# power-bi — MES Analytics (Manufacturing Execution System)

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

Dashboards de Manufacturing Execution System (MES) con Power BI, conectados a datos del PLC/SCADA. Módulo Valor Agregado del proyecto integrador APM 2026-1.

## Indicadores a visualizar

| Dashboard | KPIs | Fuente de datos |
|---|---|---|
| OEE por línea | Disponibilidad, Eficiencia, Calidad | PLC / Logix Emulate vía OPC-UA |
| Producción en tiempo real | Unidades/h, rechazos, paros | SCADA Ignition |
| Comparativo antes/después | OEE base 78.67% → objetivo ≥85% | Histórico + simulación |
| Análisis de paros | Tiempo inactividad planeada vs no planeada | PLC / SCADA |

## OEE Base (Modelo Preliminar del Equipo)

```
Disponibilidad:  89.29 %
Eficiencia:      88.17 %
Calidad:         99.93 %
OEE:           ≈ 78.67 %  → objetivo post-automatización: ≥ 85 %
```

## Contenido esperado

- `reportes/` — Archivos `.pbix` con dashboards de producción, calidad y eficiencia
- `datasets/` — Fuentes de datos (`.csv`, `.xlsx`, conectores OPC/SQL desde Ignition)

## Responsables

| Rol | Nombre | GitHub |
|---|---|:---:|
| **MES / Power BI (Responsable principal)** | **Samuel David Sanchez Cardenas** | [@samsanchezcar](https://github.com/samsanchezcar) |
| SCADA / Datos fuente | Juan Felipe Triana Aguilera | [@jutrianaa](https://github.com/jutrianaa) |
| **Supervisor de par** | **Jorge Nicolas Garzón Acevedo** | [@Nicolas-Eule](https://github.com/Nicolas-Eule) |

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
