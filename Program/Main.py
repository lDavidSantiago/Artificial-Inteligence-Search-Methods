import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from Generate_Maze import generate_maze
from Proyecto import call_allfunctions
from TreeClass import TreeNode
from Proyecto import heuristic,set_end,end_pos
import matplotlib.pyplot as plt

# Función para crear el mapa
def crear_mapa():
    global mapa
    try:
        n = int(entry_n.get())
        m = int(entry_m.get())
        mapa, start, end = generate_maze(n, m)
        
        texto_mapa.config(state=tk.NORMAL)
        texto_mapa.delete("1.0", tk.END)
        
        # Print column numbers with exact spacing
        texto_mapa.insert(tk.END, "#")
        for i in range(n):
            texto_mapa.insert(tk.END, f" {i}   ")
        texto_mapa.insert(tk.END, "\n")
        
        # Print maze with row numbers
        for i, fila in enumerate(mapa):
            texto_mapa.insert(tk.END, f"  {fila},#{i}\n")
            
        texto_mapa.config(state=tk.DISABLED)
        
        global start_pos, end_pos
        start_pos = start
        end_pos = end
        
    except ValueError:
        texto_mapa.config(state=tk.NORMAL)
        texto_mapa.delete("1.0", tk.END)
        texto_mapa.insert(tk.END, "⚠️ Error: Ingrese valores numéricos válidos.")
        texto_mapa.config(state=tk.DISABLED)

# Función para iniciar la búsqueda
def empezar_busqueda():
    texto_mapa.config(state=tk.NORMAL)
    texto_mapa.insert(tk.END, "\n🔍 Iniciando búsqueda...\n")
    texto_mapa.config(state=tk.DISABLED)
    raiz = TreeNode("R", start_pos)
    node = [raiz]
    set_end(end_pos)
    print("Este es el mapa que se genero")
    node[0].cost = node[0].base_cost
    plt.ion()
    if(call_allfunctions(node,mapa,int(entry_expansiones.get()))):
        print("Solucion encontradaaa")
    else:
        print("No se encontro el camino")
    plt.ioff()
    plt.close()

# Crear ventana principal
root = tk.Tk()
root.title("Generador de Mapas Elegante")
root.geometry("600x550")
root.configure(bg="#1C1C1C")
root.resizable(False, False)

# Estilo personalizado
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", foreground="#EAECEE", background="#1C1C1C", font=("Segoe UI", 12))
style.configure("TButton", foreground="#1C1C1C", background="#5DADE2", font=("Segoe UI", 12, "bold"), borderwidth=0)
style.map("TButton", background=[("active", "#3498DB")])
style.configure("TEntry", relief="flat", padding=5, font=("Segoe UI", 12))
style.configure("TFrame", background="#1C1C1C")

# Frame para los inputs
frame_inputs = ttk.Frame(root, padding=20)
frame_inputs.pack(pady=20)

# Input para N (tamaño filas)
label_n = ttk.Label(frame_inputs, text="📝 Tamaño N:")
label_n.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_n = ttk.Entry(frame_inputs, width=10)
entry_n.grid(row=0, column=1, padx=10, pady=10)

# Input para M (tamaño columnas)
label_m = ttk.Label(frame_inputs, text="📝 Tamaño M:")
label_m.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_m = ttk.Entry(frame_inputs, width=10)
entry_m.grid(row=1, column=1, padx=10, pady=10)

# Input para número de expansiones
label_expansiones = ttk.Label(frame_inputs, text="📈 Número de Expansiones:")
label_expansiones.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_expansiones = ttk.Entry(frame_inputs, width=10)
entry_expansiones.grid(row=2, column=1, padx=10, pady=10)

# Botones para crear mapa y empezar búsqueda
frame_botones = ttk.Frame(root, padding=10)
frame_botones.pack(pady=10)

boton_crear_mapa = ttk.Button(frame_botones, text="🗺️ Crear Mapa", command=crear_mapa)
boton_crear_mapa.grid(row=0, column=0, padx=10)

boton_busqueda = ttk.Button(frame_botones, text="🔍 Empezar Búsqueda", command=empezar_busqueda)
boton_busqueda.grid(row=0, column=1, padx=10)

# Campo de texto para mostrar el mapa
texto_mapa = ScrolledText(root, height=15, wrap=tk.WORD, font=("Consolas", 14), bg="#2E2E2E", fg="#EAECEE", relief="flat")
texto_mapa.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
texto_mapa.config(state=tk.DISABLED)

# Iniciar la aplicación
root.mainloop()
