import tkinter as tk
from tkinter import ttk, messagebox
from clases.clase_libros import Libro, guardar_libro, obtener_libros, actualizar_libro, eliminar_libro
from clases.clase_genero import GeneroManager
from clases.clase_autor import AutorManager
from clases.clase_editorial import EditorialManager


class Frame(tk.Frame): 
    def __init__(self, root = None): 
        super().__init__(root,width=480,height=320) 
        self.root = root 
        self.pack() 
        self.config(bg='#FAF0E6')
        
        self.id_libro =None
        
        self.selected_autor_id = None
        self.selected_genero_id = None
        self.selected_editorial_id = None

        self.genero_manager = GeneroManager()
        self.editorial_manager = EditorialManager()
        
        self.label_form()
        self.input_form()
        self.botones_principales()
        self.mostrar_tabla()
    
    
    def label_form(self):
        self.label_titulo = tk.Label(self, text="Título ")
        self.label_titulo.config(font=('Arial',12,'bold'),fg = '#800020')
        self.label_titulo.grid(row= 1, column=0,padx=10,pady=10)
        
        self.label_autor = tk.Label(self, text="Autor ")
        self.label_autor.config(font=('Arial',12,'bold'),fg = '#800020')
        self.label_autor.grid(row= 2, column=0,padx=10,pady=10)
        
        self.label_isbn = tk.Label(self, text="ISBN ")
        self.label_isbn.config(font=('Arial',12,'bold'),fg = '#800020')
        self.label_isbn.grid(row= 3, column=0,padx=10,pady=10)
        
        self.label_cantidad = tk.Label(self, text="Cantidad ")
        self.label_cantidad.config(font=('Arial',12,'bold'),fg = '#800020')
        self.label_cantidad.grid(row= 4, column=0,padx=10,pady=10)
        
        self.label_genero = tk.Label(self, text="Género ")
        self.label_genero.config(font=('Arial',12,'bold'),fg = '#800020')
        self.label_genero.grid(row= 5, column=0,padx=10,pady=10, columnspan='1')
        
        self.label_genero = tk.Label(self, text="Editorial ")
        self.label_genero.config(font=('Arial',12,'bold'),fg = '#800020')
        self.label_genero.grid(row= 6, column=0,padx=10,pady=10, columnspan='1')
    
    
    def input_form(self):
        self.titulo =tk.StringVar()
        self.entry_titulo = tk.Entry(self, textvariable=self.titulo)
        self.entry_titulo.config(width=50, state='disabled')
        self.entry_titulo.grid(row= 1, column=1,padx=10,pady=10)
        
        self.autor =tk.StringVar()
        self.entry_autor = tk.Entry(self, textvariable=self.autor)
        self.entry_autor.config(width=50, state='disabled')
        self.entry_autor.grid(row= 2, column=1,padx=10,pady=10)
        
        self.isbn =tk.StringVar()
        self.entry_isbn = tk.Entry(self, textvariable=self.isbn)
        self.entry_isbn.config(width=50, state='disabled')
        self.entry_isbn.grid(row= 3, column=1,padx=10,pady=10)
        
        self.cantidad =tk.IntVar()
        self.entry_cantidad = tk.Entry(self, textvariable=self.cantidad)
        self.entry_cantidad.config(width=50, state='disabled')
        self.entry_cantidad.grid(row= 4, column=1,padx=10,pady=10)
        
        self.genero_var = tk.StringVar(self) 
        self.entry_genero = ttk.Combobox(self, textvariable=self.genero_var, state="readonly") 
        self.entry_genero.config(width=25, state='disabled') 
        
        genero_nombres = self.genero_manager.get_nombres()
        
        if genero_nombres:
            self.entry_genero['values'] = ("-- Seleccione Uno --",) + tuple(genero_nombres)
            self.entry_genero.current(0)
            self.selected_genero_id = None

        def on_genero_selected(event):
            selected_index = self.entry_genero.current()
            if selected_index > 0:
                self.selected_genero_id = self.genero_manager.get_id_por_indice(selected_index - 1)
            else:
                self.selected_genero_id = None
        
        self.entry_genero.bind("<<ComboboxSelected>>", on_genero_selected) 
        self.entry_genero.grid(row=5, column=1, padx=10, pady=5, sticky='ew')
        
        self.editorial_var = tk.StringVar(self) 
        self.entry_editorial = ttk.Combobox(self, textvariable=self.editorial_var, state="readonly") 
        self.entry_editorial.config(width=25, state='disabled') 
        
        editorial_nombres = self.editorial_manager.get_nombres()
        
        if editorial_nombres:
            self.entry_editorial['values'] = ("-- Seleccione Uno --",) + tuple(editorial_nombres)
            self.entry_editorial.current(0)
            self.selected_editorial_id = None

        def on_editorial_selected(event):
            selected_index = self.entry_editorial.current()
            if selected_index > 0:
                self.selected_editorial_id = self.editorial_manager.get_id_por_indice(selected_index - 1)
            else:
                self.selected_editorial_id = None
        
        self.entry_editorial.bind("<<ComboboxSelected>>", on_editorial_selected) 
        self.entry_editorial.grid(row=6, column=1, padx=10, pady=5, sticky='ew')
    
    
    def botones_principales(self):
        self.btn_alta = tk.Button(self, text='Nuevo', command=self.habilitar_campos)
        self.btn_alta.config(width= 20,font=('Arial', 12,'bold'),fg = '#FFFFFF',bg=  '#800020',
        cursor='hand2',activebackground= '#800020',activeforeground= '#000000')
        self.btn_alta.grid(row= 7, column=0,padx=10,pady=10)
        
        self.btn_modi = tk.Button(self, text='Guardar', command=self.guardar_campos)
        self.btn_modi.config(width= 20,font=('Arial', 12,'bold'),fg = '#FFFFFF', bg= '#800020',
        cursor='hand2',activebackground= '#800020',activeforeground= '#000000', state='disabled')
        self.btn_modi.grid(row= 7, column=1,padx=10,pady=10)
        
        self.btn_cance = tk.Button(self, text='Cancelar', command=self.bloquear_campos)
        self.btn_cance.config(width= 20,font=('Arial', 12,'bold'),fg = '#FFFFFF', bg= '#800020',
        cursor='hand2',activebackground= '#800020',activeforeground= '#000000', state='disabled')
        self.btn_cance.grid(row= 7, column=2,padx=10,pady=10)   
    
    def mostrar_tabla(self):
        self.lista_p = obtener_libros()
        
        self.tabla = ttk.Treeview(self,columns=('Título', 'Autor','ISBN','Cantidad','Género','Editorial'))
        self.tabla.grid(row=8,column=0,columnspan=4, sticky='nse')

        self.scroll = ttk.Scrollbar(self, orient='vertical', command= self.tabla.yview)
        self.scroll.grid(row=8,column=7, sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll.set)
        
        self.tabla.heading('#0',text="ID")
        self.tabla.heading('#1',text="Título")
        self.tabla.heading('#2',text="Autor")
        self.tabla.heading('#3',text="ISBN")
        self.tabla.heading('#4',text="Cantidad")
        self.tabla.heading('#5',text="Género")
        self.tabla.heading('#6',text="Editorial")

        for p in self.lista_p:
            self.tabla.insert('', 'end', text=p[0],
                        values=(p[1], p[5], p[2], p[3], p[7], p[9]))
        
        #boton editar
        self.btn_editar = tk.Button(self, text='Editar', command=self.editar_registro)    
        self.btn_editar.config(width= 20,font=('Arial', 12,'bold'),fg ='#FFFFFF' ,bg='#800020',cursor='hand2',activebackground='#800020',activeforeground='#000000')    
        self.btn_editar.grid(row= 9, column=0,padx=10,pady=10)    
        
        #boton delete 
        self.btn_delete = tk.Button(self, text='Delete', command=self.eliminar_registro)    
        self.btn_delete.config(width= 20,font=('Arial', 12,'bold'),fg ='#FFFFFF' ,bg='#800020',cursor='hand2',activebackground='#800020',activeforeground='#000000')    
        self.btn_delete.grid(row= 9, column=1,padx=10,pady=10)

    def editar_registro(self):
        try:
            self.id_libro = self.tabla.item(self.tabla.selection())['text']

            self.titulo_libro = self.tabla.item(self.tabla.selection())['values'][0]
            self.autor_libro = self.tabla.item(self.tabla.selection())['values'][1]
            self.isbn_libro = self.tabla.item(self.tabla.selection())['values'][2]
            self.cantidad_libro = self.tabla.item(self.tabla.selection())['values'][3]
            self.genero_libro = self.tabla.item(self.tabla.selection())['values'][4]
            self.editorial_libro = self.tabla.item(self.tabla.selection())['values'][5]

            self.habilitar_campos()
            self.titulo.set(self.titulo_libro)
            self.autor.set(self.autor_libro)
            self.isbn.set(self.isbn_libro)
            self.cantidad.set(self.cantidad_libro)
            indice_genero = self.genero_manager.get_indice_por_nombre(self.genero_libro)
            self.entry_genero.current(indice_genero)
            indice_editorial = self.editorial_manager.get_indice_por_nombre(self.editorial_libro)
            self.entry_editorial.current(indice_editorial)
        except:
            pass  
    
    
    def eliminar_registro(self):
        self.id_libro = self.tabla.item(self.tabla.selection())['text']

        response = messagebox.askyesno("Confirmar","¿Desea borrar el registro?")
        
        if response:    
            eliminar_libro(int(self.id_libro))
            messagebox.showinfo("Eliminación Exitosa", f"Libro ID {self.id_libro} eliminado correctamente.")
        else:
            messagebox.showinfo("ADVERTENCIA", "Registro no eliminado")
        
        self.id_libro = None
        self.mostrar_tabla()


    def guardar_campos(self):
        
        titulo = self.titulo.get()
        autor_nombre = self.entry_autor.get() 
        isbn = self.isbn.get()
        cantidad = self.cantidad.get()
        genero_nombre = self.entry_genero.get() 
        editorial_nombre = self.entry_editorial.get() 
        
        if not self.titulo.get() or not self.titulo.get().strip():
            messagebox.showwarning("Validación", "El campo Título es obligatorio y no puede estar vacío.")
            return
        
        if not self.autor.get() or not self.autor.get().strip():
            messagebox.showwarning("Validación", "El campo Autor es obligatorio y no puede estar vacío.")
            return
        
        if not self.isbn.get() or not self.isbn.get().strip():
            messagebox.showwarning("Validación", "El campo ISBN es obligatorio y no puede estar vacío.")
            return
            
        # 2. Validación de Cantidad
        if self.cantidad.get() <= 0:
            messagebox.showwarning("Validación", "La Cantidad debe ser un número entero positivo (mayor a 0).")
            return
            
        if self.selected_genero_id is None:
            if self.genero_manager.get_nombres():
                messagebox.showwarning("Validación", "Debes seleccionar un Género válido.")
            else:
                messagebox.showwarning("Validación", "No hay Géneros cargados. Carga uno antes de guardar un libro.")
            return
            
        if self.selected_editorial_id is None:
            if self.editorial_manager.get_nombres():
                messagebox.showwarning("Validación", "Debes seleccionar una Editorial válida.")
            else:
                messagebox.showwarning("Validación", "No hay Editoriales cargadas. Carga una antes de guardar un libro.")
            return
        
        
        libro = Libro(
        titulo = titulo, 
        autor_nombre = autor_nombre,     
        isbn = isbn,
        cantidad = cantidad, 
        genero_nombre = genero_nombre,
        editorial_nombre = editorial_nombre,
        # se pasa el ID para la actualización
        id = self.id_libro if self.id_libro else None 
    )
    
        try:
            if self.id_libro is None:
                guardar_libro(libro)
                messagebox.showinfo("Guardar Libro", "Libro guardado exitosamente (Nuevo registro).")
            else:
                actualizar_libro(libro) 
                messagebox.showinfo("Actualizar Libro", f"Libro ID {self.id_libro} actualizado exitosamente.")
            self.bloquear_campos()
            self.mostrar_tabla()
        except ValueError as e:
            # Captura los errores lanzados por el Manager (ej. "Género o Editorial no encontrados", "ISBN duplicado", "Cantidad inválida")
            print(f"ERROR DE OPERACIÓN: {e}")


    def habilitar_campos(self): 
        self.entry_titulo.config(state='normal')
        self.entry_autor.config(state='normal')
        self.entry_isbn.config(state='normal')
        self.entry_cantidad.config(state='normal')
        self.entry_genero.config(state='normal') 
        self.entry_editorial.config(state='normal') 
        
        self.btn_modi.config(state='normal')
        self.btn_cance.config(state='normal')
        self.btn_alta.config(state='disabled')
        
    def bloquear_campos(self): 
        self.entry_titulo.config(state='disabled')
        self.entry_autor.config(state='disabled')
        self.entry_isbn.config(state='disabled')
        self.entry_cantidad.config(state='disabled')
        self.entry_genero.config(state='disabled')
        self.entry_editorial.config(state='disabled')
        
        self.btn_modi.config(state='disabled')
        self.btn_cance.config(state='disabled')
        
        #autor y genero están con combobox
        self.titulo.set('')
        self.isbn.set('')
        self.cantidad.set('')
        
        self.btn_alta.config(state='normal')