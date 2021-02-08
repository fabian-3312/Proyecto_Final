# Crear un programa que calcule y ajuste poligonales cerradas y abiertas.
# a. Leer los datos de la poligonal de un archivo csv con un formato predefinido.
# b. Pedir por pantalla el tipo de poligonal (Abierta o Cerrada)
# c. Solicitar la ruta del archivo que contiene los datos
# d. Validar si el archivo cargado cumple con el formato de ingreso de datos.
# e. Si la poligonal es cerrada solicitar:
#    Si el método de ajuste es por el método de la brújula o de tránsito.
#    Solicitar las coordenadas de los puntos de la línea de referencia de la poligonal.
# f. Si la poligonal es abierta:
#	   el ajuste realizarse por el método de Crandall.
#    Solicitar las coordenadas de los puntos de las líneas de referencia y finalización.
# g. El resultado del cálculo y el ajuste deben guardarse en un archivo de texto en la misma ruta del archivo que contiene los datos.
# h. Dibujar la poligonal a través de un archivo Geojson, json o en la consola.

import csv
import os
import math
import json
import requests
import xlsxwriter
from datetime import datetime
from matplotlib import pyplot as plt 

def gms_dec(angulo):
    grados = int(angulo)
    aux = (angulo - grados)*100
    minutos = int(aux)
    segundos = (aux - minutos)*100

    angulo_dec = grados + (minutos/60) + (segundos/3600)

    return angulo_dec

def dec_gms(angulo_dec):
    grados = int(angulo_dec)
    aux = (angulo_dec - grados)*60
    minutos = int(aux)
    segundos round((aux - minutos)*3600, 0)
    
    # Definimos los grados minuto y segundos en un espacion determinado con su respectivo simbolo
    angulo_gms = '{:03d}'.format(grados)+'°'+'{:02d}'.format(minutos)+"'"+'{:01d}'.format(segundos)+'"'
    
    return angulo_gms

