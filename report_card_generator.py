import tkinter as tk #Importar el modulo base de tkinter para crear la interface grafica
from tkinter import filedialog, messagebox #Importar funciones especificas para abrir archivos y mostrar mensajes

#----------FUNCIONES PARA LOS DATOS DE LOS ARCHIVOS----------#

def leer_datos_estudiantes(nombre_archivo):
    while True: #Inicia un bucle infinito para permitir reintentar la seleccion de archivos en caso de errores.
        estudiantes = [] #Inicializa una lista vacia para almacenar los datos de los estudiantes.
        try:
            with open(nombre_archivo, 'r') as archivo: #Abre el archivo especificado en modo lectura
                for linea in archivo: #Itera sobre cada linea del archivo abierto
                    partes = linea.strip().split(':') #Elimina espacios en blanco y divide la linea en partes usando ':' (nombre:ID)
                    if len(partes) == 2: #Verifica si la linea se dividio en exactamente dos partes (nombre y ID)
                        estudiantes.append({"nombre": partes[0].strip(), "id": partes[1].strip()}) #Agrega un diccionario con el nombre y ID del estudiante a la lista
                    else:
                        messagebox.showerror("Error", f"Formato incorrecto en el archivo de estudiantes: {linea.strip()}") #Muestra un mensaje de error si el formato del archivo es incorrecto
                        raise ValueError("Formato incorrecto") #Lanza un ValueError para activar el manejo de excepciones.
            return estudiantes #Devuelve la lista de estudiantes si el archivo se lee correctamente
        except Exception as e: #Captura cualquier excepcion que ocurra en el bloque try
            retry = messagebox.askretrycancel("Error", f"No se pudo leer el archivo de estudiantes: {str(e)}. ¿Desea seleccionar otro archivo?") #Muestra un cuadro de mensaje preguntando si desea reintentar.
            if not retry: #Verifica si el usuario eligio no reintentar.
                return None #Devuelve None si el usuario no quiere reintentar
            nombre_archivo = filedialog.askopenfilename(title="Archivo de estudiantes") #Abre un cuadro de dialogo para que el usuario seleccione un nuevo archivo de estudiantes

def leer_datos_evaluaciones(nombre_archivo): 
    while True: #Inicia un bucle infinito para permitir reintentar la seleccion de archivos en caso de errores.
        evaluaciones = [] #Inicializa una lista vacia para almacenar los datos de las evaluaciones.
        suma_porcentajes = 0 #Inicializa una variable para llevar la cuenta del porcentaje total.
        try:
            with open(nombre_archivo, 'r') as archivo: #Abre el archivo especificado en modo lectura
                for linea in archivo: #Itera sobre cada linea del archivo abierto
                    partes = linea.strip().split(':') #Elimina espacios en blanco y divide la linea en partes usando ':'
                    if len(partes) == 2: #Verifica si la linea se dividio en exactamente dos partes (nombre de evaluaciones y porcentaje)
                        nombre = partes[0].strip() #Saca el nombre de la evaluacion
                        porcentaje = float(partes[1].strip()) #Convierte el porcentaje a un numero de punto flotante
                        evaluaciones.append((nombre, porcentaje)) #Agrega una tupla con el nombre y porcentaje a la lista de evaluaciones
                        suma_porcentajes += porcentaje #Suma el porcentaje al total
                    else:
                        messagebox.showerror("Error", f"Formato incorrecto en el archivo de evaluaciones: {linea.strip()}") #Muestra un mensaje de error si el formato del archivo es incorrecto
                        raise ValueError("Formato incorrecto") #Lanza un ValueError para activar el manejo de excepciones.
            if suma_porcentajes != 100: #Verifica si el porcentaje total no es igual a 100
                raise ValueError("Porcentajes incorrectos") #Lanza un ValueError si los porcentajes son incorrectos.
            return evaluaciones #Devuelve la lista de evaluaciones si el archivo se lee correctamente
        except Exception as e: #Captura cualquier excepcion que ocurra en el bloque try
            retry = messagebox.askretrycancel("Error", f"No se pudo leer el archivo de evaluaciones: {str(e)}. ¿Desea seleccionar otro archivo?") #Muestra un cuadro de mensaje preguntando si desea reintentar.
            if not retry: #Verifica si el usuario eligio no reintentar.
                return None #Devuelve None si el usuario no quiere reintentar
            nombre_archivo = filedialog.askopenfilename(title="Archivo de evaluaciones") #Abre un cuadro de dialogo para que el usuario seleccione un nuevo archivo de evaluaciones

