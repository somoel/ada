import math
import matplotlib.pyplot as plt
import tkinter as tk

# INGRESO DE DATOS
saved_value = input("Ingrese la lista sin saltos de línea: ")
who_quit = input("Qué desea reemplazar por comas (a parte de espacios)? : ")
saved_value = saved_value.replace(who_quit, ",")
saved_value = saved_value.replace(" ", "")

# ASIGNACIÓN A LISTA
lista = [float(x) for x in saved_value.split(",")]

n_clases = int(input("Asignar N clases (si no hay: 0): "))
if n_clases == 0:
    clases = 1 +  (3.322 * (math.log(len(lista), 10))) # CALCULO DE CLASES STURGES
    clases = math.ceil(clases) if int(clases) % 2 == 0 else int(clases) # APROXIMACIÓN A IMPAR
else:
    clases = n_clases


# CALCULO DE DATO MAYOR Y MENOR
dato_menor = min(lista)
dato_mayor = max(lista)
    

amplitud = (dato_mayor - dato_menor) / clases # La amplitud aproximada hacia arriba
amplitud = math.ceil(amplitud) if all(isinstance(x, int) or (isinstance(x, float) and x.is_integer()) for x in lista) else amplitud


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
    nueva_lista += [lia, lsa] # Primero se agregan los límites 

    lastc += c # Se suma el anterior resultado de f para la acumulativa
    lasth += (c/len(lista)) # Igual que con h
    c = 0 # Y después de guardar la F se reinicia para contar desde cero f
    if i < clases - 1:
        for i in lista: # conteo de f
            if lia <= i < lsa: # veificamos si está dentro de los intervalos actuales
                c += 1 # C va a sumar 1 si encuentra algun número de la lista dentro de los intevalos
    else:
        for i in lista:
            if lia <= i <= lsa:
                c +=1

    nueva_lista += [c, c + lastc, c / len(lista), lasth + (c/len(lista)), c / len(lista) * 100, (lia + lsa)/2] # Se agregan: f, F, h, H, %, Xi

    nueva_lista += [nueva_lista[2] * nueva_lista[7]] # Y agregar Xif pa la mediana
    

    lia += amplitud # se suma la amplitud
    lsa += amplitud


    
    matriz.append(nueva_lista) # Agrega la lista


# MEDIA
media_Xif = 0 
for i in matriz: # Para cada intervalo
    media_Xif = media_Xif + i[2] * i[7] # Multiplicar f * Xi

media = media_Xif / len(lista) # Y dividimos fXi / n

for i in range(clases): # Agrega medidas de dispersión de datos
    matriz[i] += [
        abs(matriz[i][7] - media), # |Xi  - media| (9)
        abs(matriz[i][7] - media) * matriz[i][2], # |Xi - media| * f (10)
        (matriz[i][7] - media)**2, # (Xi - media)^2 (11)
        (matriz[i][7] - media)**2 * matriz[i][2] # (Xi - media)^2 * f (12)
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



# Asignación de datos a tk

class CuadroLabel(tk.Label): # Creación de clase para hacer cuadros de información
    def __init__(self, master, text, gx, gy, cs_total = False): # Clase constructora
        super().__init__(master) # Creación del label en el master
        self.config(text=text) # Configuración del texto
        self.config(bd = 1) # Borde
        self.config(relief="solid") # Tipo de borde
        self.config(font=("Arial Black", 15)) # Tamaño de fuente
        if not cs_total:
            self.grid(row = gy, column = gx, sticky="nsew") # Normal grid
        else:
            self.grid(row = gy, column = gx, sticky="nsew", columnspan = cs_total) # El total


root = tk.Tk() # Creación de la raíz
lista_col = ["Li", "Ls","f", "F", "h", "H", "%", "Xi", "Xif", "|Xi - media|", "|Xi - media| * f", "(Xi - media)^2", "(Xi - media)^2 * f"] # Lista de columnas

for i in lista_col: # Para cada elemento de las columnas
    CuadroLabel(root, i, lista_col.index(i), 0) # Agregarlas

for interv in matriz:
    for val in interv:
        CuadroLabel(root, val, interv.index(val), matriz.index(interv) + 1) # Por cada valor de las clases se indexan + 1

CuadroLabel(root, matriz[0][3], 3, 1) # Correción de matrices por datos repetidos
CuadroLabel(root, matriz[0][5], 5, 1)
CuadroLabel(root, matriz[0][6], 6, 1)

CuadroLabel(root, "TOTAL", 0, len(matriz) + 2, cs_total=2) # TOTALES
CuadroLabel(root, len(lista), 2, len(matriz) + 2) # f
CuadroLabel(root, matriz[-1][5], 4,len(matriz) + 2) # h
CuadroLabel(root, matriz[-1][5] * 100, 6, len(matriz) + 2) # %
CuadroLabel(root, media_Xif, 8, len(matriz) + 2) # Xif
CuadroLabel(root, sum_desv_media, 10, len(matriz) + 2) # |Xi - media| f
CuadroLabel(root, sum_vari, 12, len(matriz) + 2) # (Xi - media)^2 f

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
    tk.Label(info_root, text="DESVIACIÓN MEDIA = {}         VARIANZA = {}         DESVIACIÓN ESTÁNDAR = {}       COEFICIENTE DE VARIACIÓN = {}".format(desv_media, vari, math.sqrt(vari), cv),
             font=("Arial Black", 15)).grid(row = 7, column = 0)

    info_root.mainloop()

tk.Button(root, text="INFORMACIÓN", command=show_data, font=("Arial Black", 15)).grid(row = len(matriz) + 3, column = 0, pady = 10) # Botón de info


def histograma(): # Generación de Histograma
    plt.hist(lista, bins = [x[0] for x in matriz], edgecolor = 'black') 
    plt.show()

tk.Button(root, text="HISTOGRAMA", command=histograma, font=("Arial Black", 15)).grid(row = len(matriz) + 3, column = 1, pady = 10) # Botón de histograma




root.mainloop() # Mainloop del root