# Trazabilidad y control de versión

## Artefactos

- El Google Sheet es el artefacto operativo editable.
- `financiero/modelo/Modelo_FEMSA_Ulogix_2026.xlsx` es la publicación fuera de línea.
- `financiero/modelo/modelo.manifest.json` prueba fecha, tamaño y SHA-256.
- El ERP registra sus cambios de integración en `ulogix-fontibon-suite`.
- Los documentos y modelos anteriores permanecen identificados como legado.

## Convención de actualización

1. Actualizar y auditar Sheets.
2. Ejecutar la verificación del ERP.
3. Exportar el XLSX.
4. Verificar fórmulas, totales, hojas clave y render visual.
5. Actualizar los indicadores documentados si cambiaron.
6. Hacer commit humano, sin trailers de coautoría de herramientas de IA.

## Asistencia de IA

La asistencia de IA puede apoyar análisis, documentación y control de calidad. No reemplaza la aprobación de ingeniería ni la autoría del equipo y no debe agregarse como colaboradora o coautora del repositorio.
