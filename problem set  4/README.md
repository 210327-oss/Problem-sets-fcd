# Procedimientos — Análisis del Censo de Población y Vivienda 2017 (Amazonas)

## 1. % de niños 0-5 años sin red pública de desagüe

- **Población**: personas con `c5_p4_1` (edad) menor a 5 años (`c5_p4_1 < 5`), es decir, el intervalo `[0-5)` — mismo criterio usado en el Punto 2 para mantener consistencia entre ambos puntos.
- **Sin desagüe**: `c2_p10 NOT IN (1, 2)`, donde 1 y 2 representan "red pública dentro de la vivienda" y "red pública fuera de la vivienda" respectivamente. Cualquier otro código (pozo séptico, pozo ciego, río/acequia, no tiene, etc.) se cuenta como "sin acceso".
- Solo se consideran viviendas ocupadas (join con la tabla de vivienda filtrado por `c2_p2 = 1`).
- Cálculo: `% sin desagüe = (niños sin desagüe / total niños [0-5)) × 100`.

## 2 y 4. % de afiliación a seguro de salud por grupo etario

- **Grupos etarios**, intervalo cerrado a la izquierda y abierto a la derecha `[a, b)`:
  - `[0-5)`, `[5-15)`, `[15-35)`, `[35-65)`, `[65+)`
- **Afiliado** = 1 si la suma de las columnas `c5_p8_1` a `c5_p8_5` (EsSalud, SIS, privado, FFAA/Policial, otro) es mayor a 0, es decir, si la persona marcó al menos un tipo de seguro.
- Se agrupa por `age_group` y se calcula `población total`, `asegurados` y `% afiliación` en cada grupo. Además se identifica el grupo con mayor y menor cobertura.

## 3. Tasa de empleo censal (población 15-64 años)

- **Denominador**: personas con `c5_p4_1 BETWEEN 15 AND 64` (población en edad de trabajar, ambos extremos incluidos).
- **Numerador (empleados)**: `c5_p16 = 1` (trabajó la semana pasada) **OR** `c5_p17 IN (1,2,3,4,5)`, donde los códigos 1 a 5 corresponden a:
  1. No trabajó pero tenía trabajo al cual volver
  2. Tiene negocio propio al que volver
  3. Realizó trabajo ocasional (cachuelo) por pago en dinero o especie
  4. Realizó labores en chacra o crianza de animales
  5. Ayudó en la tienda o negocio de un familiar
- Cálculo: `tasa de empleo = (empleados / población en edad de trabajar) × 100`.

## Nota sobre el rango 0-5

Este script usa la misma definición de intervalo `[0-5)` (edad estrictamente menor a 5) tanto en el Punto 1 como en el Punto 2, para evitar que "niños de 0 a 5 años" signifique poblaciones distintas en cada punto. Si el enunciado del Punto 1 espera que el niño de 5 años cumplidos también se incluya, cambiar `c5_p4_1 < 5` por `c5_p4_1 BETWEEN 0 AND 5` en el Punto 1 (y, para mantener consistencia, ajustar también el primer grupo del Punto 2 a `c5_p4_1 <= 5`).
