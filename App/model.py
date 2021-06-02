﻿"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import haversine as hs
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'landing_points': None,
                    'connections': None,
                    'countries': None,
                    }

        analyzer['landing_points'] = mp.newMap(numelements=1300,
                                               maptype='PROBING',
                                               comparefunction=cmpLandingIds)

        analyzer['coordinates'] = mp.newMap(numelements=1300,
                                            maptype='PROBING',
                                            comparefunction=cmpLandingIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=3300,
                                              comparefunction=cmpLandingIds)

        analyzer['countries'] = mp.newMap(numelements=300,
                                          maptype='PROBING')
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Construccion de modelos

def addLandingPoint(analyzer, point, connection, lstPuntoActual, datosCapital):
    if lstPuntoActual is None:
        lstPuntoActual = lt.newList("ARRAY_LIST")
    puntoOrigen = connection['origin'] + '-' + connection['cable_name']
    puntoDestino = connection['destination'] + '-' + connection['cable_name']
    addPoint(analyzer, puntoOrigen)
    addPoint(analyzer, puntoDestino)
    if connection['cable_length'] != 'n.a.':
        distancia = connection['cable_length'].replace(",", "")
        distancia = float(distancia.split()[0])
    else:
        locOrigen = (float(point['latitude']), float(point['longitude']))
        locDestino = mp.get(analyzer['coordinates'],
                            connection['destination'])['value']
        distancia = round(hs.haversine(locOrigen, locDestino), 2)
    addConnection(analyzer, puntoOrigen, puntoDestino, distancia)
    addConnection(analyzer, puntoDestino, puntoOrigen, distancia)
    loc1 = (float(point["latitude"]),
            float(point["longitude"]))
    loc2 = (float(datosCapital["CapitalLatitude"]),
            float(datosCapital["CapitalLongitude"]))
    distanciaHaversine = round(hs.haversine(loc1, loc2), 2)
    capital = datosCapital['CapitalName'] + "-" + datosCapital['CountryName']
    addConnection(analyzer, puntoOrigen, capital, distanciaHaversine)
    addConnection(analyzer, capital, puntoOrigen, distanciaHaversine)
    lt.addLast(lstPuntoActual, puntoOrigen)
    return lstPuntoActual


def addConnectionsPoint(analyzer, lstPuntoActual):
    for punto1 in lt.iterator(lstPuntoActual):
        for punto2 in lt.iterator(lstPuntoActual):
            if punto1 != punto2:
                addConnection(analyzer, punto1, punto2, 0.1)
    return analyzer


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos landing_points
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer


def addPoint(analyzer, pointid):
    """
    Adiciona un landing_point-cable como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], pointid):
            gr.insertVertex(analyzer['connections'], pointid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addPoint')


def addCountry(analyzer, country):
    mp.put(analyzer['countries'],
           country['CountryName'],
           country)
    return analyzer


def addCapitals(analyzer, country):
    """
    capital = country['CapitalName'] + "-" + country['CountryName']
    addPoint(analyzer['connections'], capital)
    grado = gr.degree(analyzer['connections'], capital)
    print(grado)
    if grado == 0:
        listaPoint
    """
# Funciones para agregar informacion al catalogo


def addPosition(analyzer, punto):
    loc = (float(punto["latitude"]), float(punto["longitude"]))
    mp.put(analyzer["coordinates"], punto["landing_point_id"], loc)
    return analyzer


def addLandingPointInfo(analyzer, punto):
    mp.put(analyzer["landing_points"], punto["landing_point_id"], punto)
    return analyzer


# Funciones para creacion de datos


# Funciones de consulta


def totalPoints(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def totalCountries(analyzer):
    """
    Total de paises cargados
    """
    return mp.size(analyzer['countries'])


def firstVertex(analyzer):
    """
    Retorna la informacion del primer vértice cargado
    """
    listaVertices = mp.keySet(analyzer['landing_points'])
    primerPoint = lt.firstElement(listaVertices)
    infoPoint = mp.get(analyzer['landing_points'], primerPoint)['value']
    return infoPoint


def firstCountry(analyzer):
    """
    Retorna la informacion del primer pais cargado
    """
    listaPaises = mp.keySet(analyzer['countries'])
    ultimoPais = lt.lastElement(listaPaises)
    infoPais = mp.get(analyzer['countries'], ultimoPais)['value']
    return infoPais


def Requerimiento1(analyzer, landing_point1, landing_point2):
    """
    Retorna . . . 
    """
    clusters = scc.KosarajuSCC(analyzer['connections'])
    numClusters = scc.connectedComponents(clusters)
    mismoCluster = scc.stronglyConnected()
    return numClusters


# ==============================
# Funciones de Comparacion
# ==============================

def cmpLandingIds(landingPoint, keyValueLP):
    """
    Compara dos landing points
    """
    pointId = keyValueLP['key']
    if (landingPoint == pointId):
        return 0
    elif (landingPoint > pointId):
        return 1
    else:
        return -1


def compareconnections(connection1, connection2):
    """
    Compara dos conexiones de cable submarino
    """
    if (connection1 == connection2):
        return 0
    elif (connection1 > connection2):
        return 1
    else:
        return -1


# Funciones de ordenamiento

# ==============================
# Funciones Helper
# ==============================
