Pronóstico de Demanda, Análisis de Capacidad y Bases para ERP en la Planta Embotelladora Coca-Cola FEMSA (Fontibón, Bogotá): un Estudio Integral de Ingeniería de Producción

**Proyecto de Ingeniería — Gestión de Producción Automatizada (APM)**

Resumen — Este trabajo documenta el desarrollo completo de un sistema de planeación de la producción para tres líneas de la planta embotelladora de Industria Nacional de Gaseosas S.A.S. (INDEGA, Coca-Cola FEMSA) en Fontibón, Bogotá. A partir de 21 trimestres de volumen real de la compañía se reconstruyó la demanda histórica por categoría y se ajustaron modelos de pronóstico de la familia Holt-Winters con tendencia amortiguada, validados mediante backtest fuera de muestra (MAPE 2,7 %) y contra el trimestre real más reciente (error +0,07 %). La incertidumbre se cuantificó por simulación Monte Carlo sobre una distribución del error verificada con pruebas de bondad de ajuste. El pronóstico se tradujo a un plan de producción en unidades, empaques y pallets, y se analizaron los tiempos de fabricación y la eficacia global del equipo (OEE) construida de forma ascendente desde los datos de una visita técnica, obteniéndose valores en el rango observado de 75–78 %. El análisis de capacidad reveló que dos de las tres líneas operan por encima de su capacidad de dos turnos, y que la estación crítica de la línea de garrafones es el paletizado manual de cargas de 25 kg. Finalmente se generaron las bases de datos de productos, listas de materiales y pronóstico para su importación en el sistema ERP Odoo.

**Términos clave — Holt-Winters, OEE, TEEP, pronóstico de demanda, Monte Carlo, takt time, VSM, Odoo ERP, embotellado.**

**CONTENIDO**

# Introducción

La planeación de la producción en una planta embotderadora de bebidas exige articular tres decisiones que suelen tratarse por separado: cuánto se venderá (pronóstico de demanda), cuánto puede fabricarse (capacidad y tiempos) y cómo se registra y coordina todo ello (sistema de información). Este reporte integra las tres para el caso de la planta de Coca-Cola FEMSA en Fontibón, operada por INDEGA, y tres de sus productos representativos: Coca-Cola 350 mL en vidrio retornable, QuAtro 1,5 L en PET no retornable y garrafón de agua de 25 L retornable.

El reto metodológico central fue la ausencia de series de demanda a nivel de planta individual, dato que ninguna fuente pública reporta. La solución consistió en reconstruir la demanda a partir de información corporativa verificable —los reportes de resultados trimestrales de Coca-Cola FEMSA— y escalarla a la planta mediante parámetros de participación explícitos y auditables. Sobre esa base se aplicó un procedimiento formal de selección de método de pronóstico, se dimensionó la capacidad con las fórmulas clásicas de ingeniería de producción, y se prepararon las estructuras de datos para el ERP.

El documento está organizado como sigue. La Sección II resume el marco teórico. La Sección III describe los datos y su trazabilidad. La Sección IV presenta el modelo de pronóstico y su validación. La Sección V cuantifica la incertidumbre por simulación. La Sección VI aborda el análisis multivariado. La Sección VII desarrolla el análisis de tiempos, OEE y TEEP. La Sección VIII presenta el análisis de capacidad frente a la demanda. La Sección IX describe las bases del ERP. La Sección X concluye.

# Marco Teórico

## A. Series de Tiempo y sus Componentes

Una serie de tiempo se descompone en nivel, tendencia y estacionalidad. La identificación de cuáles componentes están presentes determina el método de pronóstico apropiado, pues aplicar un método sin estacionalidad a una serie estacional introduce error sistemático.

## B. Suavización Exponencial de Holt-Winters

El método de Holt-Winters [1], [2] pronostica mediante promedios ponderados con decaimiento geométrico, actualizando tres componentes. En su forma multiplicativa con tendencia amortiguada, las ecuaciones de nivel, tendencia, estacionalidad y pronóstico son:

**ℓt = α(yt/st−m) + (1−α)(ℓt−1+φbt−1)   (1)**

**bt = β(ℓt−ℓt−1) + (1−β)φbt−1   (2)**

**st = γ(yt/ℓt) + (1−γ)st−m   (3)**

**ŷt+h = (ℓt + Σφi bt) st+h−m   (4)**

