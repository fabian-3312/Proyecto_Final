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


def crandall():
    pass


def brujula():
    
    print()   
    print()
    print('='*173)
    print()
    print('{:^173}'.format('A J U S T E  D E  P O L I G O N A L  P O R  E L  M E T O D O  D E B R U J U L A'))
    print()
    print('='*173)
    print()
        
    auxiliar = r'C:\Users\PC Smart\Downloads\POLIGONAL_CERRADA_1.csv'
    file = input(" Indicar la ruta del archivo, ejemplo({}):".format(auxiliar))
    ruta = os.path.normpath(file)
        
    deltas = cant_deltas(ruta)
    ang_externos = int(input('¿Angulos externos? [1=si] [0=no]: '))
   
        
    # calcular la sumatoria toerica de angulos 
    if ang_externos == 1:
        suma_teorica_ang = (deltas + 2)*180
    else: 
        suma_teorica_ang = (deltas - 2)*180
        
    # soliciya las coordenadas de la linea de referencia 
        
    x_inicio = float(input('Digite la coordenada x del punto de inicio: '))
    y_inicio = float(input('Digite la coordenada y del punto de inicio: '))
    x_referencia = float(input('Digite la coordenada x del punto de referencia: '))
    y_referencia = float(input('Digite la coordenada y del punto de referencia: '))

    acimut_ref = acimut_linea(x_inicio, y_inicio, x_referencia, y_referencia)
    print('\n','El azimut calculado es: {}°'.format(dec_gms(acimut_ref)))

    print('La sumatoria teorica es: {}°'.format(suma_teorica_ang))

    datos_medidos = []
    datos_medidos.append(['DELTA', 'ANG OBSER', 'DIST', 'ANG OBSERV DEC', 'ANG OBSER CORREG', 'AZIMUTH', 'PRY X', 'PRY Y', 'PRY X CORREG', 'PRY Y CORREG', 'COORD X', 'COORD Y'])

    j = 0
    sumang = 0.0
    sumdist = 0.0
    
    with open(ruta, newline='')as File:
        reader = csv.DictReader(File)
        for row in reader: 
            nombre_delta = row['Delta']
            ang_observado = float(row['Angulo'])
            distancia = float(row)['Distancia'])
            datos_linea = [nombre_delta,ang_observado, distancia, gms_dec(ang_observado)]
            datos_medidos.append(datos_linea.copy())

            if j != 0:
                sumdist = sumdist + distancia
                sumang = sumang + datos_linea[3]
                j += 1
             else: 
                j += 1
    
    error_ang = suma_teorica_ang - sumang
    correccion_ang = error_ang / deltas

    print('El error angular es: ', error_ang)
    print('La correccion angular es:' , correccion_ang)

    datos_medidos[1].append(datos_medidos[1][3])

    # calculo los azimut
    i = 0
    suma_px = 0.0
    suma_py = 0.0
    proyec_punto = []

    for dato in datos_medidos: 
        
        if i < 2:
            i += 1
            continue
        
        datos_medidos[i].append(datos_medidos[i][3] + coreccion_ang)

        if datos_medidos[i-1][4] >= 180:
            acimut_deltas = datos_medidos[i-1][5] - 180 + datos_metidos[i][4]
        else:
            acimut_deltas = datos_metidos[i-1][5] + 180 + datos_metidos[i][4]

        if acimut_deltas >= 360:
            acimut_deltas -=360

        datos_metidos[i].append(acimut_deltas)

        proyec_punto = proyecciones(acimut_deltas, datos_metidos[i][2])

        datos_metidos[i].append(proyec_punto[0])
        datos_metidos[i].append(proyec_punto[1])

        suma_px += datos_medidos[i][6]
        sume_py += datos_metidos[i][7]

        i += 1
    
    print()

    datos_metidos[1][:] += [0. 0, 0, 0, x_incicio, y_inicio]

    i = 0  
    
    for dato in datos_metidos:
        
        if i < 2:
            i += 1
            continue
            
        # proyecciones corregidas
        datos_metidos[i].append(datos_metidos[i][6] -(suma_px / sumdist)*datos_metidos[i][2])
        datos_metidos[i].append(datos_metidos[i][7] -(suma_py / sumdist)*datos_metidos[i][2]) 
    
        # coordenadas
        datos_metidos[i].append(datos_metidos[i-1][10] + datos_metidos[i][8])
    
        datos_metidos[i].append(datos_metidos[i-1][11] + datos_metidos[i][9])
    
        i += 1
        
    print()

    print('='*173)
    print('{:^10}'.format('DELTA'), '{:^8}'.format('ANGULO'), '{:^8}'.format('DISTANCIA'), '{:^10}'.format('ANGULO'), '{:^10}'.format('AZIMUTH'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^11}'.format('COORDEN'), '{:^11}'.format('COORDEN'), sep='\t')

    print('{:^10}'.format(''), '{:^8}'.format('OBSERV'), '{:^8}'.format('N'), '{:^10}'.format('CORREGIDO'), '{:^10}'.format(''), '{:^10}'.format('X'), '{:^10}'.format('Y'), '{:^10}'.format('CORR X'), '{:^10}'.format('CORR Y'), '{:^11}'.format('X'), '{:^11}'.format('Y'), sep='\t')
    print('='*173)

    i = 0
    
    encabezado = ['Delta','Angulo_Observado','Distancia','Angulo_Corregido','Acimut','Proy_X','Proy_Y','Proy_Corregida_X','Proy_Corregida_Y','Coord_X','Coord_Y']
    salida = os.path.join(os.path.dirname(ruta),'{0}_AJUSTADA.csv'.format(os.path.basename(ruta).split('.')[0]))
    with open(salida, 'w', newline='') as csvfile:            
        writer = csv.DictWriter(csvfile, fieldnames=encabezado)
        writer.writeheader()
        
        for dato in datos_medidos:
            if i == 0:
                i += 1
                continue
            print('{:^10}'. format(dato[0]), '{:8.4f}'.format(dato[1]), '{:8.4f}'.format(dato[2]), '{:10}'.format(dec_gms(dato[4])), '{:10}'.format(dec_gms(dato[5])),'{:+010.3f}'.format(dato[6]), '{:+010.3f}'.format(dato[7]), '{:+010.3f}'.format(dato[8]), '{:+10.3f}'.format(dato[9]), '{:11.3f}'.format(dato[10]), '{:11.3f}'.format(dato[11]),sep='\t')
            datos={'Delta':dato[0], 'Angulo_Obsrvado':'{:8.4f}'.format(dato[1]),'Distancia':'{:8.4f}'.format(dato[2]),'Angulo_Corregido':'{:10}'.format(deg_gms(dato[4])),'Acimut':'{:10}'.format(dec_gms(dato[5])),'proy_X':'{:+010.3f'.format(dato[6]),''Proy_Y':'{:+010.3f}'.format(dato[7]),'Proy_Corregida_X':'{:+010.3f}'.format(dato[8]), 'Proy_Corregida_Y':'{:+010.3f}'.format(dato[9]),'Coord_X':'{:11.3f}'.format(dato[10]), 'Coord_Y':'{:11.3f}'.format(dato[11])}
            writer.writerow(datos)
            
            i +=1
    
    print('='*173)
                   
def main():
    print('='*173)
    print('{:^173}'.format('P R O Y E C T O  F I N A L'))
    print('{:^173}'.format('L O G I C A  D E  P R O G R A M A C I O N'))
    print('='*173)
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
        print('='*173)
        print('{:^173}'.format('P R O G R A M A  T E R M I N A D O'))
        print('{:^173}'.format('G R A C I A S'))
        print('='*173)         
                       
if __name__ == '__main__':
    main()
 

    
    
      
                           
                          
        
       
    
    
    
    
    
    
    
    
