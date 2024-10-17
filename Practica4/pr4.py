"""
TODO: rellenar

Asignatura: GIW
Práctica 4
Grupo: 08
Autores: Autores: Carlos Rondon Arevalo
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


import sqlite3
import csv
from datetime import datetime
def convertir_fecha(fecha):
    '''
    Convierte la fecha en ISO-8601
    '''
    #Convertimos la fecha a date
    aux = datetime.strptime(fecha, '%d/%m/%Y %H:%M')
    #Convertimos la fecha al formato yyyy-mm-dd
    date = aux.strftime('%Y-%m-%d %H:%M')
    return date

def crear_bd(db_filename):
    '''
    crea la base de datos con las dos tablas
    '''
    conn = sqlite3.connect(db_filename)
    conn.execute("DROP TABLE IF EXISTS datos_generales")
    conn.execute('''CREATE TABLE datos_generales
                 (ticker TEXT PRIMARY KEY, nombre TEXT, indice TEXT, pais TEXT)''')
    conn.execute("DROP TABLE IF EXISTS semanales_IBEX35")
    conn.execute('''CREATE TABLE semanales_IBEX35 ticker TEXT, fecha TEXT, precio REAL,
                  FOREIGN KEY (ticker) REFERENCES datos_generales(ticker))''')
    conn.commit()
    conn.close()



def cargar_bd(db_filename, tab_datos, tab_ibex35):
    '''
    Carga los datos en la base de datos
    '''
    with open(tab_datos, 'r', newline='', encoding='utf8') as fich:
        datos_generales = csv.reader(fich, delimiter=';')
        lista_datos_generales = list(datos_generales)
    with open(tab_ibex35, 'r', newline='', encoding='utf8') as fich:
        datos_ibex = csv.reader(fich, delimiter=';')
        lista_datos_ibex = list(datos_ibex)
    conn = sqlite3.connect(db_filename)
    tabla_ibex = lista_datos_ibex[1::]
    for fila in tabla_ibex:
        fecha_original = fila[1]
        new_date = convertir_fecha(fecha_original)
        fila[1] = new_date

    conn.executemany('''INSERT INTO datos_generales(ticker,nombre,indice,pais)
                      VALUES (?,?,?,?)''',lista_datos_generales[1:])
    conn.executemany('''INSERT INTO semanales_IBEX35 (ticker, fecha, precio)
                      VALUES (?, ?, ?)''',tabla_ibex)
    conn.commit()
    conn.close()



def consulta1(db_filename, indice):
    '''
    devuelve ticker y nombre con un indice determinado
    '''
    conn=sqlite3.connect(db_filename)
    cur=conn.execute('''SELECT ticker, nombre
                        FROM datos_generales
                        WHERE indice = ? 
                        ORDER BY ticker ASC''',[indice])
    return cur.fetchall()

def consulta2(db_filename):
    '''
    Devuelve ticker, nombre, precio max
    '''
    conn=sqlite3.connect(db_filename)
    cur=conn.execute('''SELECT G.ticker, G.nombre, MAX(S.precio)
                        FROM datos_generales G JOIN semanales_IBEX35 S
                        ON G.ticker=S.ticker
                        GROUP BY G.ticker
                        ORDER BY G.nombre ASC''')
    return cur.fetchall()

def consulta3(db_filename, limite):
    '''
    Devuelve el ticker, el nombre,
    el precio promedio y la diferencia entre el precio maximo y minimo
    siempre y cuando el precio medio > limite
    '''
    conn=sqlite3.connect(db_filename)
    cur=conn.execute('''SELECT G.ticker, G.nombre, AVG(S.precio) AS promedio,
                        MAX(S.precio)-MIN(S.precio) AS diff
                        FROM datos_generales G JOIN semanales_IBEX35 S ON G.ticker=S.ticker
                        GROUP BY G.ticker
                        HAVING promedio > ?
                        ORDER BY promedio DESC
                     ''',[limite])
    return cur.fetchall()

def consulta4(db_filename, ticker):
    '''
    Devuelve ticker, fecha sin hora,
    y el precio ordenado de manera descendente teniendo en cuenta la fecha
    '''
    conn=sqlite3.connect(db_filename)
    cur=conn.execute('''SELECT ticker,strftime('%Y-%m-%d', fecha) AS dia, precio
                        FROM semanales_IBEX35 
                        WHERE ticker=?
                        ORDER BY dia DESC
                     ''',[ticker])
    return cur.fetchall()
