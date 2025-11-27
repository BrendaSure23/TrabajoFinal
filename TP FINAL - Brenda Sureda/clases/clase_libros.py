import sqlite3
from modelo.conexion import ConexionDB
from .clase_autor import obtener_id_autor_por_nombre, insertar_autor
from .clase_genero import obtener_id_genero_por_nombre, insertar_genero
from .clase_editorial import obtener_id_editorial_por_nombre, insertar_editorial

class Libro:
    """Clase para representar un Libro."""
    def __init__(self, titulo, isbn, cantidad, 
                autor_nombre=None, genero_nombre=None, 
                editorial_nombre =None,
                id=None, autor_id=None, genero_id=None, editorial_id =None):
        
        # Atributos principales y IDs (se usan argumentos nombrados)
        self.id = id 
        self.titulo = titulo
        self.isbn = isbn
        
        # Validación de Cantidad
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                raise ValueError("La cantidad de libros no puede ser negativa.")
            self.cantidad = cantidad
        except ValueError as e:
            raise ValueError(f"La cantidad debe ser un número entero. Error: {e}")

        # Atributos de visualización (Nombres) y Persistencia (IDs)
        self.autor_nombre = autor_nombre
        self.genero_nombre = genero_nombre
        self.editorial_nombre = editorial_nombre
        self.autor_id = autor_id 
        self.genero_id = genero_id
        self.editorial_id = editorial_id

    def __str__(self):
        """Representación en string del objeto Libro."""
        return (f"Libro(ID: {self.id}, Título: '{self.titulo}', ISBN: {self.isbn}, "
                f"Cantidad: {self.cantidad}, Autor: {self.autor_nombre} [ID: {self.autor_id}], "
                f"Género: {self.genero_nombre} [ID: {self.genero_id}])",
                f"Editorial: {self.editorial_nombre} [ID: {self.editorial_id}])")

def obtener_libros():
    conn = ConexionDB()
    libros_lista = []
    
    sql = """
    SELECT 
        L.id, L.titulo, L.isbn, L.cantidad, 
        L.autor_id, A.nombre AS nombre_autor,
        L.genero_id, G.nombre AS nombre_genero,
        L.editorial_id, E.nombre AS editorial_nombre
    FROM Libros L
    JOIN Autores A ON L.autor_id = A.id
    JOIN Generos G ON L.genero_id = G.id
    JOIN Editoriales E on L.editorial_id = E.id
    ORDER BY L.titulo
    """
    
    try:
        conn.cursor.execute(sql)
        libros_lista = conn.cursor.fetchall()
        conn.cerrar_con()
        
        return libros_lista
    except Exception as e:
        print(f"Error al obtener libros: {e}")
        conn.cerrar_con()
        return[]

def guardar_libro(libro):
    """
    Guarda un objeto Libro en la BD. Si el Autor o Género o Editorial no existen, los crea.
    """
    
    autor_id = libro.autor_id
    genero_id = libro.genero_id
    editorial_id = libro.editorial_id

    # 1. VERIFICACIÓN Y CREACIÓN DEL AUTOR (Necesario para la FK en la BD)
    if autor_id is None and libro.autor_nombre:
        # Intenta buscarlo primero
        autor_id = obtener_id_autor_por_nombre(libro.autor_nombre)
        
        if autor_id is None:
            #Si no existe, lo insertamos.
            try:
                # Si no tienes nacionalidad en la clase Libro, usa un valor por defecto o None
                autor_id = insertar_autor(libro.autor_nombre, "Desconocida") # <-- **ASUMIMOS Nacionalidad Desconocida**
                print(f"INFO: Autor '{libro.autor_nombre}' insertado automáticamente.")
            except Exception as e:
                print(f"ERROR: No se pudo crear el nuevo autor: {e}")
                raise ValueError("Error al intentar crear el nuevo Autor.")
        
    # 2. VERIFICACIÓN Y CREACIÓN DEL GÉNERO
    if genero_id is None and libro.genero_nombre:
        # Intenta buscarlo
        genero_id = obtener_id_genero_por_nombre(libro.genero_nombre)
        
        if genero_id is None:
            # Si no existe, lo insertamos.
            try:
                genero_id = insertar_genero(libro.genero_nombre)
                print(f"INFO: Género '{libro.genero_nombre}' insertado automáticamente.")
            except Exception as e:
                print(f"ERROR: No se pudo crear el nuevo género: {e}")
                raise ValueError("Error al intentar crear el nuevo Género.")
    
    # 3. VERIFICACIÓN Y CREACIÓN DE LA EDITORIAL
    if editorial_id is None and libro.editorial_nombre:
        # Intenta buscarlo
        editorial_id = obtener_id_editorial_por_nombre(libro.editorial_nombre)
        
        if editorial_id is None:
            # Si no existe, lo insertamos.
            try:
                editorial_id = insertar_editorial(libro.editorial_nombre)
                print(f"INFO: Editorial '{libro.editorial_nombre}' insertado automáticamente.")
            except Exception as e:
                print(f"ERROR: No se pudo crear la nueva editorial: {e}")
                raise ValueError("Error al intentar crear la nueva editorial.")
    
    # 4. VERIFICACIÓN FINAL de IDs (Aunque ya no debería fallar si la inserción fue exitosa)
    if autor_id is None or genero_id is None or editorial_id is None:
        # Este mensaje solo se vería si falla la inserción automática
        print(f"Error: Autor '{libro.autor_nombre}' (ID: {autor_id}), Género '{libro.genero_nombre}' (ID: {genero_id}) o Editorial '{libro.editorial_nombre}' (ID: {editorial_id}) no encontrados")
        raise ValueError("Autor, Género o Editorial no encontrados en la base de datos.")
        
    # 5. Inserción en la BD
    conn = ConexionDB()
    sql_insert_libro = "INSERT INTO Libros (titulo, isbn, cantidad, autor_id, genero_id, editorial_id) VALUES (?, ?, ?, ?, ?, ?)"
    
    try:
        conn.cursor.execute(sql_insert_libro, (libro.titulo, libro.isbn, libro.cantidad, autor_id, genero_id, editorial_id))
        conn.cerrar_con()
        print(f"Libro '{libro.titulo}' guardado con éxito.")
        return True
    except sqlite3.IntegrityError as e:
        conn.cerrar_con()
        print(f"Error de Integridad (ISBN duplicado): {e}")
        raise ValueError("Error: El ISBN ya está registrado en la base de datos.")
    except Exception as e:
        print(f"Error al insertar el libro: {e}")
        conn.cerrar_con()
        raise

