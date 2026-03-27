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
  <img src="https://img.shields.io/badge/OEE-81%25_%E2%86%92_86%25-000000?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Tecnomatix-Plant_Simulation-000000?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/VPN-COP_2.18B-000000?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/TIR-23.16%25_anual-000000?style=flat-square"/>
</p>

# ulogix-data-finance

Repositorio técnico-financiero del proyecto de automatización brownfield para **FEMSA Fontibón** — Coca-Cola FEMSA.
Cubre: **Gestión y Evaluación de Producción**, **Planeación de Proyectos**, **MES / Valor Agregado** y **Cuadro Resumen**.

> Archivo base del modelo: `modelo_femsa_automatizacion_2026.xlsm` — reporte detallado: `reporte_detallado_version_adjunta_femsa.pdf`

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Estructura

```
ulogix-data-finance/
├── financiero/
│   ├── flujo-caja/           modelo_femsa_automatizacion_2026.xlsm
│   ├── presupuesto/          Memorias_calculo_consumo.xlsx
│   ├── indicadores/          VPN · TIR · Payback
│   └── propuesta-valor/      Reporte de estudio de mercado.docx
├── oee/                      OEE base 81% → objetivo 86% · scripts Python
│   └── scripts/
├── power-bi/
│   ├── datasets/             Fuentes OPC/SQL desde Ignition/SCADA
│   └── reportes/             Dashboards .pbix
├── simulacion/
│   ├── modelos/              Tecnomatix · Plant Simulation
│   └── resultados/           VSM actual / futuro por línea
├── tiempos/
│   ├── setup-tiempos/        Calculo de tiempos - APM .xlsx
│   ├── takt-time/            Takt time por producto
│   └── mlt/                  Manufacturing Lead Time por línea
└── reportes/                 reporte_detallado_version_adjunta_femsa.pdf · cuadro resumen
```

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Indicadores Financieros Clave (Modelo Base)

| Indicador | Valor |
|---|---|
| **TMAR anual** | 18,00 % |
| **VPN** | COP 2.180.752.718 |
| **TIR mensual** | 1,75 % |
| **TIR anual efectiva** | 23,16 % |
| **Payback simple** | 39 meses (3,25 años) |
| **Payback descontado** | 54 meses |
| **CAPEX total con contingencia** | COP 22.065.297.358 |
| **FCF acumulado mes 60** | COP 14.410.833.940 |
| **OPEX mensual licencias** | COP 14.180.736,67 |
| **Nómina mensual operación** | COP 85.915.382 |
| **Costo implementación ULogix (4 meses)** | COP 348.647.040 |

> El proyecto supera el filtro financiero en el escenario base (TIR 23,16% > TMAR 18%). La variable crítica de riesgo es el CAPEX: un incremento del +10% prácticamente elimina el VPN.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## VSM — Resultados Actuales por Línea

| Línea | Producto | Lead Time | VA | Tc |
|---|---|---|---|---|
| **Línea 2** | Bebida carbonatada — Vidrio 330 mL | 9.64 h | 6.602 s | 0.072 s/u |
| **Línea 3** | Bebida PET 1.5 L | 12.0 h | 5.61 s | 0.420 s/u |
| **Línea 7** | Agua purificada — Garrafón 25 L | 8.4 h | 22.56 s | 2.52 s/u |

## OEE y Demanda (Modelo del Equipo)

```
OEE base:    81,00 %  → Objetivo post-automatización: 86,00 %
Throughput:  +11,00 % meta de mejora
Nivel servicio base:    90,00 %  → proyecto: 99,00 %
Demanda anual total:    159.000.000 L
Inicio del modelo:      2026-04-01  (60 meses · 4 meses preoperativos)
TRM:                    COP 3.850 / USD
Inflación anual:        5,29 %  (IPC feb-2026)
Tasa renta corporativa: 35,00 %
```

### Cobertura de Capacidad por Producto (mes 1)

| Producto | Mix | Cap. base (u/mes) | Cap. proyecto (u/mes) | Cobertura |
|---|---|---|---|---|
| 330 mL retornable | 50 % | 28.350.000 | 34.965.000 | 1,68x |
| PET 1.5 L | 35 % | 8.100.000 | 9.990.000 | 3,11x |
| Garrafón 25 L | 15 % | 405.000 | 499.500 | 6,04x |

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## CAPEX por Categoría

| Categoría | Base depreciable | Vida útil | Cargo mensual |
|---|---|---|---|
| Equipos principales | COP 11.838.365.000 | 10 años | COP 98.653.042 |
| Automatización e instrumentación | COP 5.844.496.235 | 7 años | COP 69.577.336 |
| Servicios capitalizables | COP 2.134.000.000 | 5 años | COP 35.566.667 |
| Intangibles capacitación | COP 242.500.000 | 3 años | COP 6.736.111 |
| Software perpetuo | COP 34.650.000 | 3 años | COP 962.500 |

**Subtotal CAPEX:** COP 20.059.361.235 · **Contingencia 10%:** COP 2.005.936.123 · **Total:** COP 22.065.297.358

## Sensibilidad de Escenarios

| Escenario | Ventas/beneficio | CAPEX | TMAR | VPN | TIR mensual |
|---|---|---|---|---|---|
| Conservador | −5% | +15% | 20,00 % | **−COP 3.070.965.997** | 1,05 % |
| **Base** | 0% | 0% | 18,00 % | **COP 2.180.752.718** | 1,75 % |
| Optimista | +5% | −10% | 16,00 % | **COP 6.552.278.207** | 2,36 % |

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
    • EDT (WBS) y cronograma — S. Sanchez<br/>
    • Modelo financiero: <code>modelo_femsa_automatizacion_2026.xlsm</code> — VPN COP 2.18B · TIR 23.16%<br/>
    • Indicadores: VPN, TIR, Payback simple 39 meses / descontado 54 meses<br/>
    • Propuesta de valor y oferta comercial — J. Garzón / S. Sanchez
  </td>
</tr>
<tr>
  <td align="center"><img src="https://raw.githubusercontent.com/ulogix-team/assets/main/icons/node-tech.svg" width="50"/></td>
  <td>
    <strong>power-bi/ + oee/</strong> — MES y Valor Agregado (May 9)<br/>
    • MES con Power BI — dashboards de OEE, producción y calidad — S. Sanchez<br/>
    • Analítica de datos con Python desde PLC — J. Triana<br/>
    • OEE base: 81% → objetivo: 86% con automatización completa
  </td>
</tr>
<tr>
  <td align="center"><img src="https://raw.githubusercontent.com/ulogix-team/assets/main/icons/node-tech.svg" width="50"/></td>
  <td>
    <strong>reportes/</strong> — Cuadro Resumen (May 12)<br/>
    • Reporte técnico-financiero: <code>reporte_detallado_version_adjunta_femsa.pdf</code> (15 págs, 2026-03-26)<br/>
    • Evidencia tiempos antes/después de automatizar por línea<br/>
    • FCF acumulado al mes 60: COP 14.410.833.940 — J. Garzón / S. Sanchez
  </td>
</tr>
</table>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Responsables

| Módulo | Responsable | GitHub |
|---|---|:---:|
| **Finanzas · EDT · GitHub/Docs · MES Power BI** | **Samuel David Sanchez Cardenas** | [@samsanchezcar](https://github.com/samsanchezcar) |
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
