<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

# pronostico-demanda — Estudio de mercado y pronóstico de demanda

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

Pipeline reproducible sobre **datos trimestrales REALES de Coca-Cola FEMSA
Colombia (21 trimestres, 1T-2021 a 1T-2026)**, extraídos de los 17 Reportes de
Resultados Trimestrales (incluidos en `referencias/descargas/`; fuente:
https://investors.coca-colafemsa.com/informacion-financiera/reportes-trimestrales/):
reconstrucción de demanda, análisis estadístico formal, Holt-Winters
amortiguado, simulación Monte Carlo, plan en pallets/lotes, rotación de
inventarios y bases ERP (Odoo). Es la base cuantitativa que alimenta la
propuesta de valor y el modelo financiero del proyecto (`financiero/`) y el
análisis de tiempos/OEE (`tiempos/`).

## 1. Entorno (conda)
```bash
conda env create -f environment.yml
conda activate fontibon-pronostico
```
Librerías: python 3.12, numpy, pandas, scipy, statsmodels, scikit-learn,
matplotlib, openpyxl, requests, jupyterlab (opcional).

## 2. Reproducir todo el pipeline (desde `pronostico-demanda/`)
**Opción A — Notebook guiado (recomendado para lectura):**
```bash
jupyter lab Pipeline_Fontibon.ipynb   # recorre 00→12 con explicaciones y resultados
```
**Opción B — Línea de comandos:**
```bash
python run_all.py                            # ejecuta 00→12 en orden, con QA final
```
o paso a paso:
```bash
python scripts/00_extraer_kof.py             # extrae la tabla Volumen de los 17 PDFs (pypdf)
python scripts/01_reconstruccion_datos.py    # serie trimestral→mensual a escala planta
python scripts/02_pruebas_estadisticas.py    # correlación, rachas, KW, Levene, ACF
python scripts/03_modelo_holt_winters.py     # HW multiplicativo amortiguado → 2026
python scripts/04_evaluacion_errores.py      # MAD, CFE, MSE, MAPE + señal de rastreo
python scripts/05_inventario_lotes.py        # unidades→pallets→lotes + rotación
python scripts/06_export_odoo.py             # CSVs de importación Odoo
python scripts/07_generar_excel.py           # libro operativo (fórmulas Excel)
python scripts/08_distribuciones.py          # ajuste Normal: KS, Anderson-Darling, χ²
python scripts/09_montecarlo.py              # simulación N=10.000 → bandas P5–P95
python scripts/10_multivariado.py            # Box-Plot, correlación, ACF/PACF, PCA
python scripts/11_diagrama_flujo.py          # figura de metodología
python scripts/12_verificacion.py            # QA: 6 verificaciones automáticas (V1–V6)
python scripts/13_escenarios.py              # escenarios de demanda ("¿qué pasa si...?")
python scripts/14_excel_escenarios.py        # agrega la hoja Escenarios al Excel
```
Cada script imprime resultados y escribe en `data/` y `figuras/`.

## 3. Referencias primarias (descarga)
Los 17 reportes trimestrales YA están incluidos en `referencias/descargas/`.
Para bajar además los informes anuales KOF y DANE EMMET/IPI usados como
contraste:
```bash
python referencias/descargar_referencias.py
```
Extractos de los datos usados (con fuente) en `referencias/extractos/`.
Lista completa de referencias en formato IEEE: sección Referencias de
`docs/reporte-integral-fontibon.md`.

## 4. Estructura
```
environment.yml                  entorno conda
run_all.py                       ejecutor del pipeline con QA
scripts/00..14.py                pipeline completo (extracción→escenarios)
data/README.md                   diccionario de datos
data/                            CSV/JSON: históricos, pruebas, pronóstico, MC, rotación, escenarios
figuras/                         10 figuras B/N (report-ready, 150 dpi)
Pipeline_Fontibon.ipynb          notebook guiado del pipeline (usa %run sobre scripts/)
erp_odoo/                        9 CSVs de importación Odoo + guía 00_LEEME_ODOO.md
referencias/                     descargador + 17 PDFs fuente + extractos citables
docs/                            reportes técnicos en Markdown (ver §5)
gen_reporte.js / gen_reporte_integral.js   generadores de los reportes (fuente de docs/)
Modelo_Fontibon_Operativo.xlsx   libro con fórmulas (SKUs→pronóstico→lotes→rotación)
```

## 5. Reportes (`docs/`)
| Archivo | Contenido |
|---|---|
| `estudio-mercado-fontibon.md` | Estudio de mercado y pronóstico de demanda — versión v3, con marco teórico y trazabilidad completa de datos |
| `reporte-integral-fontibon.md` | Reporte integral de ingeniería: pronóstico + tiempos/OEE + capacidad + bases ERP |

## 6. Metodología (resumen)
Ruta del diagrama formal sobre 21 trimestres observados: correlación → rachas →
Kruskal-Wallis → Levene → ACF de la serie diferenciada (estacionalidad rezago 4,
Ljung-Box p=0,028 en refrescos) → **Holt-Winters multiplicativo m=4 amortiguado**
(Winters 1960; Gardner & McKenzie 1985) → Normal de residuos aceptada
(KS p=0,66–0,83; AD A²=0,36–0,66<0,72; χ² p=0,47–0,63) → **Monte Carlo** 10.000
réplicas → MAD/CFE/MSE/MAPE (**MAPE 1,9–2,7 %**, backtest 5 trimestres) →
**señal de rastreo** (toca ±4 en el quiebre del impuesto 2025, causa asignable) →
**validación un-paso: el modelo entrenado hasta 2025T4 predijo el 1T-2026 real
con +0,07 % (P1/P2) y +0,47 % (P3)** → pronóstico abr-2026→mar-2027.

## 7. Resultados clave abr-2026 → mar-2027 (planta)
| Prod | HW (M L) | MC P5–P95 (M L) | Unidades | Pallets |
|---|---|---|---|---|
| P1 Coca-Cola 350 ret | 65,4 | 61,8–69,4 | 186,9 M | 115.381 |
| P2 QuAtro 1.5 NR     | 81,6 | 77,2–86,5 | 54,4 M  | 64.796  |
| P3 Garrafón 25 L     | 7,0  | 6,2–7,8   | 280.912 | 9.369   |

Hallazgo multivariado (datos reales): el garrafón es casi independiente de las
gaseosas (r=0,12; PC2=27,5 % cargado por garrafón) → programable en contraciclo.

**Fase de tiempos:** ver `tiempos/fontibon-lotes-oee/` — lote = producción de
UN TURNO de 8 h (L1: 162 pallets · L2: 87 · L3: 96). OEE bottom-up por línea
(77,1/76,5/75,4 %, validado contra el 75–78 % de visita). Estación crítica de
L3 = paletizado MANUAL de 25 kg (480 gfn/h con 2 operarios; con 1, infactible).
Capacidad: L1/L2 sobre-utilizadas ya en 2025 con 2 turnos → 3.er turno.

## 8. Bases Odoo (alcance actual)
Carpeta `erp_odoo/`: 9 CSVs con IDs externos + guía paso a paso
(`00_LEEME_ODOO.md`). Orden de importación: UdM-categorías → UdM →
categorías de producto → terminados → componentes → empaques → LdM → líneas
LdM → pronóstico MPS. Fuera de alcance por ahora (fase financiera posterior,
ver `financiero/`): precios/costos, compras, contabilidad, lotes/series,
centros de trabajo.

## 9. Escenarios de demanda ("¿qué pasa si...?")
Motor de factores multiplicativos para simular subidas/bajadas de demanda
sobre el pronóstico base, sin tocar el modelo estadístico:
```bash
python scripts/13_escenarios.py                 # los 6 escenarios documentados
python scripts/13_escenarios.py "Mundial 2026"   # uno solo
python scripts/14_excel_escenarios.py            # agrega la hoja Escenarios al Excel (correr tras 07 y 13)
```
Los 6 escenarios base (editables/ampliables en `ESCENARIOS` dentro del script):
Base, Mundial 2026 (+6–10% jun-jul en gaseosas), Paro nacional/choque logístico
(−18% en el mes afectado), Recesión moderada (−5% sostenido en gaseosas),
Restricción hídrica adicional CAR (−15% sostenido en garrafón), Repunte
agresivo post-impuesto (+5% sostenido en gaseosas). Cada uno trae su
justificación y referencia en el propio código y en `data/escenarios_resumen.csv`.

## Responsable
Samuel David Sanchez Cardenas · [@samsanchezcar](https://github.com/samsanchezcar)

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