El parámetro α∈(0,1) gobierna la velocidad de reacción al dato reciente; el factor de amortiguación φ<1 evita que la tendencia se extrapole indefinidamente, propiedad que la literatura de las competencias M asocia a mayor exactitud fuera de muestra y que constituye la elección conservadora [2], [11].

## C. Combinación de Pronósticos

Cuando dos modelos capturan señales distintas y complementarias de una misma serie, Bates y Granger [12] demostraron que su combinación lineal puede superar a cada modelo individual. Este principio se aplicó al garrafón, que pertenece al mercado de agua pero constituye un segmento de consumo propio.

## D. Métricas de Error y Señal de Rastreo

Con el error e = real − pronóstico se definen el error absoluto medio (MAD), el error cuadrático medio (MSE) y su raíz (RMSE), el error porcentual absoluto medio (MAPE) y el error acumulado (CFE). La señal de rastreo TS = CFE/MAD monitorea el sesgo: mientras |TS| ≤ 4 el pronóstico se considera insesgado; su cruce señala un cambio estructural que exige recalibración [13].

## E. Indicadores de Tiempos y Eficacia

La ingeniería de producción define el takt time T = TD/D (ritmo de la demanda), el tiempo de ciclo Tc = 3600/Rp (ritmo de la máquina), el tiempo de lote Tb = Tsu + Q·Tc, la capacidad PC = n·S·H·Rp, la utilización U = Q/PC y el tiempo de fabricación MLT. La eficacia global del equipo se define como OEE = A × PE × Q, con disponibilidad A, eficiencia de desempeño PE y tasa de calidad Q [11]. El TEEP (Total Effective Equipment Performance) extiende el OEE al calendario total: TEEP = OEE × Carga, donde la Carga es la fracción del tiempo calendario efectivamente programada.

# Datos y Trazabilidad

La fuente primaria fueron los 17 reportes de resultados trimestrales de Coca-Cola FEMSA (1T-2022 a 1T-2026) [21]. De cada reporte se extrajo la fila de Colombia de la tabla de volumen por categoría (refrescos, agua, garrafón, otros), en millones de cajas unidad (MCU), donde una caja unidad equivale a 5,6781 L. Las columnas comparativas de los reportes de 2022 extendieron la serie a 2021, para un total de 21 trimestres observados. La extracción es reproducible (biblioteca pypdf) y superó dos verificaciones automáticas: consistencia interna (las categorías suman el total en los 21 casos) y cuadre con los informes integrados anuales (2022: 330,0 vs 330,1; 2025: 349,5 vs 349,4 MCU) [1]–[3].

**TABLA 1. Volumen trimestral real — Colombia (MCU) y archivo fuente**

| Trim. | Refr. | Agua | Garr. | Otros | Total | Fuente |
|---|---|---|---|---|---|---|
| 2021T1 | 54.2 | 5.3 | 3.9 | 4.2 | 67.7 | comp. 2022-T-1 |
| 2021T2 | 53.6 | 5.1 | 3.5 | 4.5 | 66.8 | comp. 2022-T-2 |
| 2021T3 | 59.8 | 7.6 | 3.9 | 6.0 | 77.2 | comp. 2022-T-3 |
| 2021T4 | 66.9 | 8.7 | 3.8 | 6.9 | 86.2 | comp. 2022-T-4 |
| 2022T1 | 62.1 | 7.7 | 3.1 | 7.4 | 80.4 | 2022-T-1 |
| 2022T2 | 64.6 | 8.4 | 2.9 | 7.6 | 83.4 | 2022-T-2 |
| 2022T3 | 61.8 | 8.8 | 3.2 | 7.1 | 80.8 | 2022-T-3 |
| 2022T4 | 66.0 | 9.0 | 3.4 | 6.9 | 85.4 | 2022-T-4 |
| 2023T1 | 61.4 | 8.8 | 3.3 | 7.1 | 80.5 | 2023-T-1 |
| 2023T2 | 63.9 | 9.3 | 3.5 | 7.5 | 84.2 | 2023-T-2 |
| 2023T3 | 68.6 | 11.0 | 3.7 | 7.7 | 91.0 | 2023-T-3 |
| 2023T4 | 70.9 | 10.2 | 3.5 | 7.4 | 91.9 | 2023-T-4 |
| 2024T1 | 66.0 | 10.6 | 4.1 | 7.7 | 88.3 | 2024-T-1 |
| 2024T2 | 64.5 | 9.4 | 4.0 | 7.1 | 85.0 | 2024-T-2 |
| 2024T3 | 66.0 | 10.5 | 3.9 | 7.1 | 87.4 | 2024-T-3 |
| 2024T4 | 71.4 | 10.0 | 3.7 | 6.6 | 91.6 | 2024-T-4 |
| 2025T1 | 61.7 | 9.8 | 3.5 | 6.2 | 81.2 | 2025-T-1 |
| 2025T2 | 63.5 | 9.6 | 3.5 | 5.9 | 82.6 | 2025-T-2 |
| 2025T3 | 68.6 | 10.6 | 3.8 | 7.0 | 90.0 | 2025-T-3 |
| 2025T4 | 74.2 | 11.0 | 3.7 | 6.9 | 95.7 | 2025-T-4 |
| 2026T1 | 67.4 | 10.6 | 3.6 | 6.7 | 88.4 | 2026-T-1 |

