from modelo.conexion import ConexionDB

class AutorManager:
    
    def __init__(self):
        self.autores = []
        self.cargar_autores()
    
    def cargar_autores(self):
        
        # Obtenemos la lista de tuplas (id, nombre) desde la BD
        lista_db = obtener_autores()
        
        self.autores = []
        
        for id_autor, nombre_autor in lista_db:
            self.autores.append({'id': id_autor, 'Nombre': nombre_autor})
    
    def get_nombres(self):
        """Retorna una lista de solo los nombres para llenar el ComboBox."""
        return [autor['Nombre'] for autor in self.autores]
    
    def get_id_por_indice(self, index):
        if 0 <= index < len(self.autores):
            return self.autores[index]['id']
        return None
    
    def get_indice_por_id(self, id_autor):
        for i, autor in enumerate(self.autores):
            if autor['id'] == id_autor:
                return i
        return 0 # Retorna 0 (Seleccione Uno) si no se encuentra
    
    def get_indice_por_nombre(self, nombre):
        for i, autor in enumerate(self.autores):
            if autor['Nombre'] == nombre:
                return i
        return 0

def obtener_id_autor_por_nombre(nombre_autor):
    conn = ConexionDB()
    cursor = conn.cursor
    
    # Consulta SQL segura para buscar el ID
    sql = "SELECT id FROM Autores WHERE nombre = ?"
    
    try:
        cursor.execute(sql, (nombre_autor,))
        # Usamos fetchone() para obtener la primera fila
        resultado = cursor.fetchone() 
        conn.cerrar_con()

        if resultado:
            # El resultado es una tupla, tomamos el primer elemento (el ID)
            return resultado[0] 
        else:
            return None
            
    except Exception as e:
        print(f"Error al obtener el ID del autor '{nombre_autor}': {e}")
        conn.cerrar_con()
        return None

def obtener_autores():
    
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "SELECT id, nombre FROM Autores ORDER BY nombre"
    cursor.execute(sql)
    
    autores = cursor.fetchall()
    conn.cerrar_con()
    return autores

def insertar_autor(nombre_autor, nacionalidad):
    """
    Busca si el autor ya existe. Si no existe, lo inserta y retorna su ID.
    Si ya existe, retorna el ID.
    """
    conn = ConexionDB()
    cursor = conn.cursor
    
    # 1. Verificar si ya existe
    sql_check = "SELECT id FROM Autores WHERE nombre = ?"
    cursor.execute(sql_check, (nombre_autor,))
    resultado = cursor.fetchone()
    if resultado:
        conn.cerrar_con()
        return resultado[0] # Retorna el ID existente
    
    # 2. Insertar si no existe
    sql_insert = "INSERT INTO Autores (nombre, nacionalidad) VALUES (?, ?)"
    try:
        cursor.execute(sql_insert, (nombre_autor, nacionalidad))
        autor_id = cursor.lastrowid
        conn.cerrar_con()
        return autor_id
    except Exception as e:
        print(f"Error al insertar el autor: {e}")
        conn.cerrar_con()
        return None

def actualizar_autor(id_autor, nombre_autor, nacionalidad):
    """Actualiza la información de un autor existente."""
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "UPDATE Autores SET nombre = ?, nacionalidad = ? WHERE id = ?"
    
    try:
        cursor.execute(sql, (nombre_autor, nacionalidad, id_autor))
        conn.cerrar_con()
        # Retorna True si se actualizó al menos una fila
        return cursor.rowcount > 0 
    except Exception as e:
        print(f"Error al actualizar el autor: {e}")
        conn.cerrar_con()
        return False

def eliminar_autor(id_autor):
    
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "DELETE FROM Autores WHERE id = ?"
    
    try:
        cursor.execute(sql, (id_autor,))
        conn.cerrar_con()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar el autor: {e}")
        conn.cerrar_con()
        return False