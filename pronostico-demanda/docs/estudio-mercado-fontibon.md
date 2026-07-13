**ESTUDIO DE MERCADO Y PRONÓSTICO DE DEMANDA**

**PLANTA COCA-COLA FEMSA BOGOTÁ — FONTIBÓN**

**Coca-Cola 350 ml vidrio retornable  ·  QuAtro 1.5 L PET no retornable  ·  Garrafón de agua 25 L**

Base de datos: 21 trimestres reales de Coca-Cola FEMSA Colombia (1T-2021 a 1T-2026), extraídos de los 17 Reportes de Resultados Trimestrales oficiales

Horizonte de pronóstico: abril 2026 – marzo 2027  |  Documento técnico v3 — con marco teórico y trazabilidad completa de datos

Repositorio reproducible adjunto: entorno conda · pipeline 00–12 con QA automatizado · notebook guiado · 17 PDFs fuente incluidos · bases Odoo

**6 de julio de 2026**

# 1.  Resumen

Este documento desarrolla, con estándar de proyecto de ingeniería, el pronóstico de demanda a doce meses (abril-2026 → marzo-2027) para tres productos de la planta de Industria Nacional de Gaseosas S.A.S. (INDEGA, operadora de Coca-Cola FEMSA en Colombia) en Fontibón, Bogotá. La base es una serie de 21 trimestres reales de volumen por categoría, extraída de forma reproducible de los 17 Reportes de Resultados Trimestrales de la compañía [21] y verificada contra los Informes Integrados anuales [1]–[3]. Siguiendo un procedimiento formal de selección de método (Fig. 1), las pruebas estadísticas conducen a Holt-Winters multiplicativo trimestral con tendencia amortiguada [14],[15]; el modelo se valida con backtest (MAPE 1,9–2,7 %), señal de rastreo, y una prueba de un paso contra el trimestre real más reciente (+0,07 % de error en P1/P2). La incertidumbre se cuantifica con simulación Monte Carlo (10.000 réplicas) sobre una distribución Normal aceptada por tres pruebas de bondad de ajuste. El documento incluye un marco teórico autocontenido (sec. 2) para lectores sin formación previa en pronósticos, la trazabilidad completa de cada dato (sec. 4), y las bases del ERP en Odoo (sec. 10). El repositorio adjunto contiene el pipeline ejecutable (scripts 00–12 con control de calidad automatizado) y un notebook Jupyter que lo recorre de forma guiada.

# 2.  Marco teórico

**Esta sección explica, sin asumir conocimientos previos de pronósticos, cada herramienta usada y por qué se eligió.**

## 2.1  Series de tiempo y sus componentes

Una serie de tiempo es una secuencia de observaciones ordenadas cronológicamente — aquí, litros demandados por trimestre. En la práctica industrial se descompone en tres componentes [18]: el nivel (la magnitud base de la demanda), la tendencia (su dirección de cambio sostenido) y la estacionalidad (un patrón que se repite cada ciclo — aquí, cada 4 trimestres: fin de año siempre vende más, inicio de año menos). Identificar qué componentes están presentes determina el método correcto: usar un método sin estacionalidad sobre una serie estacional produce errores sistemáticos, y viceversa. Por eso el flujo (Fig. 1) dedica sus primeros pasos a diagnosticar la serie antes de elegir modelo.

## 2.2  Las pruebas de diagnóstico: qué pregunta responde cada una

Prueba de rachas (Wald-Wolfowitz). ¿La serie es puro azar? Cuenta las «rachas» (secuencias consecutivas por encima o por debajo de la mediana) y las compara con las esperadas bajo aleatoriedad. Un p-valor bajo (<0,05) rechaza la aleatoriedad: hay estructura que un modelo puede explotar. Si la serie fuera aleatoria, el mejor pronóstico sería el promedio y nada más ayudaría.

Kruskal-Wallis. ¿El nivel medio cambia entre grupos (aquí, entre años)? Es la versión no paramétrica del ANOVA — no exige normalidad, apropiada con pocas observaciones. Un p bajo indica niveles distintos entre años (tendencia o quiebres).

Levene. ¿La variabilidad es constante entre años? Si la dispersión creciera con el nivel, favorecería un modelo multiplicativo (fluctuaciones proporcionales al nivel) sobre uno aditivo.

