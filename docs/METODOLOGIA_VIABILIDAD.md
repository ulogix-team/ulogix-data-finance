# Metodología de viabilidad económica

## Comparación antes/después

| Línea | Antes | Después | Decisión de capacidad |
|---|---|---|---|
| L1 | KRONES Mecafill usada 42.500 u/h y paletizado manual | KRONES usada 44.000 u/h, encajonadora y GANTRY | Pasa de infactible a factible con 3 turnos |
| L2 | KRONES 12.000 u/h y paletizado manual | KRONES 18.000 u/h, Variopac y GANTRY | Pasa de infactible a factible con 3 turnos |
| L3 | Monoblock suficiente, limitado por paletizado manual a 480 gfn/h | Llenadora existente 600 gfn/h y robot ABB | Se mantiene factible y aumenta holgura |

El análisis no atribuye toda la mejora al OEE. Se separan: cambio de capacidad nominal de equipos, número de turnos, OEE efectivo y reducción de cuellos de botella.

## OEE

`OEE = Disponibilidad × Rendimiento × Calidad`.

La fase financiada aplica +5 % relativo exacto al OEE base de cada línea. El aumento se distribuye 50/30/20 entre disponibilidad, rendimiento y calidad y se completa al cierre del cuarto mes preoperativo.

## Flujo incremental

1. La demanda activa determina volumen vendible.
2. La capacidad determina qué parte puede atenderse antes y después.
3. El margen por SKU se calcula desde precios y costos unitarios editables.
4. Se agregan OPEX de licencias, nómina y otros costos incrementales.
5. CAPEX se desembolsa por fases y se deprecia por vida útil.
6. Impuestos y capital de trabajo forman el flujo de caja libre.
7. VPN, TIR, ROI y payback se calculan sobre el flujo incremental de 60 meses.

## Controles mínimos

- CAPEX total = subtotal + contingencia.
- CAPEX software y OPEX de licencias concilian con `Licencias`.
- APU concilia con las tres filas de servicios en CAPEX.
- Nómina concilia con el resumen por rol de `RRHH`.
- La capacidad después cubre la demanda con la configuración de turnos declarada.
- No existen `#REF!`, `#VALUE!`, `#DIV/0!`, `#N/A`, `#NAME?` ni `#NUM!`.
- El snapshot publicado coincide con el hash del manifiesto.

## Interpretación

El escenario base vigente supera la TMAR del 18 %: VPN COP 11.032 millones, TIR 78,2 %, ROI 226,7 % y payback simple/descontado de 22/25 meses. Son resultados del snapshot fechado y deben recalcularse cuando cambien demanda, CAPEX, licencias o unit economics.
