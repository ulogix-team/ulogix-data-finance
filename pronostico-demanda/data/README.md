# Diccionario de datos (data/)

| Archivo | Generado por | Contenido |
|---|---|---|
| kof_trimestral_colombia.json | 00 | 21 trimestres reales de KOF Colombia por categoría (MCU), extraídos de los PDFs de referencias/descargas/ |
| historico_trimestral_planta.csv | 01 | Serie trimestral a escala planta: MCU del universo, litros y unidades por producto |
| historico_planta.csv | 01 | Serie mensual (desagregación intra-trimestre con pesos W) |
| parametros.json | 01 | Constantes: SHARE, ENVASE, L_CU, mezcla RET/NR, pesos W |
| pruebas_estadisticas.json | 02 | Rachas, Kruskal-Wallis, Levene, ACF-4(Δ), Ljung-Box por categoría real |
| hw_parametros.json | 03 | α, β, γ, φ, AIC por producto (Holt-Winters amortiguado, m=4) |
| pronostico_trimestral.csv | 03 | Pronóstico 2026T2–2027T1 en litros |
| pronostico_2026.csv | 03 | Pronóstico mensual abr-2026 → mar-2027 (litros y unidades) |
| residuos_P?.csv | 03 | Residuos relativos in-sample (n=21) para el ajuste de distribución |
| validacion_2026T1.json | 03 | Predicción un-paso vs dato real del 1T-2026 |
| evaluacion_backtest.csv / _resumen.json | 04 | Backtest 5 trimestres: real, pronóstico, error, CFE, MAD, TS |
| plan_unidades_lotes.csv | 05 | Mensual: unidades, agrupaciones, capas, pallets, lote estándar |
| rotacion_inventarios.csv | 05 | Rotación y cobertura por escenario de lote (diario/semanal/mensual) |
| distribuciones.json | 08 | μ, σ y pruebas KS/AD/χ² de la Normal por producto |
| montecarlo.csv | 09 | Bandas P5/P50/P95 mensuales (N=10.000, semilla 42) |
| escenarios_demanda.csv | 13 | Demanda mensual por escenario (litros/unidades), factor aplicado |
| escenarios_resumen.csv | 13 | Totales anuales por escenario, Δ% vs Base, bandas Monte Carlo |
| pca.json | 10 | Varianza explicada y matriz de correlación (categorías reales) |
