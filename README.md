<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/logos/ulogix-icon-transparent-dark.svg" height="55"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Power_BI-MES_Analytics-000000?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Python-Analítica_desde_PLC-000000?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/OEE-Indicadores_Productivos-000000?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Tecnomatix-Simulación-000000?style=flat-square"/>
</p>

# ulogix-data-finance

Repositorio de análisis productivo, simulación y evaluación económica de la línea FEMSA.  
Cubre los módulos: **Gestión y Evaluación de Producción**, **Planeación y Evaluación de Proyectos**, **Valor Agregado** y **Cuadro Resumen**.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Estructura

```
ulogix-data-finance/
├── oee/          OEE por línea y producto · scripts Python de análisis
├── tiempos/      Takt time · tiempos de setup · MLT · análisis de tiempos
├── simulacion/   Simulación Tecnomatix / Plant Simulation · VSM actual y futuro
├── financiero/   EDT · presupuesto · flujo de caja · VPN · TIR · propuesta de valor
├── power-bi/     Dashboards MES (.pbix) · datasets OPC/SQL
└── reportes/     Cuadro resumen antes/después · informes consolidados
```

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Tareas por Módulo

<table>
<tr>
  <td align="center"><img src="https://raw.githubusercontent.com/ulogix-team/assets/main/icons/node-tech.svg" width="50"/></td>
  <td>
    <strong>simulacion/ + tiempos/</strong> — Módulo 2 · Gestión de Producción (Mar 19–21)<br/>
    • VSM – Estado actual (Mar 19) — J. Garzón<br/>
    • VSM – Estado futuro (Mar 21) — J. Garzón<br/>
    • Simulación en Tecnomatix / Plant Simulation (Mar 21) — S. Sanchez / J. Garzón<br/>
    • Cálculo Takt time, OEE, MLT
  </td>
</tr>
<tr>
  <td align="center"><img src="https://raw.githubusercontent.com/ulogix-team/assets/main/icons/node-tech.svg" width="50"/></td>
  <td>
    <strong>financiero/</strong> — Módulo 3 · Planeación de Proyectos (Mar 23–24)<br/>
    • EDT (WBS) y cronograma del proyecto (Mar 23) — S. Sanchez<br/>
    • Análisis económico: presupuesto y flujo de caja (Mar 23) — S. Sanchez<br/>
    • Indicadores financieros: VPN, TIR, Payback (Mar 23) — S. Sanchez<br/>
    • Propuesta de valor y oferta comercial (Mar 24) — J. Garzón / S. Sanchez
  </td>
</tr>
<tr>
  <td align="center"><img src="https://raw.githubusercontent.com/ulogix-team/assets/main/icons/node-tech.svg" width="50"/></td>
  <td>
    <strong>power-bi/ + oee/</strong> — Valor Agregado (May 9)<br/>
    • MES con Power BI (May 9) — J. Triana<br/>
    • Analítica de datos con Python desde PLC (May 9) — J. Triana / J. Díaz
  </td>
</tr>
<tr>
  <td align="center"><img src="https://raw.githubusercontent.com/ulogix-team/assets/main/icons/node-tech.svg" width="50"/></td>
  <td>
    <strong>reportes/</strong> — Cuadro Resumen (May 12)<br/>
    • Evidencia tiempos antes/después de automatizar<br/>
    • Costo total del proyecto<br/>
    • Diferencial de la propuesta — J. Garzón / S. Sanchez
  </td>
</tr>
</table>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Indicadores Clave (Rúbrica Módulo 2)

| Indicador | Descripción | Herramienta | Fecha |
|---|---|---|---|
| **OEE** | Disponibilidad × Rendimiento × Calidad | Excel / Python | May 9 |
| **Takt Time** | Ritmo de producción requerido | Tecnomatix | Mar 21 |
| **MLT** | Manufacturing Lead Time | Simulación | Mar 21 |
| **VSM** | Value Stream Mapping antes/después | Draw.io | Mar 21 |
| **VPN** | Valor Presente Neto | Excel | Mar 23 |
| **TIR** | Tasa Interna de Retorno | Excel | Mar 23 |
| **Payback** | Periodo de recuperación | Excel | Mar 23 |

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Productos Analizados

| Producto | Línea | Volumen | OEE Objetivo |
|---|---|---|---|
| Agua purificada | Línea 2 | 600 mL | ≥ 85% |
| Bebida energética | Línea 3 | 2 L | ≥ 80% |
| Jugo natural | Línea 7 | 20 L | ≥ 75% |

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Responsables

| Módulo | Responsable | GitHub |
|---|---|:---:|
| **Finanzas / VPN / TIR / EDT / GitHub & Docs** | **Samuel David Sanchez Cardenas** | [@samsanchezcar](https://github.com/samsanchezcar) |
| VSM / OEE / Simulación / Proceso | Jorge Nicolas Garzón Acevedo | [@Nicolas-Eule](https://github.com/Nicolas-Eule) |
| Power BI / Python / MES | Juan Felipe Triana Aguilera | [@jutrianaa](https://github.com/jutrianaa) |

**Supervisores académicos:** Carlos J. Cortés · Luis M. Méndez · Víctor H. Grisales · Ricardo Ramírez · Ubaldo García · Eduardo Barrera

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Flujo de Trabajo

```
main ──────────────────► producción estable
  └── develop ─────────► integración y desarrollo
```

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