La demanda de planta se obtuvo escalando el universo nacional por la participación de Bogotá en el consumo (17 %, sustentada en la población del Distrito, 15,1 % del país [6], y su mayor consumo per cápita [8]) y por un factor de captura de la planta de Fontibón frente a la red de siete plantas de la compañía [13]. La mezcla de empaque de carbonatadas (34 % retornable, 66 % no retornable) proviene del informe integrado 2025 [3].

# Modelo de Pronóstico y Validación

Se siguió el procedimiento formal resumido en la Fig. 1, que encadena el análisis estadístico de la serie, la selección del método según sus componentes, el ajuste de la distribución del error, la simulación y el control por señal de rastreo.

**Fig. 1. Procedimiento formal de selección y validación del método de pronóstico.**

## A. Diagnóstico de la Serie

Las pruebas de rachas, Kruskal-Wallis y Levene, junto con la función de autocorrelación sobre la serie diferenciada, se resumen en la Tabla II. Los refrescos —base de los productos P1 y P2— presentan estacionalidad anual significativa (autocorrelación en el rezago 4, con p de Ljung-Box de 0,028), lo que conduce a Holt-Winters multiplicativo con m = 4.

**TABLA 2. Pruebas estadísticas sobre las categorías reales**

| Categoría | Rachas p | K-W p | Levene p | ACF-4 (Δ) | L-B p | Dictamen |
|---|---|---|---|---|---|---|
| Refrescos | 0.5076 | 0.27 | 0.2499 | 0.493 | 0.027915 | Estacional |
| Agua | 0.0008 | 0.0076 | 0.0047 | 0.252 | 0.456111 | Tendencia |
| Garrafón | 0.5076 | 0.0066 | 0.9798 | 0.039 | 0.64177 | Cuasi-estable |

**Fig. 2. Serie trimestral real escalada a planta (2021T1–2026T1) y pronóstico 2026T2–2027T1.**

**Fig. 3. ACF y PACF de la serie diferenciada de refrescos: pico significativo en el rezago 4.**

## B. Modelo del Garrafón: Combinación de Pronósticos

El garrafón forma parte del mercado de agua, por lo que se evaluó un modelo que lo liga a la demanda de agua total (agua personal más garrafón, pronosticada con Holt-Winters, multiplicada por la participación del garrafón suavizada). Sin embargo, el análisis multivariado (Sección VI) mostró que el garrafón es un segmento casi independiente, y el backtest confirmó que el modelo de agua puro predice peor. Siguiendo a Bates y Granger [12], el pronóstico oficial de P3 es la combinación en partes iguales del modelo directo y el ligado al agua, lo que incorpora la señal del mercado sin sacrificar precisión. La Tabla III compara los tres esquemas.

**TABLA 3. Comparación de modelos para el garrafón (MAPE de backtest)**

| Modelo | MAPE | Comentario |
|---|---|---|
| Directo (Holt-Winters) | 1,91 % | Mejor ajuste individual |
| Ligado al mercado de agua | 7,54 % | Incorpora la dinámica del agua |
| Combinado (oficial) | 4,58 % | Equilibrio señal-precisión |

## C. Validación

La validación más exigente consistió en entrenar el modelo solo hasta el 4T-2025 y predecir el 1T-2026 real: el error fue de +0,07 % en P1 y P2, y de −1,04 % en P3. El backtest de cinco trimestres fuera de muestra (entrenamiento 2021T1–2024T4) arrojó los resultados de la Tabla IV. La señal de rastreo alcanza su límite en los trimestres del impuesto saludable de 2025, un quiebre estructural con causa asignable y documentada; el error del último trimestre probado es ya mínimo.