def actualizar_libro(libro):
    
    autor_id = obtener_id_autor_por_nombre(libro.autor_nombre)
    if autor_id is None and libro.autor_nombre:
        try:
            autor_id = insertar_autor(libro.autor_nombre, "Desconocida") 
            print(f"INFO: Nuevo Autor '{libro.autor_nombre}' creado automáticamente durante la actualización.")
        except Exception as e:
            print(f"ERROR: No se pudo crear el nuevo autor: {e}")
            raise ValueError("Error al intentar crear el nuevo Autor durante la actualización.")
            
    # 2. GÉNERO: Obtener o Crear
    genero_id = obtener_id_genero_por_nombre(libro.genero_nombre)
    if genero_id is None and libro.genero_nombre:
        try:
            genero_id = insertar_genero(libro.genero_nombre)
            print(f"INFO: Nuevo Género '{libro.genero_nombre}' creado automáticamente durante la actualización.")
        except Exception as e:
            print(f"ERROR: No se pudo crear el nuevo género: {e}")
            raise ValueError("Error al intentar crear el nuevo Género durante la actualización.")

    # 3. EDITORIAL: Obtener o Crear
    editorial_id = obtener_id_editorial_por_nombre(libro.editorial_nombre)
    if editorial_id is None and libro.editorial_nombre:
        try:
            editorial_id = insertar_editorial(libro.editorial_nombre)
            print(f"INFO: Nueva Editorial '{libro.editorial_nombre}' creada automáticamente durante la actualización.")
        except Exception as e:
            print(f"ERROR: No se pudo crear la nueva editorial: {e}")
            raise ValueError("Error al intentar crear la nueva Editorial durante la actualización.")
            
    # --- VERIFICACIÓN FINAL y UPDATE ---

    if autor_id is None or genero_id is None or editorial_id is None:
        # Esto solo pasaría si la inserción falló y el ID sigue siendo None
        print("Error: El ID de Autor, Género o Editorial es nulo. No se puede actualizar el libro.")
        raise ValueError("Error crítico: El ID de Autor, Género o Editorial es nulo después de intentar crear/encontrar.")
    
    """Actualiza toda la información de un libro existente."""
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = """
    UPDATE Libros 
    SET titulo = ?, isbn = ?, cantidad = ?, autor_id = ?, genero_id = ?, editorial_id =? 
    WHERE id = ?
    """
    
    try:
        # Asegúrate de que los IDs no son None antes de la ejecución
        cursor.execute(sql, (libro.titulo, libro.isbn, libro.cantidad, autor_id, genero_id,editorial_id, libro.id ))
        conn.cerrar_con()
        print(f"Libro '{libro.titulo}' (ID: {libro.id}) actualizado con éxito.")
        return cursor.rowcount > 0 
    except Exception as e:
        print(f"Error al actualizar el libro: {e}")
        conn.cerrar_con()
        return False

def eliminar_libro(id_libro):
    """Elimina un libro por su ID."""
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "DELETE FROM Libros WHERE id = ?"
    
    try:
        cursor.execute(sql, (id_libro,))
        conn.cerrar_con()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar el libro: {e}")
        conn.cerrar_con()
        return False