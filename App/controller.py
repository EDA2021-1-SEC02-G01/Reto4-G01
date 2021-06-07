"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

from os import name
from DISClib.ADT import list as lt
import config as cf
import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos

def loadData(analyzer, landingFile, connectionsFile, countriesFile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    landingFile = cf.data_dir + landingFile
    connectionsFile = cf.data_dir + connectionsFile
    countriesFile = cf.data_dir + countriesFile
    landing_File = csv.DictReader(open(landingFile,
                                       encoding="utf-8"),
                                  delimiter=",")
    connections_File = csv.DictReader(open(connectionsFile,
                                           encoding="utf-8-sig"),
                                      delimiter=",")
    countries_File = csv.DictReader(open(countriesFile,
                                         encoding="utf-8"),
                                    delimiter=",")

    # Creacion de listas vacias para agregar cada uno
    #  de los elementos de los archivos
    # y asi recorrerlos mas facilmente.
    listaLandingPoints = lt.newList('ARRAY_LIST')
    listaConnections = lt.newList('ARRAY_LIST')
    listaCountries = lt.newList('ARRAY_LIST')

    for punto in landing_File:
        model.addPosition(analyzer, punto)
        model.addLandingPointInfo(analyzer, punto)
        lt.addLast(listaLandingPoints, punto)

    for connection in connections_File:
        lt.addLast(listaConnections, connection)

    for pais in countries_File:
        lt.addLast(listaCountries, pais)
        model.addCountry(analyzer, pais)

    for point in lt.iterator(listaLandingPoints):
        nombre = point['name'].split(", ")
        if len(nombre) < 2:
            pais = 'Micronesia'
        else:
            pais = nombre[1]
        for country in lt.iterator(listaCountries):
            if country['CountryName'] == pais:
                capital = country['CapitalName'] + "-" + pais
                model.addPoint(analyzer, capital)
                datosCapital = country
                break

        lstPuntoActual = None
        for connection in lt.iterator(listaConnections):
            if connection['origin'] == point['landing_point_id']:
                lstPuntoActual = model.addLandingPoint(analyzer,
                                                       point,
                                                       connection,
                                                       lstPuntoActual,
                                                       datosCapital)
        model.addConnectionsPoint(analyzer, lstPuntoActual)
    for country in lt.iterator(listaCountries):
        model.addCapitals(analyzer, country)

# Funciones de ordenamiento


# Funciones de consulta sobre el catálogo

def totalPoints(analyzer):
    """
    Total de landing points
    """
    return model.totalPoints(analyzer)


def totalConnections(analyzer):
    """
    Total de conexiones submarinas
    """
    return model.totalConnections(analyzer)


def totalCountries(analyzer):
    """
    Total de paises cargados
    """
    return model.totalCountries(analyzer)


def firstVertex(analyzer):
    """
    Retorna el primer vértice cargado
    """
    return model.firstVertex(analyzer)


def firstCountry(analyzer):
    """
    Retorna la informacion del primer pais cargado
    """
    return model.firstCountry(analyzer)


def Requerimiento1(analyzer, landing_point1, landing_point2):
    """
    Retorna el número de componentes fuertemente conectados
    del grafo
    """
    return model.Requerimiento1(analyzer, landing_point1, landing_point2)


def Requerimiento2(analyzer):
    """
    Retorna una lista con los landing Points que sirven como punto de
    interconexion a más cables en la red
    """
    return model.Requerimiento2(analyzer)


def Requerimiento3(analyzer, paisA, paisB):
    """
    Retorna la ruta minima entre dos capitales
    """
    return model.Requerimiento3(analyzer, paisA, paisB)


def Requerimiento4(analyzer):
    """
    Retorna a  redde  expansión  mínima  en  cuanto  a distancia
    que pueda darle cobertura a la mayor cantidad de landing point
    de la red
    """
    return model.Requerimiento4(analyzer)


def Requerimiento5(analyzer, landing_point):
    """
    Retorna el numero de paises afectados en caso de que falle
    el landing point, ademas de una lista con los paises
    """
    return model.Requerimiento5(analyzer, landing_point)
