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
    landing_File = csv.DictReader(open(landingFile, encoding="utf-8"), delimiter=",")
    connections_File = csv.DictReader(open(connectionsFile, encoding="utf-8-sig"), delimiter=",")
    countries_File = csv.DictReader(open(countriesFile, encoding="utf-8"), delimiter=",")

    for punto in landing_File:
        model.addPosition(analyzer, punto)

    for point in landing_File:
        name = point['name'].split(", ")
        pais = name[1]
        for country in countries_File:
            if country['CountryName'] == pais:
                capital = country['CapitalName'] + "-" + pais
                model.addPoint(analyzer, capital)
                datosCapital = country
                model.addCountry(analyzer, country)

        lstPuntoActual = None
        for connection in connections_File:
            lstPuntoActual = model.addLandingPoint(analyzer, point, connection, lstPuntoActual, datosCapital)
        model.addConnectionsPoint(analyzer, lstPuntoActual)




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
    Totald de paises cargados
    """
    return model.totalCountries(analyzer)
