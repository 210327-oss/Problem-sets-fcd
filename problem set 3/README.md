# Sistema de Gestión de Bibliotecas — Problem Set 3, Segunda Parte

Implementación parcial en SQLite + Python (`sqlite3` de la librería estándar,
sin dependencias externas).

## Archivos

| Archivo               | Contenido                                                        |
|------------------------|-------------------------------------------------------------------|
| `schema.sql`           | Punto 1 — `CREATE TABLE` de Autor, Libro, Usuario + vista `CatalogoView`, con comentarios sobre las restricciones y reglas de integridad referencial asumidas. |
| `biblioteca.py`        | Lógica de negocio: `agregar_libro` (Punto 2), `buscar_catalogo` (Punto 3), `crear_usuario` (Punto 4). |
| `main.py`              | Interfaz de consola (menú interactivo) que usa `biblioteca.py`. |
| `test_biblioteca.py`   | Pruebas automáticas que validan los 4 puntos (búsqueda por ISBN, no duplicar autor, suma de copias, búsqueda sin tildes/mayúsculas, unicidad y formato de DNI, `CHECK` de cantidad). |

## Cómo correrlo

```bash
python3 main.py
```

Esto crea (si no existe) `biblioteca.db` en la misma carpeta y muestra un
menú con las 3 operaciones implementadas.

Para correr las pruebas:

```bash
python3 test_biblioteca.py
```

## Decisiones de diseño (Punto 1)

Ver los comentarios al inicio de `schema.sql`. En resumen:

- `Libro.ISBN` es `UNIQUE`: el ISBN identifica el título/edición, por eso
  "añadir un libro que ya existe" se traduce en sumar copias, no en crear
  una fila nueva.
- `Autor` tiene `UNIQUE(Nombre, Apellido, Fecha_nacimiento)` para no
  duplicar autores.
- `Libro.AutorID` usa `ON DELETE RESTRICT` para no dejar libros sin autor.
- `Usuario.DNI` es `UNIQUE` y tiene un `CHECK` que obliga 8 dígitos
  numéricos.
- `cantidad_disponible` tiene `CHECK (>= 0)`.

---

## Punto 4 — Administrar préstamos (1 pt, diseño sin implementar)

**Qué hay que tener en cuenta:**

- Un préstamo relaciona a **un usuario** con **un ejemplar disponible de
  un libro** en una fecha determinada. Al crearse, debe **descontar 1** de
  `Libro.cantidad_disponible`; al devolverse, debe **sumar 1** de vuelta.
- Un usuario no puede tener más de **3 préstamos activos** simultáneos
  (activos = sin fecha de devolución registrada todavía).
- No hay penalidad por vencimiento, así que no hace falta una tabla de
  multas, pero sí conviene guardar una fecha de devolución esperada para
  poder reportar libros atrasados aunque no se penalicen.
- Dos operaciones (verificar disponibilidad + descontar stock + registrar
  el préstamo) deben ocurrir de forma **atómica**: si dos usuarios piden
  el último ejemplar casi al mismo tiempo, no pueden terminar ambos con un
  préstamo válido. Por eso todo el flujo debe envolverse en una
  **transacción** (`BEGIN` … `COMMIT` / `ROLLBACK`), no en updates
  sueltos.

**Relaciones nuevas que habría que crear:**

```sql
CREATE TABLE Prestamo (
    IDprestamo          INTEGER PRIMARY KEY AUTOINCREMENT,
    IDusuario           INTEGER NOT NULL REFERENCES Usuario(IDusuario),
    IDlibro             INTEGER NOT NULL REFERENCES Libro(IDlibro),
    fecha_prestamo      DATE NOT NULL DEFAULT (date('now')),
    fecha_devolucion    DATE  -- NULL mientras el préstamo sigue activo
);
```

`fecha_devolucion IS NULL` es lo que define un préstamo como "activo".

**Trigger para el límite de 3 libros por usuario:**

```sql
CREATE TRIGGER limite_prestamos_usuario
BEFORE INSERT ON Prestamo
WHEN (
    SELECT COUNT(*) FROM Prestamo
    WHERE IDusuario = NEW.IDusuario AND fecha_devolucion IS NULL
) >= 3
BEGIN
    SELECT RAISE(ABORT, 'El usuario ya tiene 3 préstamos activos.');
END;
```

**Verificación de disponibilidad** (antes de insertar el préstamo, dentro
de la misma transacción):

```sql
BEGIN TRANSACTION;

-- 1) Verificar stock
SELECT cantidad_disponible FROM Libro WHERE IDlibro = :id_libro;
-- si cantidad_disponible <= 0 -> ROLLBACK y avisar que no hay copias

-- 2) Descontar una copia
UPDATE Libro SET cantidad_disponible = cantidad_disponible - 1
WHERE IDlibro = :id_libro AND cantidad_disponible > 0;
-- (el filtro "cantidad_disponible > 0" evita que quede negativo por una
--  carrera entre dos transacciones concurrentes)

-- 3) Registrar el préstamo (aquí dispara el trigger del límite de 3)
INSERT INTO Prestamo (IDusuario, IDlibro) VALUES (:id_usuario, :id_libro);

COMMIT;  -- o ROLLBACK si algún paso falló
```

Al devolver un libro, la contraparte sería: `UPDATE Prestamo SET
fecha_devolucion = date('now') WHERE IDprestamo = ...` seguido de sumar 1 a
`cantidad_disponible`, también dentro de una transacción.
