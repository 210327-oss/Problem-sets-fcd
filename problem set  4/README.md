# Análisis Censo 2017 (CPV2017) — Región Amazonas

Script en Python (pandas + DuckDB) que cruza los microdatos de **población** y **vivienda** del CPV2017 (INEI) para Amazonas y calcula tres indicadores clave.

## Requisitos

```bash
pip install pandas duckdb
```

Archivos necesarios: `cpv2017_pob01.dta` y `cpv2017_viv01.dta`. Ajusta la variable `census_path` con la ruta local donde los tengas guardados.

## Ejecución

```bash
python nombre_del_script.py
```

## Indicadores calculados

| # | Indicador | Definición |
|---|---|---|
| 1 | Saneamiento infantil | % de niños 0-5 años sin red pública de desagüe (`c2_p10` ∉ {1,2}) |
| 2 y 4 | Afiliación a seguro | % con algún seguro de salud (`c5_p8_1`...`c5_p8_5`), por grupo de edad |
| 3 | Tasa de empleo | % de personas 15-64 años ocupadas (`c5_p16=1` o `c5_p17` en 1-5) |

## Resultados obtenidos

**1. Saneamiento infantil (0-5 años)**
→ **62.2%** sin red pública de desagüe (29,166 de 46,870).

**2/4. Afiliación a seguro por grupo etario**

| Grupo | Población | Afiliados | % |
|---|---|---|---|
| 0-5 | 38,580 | 36,079 | 93.5% |
| 5-15 | 82,340 | 76,711 | 93.2% |
| 15-35 | 109,823 | 90,959 | 82.8% |
| 35-65 | 108,910 | 90,290 | 82.9% |
| 65+ | 26,862 | 22,573 | 84.0% |

→ Mayor afiliación: **0-5 años (93.5%)**. Menor afiliación: **15-35 años (82.8%)**.

**3. Tasa de empleo (15-64 años)**
→ **52.0%** empleados (113,747 de 218,733).

## Notas

- Rangos de edad: `[a, b)`, excepto el último (65+).
- `BETWEEN 15 AND 64` es inclusivo en ambos extremos.
- Salida solo por consola; el script no genera archivos.
