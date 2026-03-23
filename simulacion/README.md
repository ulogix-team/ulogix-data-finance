<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-dark.svg" width="100%"/>

# simulacion — VSM y Análisis de Producción

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

Análisis del proceso productivo mediante VSM (Value Stream Mapping) y simulación en Tecnomatix / Plant Simulation. Módulo 2 — Gestión y Evaluación de la Producción Automatizada.

## VSM — Resultados por Línea

| Línea | Producto | LT (Lead Time) | VA (Value Added) | Interpretación |
|---|---|---|---|---|
| **Línea 2** | Bebida carbonatada — Vidrio 330 mL | 9.64 h | 6.602 s | Inventarios intermedios moderados, alto peso en preparación e inspección del retornable |
| **Línea 3** | Bebida PET 1 L–2 L | 12.0 h | 5.61 s | Mayor LT por inventarios acumulados en flujo PET y número de etapas |
| **Línea 7** | Agua purificada — Garrafón 20 L | 8.4 h | 22.56 s | Menor LT que PET pero mayor VA por unidad — formato 20 L |

**Clave:** LT >> VA en las tres líneas → oportunidad de reducción mediante automatización.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Tiempos de Ciclo y Capacidades (del Excel del equipo)

| Parámetro | Línea 2 (330 mL) | Línea 3 (1 L) | Línea 7 (20 L) | Unidad |
|---|---|---|---|---|
| Horas por turno (base Excel) | 1.0 | 7.0 | 7.0 | h/turno |
| Unidades por turno | 50 000 | 60 000 | 10 000 | u/turno |
| **Rp por hora** | **50 000** | **8 571** | **1 429** | u/h |
| Rp por minuto | 833.33 | 142.86 | 23.81 | u/min |
| Rp por segundo | 13.89 | 2.381 | 0.397 | u/s |
| **Tc adoptado** | **0.072** | **0.420** | **2.520** | s/u |

> La Línea 2 tiene la mayor capacidad instantánea → es la referencia más exigente en sincronización. La Línea 7 tiene el mayor Tc por unidad → coherente con garrafón 20 L.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Indicadores OEE — Modelo Preliminar

### Disponibilidad

| Parámetro | Valor |
|---|---|
| Tiempo total de planta | 8.00 h |
| Tiempo inactividad planeada | 1.00 h |
| Tiempo de ejecución planeada | 7.00 h |
| Tiempo inactividad no planeada | 0.75 h |
| **Tiempo de ejecución real** | **6.25 h** |
| **Disponibilidad** | **89.29 %** |

### Calidad

| Parámetro | Valor |
|---|---|
| Porcentaje de rechazo | 0.07 % |
| **Calidad** | **99.93 %** |

### Eficiencia

| Parámetro | Valor |
|---|---|
| Volumen real producido | 41 000 u |
| Tc (en horas) | 0.000168 h |
| Tiempo de ejecución real | 6.25 h |
| Ratio de eficiencia (RE) | 1.10208 |
| Score de eficiencia (SE) | 0.8 |
| **Eficiencia** | **88.17 %** |

### OEE Preliminar

```
OEE = Disponibilidad × Eficiencia × Calidad
OEE = 89.29% × 88.17% × 99.93% = 78.67% ≈ 79%
```

> Valor de referencia: OEE de clase mundial ≥ 85%. El 79% representa línea de base antes de automatización — objetivo de mejora con control automatizado.

**Expresiones de referencia:**
- `OEE = A · PE · Q`
- `Tc = 3600 / Rp` (s/u a partir de capacidad nominal)

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/dividers/divider-section-dark.svg" width="100%"/>

## Contenido de esta Carpeta

- `vsm/` — VSM estado actual (Líneas 2, 3, 7) y VSM estado futuro (post-automatización)
- `modelos/` — Archivos de simulación Tecnomatix / Plant Simulation
- `resultados/` — Comparativo antes/después de automatizar (OEE, MLT, Takt time)

## Responsables

| Rol | Nombre | GitHub |
|---|---|:---:|
| VSM / Proceso / OEE | Jorge Nicolas Garzón Acevedo | [@Nicolas-Eule](https://github.com/Nicolas-Eule) |
| Simulación / Finanzas | Samuel David Sanchez Cardenas | [@samsanchezcar](https://github.com/samsanchezcar) |
| **Supervisor de par** | **Juan Manuel Beltrán Botello** | [@JuanBeltran2024](https://github.com/JuanBeltran2024) |

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
