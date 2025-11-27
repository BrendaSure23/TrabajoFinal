from modelo.conexion import ConexionDB

class EditorialManager:
    def __init__(self):
            self.editorial = []
            self.cargar_editorial()
    
    def cargar_editorial(self):
        
        lista_db = obtener_editorial()
        
        self.editorial = []
        
        for id_editorial, nombre_editorial in lista_db:
            self.editorial.append({'id': id_editorial, 'Nombre': nombre_editorial})
        
    
    def get_nombres(self):
        """Retorna una lista de solo los nombres para llenar el ComboBox."""
        return [editorial['Nombre'] for editorial in self.editorial]
    
    def get_id_por_indice(self, index):
        if 0 <= index < len(self.editorial):
            return self.editorial[index]['id']
        return None
    
    def get_indice_por_id(self, id_editorial):
        for i, editorial in enumerate(self.editorial):
            if editorial['id'] == id_editorial:
                return i
        return 0 # Retorna 0 (Seleccione Uno) si no se encuentra
    
    def get_indice_por_nombre(self, nombre):
        for i, editorial in enumerate(self.editorial):
            if editorial['Nombre'] == nombre:
                return i
        return 0

def obtener_id_editorial_por_nombre(nombre_editorial):

    conn = ConexionDB()
    cursor = conn.cursor
    
    # Consulta SQL segura para buscar el ID
    sql = "SELECT id FROM Editoriales WHERE nombre = ?"
    
    try:
        cursor.execute(sql, (nombre_editorial,))
        # Usamos fetchone() para obtener la primera fila
        resultado = cursor.fetchone()
        conn.cerrar_con()

        if resultado:
            return resultado[0] 
        else:
            return None
            
    except Exception as e:
        print(f"Error al obtener el ID de la editorial '{nombre_editorial}': {e}")
        conn.cerrar_con()
        return None

def obtener_editorial():
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "SELECT id, nombre FROM Editoriales ORDER BY nombre"
    cursor.execute(sql)
    
    generos = cursor.fetchall()
    conn.cerrar_con()
    return generos

def insertar_editorial(nombre_editorial):
    """
    Busca si la editorial ya existe. Si no existe, lo inserta y retorna su ID.
    Si ya existe, retorna el ID.
    """
    conn = ConexionDB()
    cursor = conn.cursor
    
    # 1. Verificar si ya existe
    sql_check = "SELECT id FROM Editoriales WHERE nombre = ?"
    cursor.execute(sql_check, (nombre_editorial,))
    resultado = cursor.fetchone()
    if resultado:
        conn.cerrar_con()
        return resultado[0] # Retorna el ID existente
        
    # 2. Insertar si no existe
    sql_insert = "INSERT INTO Editoriales (nombre) VALUES (?)"
    try:
        cursor.execute(sql_insert, (nombre_editorial,))
        editorial_id = cursor.lastrowid
        conn.cerrar_con()
        return editorial_id
    except Exception as e:
        print(f"Error al insertar el editorial: {e}")
        conn.cerrar_con()
        return None

def actualizar_editorial(id_editorial, nombre_editorial):
    """Actualiza el nombre de una editorial existente."""
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "UPDATE Editoriales SET nombre = ? WHERE id = ?"
    
    try:
        cursor.execute(sql, (nombre_editorial, id_editorial))
        conn.cerrar_con()
        return cursor.rowcount > 0 
    except Exception as e:
        print(f"Error al actualizar la editorial: {e}")
        conn.cerrar_con()
        return False

def eliminar_editorial(id_editorial):
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "DELETE FROM Editoriales WHERE id = ?"
    
    try:
        cursor.execute(sql, (id_editorial,))
        conn.cerrar_con()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar la editorial: {e}")
        conn.cerrar_con()
        return False