"""
biblioteca.py
Lógica de negocio del Sistema de Gestión de Bibliotecas (PS3, Segunda Parte).

Contiene:
    - conectar / crear_tablas          -> Punto 1
    - agregar_libro                    -> Punto 2
    - buscar_catalogo / imprimir_catalogo -> Punto 3
    - crear_usuario                    -> Punto 4
"""
import os
import re
import sqlite3
import unicodedata

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "biblioteca.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


def _normalizar(texto):
    """Quita acentos/diacríticos y pasa a minúsculas.

    Se usa para que las búsquedas del Punto 3 'ignoren mayúsculas y acentos'
    (p. ej. 'García' == 'garcia' == 'GARCIA').
    """
    if texto is None:
        return ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower()


def conectar(db_path=DB_PATH):
    """Abre la conexión a la base de datos y registra la función SQL
    NORMALIZAR(texto), usada por buscar_catalogo()."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.create_function("NORMALIZAR", 1, _normalizar)
    conn.row_factory = sqlite3.Row
    return conn


def crear_tablas(conn, schema_path=SCHEMA_PATH):
    """Punto 1 (4 pts): ejecuta el script schema.sql que crea las tablas
    Autor, Libro, Usuario (con sus restricciones) y la vista CatalogoView."""
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()


# ---------------------------------------------------------------------
# Punto 2 (4 pts): Añadir libros / inventario nuevo (búsqueda por ISBN)
# ---------------------------------------------------------------------
def agregar_libro(conn, isbn, titulo, anio_publicacion, cantidad_nueva,
                   autor_nombre, autor_apellido, autor_fecha_nacimiento=None):
    """
    Reglas de negocio pedidas en el enunciado:
      - Se busca el libro por ISBN.
          * Si YA existe -> solo se suman 'cantidad_nueva' copias a
            cantidad_disponible. No se vuelve a tocar ni Autor ni Libro.
          * Si NO existe:
              - Se busca al autor por (Nombre, Apellido, Fecha_nacimiento).
                  · Si existe -> se reutiliza su AutorID.
                  · Si no existe -> se inserta un Autor nuevo.
              - Se inserta el Libro nuevo con
                cantidad_disponible = cantidad_nueva.

    Devuelve un diccionario describiendo qué se hizo (útil para la interfaz).
    """
    if cantidad_nueva <= 0:
        raise ValueError("La cantidad de copias a añadir debe ser mayor a 0.")

    cur = conn.cursor()
    cur.execute("SELECT IDlibro FROM Libro WHERE ISBN = ?", (isbn,))
    libro = cur.fetchone()

    if libro is not None:
        # El título (ISBN) ya existe: solo sumamos copias.
        cur.execute(
            "UPDATE Libro SET cantidad_disponible = cantidad_disponible + ? "
            "WHERE ISBN = ?",
            (cantidad_nueva, isbn),
        )
        conn.commit()
        return {
            "accion": "copias_sumadas",
            "isbn": isbn,
            "copias_agregadas": cantidad_nueva,
        }

    # El libro no existe todavía: resolvemos primero al autor.
    cur.execute(
        "SELECT ID FROM Autor WHERE Nombre = ? AND Apellido = ? "
        "AND Fecha_nacimiento IS ?",
        (autor_nombre, autor_apellido, autor_fecha_nacimiento),
    )
    autor = cur.fetchone()

    if autor is not None:
        autor_id = autor["ID"]
        autor_creado = False
    else:
        cur.execute(
            "INSERT INTO Autor (Nombre, Apellido, Fecha_nacimiento) "
            "VALUES (?, ?, ?)",
            (autor_nombre, autor_apellido, autor_fecha_nacimiento),
        )
        autor_id = cur.lastrowid
        autor_creado = True

    cur.execute(
        "INSERT INTO Libro (ISBN, Titulo, Anio_publicacion, "
        "cantidad_disponible, AutorID) VALUES (?, ?, ?, ?, ?)",
        (isbn, titulo, anio_publicacion, cantidad_nueva, autor_id),
    )
    conn.commit()
    return {
        "accion": "libro_creado",
        "isbn": isbn,
        "autor_creado": autor_creado,
        "autor_id": autor_id,
        "copias_agregadas": cantidad_nueva,
    }


# ---------------------------------------------------------------------
# Punto 3 (3 pts): Consultar el catálogo por título y/o autor
# ---------------------------------------------------------------------
def buscar_catalogo(conn, titulo=None, autor=None):
    """
    Busca en la vista CatalogoView (join Libro + Autor) por título y/o
    autor, ignorando mayúsculas y acentos (vía la función NORMALIZAR
    registrada en conectar()). Si no se pasa ningún filtro, devuelve
    todo el catálogo.
    """
    condiciones = []
    parametros = []

    if titulo:
        condiciones.append("NORMALIZAR(Titulo) LIKE '%' || NORMALIZAR(?) || '%'")
        parametros.append(titulo)

    if autor:
        condiciones.append(
            "(NORMALIZAR(AutorNombre) LIKE '%' || NORMALIZAR(?) || '%' "
            "OR NORMALIZAR(AutorApellido) LIKE '%' || NORMALIZAR(?) || '%')"
        )
        parametros.extend([autor, autor])

    where = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""
    query = f"""
        SELECT AutorNombre, AutorApellido, Titulo, cantidad_disponible
        FROM CatalogoView
        {where}
        ORDER BY Titulo
    """
    cur = conn.cursor()
    cur.execute(query, parametros)
    return cur.fetchall()


def imprimir_catalogo(filas):
    """Imprime autor, título y cantidad_disponible, como pide el enunciado."""
    if not filas:
        print("No se encontraron libros con esos criterios.")
        return
    print(f"{'Autor':30} {'Título':40} {'Disponibles':>11}")
    print("-" * 83)
    for fila in filas:
        autor = f"{fila['AutorNombre']} {fila['AutorApellido']}"
        print(f"{autor:30} {fila['Titulo']:40} {fila['cantidad_disponible']:>11}")


# ---------------------------------------------------------------------
# Punto 4 (3 pts): Crear usuarios (DNI único de 8 dígitos numéricos)
# ---------------------------------------------------------------------
DNI_REGEX = re.compile(r"^\d{8}$")


def crear_usuario(conn, dni, nombre, apellido, email=None, telefono=None):
    """Valida el formato del DNI en Python (mensaje de error más claro
    para la interfaz) y confía además en el CHECK de la tabla y en el
    UNIQUE(DNI) como última línea de defensa a nivel de base de datos."""
    if not DNI_REGEX.match(dni):
        raise ValueError("El DNI debe tener exactamente 8 caracteres numéricos.")

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Usuario (DNI, Nombre, Apellido, email, telefono) "
            "VALUES (?, ?, ?, ?, ?)",
            (dni, nombre, apellido, email, telefono),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise ValueError(f"Ya existe un usuario registrado con el DNI {dni}.") from e
