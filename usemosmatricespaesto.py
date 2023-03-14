import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# INGRESO DE DATOS
input_root = tk.Tk() # Creación de la raíz del input

#PARTE 1: Lista
tk.Label(input_root, text="Ingrese la lista", font=("Arial Black", 15)).grid(column = 0, row = 0) 

saved_value = tk.Text(input_root,font=("Arial Black", 10), height=5, width=50)
saved_value.grid(row=0, column=1)

#PARTE 2: Reemplazo por comas
tk.Label(input_root, text="Reemplaza por ','", font=("Arial Black", 15)).grid(row=1, column=0)

who_quit = tk.StringVar()
tk.Entry(input_root, textvariable=who_quit, justify="center", font=("Arial Black", 15)).grid(row = 1, column= 1)
who_quit.set(",")

#PARTE 3: Número de clases
tk.Label(input_root, text="N clases", font=("Arial Black", 15)).grid(column = 0, row=2)

n_clases = tk.StringVar()
tk.Entry(input_root, textvariable=n_clases, justify="center", font=("Arial Black", 15)).grid(row=2, column=1)

#PARTE 4: Redondear
tk.Label(input_root, text="Redondea", font=("Arial Black", 15)).grid(column = 0, row=3)

rounder = tk.StringVar()
tk.Entry(input_root, textvariable=rounder, justify="center", font=("Arial Black", 15)).grid(row=3, column=1)
rounder.set('4')

# Acción de asignar variables
def continueInput():
    global saved_value, who_quit, n_clases, input_root
    saved_value = saved_value.get("1.0", "end-1c")
    who_quit = who_quit.get()
    if n_clases.get() == "":
        n_clases = 0
    else:
        n_clases = int(n_clases.get())
    input_root.destroy()

tk.Button(input_root, command=continueInput, text="LISTO", font=("Arial Black", 20)).grid(column=0, row=4, columnspan=2, pady=5)


input_root.mainloop()

saved_value = saved_value.replace(who_quit, ",")
saved_value = saved_value.replace(" ", "")

# ASIGNACIÓN A LISTA
lista = [float(x) for x in saved_value.split(",")]

if n_clases == 0 or n_clases == "":
    clases = 1 +  (3.322 * (math.log(len(lista), 10))) # CALCULO DE CLASES STURGES
    clases = math.ceil(clases) if int(clases) % 2 == 0 else int(clases) # APROXIMACIÓN A IMPAR
else:
    clases = n_clases


# CALCULO DE DATO MAYOR Y MENOR
dato_menor = min(lista)
dato_mayor = max(lista)
    
def rnd(num): # Redondea según el dato ingresado
    return round(num, int(rounder.get())) 


amplitud = (dato_mayor - dato_menor) / clases # La amplitud aproximada hacia arriba
amplitud = math.ceil(amplitud) if all(isinstance(x, int) or (isinstance(x, float) and x.is_integer()) for x in lista) else amplitud
amplitud = rnd(amplitud) # Redondea

#INICIO DE LA ESTRUCTURACIÓN DE LA MATRIZ
matriz = []

lia = dato_menor # Limite Inferior
lsa = dato_menor + amplitud # Límite Superior
c = 0 # Contador para la frecuencia
lasth = 0 # Acumulativa de h
lastc = 0 # De f



 # Estructuración de cada fila matricial en el número de clases
for i in range(clases):
    nueva_lista = [] # Esta lista será la que se va a insertar, es cada fila
    nueva_lista += [rnd(lia), rnd(lsa)] # Primero se agregan los límites y se redondean

    lastc += c # Se suma el anterior resultado de f para la acumulativa
    lasth += (c/len(lista)) # Igual que con h
    c = 0 # Y después de guardar la F se reinicia para contar desde cero f
    if i < clases - 1: # Si NO es la ultima clase
        for i in lista: # conteo de f
            if lia <= i < lsa: # veificamos si está dentro de los intervalos actuales
                c += 1 # C va a sumar 1 si encuentra algun número de la lista dentro de los intevalos
    else: # Si SÍ es la última clase
        for i in lista:
            if lia <= i <= lsa:
                c +=1

    for i in [c, c + lastc, c / len(lista), lasth + (c/len(lista)), c / len(lista) * 100, (lia + lsa)/2]: # Iterador para agregar desde f hasta Xi
        i = rnd(i) # Redondea el valor
        nueva_lista.append(i) # Y lo agrega

    nueva_lista += [rnd(nueva_lista[2] * nueva_lista[7])] # Y agregar Xif pa la mediana
    

    lia += amplitud # se suma la amplitud
    lsa += amplitud


    
    matriz.append(nueva_lista) # Agrega la lista


