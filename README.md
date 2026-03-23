<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Power%20BI-MES%20Analytics-7C3AED?style=flat-square&logo=powerbi"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Python-Análisis%20de%20Datos-a855f7?style=flat-square&logo=python"/>
  &nbsp;
  <img src="https://img.shields.io/badge/OEE-Indicadores%20Productivos-7C3AED?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Excel-Cálculo%20Financiero-0e0525?style=flat-square"/>
</p>

# ulogix-data-finance · Datos, OEE y Análisis Financiero

Repositorio de análisis productivo y evaluación económica del proyecto. Abarca el cálculo de indicadores de desempeño (OEE, Takt time, MLT), simulación de producción, análisis financiero (VPN, TIR, flujo de caja) y desarrollo de dashboards con Power BI.

<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>
</p>

## 📁 Estructura del Repositorio

```
ulogix-data-finance/
│
├── oee/                        # Overall Equipment Effectiveness
│   ├── calculo-oee.xlsx        # Hojas de cálculo OEE por línea/producto
│   ├── scripts/                # Scripts Python de análisis OEE
│   └── README.md
│
├── tiempos/                    # Análisis de tiempos de producción
│   ├── takt-time/              # Cálculo Takt time por producto
│   ├── setup-tiempos/          # Tiempos de set-up y cambio de producto
│   ├── mlt/                    # Manufacturing Lead Time
│   └── README.md
│
├── simulacion/                 # Simulación del sistema productivo
│   ├── modelos/                # Modelos de simulación
│   ├── resultados/             # Outputs y análisis comparativo
│   └── README.md
│
├── financiero/                 # Análisis económico del proyecto
│   ├── presupuesto/            # EDT y presupuesto por módulo
│   ├── flujo-caja/             # Proyecciones de flujo de caja
│   ├── indicadores/            # VPN, TIR, payback
│   ├── propuesta-valor/        # Oferta comercial y diferencial
│   └── README.md
│
├── power-bi/                   # Dashboards MES con Power BI
│   ├── reportes/               # Archivos .pbix
│   ├── datasets/               # Fuentes de datos
│   └── README.md
│
└── reportes/                   # Informes consolidados
    └── README.md
```

<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>
</p>

## 📊 Indicadores Clave

| Indicador | Descripción | Herramienta |
|---|---|---|
| **OEE** | Overall Equipment Effectiveness (Disponibilidad × Rendimiento × Calidad) | Excel / Python |
| **Takt Time** | Ritmo de producción requerido por demanda | Excel |
| **MLT** | Manufacturing Lead Time | Simulación |
| **VSM** | Value Stream Mapping antes/después | Draw.io |
| **VPN** | Valor Presente Neto del proyecto | Excel |
| **TIR** | Tasa Interna de Retorno | Excel |
| **Payback** | Periodo de recuperación de inversión | Excel |

<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>
</p>

## 🏭 Productos Analizados

| Producto | Línea | Volumen | OEE Objetivo |
|---|---|---|---|
| Agua purificada | Línea 2 | 600 mL BM | ≥ 85% |
| Bebida energética | Línea 3 | 2 L MV | ≥ 80% |
| Jugo natural | Línea 7 | 20 L GV | ≥ 75% |

<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>
</p>

## 👥 Responsables

| Módulo | Responsable | GitHub |
|---|---|---|
| Finanzas / Análisis Económico | Samuel David Sanchez Cardenas | [@samsanchezcar](https://github.com/samsanchezcar) |
| Planeación de Proceso / OEE | Jorge N. Garzón | [@Nicolas-Eule](https://github.com/Nicolas-Eule) |
| SCADA / MES / Power BI | Juan F. Triana | [@jutrianaa](https://github.com/jutrianaa) |

**Supervisores académicos:** Carlos J. Cortés · Luis M. Méndez · Víctor H. Grisales · Ricardo Ramírez · Ubaldo García · Eduardo Barrera

<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>
</p>

## 🔗 Repositorios Relacionados

- [ulogix-manufacturing](https://github.com/ulogix-team/ulogix-manufacturing) — Proceso, planta, gemelo digital
- [ulogix-scada-control](https://github.com/ulogix-team/ulogix-scada-control) — SCADA, datos en tiempo real
- [ulogix-team.github.io](https://ulogix-team.github.io) — Sitio web del proyecto

<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
</p>
