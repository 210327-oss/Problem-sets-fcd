# Procedimientos — Análisis del Censo de Población y Vivienda 2017 (Amazonas)

## 1. % de niños 0-5 años sin red pública de desagüe

- **Población**: personas con `c5_p4_1` (edad) entre 0 y 5 años, ambos extremos incluidos (`BETWEEN 0 AND 5`).
- **Sin desagüe**: `c2_p10 NOT IN (1, 2)`, donde 1 y 2 representan "red pública dentro de la vivienda" y "red pública fuera de la vivienda" respectivamente. Cualquier otro código (pozo séptico, pozo ciego, río/acequia, no tiene, etc.) se cuenta como "sin acceso".
- Solo se consideran viviendas ocupadas (join con la tabla de vivienda filtrado por `c2_p2 = 1`).
- Cálculo: `% sin desagüe = (niños sin desagüe / total niños 0-5) × 100`.

## 2 y 4. % de afiliación a seguro de salud por grupo etario

- **Grupos etarios**, incluyendo la edad 5 dentro del primer grupo:
  - `[0-5]`, `(5-15)`, `[15-35)`, `[35-65)`, `[65+)`
- El primer grupo se evalúa con `c5_p4_1 <= 5` (cerrado en ambos extremos). Como el `CASE` de SQL evalúa las condiciones en orden y se queda con la primera verdadera, el segundo grupo arranca automáticamente en 6 años, sin necesidad de doble condición y sin riesgo de doble conteo del niño de 5 años.
- **Afiliado** = 1 si la suma de las columnas `c5_p8_1` a `c5_p8_5` (EsSalud, SIS, privado, FFAA/Policial, otro) es mayor a 0, es decir, si la persona marcó al menos un tipo de seguro.
- Se agrupa por `age_group` y se calcula `población total`, `asegurados` y `% afiliación` en cada grupo.

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

Se optó por incluir la edad 5 en ambos puntos (1 y 2) para mantener una única definición de "niños de 0 a 5 años" en todo el análisis. Esto se aparta de la notación literal `[0-5)` sugerida en el enunciado original del Punto 2 (abierta en 5); si la evaluación exige esa notación exacta, ajustar la condición del primer grupo a `c5_p4_1 < 5` y la de Punto 1 a `c5_p4_1 < 5` también.
