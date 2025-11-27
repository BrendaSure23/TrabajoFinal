from modelo.conexion import ConexionDB

class GeneroManager:
    def __init__(self):
            self.generos = []
            self.cargar_generos()
    
    def cargar_generos(self):
        lista_db = obtener_generos()
        
        self.generos = []
        
        for id_genero, nombre_genero in lista_db:
            self.generos.append({'id': id_genero, 'Nombre': nombre_genero})
    
    def get_nombres(self):
        return [genero['Nombre'] for genero in self.generos]
    
    def get_id_por_indice(self, index):
        if 0 <= index < len(self.generos):
            return self.generos[index]['id']
        return None
    
    def get_indice_por_id(self, id_genero):
        for i, genero in enumerate(self.generos):
            if genero['id'] == id_genero:
                return i
        return 0 # Retorna 0 (Seleccione Uno) si no se encuentra
    
    def get_indice_por_nombre(self, nombre):
        for i, genero in enumerate(self.generos):
            if genero['Nombre'] == nombre:
                return i
        return 0

def obtener_id_genero_por_nombre(nombre_genero):

    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "SELECT id FROM Generos WHERE nombre = ?"
    
    try:
        cursor.execute(sql, (nombre_genero,))
        resultado = cursor.fetchone()
        conn.cerrar_con()

        if resultado:
            return resultado[0] 
        else:
            return None
            
    except Exception as e:
        print(f"Error al obtener el ID del género '{nombre_genero}': {e}")
        conn.cerrar_con()
        return None

def obtener_generos():
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "SELECT id, nombre FROM Generos ORDER BY nombre"
    cursor.execute(sql)
    
    generos = cursor.fetchall()
    conn.cerrar_con()
    return generos

def insertar_genero(nombre_genero):
    """
    Busca si el género ya existe. Si no existe, lo inserta y retorna su ID.
    Si ya existe, retorna el ID.
    """
    conn = ConexionDB()
    cursor = conn.cursor
    
    # 1. Verificar si ya existe
    sql_check = "SELECT id FROM Generos WHERE nombre = ?"
    cursor.execute(sql_check, (nombre_genero,))
    resultado = cursor.fetchone()
    if resultado:
        conn.cerrar_con()
        return resultado[0] # Retorna el ID existente
        
    # 2. Insertar si no existe
    sql_insert = "INSERT INTO Generos (nombre) VALUES (?)"
    try:
        cursor.execute(sql_insert, (nombre_genero,))
        genero_id = cursor.lastrowid
        conn.cerrar_con()
        return genero_id
    except Exception as e:
        print(f"Error al insertar el género: {e}")
        conn.cerrar_con()
        return None

def actualizar_genero(id_genero, nombre_genero):
    """Actualiza el nombre de un género existente."""
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "UPDATE Generos SET nombre = ? WHERE id = ?"
    
    try:
        cursor.execute(sql, (nombre_genero, id_genero))
        conn.cerrar_con()
        return cursor.rowcount > 0 
    except Exception as e:
        print(f"Error al actualizar el género: {e}")
        conn.cerrar_con()
        return False

def eliminar_genero(id_genero):
    conn = ConexionDB()
    cursor = conn.cursor
    
    sql = "DELETE FROM Generos WHERE id = ?"
    
    try:
        cursor.execute(sql, (id_genero,))
        conn.cerrar_con()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar el género: {e}")
        conn.cerrar_con()
        return False