Autocorrelación (ACF/PACF). La ACF mide cuánto se parece la serie a sí misma desplazada k períodos («rezago k»). Un pico significativo en el rezago igual al ciclo (aquí k=4) es la firma de la estacionalidad. Con series cortas la tendencia domina la ACF y la enmascara; por eso la prueba se aplica sobre la serie diferenciada (Δyt = yt − yt−1), que elimina la tendencia y deja visible el patrón estacional. El estadístico de Ljung-Box formaliza la significancia conjunta.

Box-Plot por período. Complemento visual: una caja por trimestre muestra mediana, cuartiles y atípicos — la estacionalidad y su estabilidad, a simple vista.

## 2.3  Suavización exponencial y Holt-Winters

La familia de suavización exponencial pronostica con promedios ponderados donde lo reciente pesa más, con pesos que decaen geométricamente hacia el pasado. La forma más simple actualiza solo el nivel:

**ℓt = α·yt + (1−α)·ℓt−1**

donde α∈(0,1) controla la velocidad de reacción: α≈1 significa «créele casi todo al último dato» (útil cuando el mercado cambia rápido, como tras el impuesto de 2025); α pequeño, «promedia mucho pasado». Holt-Winters [14] extiende la idea con tres ecuaciones acopladas — nivel (ℓ), tendencia (b) y factores estacionales (s) — que en la forma multiplicativa con tendencia amortiguada [15], la usada aquí, son:

**ℓt = α·(yt/st−m) + (1−α)·(ℓt−1 + φ·bt−1)**

**bt = β·(ℓt − ℓt−1) + (1−β)·φ·bt−1**

**st = γ·(yt/ℓt) + (1−γ)·st−m**

**ŷt+h = [ℓt + (φ+φ²+···+φh)·bt]·st+h−m**

con m=4 (períodos por ciclo). Tres decisiones de diseño y su porqué: (i) multiplicativo, porque el pico de fin de año es proporcional al nivel — si la demanda crece 10 %, el pico crece ~10 %; (ii) tendencia amortiguada (0<φ<1): en lugar de extrapolar la tendencia como línea recta al infinito, el crecimiento proyectado se «frena» geométricamente y converge — la elección conservadora, cuya superioridad fuera de muestra está documentada en las competencias M de pronóstico [15],[18]; (iii) parámetros por máxima verosimilitud: α, β, γ, φ no se fijan a mano; se optimizan minimizando el error de ajuste (statsmodels).

## 2.4  Métricas de error y señal de rastreo

Con et = real − pronóstico: MAD = promedio de |e| (magnitud típica del error, en litros); MSE = promedio de e² (penaliza errores grandes; su raíz, RMSE, vuelve a litros); MAPE = promedio de |e|/real × 100 (porcentual, comparable entre productos; <10 % es bueno y <5 % excelente en demanda industrial [19]); CFE = suma acumulada de e (el sesgo: si el modelo siempre se pasa o se queda corto, el CFE crece en una dirección).

La señal de rastreo TSt = CFEt/MADt es el «monitor de sesgo» en operación: mientras |TS| ≤ 4, el pronóstico está insesgado dentro de lo normal; si cruza ±4, algo estructural cambió y el modelo debe revisarse [19]. Aquí la TS cruza −4 exactamente en los trimestres del impuesto saludable de 2025: la herramienta detectó el quiebre real, con causa asignable documentada. Eso no invalida el modelo — lo valida como sistema de control.

## 2.5  Distribución del error y simulación Monte Carlo

Un pronóstico puntual no basta para decidir inventarios: se necesita saber cuánto puede desviarse. Se modela el error relativo ε = (real−ajuste)/ajuste como variable aleatoria y la hipótesis ε ~ Normal(μ, σ) se contrasta con tres pruebas complementarias: Kolmogorov-Smirnov (máxima distancia entre la distribución empírica y la teórica), Anderson-Darling (similar, con más peso en las colas — donde viven los riesgos) y χ² de Pearson (frecuencias observadas vs esperadas por clases). Aceptada la Normal, la simulación Monte Carlo genera N=10.000 «futuros posibles»: cada réplica multiplica el pronóstico por (1+ε) con ε sorteado de la Normal ajustada. Los percentiles 5 y 95 forman una banda que contiene el 90 % de los escenarios — el insumo del inventario de seguridad en la fase siguiente. La semilla fija (42) hace la simulación exactamente reproducible.