# MEDIA
media_Xif = 0 
for i in matriz: # Para cada intervalo
    media_Xif = media_Xif + i[2] * i[7] # Multiplicar f * Xi

media = rnd(media_Xif / len(lista)) # Y dividimos fXi / n

for i in range(clases): # Agrega medidas de dispersión de datos
    matriz[i] += [
        rnd(abs(matriz[i][7] - media)), # |Xi  - media| (9)
        rnd(abs(matriz[i][7] - media) * matriz[i][2]), # |Xi - media| * f (10)
        rnd((matriz[i][7] - media)**2), # (Xi - media)^2 (11)
        rnd((matriz[i][7] - media)**2 * matriz[i][2]) # (Xi - media)^2 * f (12)
    ]
    


# MEDIANA
mediana_confirm = False # Variable para no buscar mediana por si F = F = Ls

search_med = len(lista) / 2 if len(lista) % 2 == 0 else (len(lista) + 1) / 2 # Buscamos el intervalo medial con n/2 o n+1 / 2 verificando su paridad
for i in matriz: # buscamos por cada intervalo
    if i[3] == search_med: # Si F es n/2
        mediana = i[1] # En caso de que encuentre uno la mediana es el Límite superior
        mediana_confirm = True # Ya encontramos la mediana entonces no necesitamos hacer más cálculos
        break # Cerramos el ciclo para ahorrar memoria y tiempo de ejecución

if not mediana_confirm: # Si aún no se encontró media con lo anterior
    lista_F = [matriz[x][3] for x in range(clases)] # Hacemos una lista con todas las F
    lista_F_mayor = [] # Creamos una lista vacia que tenga las Fs mayor a n/2
    for i in lista_F: # Para cada F
        if i > search_med: # Evaluamos cada F para ver si son mayores a n/2
            lista_F_mayor.append(i) # Agregamos ese F
    inter_mediana_F = min(lista_F_mayor) # Sacamos el mayor más cercano

    for i in matriz: # Ahora buscamos en cada intervalo
        if i[3] == inter_mediana_F: # Donde se encuentre el mayor
            i.append("ME") # Asignamos un "ME" al intervalo por si necesitamos saber lo medial que es
            index_Med = matriz.index(i) # Y buscamos de donde es ese intervalo

    datos_mediana = { # Con estos datos calculamos la mediana entonces simplificamos
        "lim_inf" : matriz[index_Med][0], 
        "nEntre2" : search_med,
        "F-1" : matriz[index_Med - 1][3],  
        "fi" :  matriz[index_Med][2],
        "amp" : amplitud
    }

    mediana = datos_mediana["lim_inf"] + ((( datos_mediana["nEntre2"] - datos_mediana["F-1"] )/ datos_mediana["fi"] ) * datos_mediana["amp"]) # Calculamos con fórmula



# MODA
lista_f = [matriz[x][2] for x in range(clases)] # Hacemos una lista de las fs
lista_f = max(lista_f) # La máxima...
for i in matriz:
    if i[2] == lista_f:
        i.append("MO") # Tiene la moda
        index_Mod = matriz.index(i) # Obtenemos índice como antes

datos_moda = {
    "lim_inf" : matriz[index_Mod][0],
    "f" : matriz[index_Mod][2],
    "f-1" : matriz[index_Mod - 1][2],
    "f+1" : matriz[index_Mod + 1][2],
    "amp" : amplitud
}

moda = datos_moda["lim_inf"] + ((datos_moda["f"] - datos_moda["f-1"] )/ (datos_moda["f"] - datos_moda["f-1"] + datos_moda["f"] - datos_moda["f+1"])) * datos_moda["amp"] # Y formula


# Desviación media

sum_desv_media = 0
for i in matriz:
    sum_desv_media += i[10]

desv_media = sum_desv_media / len(lista)

# Varianza

sum_vari = 0
for i in matriz:
    sum_vari += i[12]

