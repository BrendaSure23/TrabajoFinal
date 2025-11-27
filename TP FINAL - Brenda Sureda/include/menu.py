import tkinter as tk


def barrita_menu(root):
    barra = tk.Menu(root)
    root.config(menu = barra, width = 300 , height = 300)
    
    menu_inicio = tk.Menu(barra, tearoff=0)
    menu_libros = tk.Menu(barra, tearoff=0) 
    menu_autores = tk.Menu(barra, tearoff=0) 
    menu_genero = tk.Menu(barra, tearoff=0)
    menu_editorial = tk.Menu(barra, tearoff=0)
    menu_ayuda = tk.Menu(barra, tearoff=0)
    
    barra.add_cascade(label='Inicio', menu=menu_inicio)
    barra.add_cascade(label='Libros', menu=menu_libros)      # <-- Usa menu_libros
    barra.add_cascade(label='Autores', menu=menu_autores)    # <-- Usa menu_autores
    barra.add_cascade(label='Género', menu=menu_genero) 
    barra.add_cascade(label='Editoriales', menu=menu_editorial)# <-- Usa menu_genero
    barra.add_cascade(label='Ayuda', menu=menu_ayuda)  # <-- Usa menu_ayuda
    
    # 1. Menú Inicial 
    menu_inicio.add_command(label='Conectar Base de Datos')
    menu_inicio.add_command(label='Desconectar Base de Datos')
    menu_inicio.add_separator() 
    menu_inicio.add_command(label='Salir del Programa', command=root.destroy)
    
    # 2. Menú LIBROS (Gestión de la Entidad Libro)
    menu_libros.add_command(label='Agregar Nuevo Libro')
    menu_libros.add_command(label='Ver Listado de Libros')
    menu_libros.add_command(label='Editar / Eliminar Libro')
    
    # 3. Menú AUTORES (Gestión de la Entidad Autor)
    menu_autores.add_command(label='Agregar Nuevo Autor')
    menu_autores.add_command(label='Ver Listado de Autores')
    menu_autores.add_command(label='Editar / Eliminar Autor')

    # 4. Menú GÉNERO (Gestión de la Entidad Género)
    menu_genero.add_command(label='Agregar Nuevo Género')
    menu_genero.add_command(label='Ver Listado de Géneros')
    menu_genero.add_command(label='Editar / Eliminar Géneros')
    
    # 5. Menú EDITORIALES (Gestión de la Entidad Editorial)
    menu_editorial.add_command(label='Agregar Nueva Editorial')
    menu_editorial.add_command(label='Ver Listado de Editoriales')
    menu_editorial.add_command(label='Editar / Eliminar Editoriales')
    
    # 6. Menú AYUDA
    menu_ayuda.add_command(label='Manual de Usuario')
    menu_ayuda.add_command(label='Acerca de...')
    