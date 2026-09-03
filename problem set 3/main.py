"""
main.py
Interfaz de línea de comandos del Sistema de Gestión de Bibliotecas.
Problem Set 3 · Segunda Parte.

Uso:
    python main.py
"""
from biblioteca import (
    conectar,
    crear_tablas,
    agregar_libro,
    buscar_catalogo,
    imprimir_catalogo,
    crear_usuario,
)


def menu_agregar_libro(conn):
    print("\n--- Añadir libro / inventario ---")
    isbn = input("ISBN: ").strip()
    titulo = input("Título: ").strip()
    anio = input("Año de publicación: ").strip()
    cantidad = input("Cantidad de copias a añadir: ").strip()
    autor_nombre = input("Nombre del autor: ").strip()
    autor_apellido = input("Apellido del autor: ").strip()
    autor_fecha = input("Fecha de nacimiento del autor (YYYY-MM-DD, opcional): ").strip() or None

    try:
        resultado = agregar_libro(
            conn, isbn, titulo, int(anio), int(cantidad),
            autor_nombre, autor_apellido, autor_fecha,
        )
        if resultado["accion"] == "copias_sumadas":
            print(f"El libro ya existía (ISBN {isbn}). "
                  f"Se sumaron {resultado['copias_agregadas']} copia(s).")
        else:
            estado_autor = "se creó un autor nuevo" if resultado["autor_creado"] else "el autor ya existía"
            print(f"Libro nuevo registrado (ISBN {isbn}); {estado_autor}.")
    except ValueError as e:
        print(f"Error: {e}")


def menu_buscar_catalogo(conn):
    print("\n--- Consultar catálogo ---")
    titulo = input("Buscar por título (Enter para omitir): ").strip() or None
    autor = input("Buscar por autor (Enter para omitir): ").strip() or None
    filas = buscar_catalogo(conn, titulo, autor)
    print()
    imprimir_catalogo(filas)


def menu_crear_usuario(conn):
    print("\n--- Crear usuario ---")
    dni = input("DNI (8 dígitos): ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    email = input("Email (opcional): ").strip() or None
    telefono = input("Teléfono (opcional): ").strip() or None
    try:
        id_usuario = crear_usuario(conn, dni, nombre, apellido, email, telefono)
        print(f"Usuario creado con IDusuario = {id_usuario}.")
    except ValueError as e:
        print(f"Error: {e}")


def main():
    conn = conectar()
    crear_tablas(conn)

    opciones = {
        "1": ("Añadir libro / inventario", menu_agregar_libro),
        "2": ("Consultar catálogo", menu_buscar_catalogo),
        "3": ("Crear usuario", menu_crear_usuario),
    }

    while True:
        print("\n===== Sistema de Gestión de Bibliotecas =====")
        for clave, (etiqueta, _) in opciones.items():
            print(f"{clave}. {etiqueta}")
        print("0. Salir")
        eleccion = input("Elige una opción: ").strip()

        if eleccion == "0":
            print("Hasta luego.")
            break
        elif eleccion in opciones:
            opciones[eleccion][1](conn)
        else:
            print("Opción inválida.")

    conn.close()


if __name__ == "__main__":
    main()