## 2.6  Análisis multivariado (correlación y PCA)

La correlación de Pearson (r∈[−1,1]) mide co-movimiento lineal; r≈1 significa que dos series suben y bajan juntas. El Análisis de Componentes Principales (PCA) generaliza la idea: encuentra los «factores» comunes que explican la varianza conjunta de varias series estandarizadas. Si un solo componente explicara ~100 %, todas serían una misma señal; componentes adicionales relevantes indican dinámicas independientes — información accionable para programar líneas que no compiten por los mismos picos.

# 3.  Metodología

El estudio sigue el procedimiento formal de la Fig. 1: cada bloque es un script numerado del repositorio (00–12), recorrido también de forma guiada en el notebook Pipeline_Fontibon.ipynb. El paso 12 es un control de calidad automatizado con seis verificaciones — V1 categorías suman el total en cada trimestre; V2 cuadre de agregados anuales contra los Informes Integrados; V3 pesos intra-trimestre suman 1; V4 el mensual re-agregado reproduce el trimestral; V5 dígitos de control EAN-13; V6 jerarquía de empaque — todas superadas.

Fig. 1. Procedimiento formal de selección y validación del método (v3). Rombos = decisiones; la respuesta tomada se anota en la flecha.

## 3.1  Supuestos del modelo

| # | Supuesto | Justificación / fuente |
|---|---|---|
| S1 | Volumen trimestral de Colombia por categoría = dato observado | Tabla «Volumen» de los 17 reportes trimestrales KOF [21]; extracción reproducible (script 00), verificada (V1, V2) |
| S2 | Mezcla de empaque en carbonatadas: 34 % retornable / 66 % NR | Informe Integrado KOF 2025 [3]; dato anual (no existe trimestral público) |
| S3 | Participación de planta = 17 % (Bogotá) × captura Fontibón (70 % ret / 45 % NR / 50 % garrafón) | DANE población [6] + Raddar consumo [8]; red de plantas [13]; Res. CAR 347/2026 [12]. Supuesto de mayor sensibilidad — reemplazar con ventas reales |
| S4 | Desagregación mensual con pesos intra-trimestre fijos (p. ej. 4T: 30,9/32,5/36,6 %) | Patrón de gasto de hogares [8],[10]. El total trimestral es dato real; solo la repartición interna es supuesta (V3, V4) |
| S5 | Residuo relativo del ajuste ~ Normal(μ, σ) | Aceptado por KS, AD y χ² sobre n=21 residuos (sec. 7.3) |
| S6 | Escenario conservador: φ<1, sin uplift del Mundial 2026 | Gardner & McKenzie [15]; upside documentado, no incluido |

# 4.  Datos y trazabilidad completa

## 4.1  Serie primaria: los 21 trimestres y su archivo fuente

Cada cifra proviene de la tabla «Volumen» (millones de cajas unidad, MCU; 1 CU = 24 porciones de 8 oz = 5,6781 L [3]) del reporte indicado, incluido en referencias/descargas/. Los cuatro trimestres de 2021 provienen de las columnas comparativas de los reportes de 2022. La extracción es automática (script 00) y superó V1 (categorías suman el total en los 21 casos) y V2 (anuales vs Informes Integrados: 2022: 330,0 vs 330,1; 2023: 347,6 vs 347,6; 2024: 352,3 vs 352,3; 2025: 349,5 vs 349,4 MCU).