vari = sum_vari / len(lista)


# Coeficiente de Variación

cv = (math.sqrt(vari) / media) * 100



# POSICIÓN

# Función percentiles
def posicion(num_p):
    global lista, amplitud
    return num_p * len(lista) / 100

def percentil(num):
    global matriz, lista_F
    pos = posicion(num)
    for i in matriz:
        if i[3] == pos:
            return i[1]
        
    lista_F_mayor = []
    for i in lista_F:
        if i > pos:
            lista_F_mayor.append(i)
        inter_per_F = min(lista_F_mayor)

    for i in matriz:
        if i[3] == inter_per_F:
            index_per = matriz.index(i)

    datos_per = {
        "lim_inf" : matriz[index_per][0],
        "posi" : pos,
        "F-1" : matriz[index_per - 1][3],
        "fi" : matriz[index_per][2],
        "amp" : amplitud
    }
    
    return datos_per["lim_inf"] + ((( datos_per["posi"] - datos_per["F-1"] ) / datos_per["fi"]) * datos_per["amp"])



# Asignación de datos a tk

class CuadroLabel(tk.Label): # Creación de clase para hacer cuadros de información
    def __init__(self, master, text, gx, gy, cs_total = False, title = False, gray = False): # Clase constructora
        super().__init__(master) # Creación del label en el master
        self.config(text=text) # Configuración del texto
        self.config(bd = 1) # Borde
        self.config(relief="solid") # Tipo de borde
        self.config(font=("Arial Black", 15)) # Tamaño de fuente
        self.config(padx = 20) # Pad X para cada intv.
        if title:
            self.config(bg = "#add8e6")
        if gray:
            self.config(bg = "#dddddd")
        if not cs_total:
            self.grid(row = gy, column = gx, sticky="nsew") # Normal grid
        else:
            self.grid(row = gy, column = gx, sticky="nsew", columnspan = cs_total) # El total


root = tk.Tk() # Creación de la raíz

canvas = tk.Canvas(root, width=1920, height=600)
canvas.grid(row = 0, column = 0)

froot = tk.Frame(canvas, width=4000, height=600)
froot.grid(row = 0, column = 0)

lista_col = ["Li", "Ls","f", "F", "h", "H", "%", "Xi", "Xif", "|Xi - media|", "|Xi - media| * f", "(Xi - media)^2", "(Xi - media)^2 * f"] # Lista de columnas

for i in lista_col: # Para cada elemento de las columnas
    CuadroLabel(froot, i, lista_col.index(i), 0, title= True) # Agregarlas

for interv in matriz:
    for val in interv:
        if interv.index(val) % 2 == 0:
            CuadroLabel(froot, val, interv.index(val), matriz.index(interv) + 1, gray= True)
        else:
            CuadroLabel(froot, val, interv.index(val), matriz.index(interv) + 1) # Por cada valor de las clases se indexan + 1

CuadroLabel(froot, matriz[0][3], 3, 1) # Correción de matrices por datos repetidos
CuadroLabel(froot, matriz[0][5], 5, 1)
CuadroLabel(froot, matriz[0][6], 6, 1, gray=True)

CuadroLabel(froot, "TOTAL", 0, len(matriz) + 2, cs_total=2, title=True) # TOTALES
CuadroLabel(froot, len(lista), 2, len(matriz) + 2, title=True) # f
CuadroLabel(froot, 
            str(round(matriz[-1][5], 0))[:1] if matriz[-1][5] == 1 else rnd(matriz[-1][5]), # Si E h = 1 entonces no muestra el 1.0
              4,len(matriz) + 2, title=True) # h
CuadroLabel(froot, 
            str(round(matriz[-1][5] * 100, 0))[:3] if matriz[-1][5] == 1 else rnd(matriz[-1][5] * 100), # Si E h * 100 = 100 entonces no muestra el 100.0
              6, len(matriz) + 2, title=True) # %
CuadroLabel(froot, media_Xif, 8, len(matriz) + 2, title=True) # Xif
CuadroLabel(froot, sum_desv_media, 10, len(matriz) + 2, title=True) # |Xi - media| f
CuadroLabel(froot, sum_vari, 12, len(matriz) + 2, title=True) # (Xi - media)^2 f

