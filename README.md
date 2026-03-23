<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/logos/ulogix-icon-transparent-dark.svg" height="55"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Power_BI-MES_Analytics-000000?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Python-Analítica_PLC-000000?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/OEE-79%25_→_85%25-000000?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Tecnomatix-Plant_Simulation-000000?style=flat-square"/>
</p>

# ulogix-data-finance

Repositorio de análisis productivo, simulación y evaluación económica de la planta FEMSA.  
Cubre: **Gestión y Evaluación de Producción**, **Planeación de Proyectos**, **MES / Valor Agregado** y **Cuadro Resumen**.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Estructura

```
ulogix-data-finance/
├── oee/          OEE por línea · OEE=78.67% base → objetivo ≥85% · scripts Python
├── tiempos/      Takt time · tiempos de setup · MLT
├── simulacion/   VSM estado actual/futuro · Tecnomatix · LT y VA por línea
├── financiero/   EDT · presupuesto · flujo de caja · VPN · TIR · propuesta de valor
├── power-bi/     Dashboards MES (.pbix) · datasets OPC/SQL · reportes automáticos
└── reportes/     Cuadro resumen antes/después · informes consolidados
```

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## VSM — Resultados Actuales por Línea

| Línea | Producto | Lead Time | VA | Tc |
|---|---|---|---|---|
| **Línea 2** | Bebida carbonatada — Vidrio 330 mL | 9.64 h | 6.602 s | 0.072 s/u |
| **Línea 3** | Bebida PET 1 L–2 L | 12.0 h | 5.61 s | 0.420 s/u |
| **Línea 7** | Agua purificada — Garrafón 20 L | 8.4 h | 22.56 s | 2.52 s/u |

## OEE Preliminar (Modelo del Equipo)

```
Disponibilidad:  89.29 %   (Ejec. real 6.25 h / Ejec. planeada 7.00 h)
Eficiencia:      88.17 %   (41,000 u × 0.000168 h / 6.25 h)
Calidad:         99.93 %   (Rechazo 0.07%)
──────────────────────────────────────────
OEE actual:    ≈ 78.67 %   → Objetivo post-automatización: ≥ 85%
```

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Tareas por Módulo

<table>
<tr>
  <td align="center"><img src="https://raw.githubusercontent.com/ulogix-team/assets/main/icons/node-tech.svg" width="50"/></td>
  <td>
    <strong>simulacion/ + tiempos/</strong> — Módulo 2 · Gestión de Producción (Mar 19–21)<br/>
    • VSM estado actual: L2 (LT=9.64h, VA=6.602s) · L3 (LT=12h, VA=5.61s) · L7 (LT=8.4h, VA=22.56s)<br/>
    • VSM estado futuro (post-automatización) — J. Garzón<br/>
    • Simulación Tecnomatix / Plant Simulation (Mar 21) — S. Sanchez / J. Garzón<br/>
    • Takt time · MLT · análisis comparativo antes/después
  </td>
</tr>
<tr>
  <td align="center"><img src="https://raw.githubusercontent.com/ulogix-team/assets/main/icons/node-tech.svg" width="50"/></td>
  <td>
    <strong>financiero/</strong> — Módulo 3 · Planeación de Proyectos (Mar 23–24)<br/>
    • EDT (WBS) y cronograma (Mar 23) — S. Sanchez<br/>
    • Análisis económico: presupuesto y flujo de caja (Mar 23) — S. Sanchez<br/>
    • Indicadores financieros: VPN, TIR, Payback (Mar 23) — S. Sanchez<br/>
    • Propuesta de valor y oferta comercial (Mar 24) — J. Garzón / S. Sanchez
  </td>
</tr>
<tr>
  <td align="center"><img src="https://raw.githubusercontent.com/ulogix-team/assets/main/icons/node-tech.svg" width="50"/></td>
  <td>
    <strong>power-bi/ + oee/</strong> — MES y Valor Agregado (May 9)<br/>
    • MES con Power BI — dashboards de OEE, producción y calidad (May 9) — S. Sanchez<br/>
    • Analítica de datos con Python desde PLC (May 9) — J. Triana / J. Díaz<br/>
    • OEE base: 78.67% → objetivo: ≥ 85% con automatización completa
  </td>
</tr>
<tr>
  <td align="center"><img src="https://raw.githubusercontent.com/ulogix-team/assets/main/icons/node-tech.svg" width="50"/></td>
  <td>
    <strong>reportes/</strong> — Cuadro Resumen (May 12)<br/>
    • Evidencia tiempos antes/después de automatizar por línea<br/>
    • Costo total del proyecto y diferencial de la propuesta — J. Garzón / S. Sanchez
  </td>
</tr>
</table>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Responsables

| Módulo | Responsable | GitHub |
|---|---|:---:|
| **Finanzas · EDT · GitHub/Docs · MES Power BI · NX/DF sup.** | **Samuel David Sanchez Cardenas** | [@samsanchezcar](https://github.com/samsanchezcar) |
| VSM / OEE / Proceso / Simulación | Jorge Nicolas Garzón Acevedo | [@Nicolas-Eule](https://github.com/Nicolas-Eule) |
| SCADA / Python Analytics | Juan Felipe Triana Aguilera | [@jutrianaa](https://github.com/jutrianaa) |

**Supervisores académicos:** Carlos J. Cortés · Luis M. Méndez · Víctor H. Grisales · Ricardo Ramírez · Ubaldo García · Eduardo Barrera

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Flujo de Trabajo

```
main ──────────────────► producción estable
  └── develop ─────────► integración y desarrollo
```

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
