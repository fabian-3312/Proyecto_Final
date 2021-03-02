# Crear un programa que calcule y ajuste poligonales cerradas y abiertas.
# a. Leer los datos de la poligonal de un archivo csv con un formato predefinido.
# b. Pedir por pantalla el tipo de poligonal (Abierta o Cerrada)
# c. Solicitar la ruta del archivo que contiene los datos
# d. Validar si el archivo cargado cumple con el formato de ingreso de datos.
# e. Si la poligonal es cerrada solicitar:
#    Si el método de ajuste es por el método de la brújula o de tránsito.
#    Solicitar las coordenadas de los puntos de la línea de referencia de la poligonal.
# f. Si la poligonal es abierta:
#	 el ajuste realizarse por el método de Crandall.
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
    segundos = round((aux - minutos)*60, 0)
    
    # Definimos los grados minuto y segundos en un espacion determinado con su respectivo simbolo
    angulo_gms = '{:03d}'.format(grados) + '°' + '{:02d}'.format(minutos) + "'" + '{:04.1f}'.format(segundos) + '"'
    
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
    
    print()
    print('='*173)
    print()
    print('{:^173}'.format('A J U S T E  D E  P O L I G O N A L  P O R  E L  M E T O D O  D E  C R A N D A L L'))
    print()
    print('='*173)
    print()

    auxiliar = r'C:\Users\PC Smart\Downloads\POLIGONAL_ABIERTA_1.csv'
    file = input("Indicar la ruta del archivo, ejemplo({}): ".format(auxiliar))
    ruta = os.path.normpath(file)

    inic_gps_x = float(input('Ingrese la coordenada X del punto de referencia inicial: '))
    inic_gps_y = float(input('Ingrese la coordenada Y del punto de referencia inicial: '))
    inic_pol_x = float(input('Ingrese la coordenada X del punto inicial de la poligonal: '))
    inic_pol_y = float(input('Ingrese la coordenada Y del punto inicial de la poligonal: '))
    fin_gps_X = float(input('Ingrese la coordenada X del punto de referencia final: '))
    fin_gps_Y = float(input('Ingrese la coordenada y del punto de referencia final: '))
    fin_pol_X = float(input('Ingrese la coordenada X del punto final de la poligonal: '))
    fin_pol_Y = float(input('Ingrese la coordenada X del punto final de la poligonal: '))

    acimut_i = acimut_linea(inic_pol_x,inic_pol_y,inic_gps_x,inic_gps_y)
    acimut_f = acimut_linea(fin_pol_X,fin_pol_Y,fin_gps_X,fin_gps_Y)

    print(acimut_i)
    print(acimut_f)
    
    deltas = cant_deltas(ruta)
    datos_crandall=[]
    
    with open(ruta, newline='') as File:
        reader = csv.DictReader(File)
        for row in reader:
            delta = row['Delta']
            angulo_observado = float(row['Angulo'])
            distancia = float(row['Distancia'])
            
            linea=[delta,angulo_observado,distancia]
            datos_crandall.append(linea.copy())
            
    i = 0

    suma_px = 0.0
    suma_py = 0.0
    proyec_punto = []
    suma_correc1 = 0.0
    suma_correc2 = 0.0
    suma_correc3 = 0.0

    d = 0
    
    for dato in datos_crandall:
        if d < deltas:
            if i < 1:

                datos_crandall[i].append(acimut_i + datos_crandall[0][1])
                datos_crandall[i].append((math.sin(math.radians(datos_crandall[i][3])))*datos_crandall[0][2])
                datos_crandall[i].append((math.cos(math.radians(datos_crandall[i][3])))*datos_crandall[0][2])
                datos_crandall[i].append((datos_crandall[i][5]*datos_crandall[i][4])/datos_crandall[i][2]) 
                datos_crandall[i].append(((datos_crandall[i][5])**2)/datos_crandall[i][2])            
                datos_crandall[i].append(((datos_crandall[i][4])**2)/datos_crandall[i][2]) 
                suma_px=datos_crandall[i][4]
                suma_py=datos_crandall[i][5]
                suma_correc1 = datos_crandall[i][6]
                suma_correc2 = datos_crandall[i][7]
                suma_correc3 = datos_crandall[i][8]
                sumatoria_proyecciones_norte = inic_pol_y + datos_crandall[i][5]
                sumatoria_proyecciones_este = inic_pol_x + datos_crandall[i][4]
                i += 1

            if datos_crandall[i-1][3] >= 180:
                acimut_deltas = datos_crandall[i-1][3] - 180 + datos_crandall[i][1]
            else:
                acimut_deltas = datos_crandall[i-1][3] + 180 + datos_crandall[i][1]

            if acimut_deltas >= 360:
                acimut_deltas -= 360

            datos_crandall[i].append(acimut_deltas) 

            proyec_punto = proyecciones(acimut_deltas, datos_crandall[i][2])

            datos_crandall[i].append(proyec_punto[0]) 
            datos_crandall[i].append(proyec_punto[1]) 

            suma_px = datos_crandall[i][4] + suma_px
            suma_py = datos_crandall[i][5] + suma_py

            sumatoria_proyecciones_norte = sumatoria_proyecciones_norte + datos_crandall[i][5]

            sumatoria_proyecciones_este = sumatoria_proyecciones_este + datos_crandall[i][4]           

            datos_crandall[i].append((datos_crandall[i][5]*datos_crandall[i][4])/datos_crandall[i][2]) 

            datos_crandall[i].append(((datos_crandall[i][5])**2)/datos_crandall[i][2]) 

            datos_crandall[i].append(((datos_crandall[i][4])**2)/datos_crandall[i][2])         

            suma_correc1 = datos_crandall[i][6] + suma_correc1

            suma_correc2 = datos_crandall[i][7] + suma_correc2

            suma_correc3 = datos_crandall[i][8] + suma_correc3

            i += 1
            d += 1
        else:
            continue        
    


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
    exist = os.path.isfile(ruta)

    if exist == True:

        arch = open(ruta, 'r')
        linea = (arch.readline())

        if linea != 'Delta,Angulo,Distancia\n':
            print()
            print('='*173)
            print('Error al leer el archivo')
            print()
            print('Recuerde:','\n','El archivo debe ser (csv) de caso contrario no lo reconocera','\n','El archivo debe estar estructurado de la sigiente manera:')
            print()
            print('{:^19}'.format('Delta'),'{:^17}'.format('Angulo'),'{:^34}'.format('Distancia'), sep='|')
            print('{:^19}'.format('(Nombre del delta)'),'{:^17}'.format('(Angulo gg.mmss)'),'{:^34}'.format('(Distancia-puede ser con decimales)'), sep='|')
            print('{:^19}'.format('(Nombre del delta)'),'{:^17}'.format('(Angulo gg.mmss)'),'{:^34}'.format('(Distancia-puede ser con decimales)'), sep='|')
            print('{:^19}'.format('Repetir N veces'),'{:^17}'.format('Repetir N veces'),'{:^34}'.format('Repetir N veces'), sep='|')
            print('\n','Los nombres de la primera fila deben ser: Delta - Angulo - Distancia. Los nombres deben ser tal cual se muestran(sin comas, espacios o tildes)','\n','Favor realizar la cartera desde la primera final y la primera columna')
            print('='*173)
            print('{:^173}'.format('A R R E G L A R  A R C H I V O  Y  V O L E R  A  I N T E N T A R'))
            print('{:^173}'.format('G R A C I A S'))
            print('='*173)
            print()

        else:
        
            deltas = cant_deltas(ruta)
            ang_externos = input('¿Angulos externos? [1=si] [0=no]: ')
        
    
            # calcular la sumatoria toerica de angulos 
            if ang_externos == '1':
                suma_teorica_ang = (deltas + 2)*180

                # soliciya las coordenadas de la linea de referencia 
    
                x_inicio = float(input('Digite la coordenada x del punto de inicio: '))
                y_inicio = float(input('Digite la coordenada y del punto de inicio: '))
                x_referencia = float(input('Digite la coordenada x del punto de referencia: '))
                y_referencia = float(input('Digite la coordenada y del punto de referencia: '))

                acimut_ref = acimut_linea(x_inicio, y_inicio, x_referencia, y_referencia)
                print('\n','El azimut calculado es: {}°'.format(dec_gms(acimut_ref)))

                print('La sumatoria teorica es: {}°'.format(suma_teorica_ang))

                datos_medidos = []
                datos_medidos.append(['DELTA', 'ANG OBSER', 'DIST', 'ANG OBSERV DEC', 'ANG OBSER CORREG', 'AZIMUTH', 'PRY X', 'PRY Y', 'PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])

                j = 0
                sumang = 0.0
                sumdist = 0.0

                with open(ruta, newline='')as File:
                    reader = csv.DictReader(File)
                    for row in reader: 
                        nombre_delta = row['Delta']
                        ang_observado = float(row['Angulo'])
                        distancia = float(row['Distancia'])
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
                datos_medidos[1].append(acimut_ref + datos_medidos[1][3])

                # calculo los azimut
                i = 0
                suma_px = 0.0
                suma_py = 0.0
                proyec_punto = []

                for dato in datos_medidos: 
                
                    if i < 2:
                        i += 1
                        continue
                    
                    datos_medidos[i].append(datos_medidos[i][3] + correccion_ang)

                    if datos_medidos[i-1][4] >= 180:
                        acimut_deltas = datos_medidos[i-1][5] - 180 + datos_medidos[i][4]
                    else:
                        acimut_deltas = datos_medidos[i-1][5] + 180 + datos_medidos[i][4]

                    if acimut_deltas >= 360:
                        acimut_deltas -=360

                    datos_medidos[i].append(acimut_deltas)

                    proyec_punto = proyecciones(acimut_deltas, datos_medidos[i][2])

                    datos_medidos[i].append(proyec_punto[0])
                    datos_medidos[i].append(proyec_punto[1])

                    suma_px += datos_medidos[i][6]
                    suma_py += datos_medidos[i][7]

                    i += 1

                print()

                datos_medidos[1][:] += [0, 0, 0, 0, x_inicio, y_inicio]

                i = 0  

                for dato in datos_medidos:
                
                    if i < 2:
                        i += 1
                        continue
                    
                    # proyecciones corregidas
                    datos_medidos[i].append(datos_medidos[i][6] -(suma_px / sumdist)*datos_medidos[i][2])
                    datos_medidos[i].append(datos_medidos[i][7] -(suma_py / sumdist)*datos_medidos[i][2]) 

                    # coordenadas
                    datos_medidos[i].append(datos_medidos[i-1][10] + datos_medidos[i][8])

                    datos_medidos[i].append(datos_medidos[i-1][11] + datos_medidos[i][9])

                    i += 1

                print()

                print('='*173)
                print('{:^10}'.format('DELTA'), '{:^8}'.format('ANGULO'), '{:^8}'.format('DISTANCIA'), '{:^10}'.format('ANGULO'), '{:^10}'.format('AZIMUTH'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^11}'.format('COORDEN'), '{:^11}'.format('COORDEN'), sep='\t')

                print('{:^10}'.format(''), '{:^8}'.format('OBSERV'), '{:^8}'.format('(m)'), '{:^10}'.format('CORREGIDO'), '{:^10}'.format(''), '{:^10}'.format('X'), '{:^10}'.format('Y'), '{:^10}'.format('CORR X'), '{:^10}'.format('CORR Y'), '{:^11}'.format('X'), '{:^11}'.format('Y'), sep='\t')
                print('='*173)

                i = 0

                encabezado = ['Delta','Angulo_Observado','Distancia','Angulo_Corregido','Acimut','Proy_X','Proy_Y','Proy_Corregida_X','Proy_Corregida_Y','Coord_X','Coord_Y']
                salida = os.path.join(os.path.dirname(ruta),'{0}_AJUSTADA_{1}.csv'.format(os.path.basename(ruta).split('.')[0],str(datetime.now().strftime("%d_%m_%Y %H_%M_%S"))))
                with open(salida, 'w', newline='') as csvfile:            
                    writer = csv.DictWriter(csvfile, fieldnames=encabezado)
                    writer.writeheader()

                    for dato in datos_medidos:
                        if i == 0:
                            i += 1
                            continue
                        print('{:^10}'. format(dato[0]), '{:8.4f}'.format(dato[1]), '{:8.4f}'.format(dato[2]), '{:10}'.format(dec_gms(dato[4])), '{:10}'.format(dec_gms(dato[5])),'{:+010.3f}'.format(dato[6]), '{:+010.3f}'.format(dato[7]), '{:+010.3f}'.format(dato[8]), '{:+10.3f}'.format(dato[9]), '{:11.3f}'.format(dato[10]), '{:11.3f}'.format(dato[11]),sep='\t')
                        datos={'Delta':dato[0], 'Angulo_Observado':'{:8.4f}'.format(dato[1]),'Distancia':'{:8.4f}'.format(dato[2]),'Angulo_Corregido':'{:10}'.format(dec_gms(dato[4])),'Acimut':'{:10}'.format(dec_gms(dato[5])),'Proy_X':'{:+010.3f}'.format(dato[6]),'Proy_Y':'{:+010.3f}'.format(dato[7]),'Proy_Corregida_X':'{:+010.3f}'.format(dato[8]), 'Proy_Corregida_Y':'{:+010.3f}'.format(dato[9]),'Coord_X':'{:11.3f}'.format(dato[10]), 'Coord_Y':'{:11.3f}'.format(dato[11])}
                        writer.writerow(datos)

                        i +=1

                print('='*173)

                d = 0
                j = 1
                x = []
                y = []

                for dato in datos_medidos:
                    if d < deltas:
                        if j < 2:
                            x.append(x_referencia)
                            y.append(y_referencia)
                            x.append(x_inicio)
                            y.append(y_inicio)
                            j += 1

                        else:
                            x.append(datos_medidos[j][10])
                            y.append(datos_medidos[j][11])


                            j += 1
                            d += 1
                    else:
                        continue
                    
                print('='*173)
                print('SU ARCHIVO AJUSTADO SERA ENVIADO A LA MISMA DIRECCION DEL ARCHIVO LEIDO CON EL NOMBRE DEL ARCHIVO LEIDO + AJUSTADO + FECHA + HORA EXACTA DE ELAVORACION')
                print('='*173)
                print('{:^173}'.format('P R O G R A M A  T E R M I N A D O'))
                print('='*173)

                i = 1

                fig = plt.figure(figsize=(6,6))
                ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
                ax.set_title('POLIGONO AJUSTADO', color='0.1')
                plt.plot(x, y) 
                plt.plot(x, y, 'ro', linewidth=3)
                plt.show()



            elif ang_externos == '0': 
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
                datos_medidos.append(['DELTA', 'ANG OBSER', 'DIST', 'ANG OBSERV DEC', 'ANG OBSER CORREG', 'AZIMUTH', 'PRY X', 'PRY Y', 'PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])

                j = 0
                sumang = 0.0
                sumdist = 0.0

                with open(ruta, newline='')as File:
                    reader = csv.DictReader(File)
                    for row in reader: 
                        nombre_delta = row['Delta']
                        ang_observado = float(row['Angulo'])
                        distancia = float(row['Distancia'])
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
                datos_medidos[1].append(acimut_ref + datos_medidos[1][3])

                # calculo los azimut
                i = 0
                suma_px = 0.0
                suma_py = 0.0
                proyec_punto = []

                for dato in datos_medidos: 
                
                    if i < 2:
                        i += 1
                        continue
                    
                    datos_medidos[i].append(datos_medidos[i][3] + correccion_ang)

                    if datos_medidos[i-1][4] >= 180:
                        acimut_deltas = datos_medidos[i-1][5] - 180 + datos_medidos[i][4]
                    else:
                        acimut_deltas = datos_medidos[i-1][5] + 180 + datos_medidos[i][4]

                    if acimut_deltas >= 360:
                        acimut_deltas -=360

                    datos_medidos[i].append(acimut_deltas)

                    proyec_punto = proyecciones(acimut_deltas, datos_medidos[i][2])

                    datos_medidos[i].append(proyec_punto[0])
                    datos_medidos[i].append(proyec_punto[1])

                    suma_px += datos_medidos[i][6]
                    suma_py += datos_medidos[i][7]

                    i += 1

                print()

                datos_medidos[1][:] += [0, 0, 0, 0, x_inicio, y_inicio]

                i = 0  

                for dato in datos_medidos:
                
                    if i < 2:
                        i += 1
                        continue
                    
                    # proyecciones corregidas
                    datos_medidos[i].append(datos_medidos[i][6] -(suma_px / sumdist)*datos_medidos[i][2])
                    datos_medidos[i].append(datos_medidos[i][7] -(suma_py / sumdist)*datos_medidos[i][2]) 

                    # coordenadas
                    datos_medidos[i].append(datos_medidos[i-1][10] + datos_medidos[i][8])

                    datos_medidos[i].append(datos_medidos[i-1][11] + datos_medidos[i][9])

                    i += 1

                print()

                print('='*173)
                print('{:^10}'.format('DELTA'), '{:^8}'.format('ANGULO'), '{:^8}'.format('DISTANCIA'), '{:^10}'.format('ANGULO'), '{:^10}'.format('AZIMUTH'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^11}'.format('COORDEN'), '{:^11}'.format('COORDEN'), sep='\t')

                print('{:^10}'.format(''), '{:^8}'.format('OBSERV'), '{:^8}'.format('(m)'), '{:^10}'.format('CORREGIDO'), '{:^10}'.format(''), '{:^10}'.format('X'), '{:^10}'.format('Y'), '{:^10}'.format('CORR X'), '{:^10}'.format('CORR Y'), '{:^11}'.format('X'), '{:^11}'.format('Y'), sep='\t')
                print('='*173)

                i = 0

                encabezado = ['Delta','Angulo_Observado','Distancia','Angulo_Corregido','Acimut','Proy_X','Proy_Y','Proy_Corregida_X','Proy_Corregida_Y','Coord_X','Coord_Y']
                salida = os.path.join(os.path.dirname(ruta),'{0}_AJUSTADA_{1}.csv'.format(os.path.basename(ruta).split('.')[0],str(datetime.now().strftime("%d_%m_%Y %H_%M_%S"))))
                with open(salida, 'w', newline='') as csvfile:            
                    writer = csv.DictWriter(csvfile, fieldnames=encabezado)
                    writer.writeheader()

                    for dato in datos_medidos:
                        if i == 0:
                            i += 1
                            continue
                        print('{:^10}'. format(dato[0]), '{:8.4f}'.format(dato[1]), '{:8.4f}'.format(dato[2]), '{:10}'.format(dec_gms(dato[4])), '{:10}'.format(dec_gms(dato[5])),'{:+010.3f}'.format(dato[6]), '{:+010.3f}'.format(dato[7]), '{:+010.3f}'.format(dato[8]), '{:+10.3f}'.format(dato[9]), '{:11.3f}'.format(dato[10]), '{:11.3f}'.format(dato[11]),sep='\t')
                        datos={'Delta':dato[0], 'Angulo_Observado':'{:8.4f}'.format(dato[1]),'Distancia':'{:8.4f}'.format(dato[2]),'Angulo_Corregido':'{:10}'.format(dec_gms(dato[4])),'Acimut':'{:10}'.format(dec_gms(dato[5])),'Proy_X':'{:+010.3f}'.format(dato[6]),'Proy_Y':'{:+010.3f}'.format(dato[7]),'Proy_Corregida_X':'{:+010.3f}'.format(dato[8]), 'Proy_Corregida_Y':'{:+010.3f}'.format(dato[9]),'Coord_X':'{:11.3f}'.format(dato[10]), 'Coord_Y':'{:11.3f}'.format(dato[11])}
                        writer.writerow(datos)

                        i +=1

                print('='*173)

                d = 0
                j = 1
                x = []
                y = []

                for dato in datos_medidos:
                    if d < deltas:
                        if j < 2:
                            x.append(x_referencia)
                            y.append(y_referencia)
                            x.append(x_inicio)
                            y.append(y_inicio)
                            j += 1

                        else:
                            x.append(datos_medidos[j][10])
                            y.append(datos_medidos[j][11])


                            j += 1
                            d += 1
                    else:
                        continue
                    
                print('='*173)
                print('SU ARCHIVO AJUSTADO SERA ENVIADO A LA MISMA DIRECCION DEL ARCHIVO LEIDO CON EL NOMBRE DEL ARCHIVO LEIDO + AJUSTADO + FECHA HORA EXACTA DE ELAVORACION')
                print('='*173)
                print('{:^173}'.format('P R O G R A M A  T E R M I N A D O'))
                print('='*173)

                i = 1

                fig = plt.figure(figsize=(6,6))
                ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
                ax.set_title('POLIGONO AJUSTADO', color='0.1')
                plt.plot(x, y) 
                plt.plot(x, y, 'ro', linewidth=3)
                plt.show()

            elif ang_externos != '0' or ang_externos != '1':
                print('='*173)
                print('La opcion digitada no es valida, intente nuevamente')
                print('='*173)

    else:
        print()
        print('='*140)
        print(' Favor Revisar la extencion digitada')
        print()
        print(' Recuerde:','\n','   La ruta de su archivo debe parecerce a la seguiente y cumplir con sus criterios:')
        print()
        print('    C:','Carpeta','Carpeta','Carpeta','....','Nombre del archivo(.)Ruta del archivo', sep=' \ ')
        print('\n','   La unica separacion entre carpeta y carpeta debe ser (\)','\n','   Verifique el nombre de su archivo, ademas de su extencion, tome como ejemplo el siguiente (Archivo.csv)','\n','   Ingrese la extencion sin comillas o comas al principio y al final')
        print()
        print('='*173)
        print('{:^173}'.format('F A V O R  V O L V E R  A  I N T E N T A R'))
        print('{:^173}'.format('G R A C I A S'))
        print('='*173)
        print()
                   
def main():
    print('='*173)
    print('{:^173}'.format('P R O Y E C T O  F I N A L'))
    print('{:^173}'.format('L O G I C A  D E  P R O G R A M A C I O N'))
    print('='*173)
    print('Maritzabel Cordoba Giraldo','\n', 'Cod.:20191131053','\n','Cristian Camilo Casallas Beltrán','\n', 'Cod.:20201131025','\n','Fabian Esteban Reyes Bejarano','\n', 'Cod.:20201131048','\n','\n','Evelio Luis Madera Arteaga','\n','Universidad distrital Francisco Jose de Caldas')
    print()
    print('='*173)
    print()
    print('RECOMENDACION: SU ARCHIVO CSV DEBE TENER:','\n','-EL NOMBRE DE LOS PUNTOS DEBE ESTAR COMO "Delta"','\n','-EL NOMBRE DE LOS ANGULOS DEBE ESTAR COMO "Angulo"','\n','-EL NOMBRE DE LAS LONGITUDES DEBE ESTAR COMO "Distancia"','\n','LAS PALABRAS SE ESCRIBEN TALCUAL ESTAN ANTERIORMENTE Y EN EL MISMO ORDEN SIN ESPACIOS','\n')
    print('='*173)
    proceso = input('Desea realizar un ajuste de poligonal [Si=1][No=0]: ')
                       
    if proceso == '1':
        print('='*173)
        solucion = input('¿Su poligonal es abierta o cerrada? [Abierta=1][Cerrada=0]: ')
        if solucion == '1':
            print('='*173)
            crandall()
        elif solucion == '0':
            print('='*173)
            brujula()
        elif solucion != '1' or solucion != '0':
            print('='*173)
            print('El numero digitado no es valido, intente nuevamente')
            print('='*173)
    elif proceso == '0':
        print('='*173)
        print('{:^173}'.format('P R O G R A M A  T E R M I N A D O'))
        print('{:^173}'.format('G R A C I A S'))
        print('='*173)  
    elif proceso != '0' or proceso != '1':
        print('='*173)
        print('La opcion digitada no es valida, intente nuevamente')
        print('='*173)
                       
if __name__ == '__main__':
    main()
 
