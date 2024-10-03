"""
Asignatura: GIW
Práctica 1
Grupo: 08
Autores: Carlos Rondon Arevalo
         Pablo Padial Iniesta
         David Llanes Martín
         Agustín Moure Rodríguez

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""
from collections import Counter

def dimension(matriz):
    """
    Funcion que se encarga de obtener la dimension de una matriz
    si la matriz no es valida devuelve "None"
    en caso de que si sea valida devuelve sus dimensiones en forma de tupla
    
    """

    #Comprobamos matriz vacía
    if len(matriz)<=0:
        return None
    #Guardamos valor de columnas
    col=len(matriz[0])
    for fila in matriz:
        if len(fila)!=col :#Si hay columnas de distinto tamaño matriz mal formada
            return None
    #Si la matriz esta bien formada devolvemos la tupla correspondiente
    dim=(len(matriz),col)
    return dim

def es_cuadrada(matriz):
    """
    Devuelve si una matriz es cuadrada o no
    Si la matriz no es valida devuelve None
    """
    if dimension(matriz) is None: #Si la matriz esta malformada o es vacía entonces no es cuadrada
        return False
    return len(matriz)==len(matriz[0])

def es_simetrica(matriz):
    """
    Devuelve si la matriz es simetrica
    """
    if not es_cuadrada(matriz): #Si una matriz no es cuadrada no puede ser simétrica
        return False
    #matriz[i][j]=matriz[j][i]
    for i,fila in enumerate(matriz):
            #Recorremos el triángulo inferior a la diagonal principal
            # ya que si hicieramos for col in range(len(matriz[0]))
            #  estaríamos haciendo las comprobaciones dos veces
        for j in range(i):
            if fila[j]!=matriz[j][i] :
                return False
    return True

def multiplica_escalar(matriz, k):
    """
    Genera una nueva matriz donde todos los elementos 
    de la matriz pasada por argumento son multiplicados por k
    """
    #Si la matriz esta mal formada o esta vacía entonces no se puede multiplicar
    if dimension(matriz) is None:
        return None
    new_mat=[]

    for i,fila in enumerate(matriz):
        new_mat.append([])#Añadimos la fila vacía a la que se le van a añadir los valores
        for elem in fila:
            new_mat[i].append(elem*k) #Añadimos cada valor
    return new_mat

def suma(matriz1, matriz2):
    """
    Genera una nueva matriz que se corresponde
    a la suma de las dos dadas, si no es posible
    devuelve None
    """
    if dimension(matriz1) is None or dimension(matriz1)!=dimension(matriz2):
        return None
    new_mat=[]

    for i,fila in enumerate(matriz1):
        new_mat.append([])#Añadimos la fila vacía a la que se le van a añadir los valores
        for col,elem in enumerate(fila):
            new_mat[i].append(elem+matriz2[i][col])#Añadimos cada valor
    return new_mat

def validar_nodos(grafo):
    """
    Comprueba que del grafo la clave "nodos" es correcta
    """

    if len(grafo["nodos"]) == 0:
        return False
    #Comprobar que en grafo["nodos"] no haya mas de 1 vez el mismo nodo
    #Si el valor más comun es 1 se sabe que todos los demas son 1
    _, repeat=Counter(grafo["nodos"]).most_common(1)[0]
    if repeat>1:
        return False
    return True

def validar_aristas(grafo):
    """
    Comprueba que la clave "aristas" es correcta
    """
    #Todos los nodo en grafo["nodos"]debe estar en g["aristas"]
    for nodo in grafo["nodos"]:
        if nodo not in grafo["aristas"]:#Si un nodo no aparece como nodo origen
            return False

    for nodo_o, nodos_d in grafo["aristas"].items():
        if nodo_o not in grafo["nodos"]:#Si el nodo origen no es valido
            return False
        _, repeat=Counter(nodos_d).most_common(1)[0]
        if repeat>1:
            return False
        for nodo_d in nodos_d:
            if nodo_d not in grafo["nodos"]:#Si algun nodo destino no es valido
                return False
    return True

def validar(grafo):
    """
    Validara un grafo siempre que se cumplan las condiciones
    """
    claves = grafo.keys()
    #Comprueba las claves
    if len(claves) != 2 or "nodos" not in grafo or "aristas" not in grafo:
        return False
    #Comprueba que tanto nodos como aristas son validos
    return validar_nodos(grafo) and validar_aristas(grafo)


def grado_entrada(grafo, nodo):
    """
    Determina el grado de entrada del nodo en el grafo
    """
    #Si el grafo no es valido o el nodo no existe en el grafo
    if not validar(grafo)or nodo not in grafo["nodos"]:
        return -1
    grado=0
    for _,destiny in grafo["aristas"].items():
        if nodo in destiny:
            grado+=1
    return grado


def distancia(grafo, nodo):
    """
    Determina la distancia a todos los nodos desde el nodo
    """
    visit=[]
    dist={}
    pending=[]
    pending.append(nodo)
    dist[nodo]=0
    visit.append(nodo)
    #Comprueba que el nodo esta dentro del grafo que esta bien formado
    if not validar(grafo) or nodo not in grafo["nodos"]:
        return None
    #Recorre el grafo comprobando la distancia entre los nodos
    while len(pending)>0:
        current=pending[0]
        pending.pop()
        for elem in grafo["aristas"][current]:
            if elem not in visit :
                pending.append(elem)
                visit.append(elem)
                dist[elem]=dist[current]+1
    #Comprueba si existe algun nodo inalcanzable
    for nodo_aux in grafo["nodos"]:
        if nodo_aux not in dist:
            dist[nodo_aux]=-1
    return dist