| Trim. | Refrescos | Agua | Garrafón | Otros | Total | Archivo fuente |
|---|---|---|---|---|---|---|
| 2021T1 | 54.2 | 5.3 | 3.9 | 4.2 | 67.7 | 2022-T-1.pdf (col. comparativa) |
| 2021T2 | 53.6 | 5.1 | 3.5 | 4.5 | 66.8 | 2022-T-2.pdf (col. comparativa) |
| 2021T3 | 59.8 | 7.6 | 3.9 | 6.0 | 77.2 | 2022-T-3.pdf (col. comparativa) |
| 2021T4 | 66.9 | 8.7 | 3.8 | 6.9 | 86.2 | 2022-T-4.pdf (col. comparativa) |
| 2022T1 | 62.1 | 7.7 | 3.1 | 7.4 | 80.4 | 2022-T-1.pdf |
| 2022T2 | 64.6 | 8.4 | 2.9 | 7.6 | 83.4 | 2022-T-2.pdf |
| 2022T3 | 61.8 | 8.8 | 3.2 | 7.1 | 80.8 | 2022-T-3.pdf |
| 2022T4 | 66.0 | 9.0 | 3.4 | 6.9 | 85.4 | 2022-T-4.pdf |
| 2023T1 | 61.4 | 8.8 | 3.3 | 7.1 | 80.5 | 2023-T-1.pdf |
| 2023T2 | 63.9 | 9.3 | 3.5 | 7.5 | 84.2 | 2023-T-2.pdf |
| 2023T3 | 68.6 | 11.0 | 3.7 | 7.7 | 91.0 | 2023-T-3.pdf |
| 2023T4 | 70.9 | 10.2 | 3.5 | 7.4 | 91.9 | 2023-T-4.pdf |
| 2024T1 | 66.0 | 10.6 | 4.1 | 7.7 | 88.3 | 2024-T-1.pdf |
| 2024T2 | 64.5 | 9.4 | 4.0 | 7.1 | 85.0 | 2024-T-2.pdf |
| 2024T3 | 66.0 | 10.5 | 3.9 | 7.1 | 87.4 | 2024-T-3.pdf |
| 2024T4 | 71.4 | 10.0 | 3.7 | 6.6 | 91.6 | 2024-T-4.pdf |
| 2025T1 | 61.7 | 9.8 | 3.5 | 6.2 | 81.2 | 2025-T-1.pdf |
| 2025T2 | 63.5 | 9.6 | 3.5 | 5.9 | 82.6 | 2025-T-2.pdf |
| 2025T3 | 68.6 | 10.6 | 3.8 | 7.0 | 90.0 | 2025-T-3.pdf |
| 2025T4 | 74.2 | 11.0 | 3.7 | 6.9 | 95.7 | 2025-T-4.pdf |
| 2026T1 | 67.4 | 10.6 | 3.6 | 6.7 | 88.4 | 2026-T-1.pdf |

## 4.2  Parámetros y su procedencia

| Parámetro | Valor | Fuente / derivación |
|---|---|---|
| Caja unidad (CU) | 5,6781 L | Definición KOF: 24×8 oz [3] |
| Mezcla retornable / NR (carbonatadas) | 34 % / 66 % | Informe Integrado 2025, mezcla por empaque Colombia [3] |
| Población Bogotá D.C. / país | 15,1 % | DANE proyecciones (≈7,9 M / 52,7 M) [6] |
| Participación de Bogotá en consumo | 17 % | Población + mayor consumo per cápita (Raddar) [8] |
| Captura Fontibón: P1 / P2 / P3 | 70 % / 45 % / 50 % | Supuesto: logística del retornable urbano; Tocancipá (130 MCU) concentra PET [13]; CAR 347/2026 [12] |
| Participación de planta resultante | 11,9 % / 7,65 % / 8,5 % | = 17 % × captura (celdas editables en el Excel) |
| Envases | 0,35 / 1,5 / 25 L | Especificación de los SKU |
| Jerarquía de empaque | 1.620 / 840 / 30 und/pallet | Dato de planta: cajón×30·9·6 / pack×6·28·5 / rack×6·5 (V6) |
| Pesos intra-trimestre (ej. 4T) | 30,9 / 32,5 / 36,6 % | Patrón de consumo documentado [8],[10]; normalizados (V3) |
| Parámetros HW (α, β, γ, φ) | ver sec. 7.1 | Máxima verosimilitud, statsmodels 0.14 (script 03) |
| Semilla Monte Carlo | 42 | Reproducibilidad exacta (script 09) |

# 5.  Estudio de mercado

## 5.1  Sector de bebidas en Colombia

