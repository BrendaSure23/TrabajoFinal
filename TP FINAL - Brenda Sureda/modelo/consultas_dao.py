import sqlite3
from modelo.conexion import ConexionDB 
from clases.clase_libros import Libro, guardar_libro
from clases.clase_autor import insertar_autor
from clases.clase_genero import insertar_genero
from clases.clase_editorial import insertar_editorial

def crear_tabla():
    conn = ConexionDB()

    # Usamos executescript para ejecutar todas las sentencias de una vez
    sql= '''
        -- Tabla Autores
        CREATE TABLE IF NOT EXISTS Autores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            nacionalidad TEXT
        );
        
        -- Tabla Editoriales
        CREATE TABLE IF NOT EXISTS Editoriales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
        
        -- Tabla Generos
        CREATE TABLE IF NOT EXISTS Generos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
    
        -- Tabla Libros
        CREATE TABLE IF NOT EXISTS Libros (
            -- Agregado AUTOINCREMENT para evitar problemas de ID con los datos de prueba
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            titulo TEXT NOT NULL,
            isbn TEXT UNIQUE,
            cantidad INTEGER NOT NULL DEFAULT 0,
            autor_id INTEGER,
            genero_id INTEGER,
            editorial_id INTEGER,
            FOREIGN KEY (autor_id) REFERENCES Autores (id) ON DELETE CASCADE,
            FOREIGN KEY (genero_id) REFERENCES Generos (id) ON DELETE CASCADE,
            FOREIGN KEY (editorial_id) REFERENCES Editoriales (id) ON DELETE CASCADE
        );
    '''
    try:
        conn.cursor.executescript(sql)
        conn.cerrar_con()
    except Exception as e:
        print(f"ERROR: Fallo al ejecutar script SQL de creación de tablas: {e}")


def inicializar_datos():
    """
    Inserta un set de autores, géneros, editoriales y libros de prueba.
    """
    
    print("\n--- INICIALIZANDO DATOS DE PRUEBA ---")
    
    # --- 1. Autores ---
    autor_ggm_id = insertar_autor("Gabriel García Márquez", "Colombiana")
    autor_ia_id = insertar_autor("Isabel Allende", "Chilena")
    autor_jlb_id = insertar_autor("Jorge Luis Borges", "Argentina")
    
    # --- 2. Editoriales ---
    editorial_penguin_id = insertar_editorial("Penguin Random House")
    editorial_ateneo_id = insertar_editorial("El Ateneo")
    editorial_planeta_id = insertar_editorial("Grupo Planeta")
    
    # --- 3. Géneros ---
    genero_ficcion_id = insertar_genero("Ficción")
    genero_no_fic_id = insertar_genero("No Ficción")
    genero_fantasia_id = insertar_genero("Fantasía")
    
    # --- 4. Libros ---
    print("\n--- Insertando Libros de Prueba (Latinoamericanos) ---")
    
    # Libro 1: Gabriel García Márquez
    # Comprobación de que todos los IDs existen antes de intentar guardar
    if autor_ggm_id and genero_ficcion_id and editorial_planeta_id:
        libro1 = Libro(
            titulo="Cien años de soledad", 
            isbn="978-0307474728", 
            cantidad=4, 
            autor_nombre="Gabriel García Márquez", 
            genero_nombre="Ficción",
            editorial_nombre= "Penguin Random House",
            autor_id=autor_ggm_id, 
            genero_id=genero_ficcion_id,
            editorial_id = editorial_penguin_id
        )
        guardar_libro(libro1)
        
    # Libro 2: Gabriel García Márquez
    if autor_ggm_id and genero_ficcion_id and editorial_planeta_id:
        libro2 = Libro(
            titulo="El amor en los tiempos del cólera", 
            isbn="978-0307474773", 
            cantidad=8, 
            autor_nombre="Gabriel García Márquez", 
            genero_nombre="Ficción",
            editorial_nombre= "Grupo Planeta",
            autor_id=autor_ggm_id, 
            genero_id=genero_ficcion_id,
            editorial_id = editorial_planeta_id
        )
        guardar_libro(libro2)
        
    # Libro 3: Jorge Luis Borges
    if autor_jlb_id and genero_ficcion_id and editorial_ateneo_id:
        libro3 = Libro(
            titulo="El aleph", 
            isbn="978-9875666481", 
            cantidad=3, 
            autor_nombre="Jorge Luis Borges", 
            genero_nombre="Ficción",
            editorial_nombre= "El Ateneo",
            autor_id=autor_jlb_id, 
            genero_id=genero_ficcion_id,
            editorial_id = editorial_ateneo_id
        )
        guardar_libro(libro3)
        
    # Libro 4: Isabel Allende
    if autor_ia_id and genero_fantasia_id and editorial_penguin_id:
        libro4 = Libro(
            titulo="La Casa de los Espíritus", 
            isbn="978-0345378730", 
            cantidad=5, 
            autor_nombre="Isabel Allende", 
            genero_nombre="Fantasía",
            editorial_nombre= "Penguin Random House",
            autor_id=autor_ia_id, 
            genero_id=genero_fantasia_id,
            editorial_id = editorial_penguin_id
        )
        guardar_libro(libro4)

    print("--- INICIALIZACIÓN DE DATOS COMPLETADA ---")


def inicializar_base_de_datos():
    """
    Función que llama a la creación de tablas y a la inserción de datos.
    """
    try:
        crear_tabla()
        inicializar_datos()
        print("INFO: Configuración de BD y datos iniciales completada.")
        return True
    except Exception as e:
        print(f"ERROR: Fallo crítico al inicializar la BD: {e}")
        return False