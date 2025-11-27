📚 Sistema de Gestión de Libros (Tkinter + SQLite)

Este es un sistema de escritorio simple desarrollado en Python utilizando la librería tkinter y SQLite como base de datos local. El objetivo es gestionar un inventario de libros, incluyendo detalles como Título, ISBN, Cantidad, y sus relaciones con Autores, Géneros y Editoriales.

🛠️ Tecnologías Utilizadas

Lenguaje: Python 3.x

Interfaz Gráfica (GUI): tkinter y tkinter.ttk

Base de Datos: SQLite 3 (Integrado en Python)

Patrón: Orientación a Objetos (Clases para Entidades y Managers)

📦 Estructura del Proyecto

El proyecto se organiza en la siguiente estructura de carpetas y archivos:

ddbb/gestión_libro.db <-- Archivo de la base de datos SQLite


clases/clase_autor.py <-- Manager para Autores

clases/clase_editorial.py    <-- Manager para Editoriales

clases/clase_genero.py <-- Manager para Géneros

clases/clase_libros.py <-- Clase Libro y funciones CRUD


modelo/conexion.py <-- Establece conexión con BD (cierra, guarda cambios)

modelo/consultas_dao.py <-- Módulo de Data Access Object (conexión y consultas SQL)


vistas/vista.py <-- Módulo principal de la Interfaz Gráfica (Tkinter Frame)


main.py <-- Archivo de arranque del programa


README.md <-- Este archivo             

⚙️ Instalación y Requisitos

Requisitos

Necesitas tener instalado Python 3.x.

Instalación de Dependencias

Este proyecto utiliza librerías estándar de Python (tkinter, sqlite3, os) que generalmente vienen incluidas en la instalación base de Python.

▶️ Ejecución del Programa

Para iniciar la aplicación, simplemente ejecuta el archivo principal desde tu terminal:

python main.py

Primer Arranque

Si es la primera vez que ejecutas el programa y el archivo ddbb/gestión_libros.db no existe:

El programa creará automáticamente el archivo gestión_libros.db.

Ejecutará la función de inicialización para crear las tablas (Libros, Autor, Genero, Editorial).

Cargará algunos datos iniciales (Autores, Géneros, Editoriales) para que puedas comenzar a trabajar inmediatamente con los Combobox.

📝 Funcionalidades

El sistema soporta las operaciones básicas CRUD (Crear, Leer, Actualizar, Borrar) sobre la tabla de libros:

Nuevo: Habilita los campos de entrada y los botones "Guardar" y "Cancelar" para ingresar un nuevo libro.

Guardar: Guarda el libro actual (Nuevo o Editado) en la base de datos. Realiza validaciones básicas de campos.

Cancelar: Bloquea los campos y borra cualquier entrada temporal.

Tabla (Treeview): Muestra todos los libros con la información completa, incluyendo los nombres asociados (Autor, Género, Editorial).

Editar: Selecciona un libro de la tabla, carga sus datos en los campos de entrada y habilita el modo de edición.

Delete: Elimina el registro seleccionado de la tabla y la base de datos, pidiendo una confirmación previa.
