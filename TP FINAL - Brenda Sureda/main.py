import tkinter as tk
import os
from vistas.vista import Frame
from include.menu import barrita_menu
from modelo.consultas_dao import inicializar_base_de_datos

def main():
    ventana = tk.Tk()
    ventana.title('Gestión de Libros')
    ventana.resizable(0,0)
    
    barrita_menu(ventana)
    app = Frame(root = ventana)
    
    ventana.mainloop()

archivo_base_de_datos = 'ddbb/gestión_libros.db'

if __name__ == '__main__':
    
    if not os.path.exists(archivo_base_de_datos):
        print("-" * 50)
        print(f"Base de datos '{archivo_base_de_datos}' no encontrada.")
        print("INICIALIZANDO: Creando tablas y datos iniciales...")
        inicializar_base_de_datos()
        print("Inicialización de BBDD completa.")
        print("-" * 50)
        main()
    else:
        # Si el archivo SÍ existe, simplemente lo notificamos y continuamos.
        print(f"Base de datos '{archivo_base_de_datos}' encontrada. Saltando la inicialización de datos.")
        main()