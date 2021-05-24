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
                                               comparefunction=compareLandingIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=3300,
                                              comparefunction=compareLandingIds)
        
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
        distancia = float(connection['cable_length'].replace(",","").split()[0])
    else:
        locOrigen = (float(point['latitude']), float(point['longitude']))
        locDestino = mp.get(analyzer['landing_points'], connection['destination'])['value']
        distancia = round(hs.haversine(locOrigen,locDestino), 2)
    addConnection(analyzer, puntoOrigen, puntoDestino, distancia)
    loc1 = (float(point["latitude"]), float(point["longitude"]))
    loc2 = (float(datosCapital["CapitalLatitude"]), float(datosCapital["CapitalLongitude"]))
    distanciaHaversine = round(hs.haversine(loc1,loc2), 2)
    capital = datosCapital['CapitalName'] + "-" + datosCapital['CountryName']
    addConnection(analyzer, puntoOrigen, capital, distanciaHaversine)
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
    mp.put(analyzer['countries'], country['CountryName'],country['CapitalName'])
    return analyzer


# Funciones para agregar informacion al catalogo


def addPosition(analyzer, punto):
    loc = (float(punto["latitude"]), float(punto["longitude"]))
    mp.put(analyzer["landing_points"], punto["landing_point_id"], loc)
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



# ==============================
# Funciones de Comparacion
# ==============================

def compareLandingIds(landingPoint, keyValueLP):
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