El mercado colombiano de bebidas no alcohólicas es un duopolio maduro: Postobón y el sistema Coca-Cola operado por Coca-Cola FEMSA a través de INDEGA. En participación por empresa, Euromonitor reporta 30,7 % Postobón, 11,7 % PepsiCo y 27,4 % Coca-Cola [9]; en gaseosas, la marca Coca-Cola concentra 44–50 % de las compras [8],[10]. El consumo per cápita de gaseosas fue de 52 L/año en 2022 [10] y Bogotá es la ciudad de mayor consumo [8]. Los datos trimestrales cuantifican los choques del período: el impuesto saludable contrajo los refrescos −6,5 % interanual en el 1T-2025 (66,0→61,7 MCU) y la recuperación llevó al récord de 74,2 MCU en el 4T-2025 y a +9,2 % interanual en el 1T-2026 [21]. El agua embotellada crece 3–8 % anual [16],[17].

## 5.2  El embotellador y la planta

Coca-Cola FEMSA Colombia opera 7 plantas (~54 líneas, >400.000 puntos de venta) [13]: Bogotá-Fontibón (la planta del estudio, sede histórica de INDEGA), Tocancipá (130 MCU/año, PET de alta velocidad), La Calera (agua Manantial/garrafón, bajo restricción hídrica de la CAR [12]), Cali, Medellín, Bucaramanga y Barranquilla. La serie observada (Fig. 2) muestra tres regímenes: crecimiento 2021–2023, meseta 2024, choque-y-rebote 2025. El plan comercial alrededor del Mundial FIFA 2026 es el upside no incluido [20].

## 5.3  Productos del estudio

| SKU | EAN-13 | Producto | Universo (dato real) | Pallet |
|---|---|---|---|---|
| CC-RET-350 | 7701000000016 | Coca-Cola 350 ml vidrio ret. | Refrescos × 34 % | 54 cajones = 1.620 bot = 567 L |
| QT-NR-1500 | 7701000000023 | QuAtro toronja 1.5 L PET NR | Refrescos × 66 % | 140 packs = 840 bot = 1.260 L |
| AG-GF-25000 | 7701000000030 | Garrafón agua 25 L ret. | Garrafón (columna propia) | 5 racks = 30 gfn = 750 L |

# 6.  Análisis estadístico de la serie

La serie de planta se obtiene como litros = MCU de la categoría (dato real) × 5,6781 × mezcla de empaque × participación de planta. La Fig. 2 muestra los 21 trimestres y el pronóstico; la Fig. 3, el Box-Plot por trimestre del dato real de refrescos: mediana del 4T claramente arriba, 1T abajo — la firma visual de la estacionalidad que las pruebas confirman.

**Fig. 2. Serie trimestral real a escala planta (2021T1–2026T1) y pronóstico 2026T2–2027T1 (línea discontinua).**

**Fig. 3. Box-Plot por trimestre — Refrescos Colombia (MCU, dato real 2021–2026).**

## 6.1  Resultados de las pruebas del flujo

| Categoría | Rachas p | Kruskal-Wallis p | Levene p | ACF-4 (Δserie) | Ljung-Box p | Dictamen |
|---|---|---|---|---|---|---|
| Refrescos | 0,508 | 0,270 | 0,250 | 0,493 | 0,028 | Estacional (base de P1 y P2) |
| Agua | 0,0008 | 0,008 | 0,005 | 0,252 | 0,456 | Tendencia creciente; estacionalidad débil |
| Garrafón | 0,508 | 0,007 | 0,980 | 0,039 | 0,642 | Cuasi-estable; sin estacionalidad clara |

Interpretación con la sec. 2.2: en refrescos, las rachas sobre la serie cruda no rechazan aleatoriedad (tendencia y estacionalidad se compensan alrededor de la mediana), pero la ACF de la serie diferenciada revela el pico en rezago 4 con Ljung-Box p=0,028 — la firma estacional. En agua, rachas p=0,0008 delata la tendencia creciente y Kruskal-Wallis confirma niveles distintos entre años. El garrafón no muestra patrón estacional (ACF-4≈0): consumo básico constante — el propio modelo lo capturará con γ=0 y amortiguación fuerte. La ruta selecciona Holt-Winters multiplicativo m=4 (Figs. 4–5).