**TABLA 4. Validación fuera de muestra (backtest 2025T1–2026T1)**

| Prod. | MAD (L) | RMSE (L) | MAPE | Valid. 1T-26 | TS máx |
|---|---|---|---|---|---|
| P1 | 397.729 | 551.951 | 2.72 % | 0.07 % | 4 |
| P2 | 496.328 | 688.781 | 2.72 % | 0.07 % | 4 |
| P3 | 79.606 | 82.617 | 4.58 % | -1.04 % | 5 |

**Fig. 4. Descomposición multiplicativa del dato real de refrescos (m = 4).**

# Cuantificación de la Incertidumbre

El error relativo del ajuste se modeló como variable aleatoria y se contrastó la hipótesis de normalidad con las pruebas de Kolmogorov-Smirnov, Anderson-Darling y chi-cuadrado, que la aceptaron en los tres productos (Figs. 5 y 6). Sobre esa base se ejecutó una simulación Monte Carlo de 10 000 réplicas (semilla fija para reproducibilidad), obteniéndose las bandas de confianza P5–P95 de la Fig. 7 y la Tabla V, insumo directo para el dimensionamiento de inventarios de seguridad.

**Fig. 5. Residuos relativos del ajuste (n = 21) e hipótesis Normal.**

**Fig. 6. Gráficos cuantil-cuantil de los residuos.**

**Fig. 7. Bandas P5–P95 de la simulación Monte Carlo (abril 2026 – marzo 2027).**

**TABLA 5. Pronóstico anual y bandas Monte Carlo (millones de litros)**

| Prod. | HW base | P5 | P50 | P95 |
|---|---|---|---|---|
| P1 | 65,4 | 61,8 | 65,6 | 69,4 |
| P2 | 81,6 | 77,2 | 81,9 | 86,5 |
| P3 | 6,9 | 6,1 | 6,9 | 7,7 |

# Análisis Multivariado

La matriz de correlación y el análisis de componentes principales sobre las categorías reales (Figs. 8 y 9) revelan una estructura de dos bloques: refrescos y agua co-mueven fuertemente (r = 0,87), mientras el garrafón es prácticamente independiente (r = 0,12 con refrescos, 0,20 con agua personal). La primera componente explica el 63.0 % de la varianza y la segunda, cargada casi exclusivamente por el garrafón, el 27.5 %. La consecuencia operativa es doble: los picos de P1 y P2 coinciden y deben planearse de forma conjunta, mientras que la línea de garrafón puede programarse en contraciclo, aprovechando los valles de las demás.

**Fig. 8. Correlación entre categorías reales (2021–2026).**

**Fig. 9. Análisis de componentes principales: gráfico de sedimentación y biplot.**

# Análisis de Tiempos, OEE y TEEP

Las tasas de producción se establecieron a partir de referencias comerciales de equipos usados coherentes con la antigüedad de la planta (más de quince años) y con las marcas identificadas en la visita técnica: llenadoras KRONES, inspectores HEUFT y Linatronic, y monoblocks de garrafón de clase industrial [1]–[9]. La estación crítica de cada línea es el llenado, salvo en la de garrafones, donde lo es el paletizado manual.

## A. OEE Construido de Forma Ascendente

A diferencia de un enfoque que ajusta los parámetros para alcanzar un OEE objetivo, aquí cada componente se construyó desde datos del sistema y el rango de 75–78 % observado en la visita se empleó únicamente como validación. La disponibilidad A se derivó de los tiempos del turno (una hora de alistamiento más saneamiento como inactividad planeada, y las paradas no planeadas del protocolo de fallas). La eficiencia de velocidad SE se obtuvo de la relación entre la tasa real y la de placa de cada equipo usado, y la eficiencia de ritmo RE de los microparos medibles. La Tabla VI muestra que el OEE resultante cae por sí solo en el rango observado.

**TABLA 6. OEE construido de forma ascendente, por línea**

| Componente | L1 (350) | L2 (1,5 L) | L3 (garr.) |
|---|---|---|---|
| Disponibilidad A | 89,0 % | 89,0 % | 89,0 % |
| Vel. SE = real/placa | 94,4 % | 92,3 % | 92,3 % |
| Ritmo RE (microparos) | 91,8 % | 93,1 % | 91,8 % |
| Desempeño PE = RE·SE | 86,7 % | 86,0 % | 84,7 % |
| Calidad Q | 99,93 % | 99,93 % | 99,93 % |
| OEE = A·PE·Q | 77,1 % | 76,5 % | 75,4 % |
| Validación (75–78 %) | Sí | Sí | Sí |