def show_data(): # Función para mostrar la información
    info_root = tk.Tk() # Nueva ventana

    tk.Label(info_root, text="Medidas básicas", font=("Arial Black",20)).grid(row = 0, column = 0) 
    tk.Label(info_root, text="DATOS = {}      K = {}     Dm = {}    DM = {}    R = {}      A = {}".format(len(lista), clases, dato_menor, dato_mayor, dato_mayor - dato_menor, amplitud),
             font=("Arial Black", 15)).grid(row = 1, column = 0)
    
    tk.Label(info_root).grid(row=2, column= 0, pady = 10) # Separadores

    tk.Label(info_root, text="Medidas de Tendencia Central", font=("Arial Black",20)).grid(row = 3, column = 0)
    tk.Label(info_root, text="MEDIA = {}     MEDIANA = {}      MODA = {}".format(media, mediana, moda),
             font=("Arial Black", 15)).grid(row = 4, column = 0)
    
    tk.Label(info_root).grid(row=5, column= 0, pady = 10)

    tk.Label(info_root, text="Medidas de Dispersión", font=("Arial Black",20)).grid(row = 6, column = 0)
    tk.Label(info_root, text="DESVIACIÓN MEDIA = {}         VARIANZA = {}    \n     DESVIACIÓN ESTÁNDAR = {}       COEFICIENTE DE VARIACIÓN = {}".format(desv_media, vari, math.sqrt(vari), cv),
             font=("Arial Black", 15)).grid(row = 7, column = 0)

    info_root.mainloop()

tk.Button(froot, text="INFORMACIÓN", command=show_data, font=("Arial Black", 15)).grid(row = len(matriz) + 3, column = 0, pady = 10) # Botón de info


def histograma(): # Generación de Histograma
    plt.hist(lista, bins = [x[0] for x in matriz] + [matriz[-1][1]], edgecolor = 'black')
    plt.plot([x[7] for x in matriz],[x[2] for x in matriz], "o-")
    for i, j in zip([x[7] for x in matriz], [x[2] for x in matriz]): 
        plt.annotate(str(j), xy=(i, j + 0.5), fontsize=15)

    plt.xticks([x[0] for x in matriz] + [matriz[-1][1]], [x[0] for x in matriz] + [matriz[-1][1]])
    plt.show()

tk.Button(froot, text="HISTOGRAMA", command=histograma, font=("Arial Black", 15)).grid(row = len(matriz) + 3, column = 1, pady = 10) # Botón de histograma


def pizza(): # Generación del diagrama de Pizza
    plt.pie([x[6] for x in matriz], labels=[x[7] for x in matriz])
    plt.show()

tk.Button(froot, text="PIZZA", command=pizza, font=("Arial Black", 15)).grid(row = len(matriz) + 3, column = 2, pady = 10) # Botón de pizza


def ojiva(): # Generación del diagrama de Ojiva
    plt.plot([x[7] for x in matriz],[x[3] for x in matriz], "o-")
    for i, j in zip([x[7] for x in matriz], [x[3] for x in matriz]):
        plt.annotate(str(j), xy=(i, j + 1), fontsize = 15)
    plt.show()

tk.Button(froot, text="OJIVA", command=ojiva, font=("Arial Black", 15)).grid(row = len(matriz) + 3, column = 3, pady = 10) # Botón de ojiva


# CALCULO DE PERCENTILES

perc_calc = tk.StringVar()

tk.Entry(froot, textvariable=perc_calc, font=("Arial", 10)).grid(row = len(matriz) + 4, column = 0, columnspan= 2)

def calculemosPercentiles():
    global perc_calc
    perc_most = int(perc_calc.get())
    
    messagebox.showinfo("Percentil P" + str(perc_most), "Posición: {}\nPercentil P{}: {}".format(posicion(perc_most), perc_most, percentil(perc_most)))

tk.Button(froot, text="PERCENTIL", command=calculemosPercentiles, font=("Arial Black", 15)).grid(row = len(matriz) + 4, column= 2)



scrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scrollbar.grid(row=10, column=0, sticky="ew")

canvas.configure(xscrollcommand=scrollbar.set)

canvas.create_window((0, 0), window=froot, anchor="nw")
canvas.configure(scrollregion=canvas.bbox("all"))

root.mainloop() # Mainloop del froot    