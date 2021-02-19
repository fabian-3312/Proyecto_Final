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


def cant_deltas(archivo):
    with open(archivo, newline='') as File:
        reader = csv.DictReader(File)
        deltas = [fila['Delta'] for fila in reader]
    return len(deltas)-1


def dec_gms(angulo_dec):
    grados = int(angulo_dec)
    aux = (angulo_dec - grados)*60
    minutos = int(aux)
    segundos = round((aux - minutos)*3600, 0)
    
    # Definimos los grados minuto y segundos en un espacion determinado con su respectivo simbolo
    angulo_gms = '{:03d}'.format(grados)+'°'+'{:02d}'.format(minutos)+"'"+'{:01d}'.format(segundos)+'"'
    
    return angulo_gms


def acimut_linea(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if dy != 0:
        rumbo = math.degrees(math.atan(dx/dy))
        if dy > 0 and dy > 0:
            acimut = rumbo
        elif dx > 0 and dy < 0:
            acimut = 180 + rumbo
        elif dx < 0 and dy < 0:
            acimut = 180 + rumbo
        elif dx < 0 and dy > 0:
            acimut = 360 + rumbo
        elif dx == 0 and dy > 0:
            acimut = 0
        elif dx == 0 and dy < 0:
            acimut = 180
    else:
        if dx > 0:
            acimut = 90
        elif dx < 0:
            acimut = 270
        else:
            acimut = -1 
                             
    return acimut     


def proyecciones(acimut, distancia):
    acimut = math.radians(acimut)
    
    valor_proyecciones = []
    valor_proyecciones.append(math.sin(acimut)*distancia)
    valor_proyecciones.append(math.cos(acimut)*distancia)
    
    return valor_proyecciones 


def acimut_poligonal(acimut_anterior, angulo_observado):
    if acimut_anterior >= 180:
        contra_acimut = acimut_anterior -180
    else: 
        contra_acimut = acimut_anterior + 180
  
    acimut = contra_acimut + angulo_observado

    if acimut >= 360:
        acimut = acimut-360
    
    return acimut 


def brujula():
    
    print()   
    print()
    print('='*173)
    print()
    print('{:^173}'.format('A J U S T E  D E  P O L I G O N A L  P O R  E L M E T O D O  D E B R U J U L A'))
    print()
    print('='*173)
    print()
        
    auxiliar = r'C:\Users\PC Smart\Downloads\POLIGONAL_CERRADA_1.csv'
    file = input(" Indicar la ruta del archivo, ejemplo({}):".format(auxiliar))
    ruta = os.path.normpath(file)
        
    deltas = cant_deltas(ruta)
    ang_externos = int(input('¿Angulos externos [1=si] [0=no]: '))
   
        
    # calcular la sumatoria toerica de angulos 
    if ang_externos == 1:
        suma_teorica_ang = (deltas + 2)*180
    else: 
        suma_teorica_ang = (deltas - 2)*180
        
    # soliciya las coordenadas de la linea de referencia 
        
    x_inicio = float(input('Digite la coordenada x del punto de inicio: '))
    y_inicio = float(input('Digite la coordenada y del punto de inicio: '))
    x_referencia = float(input('Digite la coordenada x del punto de referencia: '))
    x_referencia = float(input('Digite la coordenada y del punto de referencia: '))

    acimut_ref =acimut
                       
                       
def main():
    print('Maritzabel Cordoba Giraldo','\n', 'Cod.:20191131053','\n','Cristian Camilo Casallas Beltrán','\n', 'Cod.:20201131025','\n','Fabian Esteban Reyes Bejarano','\n', 'Cod.:20201131048','\n','\n','Evelio Luis Madera Arteaga','\n','Universidad distrital Francisco Jose de Caldas')
    print('='*173)
    print('RECOMENDACION: SU ARCHIVO CSV DEBE TENER:','\n','-EL NOMBRE DE LOS PUNTOS DEBE ESTAR COMO "Delta"','\n','-EL NOMBRE DE LOS ANGULOS DEBE ESTAR COMO "Angulo"','\n','-EL NOMBRE DE LAS LONGITUDES DEBE ESTAR COMO "Distancia"','\n','LAS PALABRAS SE ESCRIBEN TALCUAL ESTAN ANTERIORMENTE Y EN EL MISMO ORDEN SIN ESPACIOS','\n')
    proceso = float(input('Desea realizar un ajuste de poligonal [Si=1][No=0]: '))
                       
    if proceso == 1:
        print('='*173)
        solucion = float(input('¿Su poligonal es abierta o cerrada? [Abierta=1][Cerrada=0]: '))
        if solucion == 1:
            print('='*173)
            crandall()
        else:
            print('='*173)
            brujula()
    else:
        print('='*140)
        print('PROGRAMA TERMINADO','\n','GRACIAS.')
        print('='*140)          
                       
if __name__ == '__main__':
    main()
 
                       
        
                           
                          
        
       
    
    
    
    
    
    
    
    
