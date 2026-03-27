<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

# tiempos — Análisis de Tiempos de Producción

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

Cálculo y análisis de tiempos del proceso para evaluación productiva. Módulo 2 — Gestión y Evaluación de la Producción Automatizada.

## Archivos

| Archivo | Carpeta | Descripción |
|---|---|---|
| `Calculo de tiempos - APM .xlsx` | `setup-tiempos/` | Cálculo de tiempos de ciclo, setup y OEE por línea |

## Tiempos de Ciclo y Capacidades por Línea

| Parámetro | Línea 2 (330 mL) | Línea 3 (PET 1.5 L) | Línea 7 (25 L) | Unidad |
|---|---|---|---|---|
| **Tc adoptado** | **0.072** | **0.420** | **2.520** | s/u |
| Rp por hora | 50.000 | 8.571 | 1.429 | u/h |
| Rp por minuto | 833,33 | 142,86 | 23,81 | u/min |
| Capacidad base (u/mes) | 28.350.000 | 8.100.000 | 405.000 | u/mes |
| Capacidad proyecto (u/mes) | 34.965.000 | 9.990.000 | 499.500 | u/mes |

> La Línea 2 tiene la mayor cadencia instantánea → referencia más exigente en sincronización. La Línea 7 tiene el mayor Tc por unidad → coherente con garrafón 25 L.

## VSM — Lead Time vs Valor Agregado

| Línea | Producto | Lead Time (LT) | Valor Agregado (VA) |
|---|---|---|---|
| Línea 2 | 330 mL retornable | 9.64 h | 6.602 s |
| Línea 3 | PET 1.5 L | 12.0 h | 5.61 s |
| Línea 7 | Garrafón 25 L | 8.4 h | 22.56 s |

**LT >> VA** en las tres líneas → oportunidad de reducción mediante automatización brownfield.

## Takt Time (referencia modelo)

```
Takt Time = Tiempo disponible / Demanda
Demanda mensual base: 13.250.000 L/mes
Crecimiento anual demanda: 1,50 %
Stock de seguridad objetivo: 5,00 %
```

## Contenido esperado

- `setup-tiempos/` — `Calculo de tiempos - APM .xlsx` ✅
- `takt-time/` — Cálculo del Takt time por producto según demanda
- `mlt/` — Manufacturing Lead Time por línea (antes/después de automatización)

## Responsable

Jorge Nicolas Garzón Acevedo · [@Nicolas-Eule](https://github.com/Nicolas-Eule)

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