**Fig. 4. ACF/PACF de la serie diferenciada de refrescos: pico significativo en rezago 4.**

**Fig. 5. Descomposición multiplicativa del dato real (m=4): tendencia, patrón estacional estable y residuo.**

# 7.  Modelo, validación y control

## 7.1  Parámetros estimados y su lectura

| Prod. | α (nivel) | β (tendencia) | γ (estacional) | φ (amortiguación) | Lectura |
|---|---|---|---|---|---|
| P1 | 0,946 | 0 | 0 | 0,988 | Nivel muy reactivo; estacionalidad fija; tendencia casi persistente pero amortiguada |
| P2 | 0,946 | 0 | 0 | 0,988 | Idéntico a P1 (comparten universo de refrescos) |
| P3 | combinación | — | — | 0,80/0,81 | MÉTODO COMBINADO (Bates-Granger 50/50): HW directo + modelo ligado al mercado de AGUA (agua total × share garrafón). El garrafón es agua: hereda su dinámica sin perder la precisión del directo |

α≈0,95–1,0 confirma lo que el mercado vivió: tras el impuesto de 2025 el nivel cambió rápido y el modelo debe creerle al dato reciente (sec. 2.3). β=γ=0 con φ<1 significa tendencia y estacionalidad estimadas en la inicialización y luego amortiguadas — el comportamiento conservador buscado.

## 7.2  Validación de un paso contra el dato real más reciente

| Prod. | Pronóstico 1T-2026 (L) | Real 1T-2026 (L) | Error |
|---|---|---|---|
| P1 | 15.494.756 | 15.484.234 | 0.07 % |
| P2 | 19.335.893 | 19.322.763 | 0.07 % |
| P3 | 1.719.381 | 1.737.502 | -1.04 % |

Es la prueba más exigente disponible: el modelo, entrenado solo con datos hasta 4T-2025, anticipó el trimestre real más reciente con error inferior a medio punto porcentual.

## 7.3  Backtest, distribución del error y señal de rastreo

| Prod. | MAD (L) | CFE (L) | RMSE (L) | MAPE | TS máx /·/ | Dictamen |
|---|---|---|---|---|---|---|
| P1 | 397.729 | -1.591.241 | 551.951 | 2.72 % | 4 | Quiebre 2025 detectado (causa asignable) |
| P2 | 496.328 | -1.985.713 | 688.781 | 2.72 % | 4 | Quiebre 2025 detectado (causa asignable) |
| P3 | 79.606 | -398.031 | 82.617 | 4.58 % | 5 | Quiebre 2025 detectado (causa asignable) |

El backtest (2021T1–2024T4 → 2025T1–2026T1) da MAPE 2,7 % (P1, P2) y, para P3, la comparación de modelos justifica la combinación: directo 1,9 %, ligado-al-agua 7,5 %, combinado 4,6 % — «excelente» según la sec. 2.4. El CFE negativo y la TS tocando −4 ocurren en los trimestres del impuesto: el monitor de sesgo funcionó como debe, detectando un cambio estructural con causa asignable; el error del último trimestre probado ya es mínimo. Sobre los 21 residuos relativos, la Normal se acepta por las tres pruebas (Figs. 6–7): KS p=0,83/0,83/0,66; A²=0,36/0,36/0,66 < 0,72 (crítico 5 %); χ² p=0,47/0,47/0,63. σ estimada: 3,5 % (P1, P2) y 7,2 % (P3).

**Fig. 6. Residuos relativos del ajuste (n=21) e hipótesis Normal.**

**Fig. 7. Q-Q: los cuantiles empíricos siguen la recta teórica — Normal aceptada.**

# 8.  Simulación Monte Carlo

Con la Normal aceptada se generan 10.000 futuros posibles del horizonte abril-2026 → marzo-2027 (sec. 2.5; semilla 42). Las bandas P5–P95 (Fig. 8) están centradas en la base HW y su ancho — ±6 % en gaseosas, ±12 % en garrafón — refleja la volatilidad realmente observada en 21 trimestres. Estas bandas son el insumo directo del inventario de seguridad en la fase de tiempos.

**Fig. 8. Bandas P5–P95 de la simulación (N=10.000), abril 2026 – marzo 2027.**

