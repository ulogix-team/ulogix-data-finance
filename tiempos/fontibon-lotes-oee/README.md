# fontibon-lotes-oee

`Tiempos_Fontibon_Corregido.xlsx` — OEE bottom-up por línea (L1/L2/L3) y
dimensionamiento de lotes, construido desde datos de una visita técnica y
ligado al pronóstico de demanda de `pronostico-demanda/` (las cantidades
mensuales por SKU se convierten aquí en pallets y lotes de un turno).

## Resumen

- **Lote** = producción de UN TURNO de 8 h. L1: 162 pallets · L2: 87 · L3: 96.
- **OEE bottom-up por línea**: 77,1 % (L1) / 76,5 % (L2) / 75,4 % (L3),
  validado contra el 75–78 % observado en visita.
- **Estación crítica de L3**: paletizado MANUAL de garrafones de 25 kg
  (480 gfn/h con 2 operarios; con 1 operario resulta infactible).
- **Capacidad**: L1 y L2 ya operan sobre-utilizadas en 2025 con 2 turnos →
  sustenta la necesidad de un 3.er turno.

Desarrollo completo, fórmulas y supuestos en
`../../pronostico-demanda/docs/reporte-integral-fontibon.md` (sección VII,
"Tiempos, OEE y TEEP").

> Nomenclatura de línea (L1/L2/L3) propia de este levantamiento; distinta de
> la numeración de línea 2/3/7 usada en `../setup-tiempos/` — ver nota en
> `../README.md`.
