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
    """
    Devuelve si una matriz es cuadrada o no
    Si la matriz no es valida devuelve None
    """
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

#TODO Aqui cambiaria la i para usar el enumerate en el bucle
def multiplica_escalar(matriz, k):
    """
    Genera una nueva matriz donde todos los elementos 
    de la matriz pasada por argumento son multiplicados por k
    """
    #Si la matriz esta mal formada o esta vacía entonces no se puede multiplicar
    if dimension(matriz)=="None":
        return "None"
    new_mat=[]
    i=0 #Marcador de la fila actual
    for fila in matriz:
        new_mat.append([])#Añadimos la fila vacía a la que se le van a añadir los valores
        for elem in fila:
            new_mat[i].append(elem*k) #Añadimos cada valor
        i=i+1 #actualizar marcador
    return new_mat


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

from collections import Counter
#TODO preguntar porque 8 returns son demasiados y como seria mejorable puesto que lo que hace es tener cada condicion de manera independiente
def validar(grafo):
    """
    Validara un grafo siempre que se cumplan las condiciones
    """
    claves = grafo.keys()
    if len(claves) != 2 or "nodos" not in grafo or "aristas" not in grafo:
        return False

    if len(grafo["nodos"]) == 0:
        return False
    #Comprobar que en grafo["nodos"] no haya mas de 1 vez el mismo nodo
    #Si el valor más comun es 1 se sabe que todos los demas son 1
    _, repeat=Counter(grafo["nodos"]).most_common(1)[0]
    if repeat>1:
        print("Nodo repetido en grafo[nodos]")
        return False
    #Todos los nodo en grafo["nodos"]debe estar en g["aristas"]
    for nodo in grafo["nodos"]:
        if nodo not in grafo["aristas"]:#Si un nodo no aparece como nodo origen
            print("el nodo %s no aparece en grafo[aristas]",nodo)
            return False

    for nodo_o, nodos_d in grafo["aristas"].items():
        if nodo_o not in grafo["nodos"]:#Si el nodo origen no es valido
            print("Nodo origen no existe en los nodos proporcionados")
            return False
        _, repeat=Counter(nodos_d).most_common(1)[0]
        if repeat>1:
            print("Nodo repetido en nodos destino de %s",nodo_o)
            return False
        for nodo_d in nodos_d:
            if nodo_d not in grafo["nodos"]:#Si algun nodo destino no es valido
                print("Nodo destino no existe en los nodos proporcionados")
                return False
    return True


def grado_entrada(grafo, nodo):
    """
    Determina el grado de entrada del nodo en el grafo
    """
    if not validar(grafo)or nodo not in grafo["nodos"]:
        return -1
    aux=0
    for _,destiny in grafo["aristas"].items():
        if nodo in destiny:
            aux=aux+1
    return aux


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
    if not validar(grafo) or nodo not in grafo["nodos"]:
        return "None"
    while len(pending)>0:
        current=pending[0]
        pending.pop()
        for elem in grafo["aristas"][current]:
            if elem not in visit :
                pending.append(elem)
                visit.append(elem)
                dist[elem]=dist[current]+1
    for nodo_aux in grafo["nodos"]:
        if nodo_aux not in dist:
            dist[nodo_aux]=-1
    return dist