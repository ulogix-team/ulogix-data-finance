<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

# Tiempos, OEE y capacidad

La nomenclatura canónica del proyecto es **L1/L2/L3**. El levantamiento histórico con líneas 2/3/7 se conserva únicamente como insumo; la hoja `Tiempos` del libro vivo es la consolidación vigente.

| Línea | Producto | MLT antes | OEE antes | OEE después | Capacidad antes | Capacidad después | Dictamen |
|---|---|---:|---:|---:|---:|---:|---|
| L1 | Coca-Cola 350 ml vidrio | 16,98 h | 77,12 % | 80,97 % | 149,97 M u/año | 244,55 M u/año | Factible con 3 turnos |
| L2 | QuAtro 1.5 L PET | 19,26 h | 76,50 % | 80,32 % | 42,01 M u/año | 99,24 M u/año | Factible con 3 turnos |
| L3 | Garrafón 25 L | 15,57 h | 75,37 % | 79,14 % | 347.309 u/año | 455.843 u/año | Factible con 1 turno |

La capacidad después combina equipo, turnos y OEE; no se obtiene multiplicando la capacidad anterior solo por 1,05. Asimismo, `t_ciclo_ideal`, `t_ciclo` y takt son magnitudes distintas.

## Archivos

| Archivo | Uso |
|---|---|
| `fontibon-lotes-oee/Tiempos_Fontibon_Corregido.xlsx` | Auditoría bottom-up, lotes, MLT y máquinas por L1/L2/L3 |
| `setup-tiempos/Calculo de tiempos - APM .xlsx` | Levantamiento histórico, conservado como evidencia |

La mejora +5 % relativa se completa al cierre del mes 4 de preoperación; la meta ≥86 % corresponde a etapas posteriores.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