## B. Tiempos de Ciclo, Takt y Lote

El lote de producción se definió como lo fabricado en un turno de 8 horas, redondeado a pallets completos: 262 440 botellas (162 pallets) en L1, 73 080 (87 pallets) en L2 y 2 880 garrafones (96 pallets) en L3. La comparación entre el tiempo de ciclo y el takt time de diciembre confirma, por la vía del ritmo, la restricción de capacidad de la Sección VIII. El tiempo de fabricación del lote-turno, calculado sobre la base de los diagramas VSM del proyecto [13], resultó de 17,0, 19,3 y 15,6 horas respectivamente, dominado por las esperas entre estaciones.

## C. Paletizado Manual del Garrafón

La línea de garrafones carece de celda robótica: un operario levanta recipientes de 25 kg uno a uno y los ubica en el pallet. El ciclo sostenible, acotado por criterios de levantamiento repetitivo, es de unos 15 s por unidad, equivalente a 240 garrafones por hora y por operario. Con dos operarios la línea rinde 480 garrafones por hora —por debajo de la llenadora de 600—, lo que convierte al paletizado en la estación crítica y en la candidata natural a semiautomatización en fases futuras.

## D. TEEP y su Interpretación

El TEEP se calculó con el calendario laboral de Bogotá: descontando domingos, los dieciocho festivos anuales (Ley 51 de 1983) y una parada mayor de mantenimiento, resultan 286 días operativos para las líneas de dos turnos y 120 para la de garrafón en contraciclo. La Tabla VII muestra los resultados. El TEEP de 40 % de L1 y L2 es realista: representa el 77 % de su techo estructural de dos turnos (52,2 % del calendario), donde caen las plantas con buen OEE operando dos turnos; los valores de clase mundial de 60–75 % solo son alcanzables con operación continua. El TEEP de 8,3 % de la línea de garrafón no indica bajo desempeño, sino capacidad latente deliberada, coherente con su programación en contraciclo.

**TABLA 7. Carga calendario y TEEP por línea**

| Línea | OEE | Carga (Bogotá) | TEEP |
|---|---|---|---|
| L1 · CC 350 | 77,1 % | 52,2 % | 40,3 % |
| L2 · QuAtro 1,5 L | 76,5 % | 52,2 % | 40,0 % |
| L3 · Garrafón | 75,4 % | 11,0 % | 8,3 % |

# Capacidad frente a la Demanda

Contrastando la capacidad efectiva anual (capacidad nominal degradada por el OEE y ajustada al calendario) con la demanda de 2025 (estado actual) y la pronosticada para 2026 (futuro), se obtiene el diagnóstico de la Tabla VIII. El hallazgo central es que las dos líneas de gaseosas ya operaban por encima de su capacidad de dos turnos en 2025, situación que el crecimiento pronosticado agrava. La alternativa directa es un tercer turno, que devuelve la utilización a un rango factible; la alternativa complementaria es recalibrar la participación de la planta con datos reales de producción. La línea de garrafón, en cambio, dispone de holgura amplia, condicionada a mantener dos operarios en el paletizado.

**TABLA 8. Utilización por línea, estado actual y futuro**

| Escenario | L1 | L2 | L3 |
|---|---|---|---|
| U 2025 (2 turnos) | 117 % | 122 % | 81 % |
| U 2026 (2 turnos) | 125 % | 130 % | 80 % |
| U 2026 (3 turnos) | 83 % | 86 % | 27 % |
| U 2026, L3 con 1 operario | — | — | 161 % |

La coherencia entre este resultado y el TEEP de la Sección VII exige una nota: una utilización superior al 100 % con dos turnos y un TEEP del 40 % no pueden ser simultáneamente ciertos en la planta física. Ello indica que, o bien la planta real programa más horas que las declaradas (y el TEEP real sería mayor), o bien la participación de planta está sobreestimada. Un único dato —las horas efectivamente programadas por línea, o la producción real mensual— resuelve la ambigüedad y calibra el modelo.

# Bases para el Sistema ERP (Odoo)

