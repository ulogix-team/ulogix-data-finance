# Reporte de estudio de mercado

ULogix - Proyecto Automatización FEMSA

—

| Datos del reporte |  |
|---|---|
| Elabora | Andres Mauricio Morales Martinez |
| Fecha | Martes 03 de Marzo del 2026 |
| Revisa | – |
| Backlog de comentarios |  |

## Resumen ejecutivo

Este documento tiene como objetivo identificar el estado de producción, demanda y mercado de los últimos años respecto a la empresa de embotellamiento FEMSA de Coca Cola. La propuesta de automatización se enfocará únicamente en tres productos: 1) CocaCola Retornable 330 mL, 2) Coca Cola no retornable 1.5 L y 3) Garrafones de Agua de 25L aprox

**Estimación de consumo de Coca Cola en Bogotá**

Según el DANE [1], se proyecta un total de 8’168,421 de habitantes para el 2026. Supondremos que la automatización se realizará desde esta primera mitad del año y que estas cifras se mantendrán durante el año.

El DANE también estima que el 78% de la población Colombiana consume Gaseosas. Para Bogotá, supondremos que la tendencia se mantiene pero baja ligeramente al 70%. Por tanto tendríamos 5’717,894 Consumidores de Coca Cola en Bogotá

**Tabla 1: Modelo de consumo promedio en L/año por habitante en bogotá**

| Grupo Consumo | Porcentaje en consumidores totales | Consumo (L/año) |
|---|---|---|
| Bajo | 65% | 18 |
| Medio | 25% | 42 |
| Alto | 10% | 121 |

Por tanto en promedio tendríamos un consumo de 34.3 L/año por habitante en bogotá para el año 2026. Eso implica un consumo de 158,511,578.10 Litros al año en Bogotá.

A partir del modelo de consumo previamente desarrollado, se obtuvo una demanda total anual de:

159,000,000 litros/año

Por tanto, la demanda diaria es:

159,000,000 / 365 ≈ 438,000 litros/día

La planta debe ser capaz de suplir la demanda diaria estimada de: ≈ 360,000 litros/día y en términos de producción continua:

438,000 / 24 ≈ 18,250 litros/hora

Asumiendo que el cálculo se hizo exclusivamente para botellas de 330mL y suponiendo que se mantiene esta tendencia para los demás productos con su proporción actual equivale a

**55.300 botellas / hora**

Actualmente se parte del supuesto de una producción (Rp) de 50,000 botellas por hora, por lo que buscaremos un incremento de 11% de la producción

**TODO: Cantidad de Puntos de Venta de Coca Cola**

De acuerdo con reportes corporativos de Coca-Cola FEMSA, la compañía atiende aproximadamente 400,000 puntos de venta en Colombia. Considerando que Bogotá concentra entre el 15% y el 20% de la actividad comercial del país, se adopta un valor intermedio del 18% para estimar el número de puntos de venta en la ciudad.

400,000 × 0.18 ≈ 72,000 puntos de venta en Bogotá

Se asume una distribución típica del canal de ventas en Colombia, donde el canal tradicional domina el mercado:

| Tipo de punto de venta | Porcentaje | Cantidad estimada |
|---|---|---|
| Tiendas de barrio | 70% | 50,400 |
| Minimarkets | 20% | 14400 |
| Cadenas | 10% | 7,200 |

Esta segmentación es consistente con la estructura del comercio minorista en economías latinoamericanas, donde predominan los pequeños comercios.

**Referencias:**

- https://www.dane.gov.co/index.php/estadisticas-por-tema/demografia-y-poblacion/proyecciones-de-poblacion/proyecciones-de-poblacion-bogota