#----------GENERADOR DEL ARCHIVO CSV----------#

def generar_csv(data):
    estudiantes = leer_datos_estudiantes(data['archivo_estudiantes']) #Llama a la funcion para leer los datos de los estudiantes desde el archivo especificado.
    if estudiantes is None: #Verifica si no se pudo leer los datos de los estudiantes
        return #Sale de la funcion si no hay datos de estudiantes
    estudiantes.sort(key=lambda x: x['nombre']) #Ordena la lista de estudiantes por nombre

    evaluaciones = leer_datos_evaluaciones(data['archivo_evaluaciones']) #Llama a la funcion para leer los datos de las evaluaciones desde el archivo especificado
    if evaluaciones is None: #Verifica si no se pudo leer los datos de las evaluaciones
        return #Sale de la funcion si no hay datos de evaluaciones
    
    curva = data['curva'] #Recupera la curva de calificacion de los datos de entrada (ej: "A 90 B 80 C 70 D 60 F 0")
    partes_curva = curva.split() #Divide la cadena de la curva en partes en una lista (['A', '90', 'B', '80'...])
    valores_curva = {} #Inicia un diccionario para almacenar los valores de la curva
    for i in range(0, len(partes_curva), 2): #Itera sobre las partes de la curva en pasos de dos (nombre y valor) 
        valores_curva[partes_curva[i]] = int(partes_curva[i +1]) #Agrega los valores de la curva al diccionario, convirtiendolos a enteros (ej: {'A':90, 'B':80...})
    
    try:
        with open(data['archivo_csv'], 'w') as archivo: #Abre el archivo CSV especificando en modo escritura
            archivo.write(f",{data['universidad']}\n") #Escribe el nombre de la universidad en el archivo CSV
            archivo.write(f",{data['campus']}\n") #Escribe el campus en el archivo CSV
            archivo.write(f",{data['departamento']}\n") #Escribe el departamente en el archivo CSV
            archivo.write(f"Semestre: {data['semestre']}\n") #Escribe el semestre en el archivo CSV
            archivo.write(f"Profesor: {data['profesor']}\n") #Escribe el nombre del profesor en el archivo CSV
            archivo.write(f"Curso: {data['curso']}-({data['seccion']})\n\n") #Escribe el curso y seccion en el archivo CSV

            titulos = ["NUM", "NOMBRE", "ID"] #Inicializa una lista de titulos de columnas para el CSV
            for x in evaluaciones: #Itera sobre las evaluaciones
                titulos.append(x[0]) #Agrega el nombre de cada evaluacion a la lista de titulos
            titulos += ["AVG", "NOTA"] #Agrega 'AVG' y 'NOTA' a la lista de titulos
            archivo.write(",".join(titulos) + "\n") #Une los titulos con comas y los escribe como la primera fila en el CSV

            fila = 9 #Inicializa una variable para el numero de fila actual en el CSV
            for i, est in enumerate(estudiantes, start=1): #Itera sobre la lista de estudiantes, comenzando el indice en 1. (1,2,3,...)
                nombre = est['nombre'] #Coge el nombre del estudiante.
                fila_linea = [str(i), f'"{nombre}"', est['id']] #Inicializa una lista con los datos de la fila, incluyendo el numero de estudiante, nombre y ID.

                for _ in evaluaciones: #Agrega columnas vacias para cada evaluacion
                    fila_linea.append("") #Agrega una cadena vacia para cada evaluacion

                col = ord('D') #Inicializa una variable para representar la columna de inicio para las evaluaciones.
                partes = [] #Inicializa una lista vacia para almacenar partes de la formula del promedio.
                for j, (_,peso) in enumerate(evaluaciones): #Itera sobre las evaluaciones para obtener sus pesos.
                    partes.append(f"{chr(col + j)}{fila}*{peso/100}") #Construye las partes de la formula para calcular el promedio basado en los pesos
                promedio = f"=AVERAGE({'+'.join(partes)})" #Crea la formula del promedio usadno las partes contruidas
                fila_linea.append(promedio) #Agrega la formula del promedio a los datos de la fila

                formula_parts = [] #Inicializa una lista vacía para las partes de la fórmula de la Nota Final.
                for nota in ("A", "B", "C", "D"): #Itera sobre las letras de calificacion
                    formula_parts.append(f'K{fila}>={valores_curva[nota]}, ""{nota}""') #Agrega condiciones para cada calificacion a las partes de la formula
                formula_parts.append('TRUE, ""F""') #Agrega la condicion por defecto para la calificacion de reprobacion (F)
                formula = f'=IFS({",".join(formula_parts)})' #Construye la formula final de la nota final usando la funcion IFS
                fila_linea.append(f'"{formula}"') #Agrega la formula de la nota final a los datos de la fila

                archivo.write(",".join(fila_linea) + "\n") #Une los datos de la fila con comas y los escribe en el archivo CSV.
                fila += 1 #Incrementa el número de fila para el siguiente estudiante.


        messagebox.showinfo("Exito", f"Archivo CSV generado exitosamente: {data['archivo_csv']}") #Muestra un mensaje de exito indicando que el archivo CSV fue creado
    except Exception as e: #Captura cualquier excepcion que ocurra durante la escritura del archivo
        messagebox.showerror("Error", f"No se pudo crear el archivo CSV: {str(e)}") #Muestra un mensaje de error si no se pudo crear el archivo CSV

