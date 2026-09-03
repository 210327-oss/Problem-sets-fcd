import os
import sqlite3
from biblioteca import conectar, crear_tablas, agregar_libro, buscar_catalogo, crear_usuario

TEST_DB = "test_biblioteca.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)

conn = conectar(TEST_DB)
crear_tablas(conn)
print("[OK] Tablas y vista creadas.")

# --- Punto 2: agregar libro nuevo (autor nuevo) ---
r1 = agregar_libro(conn, "978-0-13-468599-1", "Cien años de soledad", 1967, 3,
                    "Gabriel", "García Márquez", "1927-03-06")
assert r1["accion"] == "libro_creado" and r1["autor_creado"] is True
print("[OK] Libro nuevo + autor nuevo:", r1)

# --- mismo autor, libro nuevo (autor NO se debe duplicar) ---
r2 = agregar_libro(conn, "978-0-06-088328-7", "El amor en los tiempos del cólera", 1985, 2,
                    "Gabriel", "García Márquez", "1927-03-06")
assert r2["accion"] == "libro_creado" and r2["autor_creado"] is False
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM Autor")
assert cur.fetchone()[0] == 1, "No debería haberse duplicado el autor"
print("[OK] Segundo libro reutiliza autor existente:", r2)

# --- mismo ISBN otra vez -> solo debe sumar copias ---
r3 = agregar_libro(conn, "978-0-13-468599-1", "Cien años de soledad", 1967, 5,
                    "Gabriel", "García Márquez", "1927-03-06")
assert r3["accion"] == "copias_sumadas"
cur.execute("SELECT cantidad_disponible FROM Libro WHERE ISBN = ?", ("978-0-13-468599-1",))
cantidad = cur.fetchone()[0]
assert cantidad == 8, f"Se esperaban 8 copias, hay {cantidad}"
print(f"[OK] ISBN repetido solo suma copias (total={cantidad}).")

# --- Punto 3: búsqueda ignorando mayúsculas y acentos ---
resultados = buscar_catalogo(conn, autor="garcia marquez")  # sin tilde, minúsculas
assert len(resultados) == 2, f"Se esperaban 2 libros, hubo {len(resultados)}"
print("[OK] Búsqueda por autor ignora tildes/mayúsculas:", [r["Titulo"] for r in resultados])

resultados_titulo = buscar_catalogo(conn, titulo="AMOR")
assert len(resultados_titulo) == 1
print("[OK] Búsqueda por título ignora mayúsculas:", resultados_titulo[0]["Titulo"])

# --- Punto 4: crear usuario válido ---
uid = crear_usuario(conn, "12345678", "Ana", "Torres", "ana@example.com", "999888777")
print(f"[OK] Usuario creado con IDusuario={uid}")

# --- DNI duplicado debe fallar ---
try:
    crear_usuario(conn, "12345678", "Otro", "Nombre")
    raise AssertionError("Debió fallar por DNI duplicado")
except ValueError as e:
    print(f"[OK] DNI duplicado rechazado correctamente: {e}")

# --- DNI con formato inválido debe fallar ---
for dni_malo in ["1234567", "abcdefgh", "123456789"]:
    try:
        crear_usuario(conn, dni_malo, "X", "Y")
        raise AssertionError(f"Debió fallar con DNI inválido: {dni_malo}")
    except ValueError:
        pass
print("[OK] DNIs con formato inválido (7 dígitos, letras, 9 dígitos) rechazados.")

# --- CHECK de cantidad_disponible >= 0 a nivel de base de datos ---
try:
    conn.execute("UPDATE Libro SET cantidad_disponible = -1 WHERE ISBN = ?",
                 ("978-0-13-468599-1",))
    conn.commit()
    raise AssertionError("Debió fallar el CHECK de cantidad_disponible >= 0")
except sqlite3.IntegrityError:
    print("[OK] CHECK cantidad_disponible >= 0 funciona a nivel de BD.")

conn.close()
os.remove(TEST_DB)
print("\nTODAS LAS PRUEBAS PASARON CORRECTAMENTE.")
