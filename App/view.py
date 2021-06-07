"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import threading
import tracemalloc
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


landingFile = 'landing_points.csv'
connectionsFile = 'connections.csv'
countriesFile = 'countries.csv'
initialPoints = None


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Cargar Datos")
    print("3- Requerimiento 1")
    print("4- Requerimiento 2")
    print("5- Requerimiento 3")
    print("6- Requerimiento 4")
    print("7- Requerimiento 5")
    print("0- Salir")


def optionTwo(cont):
    # toma de tiempo
    start_time = controller.getTime()
    controller.loadData(cont, landingFile, connectionsFile, countriesFile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalPoints(cont)
    numCountries = controller.totalCountries(cont)
    firstVertex = controller.firstVertex(cont)
    lastCountry = controller.firstCountry(cont)
    print("="*5 + " DATOS CARGADOS " + "="*5)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('Numero de paises:' + str(numCountries))
    print('Primer landing point cargado: ' +
          str(firstVertex['landing_point_id']))
    print('Nombre landing point: ' + firstVertex['name'])
    print('Latitud: ' + str(firstVertex['latitude']))
    print('Longitud: ' + str(firstVertex['longitude']))
    print('Ultimo pais cargado:', lastCountry['CountryName'])
    print('Población de ' + lastCountry['CountryName'] + ": " +
          lastCountry['Population'])
    print('Usuarios de internet de ' + lastCountry['CountryName'] + ": " +
          str(lastCountry['Internet users']))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    # toma de tiempo 
    stop_time = controller.getTime()
    delta_time = round(stop_time - start_time, 2)
    # toma de tiempo
    print(f"Tiempo de ejecucion: {delta_time}")
    print('')


def optionThree(cont):
    
    landing_point1 = input("Ingrese el nombre del landing point 1: ")
    landing_point2 = input("Ingrese el nombre del landing point 2: ")
    # toma de tiempo
    start_time = controller.getTime()
    numClusters, mismoCluster = controller.Requerimiento1(cont,
                                                          landing_point1,
                                                          landing_point2)
    print("="*5 + " REQUERIMIENTO 1 " + "="*5)
    print("Total de clústeres: " + str(numClusters))
    if mismoCluster:
        print(f"{landing_point1} y {landing_point2} estan fuertemente" +
              " conectados")
    elif mismoCluster == -1:
        print("Al menos uno de los vertices ingresados no existen en el grafo")
    else:
        print(f"{landing_point1} y {landing_point2} NO estan fuertemente" +
              " conectados")
    # toma de tiempo 
    stop_time = controller.getTime()
    delta_time = round(stop_time - start_time, 2)
    # toma de tiempo
    print(f"Tiempo de ejecucion: {delta_time}")
    print()


def optionFour(cont):
    # toma de tiempo
    start_time = controller.getTime()
    lstLP = controller.Requerimiento2(cont)
    print("="*5 + " REQUERIMIENTO 2 " + "="*5)
    for punto, totalCables in lt.iterator(lstLP):
        nombre = punto['name'].split(", ")[0]
        pais = punto['name'].split(", ")[1] 
        identificador = punto['landing_point_id']
        print(f"El punto {nombre} del pais {pais} con identificador" +
              f" {identificador} sirve de interconexion a {totalCables} cables.")
    # toma de tiempo 
    stop_time = controller.getTime()
    delta_time = round(stop_time - start_time, 2)
    # toma de tiempo
    print(f"Tiempo de ejecucion: {delta_time}")
    print()


def optionFive(cont):

    paisA = input("Ingrese el pais de origen: ")
    paisB = input("Ingrese el pais destino: ")
    # toma de tiempo
    start_time = controller.getTime()
    ruta, distancia, distHaversine = controller.Requerimiento3(cont, paisA, paisB)
    print("="*5 + " REQUERIMIENTO 3 " + "="*5)
    if ruta == -1:
        print(f"El país {paisA} no se encontró")
    elif ruta == -2:
        print(f"El país {paisB} no se encontró")
    else:
        print("--RUTA--")
        i = 1
        for cableInfo in lt.iterator(ruta):
            vertexA = cableInfo['vertexA']
            vertexB = cableInfo['vertexB']
            peso = cableInfo['weight']
            print(f"{i}. Desde {vertexA} hasta {vertexB}: {peso} Km")
            i += 1
        print()
        print(f"DISTANCIA TOTAL DE LA RUTA: {distancia} Km")
        print(f"DISTANCIA GEOGRÁFICA ENTRE LAS CAPITALES: {distHaversine} Km")
    # toma de tiempo 
    stop_time = controller.getTime()
    delta_time = round(stop_time - start_time, 2)
    # toma de tiempo
    print(f"Tiempo de ejecucion: {delta_time}")
    print()


def optionSix(cont):
    # toma de tiempo
    start_time = controller.getTime()
    numNodos, pesoMst = controller.Requerimiento4(cont)
    print("="*5 + " REQUERIMIENTO 5 " + "="*5)
    print(f"El numero de nodos conectados a la red de expansión mínima es: {numNodos}")
    print(f"El costo total de la red de expansión mínima es de: {pesoMst} Km")
    # toma de tiempo 
    stop_time = controller.getTime()
    delta_time = round(stop_time - start_time, 2)
    # toma de tiempo
    print(f"Tiempo de ejecucion: {delta_time}")
    print()


def optionSeven(cont):
    landing_point = input("Ingrese el nombre del landing point: ")
    # toma de tiempo
    start_time = controller.getTime()
    req5 = controller.Requerimiento5(cont, landing_point)
    print("="*5 + " REQUERIMIENTO 5 " + "="*5)
    numPaises, listaPaises = req5
    print(f"El numero de paises afectados es: {numPaises}")
    for pais in lt.iterator(listaPaises):
        nombre = pais[0]
        distancia = pais[1]
        print(f"{nombre}: {distancia} Km")
    # toma de tiempo 
    stop_time = controller.getTime()
    delta_time = round(stop_time - start_time, 2)
    # toma de tiempo
    print(f"Tiempo de ejecucion: {delta_time}")
    print()

catalog = None


"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("Cargando información de los archivos ....")
            cont = controller.init()
        elif int(inputs[0]) == 2:
            optionTwo(cont)
        elif int(inputs[0]) == 3:
            optionThree(cont)
        elif int(inputs[0]) == 4:
            optionFour(cont)
        elif int(inputs[0]) == 5:
            optionFive(cont)
        elif int(inputs[0]) == 6:
            optionSix(cont)
        elif int(inputs[0]) == 7:
            optionSeven(cont)
        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