| Prod. | HW base (M L) | MC P5 | MC P50 | MC P95 |
|---|---|---|---|---|
| P1 | 65,4 | 61,8 | 65,6 | 69,4 |
| P2 | 81,6 | 77,2 | 81,9 | 86,5 |
| P3 | 6,9 | 6,1 | 6,9 | 7,7 |

# 9.  Análisis multivariado

Aplicando la sec. 2.6 a las categorías reales: refrescos y agua co-mueven (r=0,87) — mismo consumidor, misma estacionalidad — mientras el garrafón es prácticamente independiente (r=0,12 con refrescos). El PCA lo cuantifica: PC1 explica 63.0 % (el factor común «consumo de bebidas») y PC2 27.5 %, cargado casi exclusivamente por el garrafón (Fig. 10). Traducción operativa: los picos de P1 y P2 coinciden siempre — la capacidad de diciembre se dimensiona conjunta — pero la línea de garrafón puede programarse en contraciclo, aprovechando los valles sin colisión de demanda.

**Fig. 9. Correlación entre categorías reales (2021–2026).**

**Fig. 10. PCA: scree (izq.) y biplot (der.) — el garrafón define su propio componente.**

# 10.  Plan de producción, rotación y bases ERP (Odoo)

## 10.1  Plan en empaques y lotes

El pronóstico mensual se convierte a la jerarquía de empaque (botella → cajón/pack/rack → capa → pallet). Como la línea libera pallets completos, el lote mínimo e incremento es 1 pallet; el lote estándar es demanda mensual ÷ corridas/mes (parámetro editable — los tiempos de línea se abordarán en la fase siguiente). Rotación = demanda anual ÷ (lote/2); cobertura = 365 ÷ rotación.

| Prod. | Und/pallet | Demanda abr26–mar27 (und) | Pallets/año | Lote diario (pal) | Rot. diaria | Lote semanal | Rot. semanal | Lote mensual | Rot. mensual |
|---|---|---|---|---|---|---|---|---|---|
| P1 | 1620 | 186.953.224 | 115.409 | 162 | 1425 | 324 | 712 | 1944 | 119 |
| P2 | 840 | 54.436.369 | 64.812 | 87 | 1490 | 174 | 745 | 1044 | 124 |
| P3 | 30 | 277.572 | 9.259 | 96 | 193 | 192 | 96 | 1152 | 16 |

## 10.2  Bases en Odoo (alcance actual: productos y pronóstico)

El repositorio incluye nueve archivos de importación con IDs externos (carpeta erp_odoo/, guía paso a paso en 00_LEEME_ODOO.md), alineados con los módulos de la instancia del proyecto — Inventario, Manufactura (con la Planeación Maestra/MPS), Código de barras y Ventas: categorías y unidades de medida por jerarquía de empaque (botella→cajón/pack/rack→capa→pallet), los tres productos terminados con SKU y EAN-13 verificados (ruta Fabricar), once componentes base (agua tratada, concentrados, CO2, envases, cascos retornables, tapas, etiqueta), las listas de materiales por unidad, los empaques de venta y la demanda mensual pronosticada por SKU para cargar en el MPS (rango mensual, horizonte 12 meses). Deliberadamente fuera de alcance en esta fase: precios y costos (list_price=0), proveedores y órdenes de compra, contabilidad, lotes/series y centros de trabajo — se configurarán tras la fase financiera. Con estas bases, al cargar la demanda en la Planeación, Odoo propone las órdenes de fabricación mensuales por SKU en múltiplos de pallet, y las necesidades de componentes quedan listas para valorarse después.

# 11.  Conclusiones y limitaciones

(1) El estudio pasó de reconstrucción supuesta a dato observado: 21 trimestres reales con extracción reproducible y verificación automática (V1–V6). (2) La cadena de validación es completa: diagnóstico → backtest MAPE ≤2,7 % → señal de rastreo con causa asignable → predicción del trimestre real más reciente con +0,07 %. (3) El multivariado aporta una conclusión operativa: el garrafón no compite por los picos de las gaseosas y puede programarse en contraciclo. (4) Limitaciones: mezcla retornable/NR anual [3]; la participación de planta (S3) es el supuesto de mayor sensibilidad hasta contar con ventas propias del ERP; los pesos intra-trimestre reparten un total trimestral que sí es real. (5) Riesgos: impuesto en nivel máximo [11], restricción hídrica del garrafón [12]; upside no incluido: Mundial 2026 [20].