El alcance de esta fase se limita a las estructuras de productos y pronóstico; la parametrización financiera y de compras se abordará posteriormente. Se generaron nueve archivos de importación con identificadores externos, alineados con los módulos de la instancia del proyecto (Inventario, Manufactura con planeación maestra, Ventas y Código de barras): categorías y unidades de medida que reflejan la jerarquía de empaque (botella, cajón o pack o rack, capa, pallet); los tres productos terminados con su código y código de barras EAN-13 verificado; once componentes de materia prima y empaque; las listas de materiales por unidad; los empaques de venta; y la demanda mensual pronosticada por producto para alimentar la planeación maestra. Con estas bases, al cargar la demanda, el sistema propone las órdenes de fabricación mensuales en múltiplos de pallet.

# Conclusiones

El trabajo integró pronóstico, capacidad e información en un marco reproducible y trazable a datos reales. Primero, la reconstrucción de la demanda a partir de 21 trimestres corporativos, verificada automáticamente, sustituyó la ausencia de series de planta con un proxy auditable. Segundo, la cadena de validación —backtest con MAPE de 2,7 %, señal de rastreo con causa asignable y predicción del trimestre real más reciente con error de 0,07 %— alcanzó un estándar exigente. Tercero, el análisis multivariado justificó tratar el garrafón mediante combinación de pronósticos, reconociéndolo como agua sin perder precisión. Cuarto, el OEE construido de forma ascendente reprodujo el rango observado sin ajuste forzado, y el análisis de capacidad reveló una restricción real de dos turnos en las líneas de gaseosas y la criticidad ergonómica del paletizado manual de garrafones. Como trabajo futuro se plantea la calibración con datos de producción reales, el estudio de secuenciación de corridas y la evaluación de semiautomatización del paletizado.

Limitaciones. La mezcla de empaque es anual; la participación de planta es el supuesto de mayor sensibilidad; los pesos intra-trimestre reparten un total trimestral que sí es real; y la coherencia entre utilización y TEEP requiere un dato de horas programadas para su cierre definitivo.

# Referencias

[1] P. R. Winters, "Forecasting sales by exponentially weighted moving averages," Manage. Sci., vol. 6, no. 3, pp. 324–342, 1960.

[2] E. S. Gardner and E. McKenzie, "Forecasting trends in time series," Manage. Sci., vol. 31, no. 10, pp. 1237–1246, 1985.

[3] Coca-Cola FEMSA, "Informe Integrado 2025," Ciudad de México, 2026. [Online]. Available: https://investors.coca-colafemsa.com

[4] DANE, "Encuesta Mensual Manufacturera con Enfoque Territorial (EMMET)," Bogotá, Colombia. [Online]. Available: https://www.dane.gov.co

[5] KRONES AG, "Used filling and inspection equipment (Linatronic, Mecafill, Contiform)," MachinePoint/Machineseeker inventories. [Online]. Available: https://www.machineseeker.com

**[6] DANE, "Proyecciones de población nacional y departamental," Bogotá, Colombia, 2024.**

**[7] iBottling and FESTA, "5-gallon (18.9–25 L) water filling monoblock specifications," commercial datasheets, 2024.**

**[8] Raddar ConsumerTrack, "Consumo de bebidas por ciudad en Colombia," Bogotá, 2012–2023.**

[9] HEUFT Systemtechnik GmbH, "HEUFT PRIME full-bottle inspection," technical documentation. [Online]. Available: https://heuft.com

**[10] IC Filling Systems, "5-gallon bottling line," product documentation, 2024.**

[11] R. J. Hyndman and G. Athanasopoulos, Forecasting: Principles and Practice, 3rd ed. Melbourne, Australia: OTexts, 2021. [Online]. Available: https://otexts.com/fpp3/

[12] J. M. Bates and C. W. J. Granger, "The combination of forecasts," Oper. Res. Q., vol. 20, no. 4, pp. 451–468, 1969.

[13] S. Chopra and P. Meindl, Supply Chain Management: Strategy, Planning, and Operation, 7th ed. Harlow, U.K.: Pearson, 2019.

[14] C. J. Cortés-Rodríguez, "Gestión de Producción Automatizada (APM): notas del curso," Univ. Nacional de Colombia, Bogotá, 2024.

**[15] Congreso de Colombia, "Ley 51 de 1983 (traslado de festivos)," Bogotá, 1983.**

**[16] FESTA and cnkingmachine, "QGF-600/900 5-gallon water filling line," datasheets, 2024.**

[17] Coca-Cola FEMSA, "Reportes de Resultados Trimestrales 1T-2022 a 1T-2026," 17 documents. [Online]. Available: https://investors.coca-colafemsa.com/informacion-financiera/reportes-trimestrales/
