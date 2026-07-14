<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

<p align="center">
  <img src="https://raw.githubusercontent.com/ulogix-team/assets/main/logos/ulogix-icon-transparent-dark.svg" height="58" alt="ULogix"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/modelo-Google_Sheets_vivo-000000?style=flat-square" alt="Modelo vivo"/>
  &nbsp;
  <img src="https://img.shields.io/badge/CAPEX-COP_9.166B-000000?style=flat-square" alt="CAPEX"/>
  &nbsp;
  <img src="https://img.shields.io/badge/VPN-COP_11.032B-000000?style=flat-square" alt="VPN"/>
  &nbsp;
  <img src="https://img.shields.io/badge/TIR-78.2%25_E.A.-000000?style=flat-square" alt="TIR"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Payback-22_meses-000000?style=flat-square" alt="Payback"/>
</p>

# ULogix · Data & Finance

Repositorio técnico-financiero del retrofit brownfield de **Coca-Cola FEMSA / INDEGA Fontibón**. Integra la evidencia de demanda, tiempos, OEE, capacidad, CAPEX, licencias, APU de ingeniería y viabilidad económica de las tres líneas del proyecto:

| Línea | Producto | Intervención principal |
|---|---|---|
| **L1** | Coca-Cola 350 ml vidrio retornable | Llenadora KRONES usada, encajonadora 30×30 y GANTRY ABB compartido |
| **L2** | QuAtro 1.5 L PET NR | Llenadora KRONES usada, Variopac usada y GANTRY ABB compartido |
| **L3** | Garrafón 25 L retornable | Se conserva la llenadora; se automatiza el paletizado con robot ABB |

> **Fuente de verdad:** el libro de Google Sheets gobierna CAPEX, licencias, parámetros, RRHH y resultados. Los libros incluidos aquí son publicaciones fechadas para auditoría; no sustituyen el modelo vivo ni las integraciones del ERP.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Resultado base vigente

Snapshot publicado el **14 de julio de 2026**:

| Indicador | Resultado |
|---|---:|
| CAPEX total con contingencia | **COP 9.165.554.245** |
| CAPEX de software | COP 112.086.015 |
| OPEX mensual de licencias y hosting | COP 8.262.150 |
| VPN a 60 meses | **COP 11.032.069.063** |
| TIR anual efectiva | **78,2 %** |
| ROI | **226,7 %** |
| Payback simple | **22 meses** |
| Payback descontado | **25 meses** |
| Nómina mensual de operación | COP 85.915.382 |
| Nómina mensual de implementación | COP 87.161.760 |

La evaluación compara explícitamente el estado **antes** de la inversión con el estado **después**. La mejora tecnológica de OEE es exactamente **+5 % relativo por línea**, no un objetivo plano: L1 77,12 %→80,97 %, L2 76,50 %→80,32 % y L3 75,37 %→79,14 %. La meta aspiracional de programa (≥86 %) se documenta aparte.

## Arquitectura de información

```text
KOF / históricos / pronóstico ──► demanda y escenarios ──► MRP / capacidad
                                                               │
Sheets vivo ──► CAPEX · Licencias · APU · RRHH · Tiempos ──────┤
    │                                                          ▼
    ├──► modelo financiero de 60 meses ──► VPN · TIR · ROI · payback
    ├──► ERP Streamlit / Odoo
    └──► snapshot XLSX y documentación de este repositorio

UNS MQTT / MES ──► producción real · OEE vivo
                   (no alimenta las hojas documentales de Tiempos/OEE)
```

La separación entre OEE documental y OEE vivo es deliberada: el modelo de ingeniería compara estados antes/después; el MES toma los KPI operativos exclusivamente del UNS MQTT.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Contenido

```text
ulogix-data-finance/
├── docs/                    arquitectura, gobierno, método y trazabilidad
├── financiero/
│   ├── modelo/              snapshot XLSX vigente + metadatos de publicación
│   ├── flujo-caja/          modelo histórico, conservado como legado
│   ├── presupuesto/         memorias de consumo
│   └── propuesta-valor/     alcance comercial y comparación antes/después
├── pronostico-demanda/      pipeline reproducible, datos, MC, escenarios y Odoo
├── tiempos/                 levantamientos y OEE bottom-up por L1/L2/L3
├── simulacion/              contrato de simulación y comparación de estados
├── oee/                     definición y gobierno del OEE
├── power-bi/                contrato analítico MES
├── reportes/                publicaciones históricas y vigentes
└── tools/                   exportación reproducible del libro vivo
```

Guías centrales:

- [Arquitectura del modelo](docs/ARQUITECTURA_MODELO.md)
- [Gobierno y fuentes de datos](docs/GOBERNANZA_DATOS.md)
- [Metodología de viabilidad](docs/METODOLOGIA_VIABILIDAD.md)
- [Proveedores y cotizaciones CAPEX](docs/PROVEEDORES_CAPEX.md)
- [Trazabilidad y control de versión](docs/TRAZABILIDAD.md)
- [Modelo financiero publicado](financiero/README.md)
- [Pronóstico de demanda](pronostico-demanda/README.md)

## Publicar el modelo vivo

```bash
python -m pip install -r requirements.txt
python tools/exportar_modelo_sheets.py --env-file ../ulogix-fontibon-suite/.env
```

El comando exporta el libro con fórmulas y formato a `financiero/modelo/Modelo_FEMSA_Ulogix_2026.xlsx` y genera un manifiesto SHA-256. La cuenta de servicio y el ID del libro se leen del `.env`; ninguna credencial se versiona.

## Repositorios relacionados

- [`ulogix-fontibon-suite`](https://github.com/ulogix-team/ulogix-fontibon-suite): ERP/MES, Odoo, MRP, MQTT/UNS y consumidor del modelo vivo.
- [`assets`](https://github.com/ulogix-team/assets): identidad visual compartida de la organización.

## Trazabilidad del uso de IA

Se utilizó asistencia de inteligencia artificial para análisis, documentación, revisión de consistencia y automatización de tareas. Las decisiones de ingeniería, cifras, validaciones y publicaciones pertenecen al equipo humano. Las herramientas de IA no figuran como autoras, coautoras ni colaboradoras de los commits.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
