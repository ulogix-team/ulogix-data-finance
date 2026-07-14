<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

# Simulación · planta antes y después

La simulación en Tecnomatix Plant Simulation debe representar dos estados reproducibles:

| Línea | Estado antes | Estado después |
|---|---|---|
| L1 | 42.500 u/h, OEE 77,12 %, paletizado manual | 44.000 u/h, OEE 80,97 %, encajonadora y GANTRY compartido |
| L2 | 12.000 u/h, OEE 76,50 %, paletizado manual | 18.000 u/h, OEE 80,32 %, Variopac y GANTRY compartido |
| L3 | 480 gfn/h efectivos, OEE 75,37 %, paletizado manual | 600 gfn/h, OEE 79,14 %, robot ABB; misma llenadora |

El modelo debe conservar por corrida: versión, escenario, semilla, turnos, calendario, tasa nominal, OEE, microparos, MLT, WIP, throughput y utilización. L1 y L2 comparten físicamente el GANTRY, por lo que la lógica de alternancia es una restricción del modelo, no dos recursos independientes.

Los resultados se publican al UNS con la misma semántica de la planta: KPI por línea y `AvailableQuantity` absoluto para la orden activa. La simulación no publica órdenes; estas provienen del ERP.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
