import pandas as pd
import duckdb

census_path = r"D:\CEU INEI\FUNDAMENTOS DE CIENCIA DE DATO\PROBLEM SET 4\Amazonas"

pop_cols = [
    "id_viv_imp_f", "id_hog_imp_f", "id_pob_imp_f",
    "c5_p4_1",
    "c5_p8_1", "c5_p8_2", "c5_p8_3", "c5_p8_4", "c5_p8_5",
    "c5_p16", "c5_p17",
]
population = pd.read_stata(census_path + r"\cpv2017_pob01.dta",
                          columns=pop_cols, convert_categoricals=False)

house_cols = ["id_viv_imp_f", "c2_p2", "c2_p10"]
housing = pd.read_stata(census_path + r"\cpv2017_viv01.dta", columns=house_cols, convert_categoricals=False)

con = duckdb.connect()
con.register("population", population)
con.register("housing", housing)

con.execute("""
    CREATE OR REPLACE TABLE people AS
    SELECT p.*, h.c2_p10
    FROM population AS p
    INNER JOIN housing AS h
        ON p.id_viv_imp_f = h.id_viv_imp_f
    WHERE h.c2_p2 = 1
""")


def print_header(titulo: str, ancho: int = 70):
    print("\n" + "=" * ancho)
    print(titulo.center(ancho))
    print("=" * ancho)


def print_tabla(df: pd.DataFrame, pct_cols=None):
    """Imprime un dataframe con enteros con separador de miles y % con simbolo."""
    df = df.copy()
    pct_cols = pct_cols or []
    for col in df.columns:
        if col in pct_cols:
            df[col] = df[col].map(lambda x: f"{x:.1f}%")
        elif pd.api.types.is_integer_dtype(df[col]):
            df[col] = df[col].map(lambda x: f"{x:,}")
    print(df.to_string(index=False))


# ---------------------------------------------------------------------------
# Punto 1: % de ninos 0-5 sin red publica de desague
# ---------------------------------------------------------------------------
q1 = con.execute("""
    SELECT
        SUM(CASE WHEN c2_p10 NOT IN (1, 2) THEN 1 ELSE 0 END)::INT AS kids_no_sewer,
        COUNT(*)                                                   AS kids_total,
        ROUND(100.0 * SUM(CASE WHEN c2_p10 NOT IN (1, 2) THEN 1 ELSE 0 END)
              / COUNT(*), 1)                                       AS pct_no_sewer
    FROM people
    WHERE c5_p4_1 < 5
""").df()

print_header("PUNTO 1: Ninos 0-5 anos sin red publica de desague")
print_tabla(q1, pct_cols=["pct_no_sewer"])
print(f"\n-> {q1['pct_no_sewer'][0]:.1f}% de los ninos de 0 a 5 anos "
      f"({q1['kids_no_sewer'][0]:,} de {q1['kids_total'][0]:,}) "
      "no tiene acceso a red publica de desague.")


# ---------------------------------------------------------------------------
# Punto 2 y 4: % de afiliacion a seguro por grupo etario
# Intervalos: cerrado por la izquierda, abierto por la derecha [a, b)
# ---------------------------------------------------------------------------
q2 = con.execute("""
    WITH t AS (
        SELECT
            CASE
                WHEN c5_p4_1 < 5  THEN '1: [0-5)'
                WHEN c5_p4_1 < 15 THEN '2: [5-15)'
                WHEN c5_p4_1 < 35 THEN '3: [15-35)'
                WHEN c5_p4_1 < 65 THEN '4: [35-65)'
                ELSE                   '5: [65+)'
            END AS age_group,
            CASE WHEN (COALESCE(c5_p8_1,0) + COALESCE(c5_p8_2,0)
                     + COALESCE(c5_p8_3,0) + COALESCE(c5_p8_4,0)
                     + COALESCE(c5_p8_5,0)) > 0 THEN 1 ELSE 0 END AS has_insurance
        FROM people
    )
    SELECT
        age_group,
        COUNT(*)                                        AS pop,
        SUM(has_insurance)::INT                          AS insured,
        ROUND(100.0 * SUM(has_insurance) / COUNT(*), 1) AS pct_insured
    FROM t
    GROUP BY age_group
    ORDER BY age_group
""").df()

print_header("PUNTOS 2 y 4: Afiliacion a seguro de salud por grupo etario")
print_tabla(q2, pct_cols=["pct_insured"])
fila_min = q2.loc[q2["pct_insured"].idxmin()]
fila_max = q2.loc[q2["pct_insured"].idxmax()]
print(f"\n-> Mayor afiliacion: grupo {fila_max['age_group']} ({fila_max['pct_insured']:.1f}%).")
print(f"-> Menor afiliacion: grupo {fila_min['age_group']} ({fila_min['pct_insured']:.1f}%).")


# ---------------------------------------------------------------------------
# Punto 3: tasa de empleo (15-64)
# ---------------------------------------------------------------------------
q3 = con.execute("""
    SELECT
        SUM(CASE WHEN c5_p16 = 1 OR c5_p17 IN (1,2,3,4,5)
                 THEN 1 ELSE 0 END)::INT              AS employed,
        COUNT(*)                                      AS working_age_pop,
        ROUND(100.0 * SUM(CASE WHEN c5_p16 = 1 OR c5_p17 IN (1,2,3,4,5)
                         THEN 1 ELSE 0 END)
              / COUNT(*), 1)                          AS employment_rate
    FROM people
    WHERE c5_p4_1 BETWEEN 15 AND 64
""").df()

print_header("PUNTO 3: Tasa de empleo, poblacion 15-64 anos")
print_tabla(q3, pct_cols=["employment_rate"])
print(f"\n-> Tasa de empleo: {q3['employment_rate'][0]:.1f}% "
      f"({q3['employed'][0]:,} de {q3['working_age_pop'][0]:,} personas en edad de trabajar).")

con.close()