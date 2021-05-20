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
                    'info': None,
                    'landing points': None,
                    'connections': None,
                    'countries': None,
                    'paths': None
                    }

        analyzer['info'] = mp.newMap(maptype='PROBING',
                                     comparefunction=compareLandingIds)

        analyzer['landing_points'] = mp.newMap(numelements=1300,
                                               maptype='PROBING',
                                               comparefunction=compareLandingIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=3300,
                                              comparefunction=compareLandingIds)
        
        analyzer['countries'] = mp.newMap(numelements=300,
                                          maptype='PROBING')
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Construccion de modelos

def prepareData(analyzer, point):
    connectionsLst = lt.newList('ARRAY_LIST', cmpfunction=compareconnections)
    mp.put(analyzer['landing_points'], point['landing_point_id'], connectionsLst)


def loadData(analyzer, connection):
    entry = mp.get(analyzer['landing_points'], connection['origin'])
    cableLst = entry["value"]
    cableName = connection['cable_name']
    if not lt.isPresent(cableLst, cableName):
        lt.addLast(cableLst, cableName)
    pointName = formatVertex(connection)
    entry = mp.get(analyzer['info'], pointName)
    if entry is None:
        connectionsLst = lt.newList()
        mp.put(analyzer['info'], pointName, connectionsLst)
    else:
        connectionsLst = me.getValue(entry)
    lt.addLast(connectionsLst, connection)


def loadCountry(analyzer, country):
    mp.put(analyzer['countries'], country['CountryName'], country)


def addLandingPoints(analyzer):
    pointsLst = mp.keySet(analyzer['landing_points'])
    for key in lt.iterator(pointsLst):
        cablelst = mp.get(analyzer['landing_points'], key)['value']
        for cableName in lt.iterator(cablelst):
            LPname = key + "-" + cableName
            addPoint(analyzer, LPname)


def addPointConnections(analyzer):
    pointsLst = mp.keySet(analyzer['landing_points'])
    for key in lt.iterator(pointsLst):
        cablesLst = mp.get(analyzer['landing_points'], key)['value']
        prevPoint = None
        for cable in lt.iterator(cablesLst):
            origin = key + "-" + cable
            info = mp.get(analyzer['info'], origin)["value"]
            for connection in lt.iterator(info):
                destination = connection['destination'] + "-" + cable
                addConnection(analyzer, origin, destination, info)
                addConnection(analyzer, destination, origin, info)


def addConnection(analyzer, destination, origin, distance):
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


# Funciones para agregar informacion al catalogo

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

def formatVertex(connection):
    """
    Se formatea el nombre del vertice con el id del landing point
    seguido del nombre del cable.
    """
    name = connection['origin'] + '-'
    name = name + connection['cable_name']
    return name

