"""
TODO: rellenar

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


# Ejercicio 1
a=[[1, 0, 2, 5],[0, 3, 3,5],[1, 2, 2, 5]]
b=[[1, 0, 1],[0, 3, 2],[1, 2, 2]]
c=[[1, 2, 1],[0, 3, 2],[1, 2, 2]]
d=[[1, 0, 1],[0, 3, 2],[1, 7, 2]]
e=[]
f=[[1, 0, 2, 5],[0, 3, 3],[1, 2, 2, 5]]
def dimension(matriz):
    #Comprobamos matriz vacía
    if len(matriz)<=0:
        return "None"
    #Guardamos valor de columnas
    col=len(matriz[0])
    for fila in range(len(matriz)):
        if len(matriz[fila])!=col :#Si hay columnas de distinto tamaño matriz mal formada
            return "None"
    #Si la matriz esta bien formada devolvemos la tupla correspondiente
    dim=(len(matriz),col)
    return dim


def es_cuadrada(matriz):
    if dimension(matriz)=="None":#Si la matriz esta malformada o es vacía entonces no es cuadrada
        return False
    return len(matriz)==len(matriz[0])
    
def es_simetrica(matriz):
    if not es_cuadrada(matriz): #Si una matriz no es cuadrada no puede ser simétrica
        return False 
    #matriz[i][j]=matriz[j][i]
    for fila in range(len(matriz)):
        for col in range(fila):#Recorremos el triángulo inferior a la diagonal principal ya que si hicieramos for col in range(len(matriz[0])) estaríamos haciendo las comprobaciones dos veces
            if(matriz[fila][col]!=matriz[col][fila]):
                return False
    return True


def multiplica_escalar(matriz, k):
    if dimension(matriz)=="None":#Si la matriz esta mal formada o esta vacía entonces no se puede multiplicar
        return "None"
    newMat=[]
    i=0 #Marcador de la fila actual
    for fila in matriz:
        newMat.append([])#Añadimos la fila vacía a la que se le van a añadir los valores
        for n in fila:
            newMat[i].append(n*k) #Añadimos cada valor
        i=i+1 #actualizar marcador
    return newMat


def suma(matriz1, matriz2):
    if dimension(matriz1)=="None" or dimension(matriz1)!=dimension(matriz2):
        return "None"
    newMat=[]
    i=0#Marcador de la fila actual
    for fila in range(len(matriz1)):
        newMat.append([])#Añadimos la fila vacía a la que se le van a añadir los valores
        for col in range(len(matriz1[fila])):
            newMat[i].append(matriz1[fila][col]+matriz2[fila][col])#Añadimos cada valor
        i=i+1
    return newMat#actualizar marcador

# Ejercicio 2
g = {"nodos": ["a", "b", "c", "d"],
     "aristas": {"a": ["a", "b", "c"],
                 "b": ["a", "c"],
                 "c": ["c"],
                 "d": ["c"]
                 }
     }


def validar(grafo):
    claves = grafo.keys()
    if (len(claves) != 2 or "nodos" not in grafo or "aristas" not in grafo):
        return False

    if (len(grafo["nodos"]) == 0):
        return False
    #Preguntar si podemos usar la biblioteca collections
    # TODO Falta condicion de NO nodos repitidos

    for nodo in g["nodos"]:
        if(nodo not in g["aristas"]):#Si un nodo no aparece como nodo destino
            return False

    for nodoO, nodosD in g["aristas"]:
        if nodoO not in g["nodos"]:#Si el nodo origen no es valido
            return False
        for nodoD in nodosD:
            if(nodoD not in g["nodos"]):#Si algun nodo destino no es valido
                return False
    return True

def grado_entrada(grafo, nodo):
    if(not validar(grafo)or nodo not in grafo["nodos"]):
        return -1
    aux=0
    for o,d in g["aristas"].items():
        if nodo in d:
            aux=aux+1 
    return aux


def distancia(grafo, nodo):
    ...
   