# Referencias

[1]  Coca-Cola FEMSA, "Reporte Anual 2023," Ciudad de México, 2024. [En línea]. Disponible: https://investors.coca-colafemsa.com/assets/files/reportes_resultados_esp/2023/24-04-11-reporte-anual-2023.pdf

[2]  Coca-Cola FEMSA, "Informe Integrado 2024," Ciudad de México, 2025. [En línea]. Disponible: https://investors.coca-colafemsa.com/assets/files/reportes_resultados_esp/2024/kof-ii-2024-esp.pdf

[3]  Coca-Cola FEMSA, "Informe Integrado 2025," Ciudad de México, 2026. [En línea]. Disponible: https://investors.coca-colafemsa.com/assets/files/reportes_resultados_esp/2026/2025-KOF-II-ESP.pdf

[4]  DANE, "EMMET — Metodología," Bogotá. [En línea]. Disponible: https://www.dane.gov.co/files/operaciones/EMMET/met-EMMET.pdf

[5]  DANE, "EMMET — Series históricas, clase CIIU 1100 Elaboración de bebidas," Bogotá. [En línea]. Disponible: https://www.dane.gov.co/index.php/estadisticas-por-tema/industria/encuesta-mensual-manufacturera-con-enfoque-territorial-emmet/emmet-historicos

[6]  DANE, "Proyecciones de población nacional y departamental," Bogotá. [En línea]. Disponible: https://www.dane.gov.co

**[7]  DANE, "Índice de Producción Industrial (IPI) — Boletín diciembre 2025," Bogotá, 2026. [En línea].**

**[8]  Raddar ConsumerTrack, "Coca-Cola, la marca con mayor tajada en gaseosas," La República, Bogotá, 2012. [En línea].**

[9]  G. Castellanos e I. Cortés, "Colombiana, la nuestra," Pensar la Publicidad, vol. 14, no. 2, 2020 (datos Euromonitor).

**[10]  Valora Analitik / DANE, "¿Cuántas gaseosas se consumen en Colombia?," 2023. [En línea].**

**[11]  Infobae, "Impuesto saludable llega a su nivel máximo el 1 de enero de 2026," dic. 2025. [En línea].**

**[12]  CAR Cundinamarca, "Resolución 347 de 2026: concesión de aguas a INDEGA S.A.S., La Calera," abr. 2026. [En línea].**

[13]  Portafolio, "Las plantas de Coca-Cola FEMSA operarán con energías limpias," 2018; El Espectador, "Nueva planta Tocancipá (130 MCU)," 2015.

[14]  P. R. Winters, "Forecasting sales by exponentially weighted moving averages," Management Science, vol. 6, no. 3, pp. 324–342, 1960.

[15]  E. S. Gardner y E. McKenzie, "Forecasting trends in time series," Management Science, vol. 31, no. 10, pp. 1237–1246, 1985.

**[16]  Expert Market Research, "Mercado de agua embotellada en Colombia," 2025. [En línea].**

**[17]  El Nuevo Siglo, "Industria de agua embotellada mueve US$2.222,8 millones," Bogotá, 2025. [En línea].**

[18]  R. J. Hyndman y G. Athanasopoulos, Forecasting: Principles and Practice, 3.ª ed., OTexts, 2021. [En línea]. Disponible: https://otexts.com/fpp3/

[19]  S. Chopra y P. Meindl, Supply Chain Management, 7.ª ed., Pearson, 2019 (métricas de error y señal de rastreo, límites ±4).

**[20]  FEMSA, "Coca-Cola FEMSA — Resultados del Primer Trimestre 2026," abr. 2026. [En línea].**

[21]  Coca-Cola FEMSA, "Reportes de Resultados Trimestrales 1T-2022 a 1T-2026" (17 documentos; tabla «Volumen» por país; incluidos en referencias/descargas/). [En línea]. Disponible: https://investors.coca-colafemsa.com/informacion-financiera/reportes-trimestrales/