#----------INTERFAZ DE USUARIO CON TKINTER----------#

root = tk.Tk() #Crea la ventana principal de la aplicacion.
root.title("Generador de Reporte de Notas") #Titulo de la ventana
root.geometry("600x600") #Establece el tamaño de la ventana

entradas = {} #Inicializa un diccionario para almacenar las entradas de los campos.

campos = [ #Define una lista de campos que se mostraran en la interfaz.
    ("universidad", "Nombre de la Universidad:"),
    ("campus", "Campus:"),
    ("departamento", "Departamento:"),
    ("semestre", "Semestre:"),
    ("curso", "Curso:"),
    ("seccion", "Seccion:"),
    ("profesor", "Nombre del Profesor"),
    ("curva", "Curva a utilizar para A, B, C, D, F (ejemplo: A 90 B 80 C 70 D 60 F 0)"),
    ("archivo_csv", "Nombre del archivo que contendra al registro de notas:")
]

for clave, texto in campos: #Itera sobre los campos definidos.
    tk.Label(root, text=texto).pack() #Crea y muestra una etiqueta para cada campo.
    entradas[clave] = tk.Entry(root, width=60) #Crea un campo de entrada para cada campo
    entradas[clave].pack() #Muestra el campo de entrada en la ventana.

def seleccionar_archivo_estudiantes():
    archivo = filedialog.askopenfilename(title="Archivo de estudiantes") #Abre un cuadro de dialogo para seleccionar un archivo de estudiantes.
    entradas['archivo_estudiantes'].delete(0, tk.END) #Elimina el contenido actual del campo de entrada de estudiantes.
    entradas['archivo_estudiantes'].insert(0, archivo) #Inserta la ruta del archivo seleccionado en el campo de entrada.

def seleccionar_archivo_evaluaciones():
    archivo = filedialog.askopenfilename(title="Archivo de evaluaciones") #Abre un cuadro de dialogo para seleccionar un archivo de evaluaciones.
    entradas['archivo_evaluaciones'].delete(0, tk.END) #Elimina el contenido actual del campo de entrada de evaluaciones.
    entradas['archivo_evaluaciones'].insert(0, archivo) #Inserta la ruta del archivo seleccionado en el campo de entrada.

tk.Button(root, text="Seleccionar archivo de estudiantes", command=seleccionar_archivo_estudiantes).pack() #Crea un boton para seleccionar el archivo de estudiantes.
entradas['archivo_estudiantes'] = tk.Entry(root, width=60) #Crea un campo de entrada para la ruta del archivo de estudiantes.
entradas['archivo_estudiantes'].pack() #Muestra el campo de entrada en la ventana.

tk.Button(root, text="Seleccionar archivo de evaluaciones", command=seleccionar_archivo_evaluaciones).pack() #Crea un boton para seleccionar el archivo de evaluaciones.
entradas['archivo_evaluaciones'] = tk.Entry(root, width=60) #Crea un campo de entrada para la ruta del archivo de evaluaciones.
entradas['archivo_evaluaciones'].pack() #Muestra el campo de entrada en la ventana.

def ejecutar():
    datos = {} #Inicializa un diccionario vacio para almacenar los datos
    for clave in entradas: #Itera sobre las claves en el diccionario de entradas
        datos[clave] = entradas[clave].get() #Asigna el valor de cada entrada al diccionario
    generar_csv(datos) #Llama a la funcion para generar el archivo CSV con los datos recopilados

tk.Button(root, text="Generar CSV", command=ejecutar, bg="green", fg="white").pack(pady=10) #Crea un boton para generar el CSV, color verde y texto blanco

root.mainloop() #Inicia el bucle principal de la interfaz grafica
