<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

# financiero — Análisis Económico del Proyecto

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

Evaluación técnico-económica del retrofit brownfield para FEMSA Fontibón. El modelo cubre 60 meses desde 2026-04-01 con 4 meses preoperativos, 3 turnos y continuidad operativa durante la implementación.

## Archivos

| Archivo | Carpeta | Descripción |
|---|---|---|
| `modelo_femsa_automatizacion_2026.xlsm` | `flujo-caja/` | Modelo financiero completo (15 hojas) |
| `Memorias_calculo_consumo.xlsx` | `presupuesto/` | Memorias de cálculo de consumo energético |
| `Reporte de estudio de mercado.docx` | `propuesta-valor/` | Propuesta de valor y oferta comercial |

## Resultados del Modelo (`modelo_femsa_automatizacion_2026.xlsm`)

### KPIs Financieros

| Indicador | Valor |
|---|---|
| TMAR anual | 18,00 % |
| TMAR mensual | 1,39 % |
| **VPN** | **COP 2.180.752.718** |
| TIR mensual | 1,75 % |
| **TIR anual efectiva** | **23,16 %** |
| Payback simple | **39 meses** (3,25 años) |
| Payback descontado | **54 meses** |
| CAPEX total con contingencia | COP 22.065.297.358 |
| FCF acumulado mes 60 | COP 14.410.833.940 |

### Supuestos Macro

| Parámetro | Valor |
|---|---|
| Fecha inicio | 2026-04-01 |
| Horizonte | 60 meses |
| Meses preoperativos | 4 |
| Inflación anual | 5,29 % |
| TRM COP/USD | 3.850 |
| Tasa renta corporativa | 35,00 % |
| OEE base → objetivo | 81 % → 86 % |
| Throughput mejora | +11 % |
| Factor monetización uplift | 31 % |
| Factor RFQ/reuso activos | 97 % |

### Cronograma de Implementación (4 meses preoperativos)

| Fase | Inicio | Fin | Peso CAPEX |
|---|---|---|---|
| Ingeniería de detalle / especificación | Abr-2026 | May-2026 | 20 % |
| Compras OEM / software / paneles | Abr-2026 | Jun-2026 | 35 % |
| Instalación y montaje | May-2026 | Jul-2026 | 25 % |
| FAT/SAT + integración + ciberseguridad | Jun-2026 | Jul-2026 | 10 % |
| Capacitación / arranque / estabilización | Jul-2026 | Ago-2026 | 10 % |

### FCF por Año (Resumen)

| Año | Ingresos incrementales | EBITDA incremental | FCF |
|---|---|---|---|
| Año 1 | COP 15.982.635.404 | COP 8.053.914.020 | −COP 17.740.891.911 |
| Año 2 | COP 20.897.988.115 | COP 10.760.744.027 | COP 7.866.622.082 |
| Año 3 | COP 21.211.457.937 | COP 10.935.072.412 | COP 7.979.693.383 |
| Año 4 | COP 21.529.629.806 | COP 11.112.015.723 | COP 8.094.460.753 |
| Año 5 | COP 21.852.574.253 | COP 11.291.613.183 | COP 8.210.949.634 |

### Sensibilidad

| Variable | Cambio | VPN estimado |
|---|---|---|
| CAPEX | −10 % | COP 4.390.747.454 |
| CAPEX | +10 % | −COP 29.242.018 |
| Ventas/beneficio | −5 % | COP 2.071.715.082 |
| Ventas/beneficio | +5 % | COP 2.289.790.354 |
| TMAR | −2 p.p. | COP 2.355.212.935 |
| TMAR | +2 p.p. | COP 2.006.292.500 |

> **Riesgo crítico:** el CAPEX es la variable más sensible. Un aumento del 10% prácticamente elimina el VPN del escenario base.

## Responsables

Samuel David Sanchez Cardenas · [@samsanchezcar](https://github.com/samsanchezcar)
Jorge Nicolas Garzón Acevedo · [@Nicolas-Eule](https://github.com/Nicolas-Eule)

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
