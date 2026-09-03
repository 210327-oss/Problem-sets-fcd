--  Autor: Limberg Michael Miranda Curampa

-- =====================================================================
-- Problem Set 3 · Segunda Parte · Punto 1 (4 pts)
-- Creación de las tablas del Sistema de Gestión de Bibliotecas
-- =====================================================================
--
-- REGLAS ADICIONALES ASUMIDAS PARA MANTENER LA INTEGRIDAD REFERENCIAL
-- (cada una también está comentada junto a la restricción que la aplica):
--
-- 1. Un ISBN identifica un título/edición de forma única. Por eso
--    Libro.ISBN es UNIQUE: si se vuelve a "añadir" el mismo ISBN, en
--    realidad se están sumando copias a cantidad_disponible, no creando
--    una fila nueva (ver Punto 2).
-- 2. cantidad_disponible nunca puede ser negativa (CHECK >= 0).
-- 3. Un Autor se considera "la misma persona" si coincide
--    Nombre + Apellido + Fecha_nacimiento (UNIQUE compuesto). Esto evita
--    duplicar al autor si se ingresa dos veces con los mismos datos.
-- 4. No se puede borrar un Autor si todavía tiene libros asociados
--    (ON DELETE RESTRICT en Libro.AutorID), para no dejar libros
--    "huérfanos" sin autor.
-- 5. El DNI de Usuario debe ser único (no pueden existir dos usuarios
--    con el mismo DNI) y debe tener exactamente 8 dígitos numéricos
--    (CHECK con GLOB, ver Punto 4 del enunciado).
-- 6. Anio_publicacion debe caer en un rango razonable (después de la
--    imprenta de Gutenberg y no en el futuro), para evitar datos basura.
-- 7. Se activa PRAGMA foreign_keys = ON porque SQLite no aplica las
--    llaves foráneas por defecto.
-- =====================================================================

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Autor (
    ID                 INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre             TEXT NOT NULL,
    Apellido           TEXT NOT NULL,
    Fecha_nacimiento   DATE,
    UNIQUE (Nombre, Apellido, Fecha_nacimiento)      -- regla 3
);

CREATE TABLE IF NOT EXISTS Libro (
    IDlibro              INTEGER PRIMARY KEY AUTOINCREMENT,
    ISBN                 TEXT NOT NULL UNIQUE,                              -- regla 1
    Titulo               TEXT NOT NULL,
    Anio_publicacion     INTEGER CHECK (Anio_publicacion BETWEEN 1450 AND 2100), -- regla 6
    cantidad_disponible  INTEGER NOT NULL DEFAULT 0 CHECK (cantidad_disponible >= 0), -- regla 2
    AutorID              INTEGER NOT NULL,
    FOREIGN KEY (AutorID) REFERENCES Autor(ID)
        ON DELETE RESTRICT ON UPDATE CASCADE                                -- regla 4
);

CREATE TABLE IF NOT EXISTS Usuario (
    IDusuario         INTEGER PRIMARY KEY AUTOINCREMENT,
    DNI               TEXT NOT NULL UNIQUE,                                 -- regla 5
    Nombre            TEXT NOT NULL,
    Apellido          TEXT NOT NULL,
    email             TEXT,
    telefono          TEXT,
    fecha_membresia   DATE NOT NULL DEFAULT (date('now')),
    CHECK (length(DNI) = 8 AND DNI GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]') -- regla 5
);

-- Vista usada en el Punto 3 para consultar el catálogo (join Libro + Autor)
CREATE VIEW IF NOT EXISTS CatalogoView AS
SELECT
    Libro.IDlibro,
    Libro.ISBN,
    Libro.Titulo,
    Libro.Anio_publicacion,
    Libro.cantidad_disponible,
    Autor.ID        AS AutorID,
    Autor.Nombre    AS AutorNombre,
    Autor.Apellido  AS AutorApellido
FROM Libro
JOIN Autor ON Libro.AutorID = Autor.ID;
